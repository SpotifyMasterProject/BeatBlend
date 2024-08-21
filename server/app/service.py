import os
import jwt
import uuid

from ws.websocket_manager import WebsocketManager
from spotipy.oauth2 import SpotifyOAuth, Spotify
from contextlib import asynccontextmanager
from repository import Repository
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from models.user import User
from models.token import Token
from datetime import timedelta, datetime, timezone
from models.session import Session
from models.song import Song

manager = WebsocketManager()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await manager.connect()
    yield
    await manager.disconnect()


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
        secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("JWT_ALGORITHM")
        auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")

        try:
            payload = jwt.decode(token, key=secret_key, algorithms=[algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise auth_exception
        except InvalidTokenError:
            raise auth_exception
        return user_id

    @staticmethod
    def generate_token(user: User) -> Token:
        jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
        secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("JWT_ALGORITHM")

        to_encode = {"sub": user.id, "username": user.username}
        access_token_expires = timedelta(minutes=jwt_expire_minutes)
        expire = datetime.now(timezone.utc) + (access_token_expires or timedelta(minutes=30))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            secret_key,
            algorithm=algorithm
        )
        return Token(access_token=encoded_jwt, token_type="bearer")

    async def create_user(self, user: User) -> User:
        user.id = str(uuid.uuid4())
        await self.repo.set_user(user)

        return user

    async def get_user(self, user_id: str) -> User:
        result = await self.repo.get_user_by_id(user_id)
        return User.model_validate_json(result)

    async def validate_user(self, user_id: str) -> None:
        await self.repo.validate_user_by_id(user_id)

    async def create_session(self, host: User, session: Session) -> Session:
        session.id = str(uuid.uuid4())
        session.host = str(host.id)
        session.host_name = host.username
        session.creation_date = datetime.now()

        # TODO: adjust URL
        session.invite_link = f'{os.getenv("LOCAL_IP_ADDRESS")}:8080/{session.id}/join'

        await self.repo.set_session(session)
        await manager.publish(channel=self.repo.get_session_key(session.id), message="New session created")

        host.sessions.append(session.id)
        await self.repo.set_user(host)

        return session

    async def get_session(self, session_id: str) -> Session:
        result = await self.repo.get_session_by_id(session_id)
        return Session.model_validate_json(result)

    async def add_guest_to_session(self, guest: User, session_id: str) -> Session:
        result = await self.repo.get_session_by_id(session_id)
        session = Session.model_validate_json(result)

        if guest.id not in session.guests:
            session.guests.append(guest.id)
            await self.repo.set_session(session)
            await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest.id} has joined the session")

            guest.sessions.append(session.id)
            await self.repo.set_user(guest)

        return session

    # async def add_song_to_session(self, user_id: str, session_id: str, song_id: str) -> Session:
    #     result = await self.repo.get_session_by_id(session_id)
    #     session = Session.model_validate_json(result)
    #     # TODO: try -> search database with song_id
    #     try:
    #         result = await self.repo.get_song_by_id(song_id)
    #         song = Song.model_validate_json(result)
    #         session.playlist.append(song)
    #     # TODO: catch -> Spotify API call to retrieve information
    #     except Exception:
    #         song_info = self.spotify_client.track(song_id)
    #         session.playlist.append(Song(**song_info))
    #
    #     await self.repo.set_session(session)
    #     await manager.publish(channel=self.repo.get_session_key(session.id), message=f"User {user_id} has added a song")
    #
    #     return session

    async def remove_guest_from_session(self, host_id: str, guest: User, session_id: str) -> None:
        result = await self.repo.get_session_by_id(session_id)
        session = Session.model_validate_json(result)

        if host_id and session.host != str(host_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not host of session.")

        if guest.id in session.guests:
            session.guests.remove(guest.id)
            await self.repo.set_session(session)
            await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest.id} was removed from session")

            guest.sessions.remove(session.id)
            await self.repo.set_user(guest)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not part of session.")

    async def validate_session(self, session_id: str) -> None:
        await self.repo.validate_session_by_id(session_id)

    async def establish_ws_connection_to_session(self, websocket: WebSocket, session_id: str) -> None:
        channel = self.repo.get_session_key(session_id)

        async with manager.subscribe(channel=channel) as subscriber:
            try:
                async for event in subscriber:
                    await websocket.send_text(event.message)
            except WebSocketDisconnect:
                pass
