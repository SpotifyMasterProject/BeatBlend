import jwt
import os
import time
import uuid

from datetime import timedelta, datetime, timezone
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from contextlib import asynccontextmanager
from repository import Repository
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from models.user import User
from models.token import Token
from models.session import Session
from models.song import Song
from models.song_list import SongList
from ws.websocket_manager import WebsocketManager

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
LOCAL_IP_ADDRESS = os.getenv("LOCAL_IP_ADDRESS")

manager = WebsocketManager()
repo = Repository()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await manager.connect()
    for attempt in range(10):
        try:
            await repo.postgres_connect()
            break
        except ConnectionRefusedError as e:
            if attempt == 9:
                raise e
            time.sleep(6)
    yield
    await manager.disconnect()
    await repo.postgres_disconnect()


class Service:
    def __init__(self):
        self.repo = repo
        self.spotify_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-library-read"  # scope defines functionalities
        )

        self.spotify_client = Spotify(auth_manager=self.spotify_oauth)

    @staticmethod
    def generate_token(user: User, spotify_token: Token = None) -> Token:
        to_encode = {"sub": user.id, "username": user.username}
        if spotify_token:  # additionally encode the spotify token for hosts
            to_encode["spotify_token"] = spotify_token.dict()
        access_token_expires = timedelta(minutes=JWT_EXPIRES_MINUTES)
        expire = datetime.now(timezone.utc) + (access_token_expires or timedelta(minutes=30))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return Token(access_token=encoded_jwt, token_type="bearer")

    @staticmethod
    def verify_token(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]) -> str:
        auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise auth_exception
        except InvalidTokenError:
            raise auth_exception
        # TODO: Consider also returing the spotify token.
        return user_id

    @staticmethod
    def verify_host_of_session(host_id: str, session: Session) -> None:
        if session.host != host_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not host of session.")

    async def verify_instances(self, user_ids: str | list[str] = "", session_id: str = ""):
        if isinstance(user_ids, str) and user_ids:
            await self.verify_user(user_ids)
        elif isinstance(user_ids, list):
            for user_id in user_ids:
                await self.verify_user(user_id)
        if session_id:
            await self.verify_session(session_id)

    def get_spotify_name(self) -> str:
        user_profile = self.spotify_client.me()
        return user_profile['id']

    async def create_user(self, user: User) -> User:
        user.id = str(uuid.uuid4())
        await self.repo.set_user(user)
        return user

    async def get_user(self, user_id: str) -> User:
        result = await self.repo.get_user_by_id(user_id)
        return User.model_validate_json(result)

    async def verify_user(self, user_id: str) -> None:
        await self.repo.verify_user_by_id(user_id)

    async def create_session(self, host_id: str, session: Session) -> Session:
        host = await self.get_user(host_id)
        session.id = str(uuid.uuid4())
        session.host_id = str(host.id)
        session.host_name = host.username
        session.creation_date = datetime.now()
        # session.is_running = True
        # TODO: adjust URL
        session.invite_link = f'http://{LOCAL_IP_ADDRESS}:8080/{session.id}/join'

        await self.repo.set_session(session)
        host.sessions.append(session.id)
        await self.repo.set_user(host)
        await manager.publish(channel=self.repo.get_session_key(session.id), message="New session created")

        return session

    # TODO: used for getting all artifacts
    # async def get_user_sessions(self, user: User) -> List[Session]:
    #     sessions = []
    #     for session_id in user.sessions:
    #         session = await self.get_session(session_id)
    #         sessions.append(session)
    #     return sessions

    async def get_session(self, session_id: str) -> Session:
        result = await self.repo.get_session_by_id(session_id)
        return Session.model_validate_json(result)

    async def add_guest_to_session(self, guest_id: str, session_id: str) -> Session:
        guest = await self.get_user(guest_id)
        session = await self.get_session(session_id)

        if guest.id not in session.guests:
            session.guests.append(guest.id)
            await self.repo.set_session(session)
            guest.sessions.append(session.id)
            await self.repo.set_user(guest)
            await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest_id} has joined the session")
        return session

    async def add_song_to_session(self, user_id: str, session_id: str, song_id: str) -> Session:
        session = await self.get_session(session_id)
        if user_id not in session.guests and user_id != session.host_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not part of session")
        try:
            song = await self.get_song_from_database(song_id)
        except HTTPException:
            song = await self.add_song_to_database(song_id)

        session.playlist.append(song)
        await self.repo.set_session(session)
        await manager.publish(channel=self.repo.get_session_key(session.id), message=f"User {user_id} has added song {song.name}")

        return session

    async def remove_song_from_session(self, host_id: str, session_id: str, song_id: str) -> None:
        session = await self.get_session(session_id)
        self.verify_host_of_session(host_id, session)
        for idx, song in enumerate(session.playlist):
            if song.id == song_id:
                del session.playlist[idx]
                await manager.publish(channel=self.repo.get_session_key(session.id), message=f"User {host_id} has removed song {song.name}")
                return

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not part of playlist")

    async def remove_guest_from_session(self, host_id: str, guest_id: str, session_id: str) -> None:
        guest = await self.get_user(guest_id)
        session = await self.get_session(session_id)

        if host_id:
            self.verify_host_of_session(host_id, session)

        if guest.id in session.guests:
            session.guests.remove(guest.id)
            await self.repo.set_session(session)
            guest.sessions.remove(session.id)
            await self.repo.set_user(guest)
            if host_id:
                await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest_id} was removed from session by host")
            else:
                await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest_id} left session")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not part of session.")

    async def verify_session(self, session_id: str) -> None:
        await self.repo.verify_session_by_id(session_id)

    async def establish_ws_connection_to_session(self, websocket: WebSocket, session_id: str) -> None:
        channel = self.repo.get_session_key(session_id)

        async with manager.subscribe(channel=channel) as subscriber:
            try:
                async for event in subscriber:
                    await websocket.send_text(event.message)
            except WebSocketDisconnect:
                pass

    async def add_song_to_database(self, song_id: str) -> Song:
        song_info = self.spotify_client.track(song_id)
        await self.repo.add_song_by_info(song_info)
        return Song(**song_info)

    async def get_song_from_database(self, song_id: str) -> Song:
        result = await self.repo.get_song_by_id(song_id)
        return Song.model_validate_json(result)

    async def get_matching_songs_from_database(self, pattern: str, limit: int) -> SongList:
        result = await self.repo.get_songs_by_pattern(pattern, limit)
        songs = [Song.model_validate_json(row) for row in result]
        return SongList(songs=songs)

    # async def delete_song_from_database(self, song_id: str) -> None:
    #     await self.repo.delete_song_by_id(song_id)
