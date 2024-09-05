import jwt
import os
import time
import uuid

from datetime import timedelta, datetime, timezone
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from contextlib import asynccontextmanager
from repository import Repository, postgres
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from models.user import User
from models.token import Token
from models.session import Session
from ws.websocket_manager import WebsocketManager

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

manager = WebsocketManager()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await manager.connect()
    for attempt in range(10):
        try:
            await postgres.connect()
            break
        except ConnectionRefusedError as e:
            if attempt == 9:
                raise e
            time.sleep(6)
    yield
    await manager.disconnect()
    await postgres.disconnect()


class Service:
    def __init__(self):
        self.repo = Repository()
        self.spotify_oauth = SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-library-read"  # scope defines functionalities
        )

        self.spotify_client = Spotify(auth_manager=self.spotify_oauth)

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
    def generate_token(user: User, spotify_token: Optional[Token] = None) -> Token:
        to_encode = {"sub": user.id, "username": user.username}
        # Also encode the spotify token for this session.
        if spotify_token is not None:
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

    def get_spotify_name(self) -> str:
        user_profile = self.spotify_client.me()
        return user_profile['id']

    async def verify_instances(self, user_ids: str | list[str] = "", session_id: str = ""):
        if isinstance(user_ids, str) and user_ids:
            await self.verify_user(user_ids)
        elif isinstance(user_ids, list):
            for user_id in user_ids:
                await self.verify_user(user_id)
        if session_id:
            await self.verify_session(session_id)

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
        session.invite_link = f'http://{os.getenv("LOCAL_IP_ADDRESS")}:8080/{session.id}/join'

        await self.repo.set_session(session)
        await manager.publish(channel=self.repo.get_session_key(session.id), message="New session created")

        host.sessions.append(session.id)
        await self.repo.set_user(host)

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
            await manager.publish(channel=self.repo.get_session_key(session.id),
                                  message=f"Guest {guest_id} has joined the session")
            guest.sessions.append(session.id)
            await self.repo.set_user(guest)
        return session

    # TODO: this will be adapted once we have the postgres database
    # async def add_song_to_session(self, user_id: str, session_id: str, song_id: str) -> Session:
    #     session = await self.get_session(session_id)
    #     try:
    #         result = await self.repo.get_song_by_id(song_id)
    #         song = Song.model_validate_json(result)
    #         session.playlist.append(song)
    #     except Exception:
    #         song_info = self.spotify_client.track(song_id)
    #         session.playlist.append(Song(**song_info))
    #
    #     await self.repo.set_session(session)
    #     await manager.publish(channel=self.repo.get_session_key(session.id), message=f"User {user_id} has added a song")
    #
    #     return session

    async def remove_guest_from_session(self, host_id: str, guest_id: str, session_id: str) -> None:
        guest = await self.get_user(guest_id)
        session = await self.get_session(session_id)

        if host_id and session.host_id != str(host_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not host of session.")

        if guest.id in session.guests:
            session.guests.remove(guest.id)
            await self.repo.set_session(session)
            await manager.publish(channel=self.repo.get_session_key(session.id),
                                  message=f"Guest {guest_id} was removed from session")
            guest.sessions.remove(session.id)
            await self.repo.set_user(guest)
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

    async def end_session(self, host_id: str, session_id: str):
        host = await self.get_user(host_id)
        session = await self.get_session(session_id)
        self.verify_host_of_session(host_id, session)
        host.sessions.remove(session.id)
        for guest_id in session.guests:
            guest = await self.get_user(guest_id)
            guest.sessions.remove(session.id)
        await self.repo.delete_session_by_id(session_id)
        # TODO: create and return session artifact
        return
