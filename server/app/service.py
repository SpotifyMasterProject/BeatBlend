import os
import jwt
import uuid

from server.app.ws.websocket_manager import WebsocketManager
from contextlib import asynccontextmanager
from repository import Repository
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from models.user import User
from models.token import Token
from datetime import timedelta, datetime, timezone
from models.session import Session

manager = WebsocketManager()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await manager.connect()
    yield
    await manager.disconnect()


class Service:
    def __init__(self):
        self.repo = Repository()

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

    # @staticmethod
    # def exchange_code_for_token(auth_code: str) -> str:
    #     id_secret = f'{os.getenv("SPOTIFY_CLIENT_ID")}:{os.getenv("SPOTIFY_CLIENT_SECRET")}'
    #     base64_encoded = base64.b64encode(id_secret.encode()).decode()
    #
    #     response = requests.post(
    #         "https://accounts.spotify.com/api/token",
    #         headers={
    #             "content-type": "application/x-www-form-urlencoded",
    #             "Authorization": "Basic " + base64_encoded,
    #         },
    #         data={
    #             "grant_type": "authorization_code",
    #             "code": auth_code,
    #             "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    #         }
    #     )
    #     return response.json()["access_token"]

    async def create_user(self, user: User) -> User:
        user.id = str(uuid.uuid4())
        await self.repo.set_user(user)

        return user

    async def get_user(self, user_id: str) -> User:
        result = await self.repo.get_user_by_id(user_id)
        return User.model_validate_json(result)

    async def validate_user(self, user_id: str) -> None:
        await self.repo.validate_user_by_id(user_id)

    async def create_session(self, host_id: str, session: Session) -> Session:
        session.id = str(uuid.uuid4())
        session.host = str(host_id)

        session.invite_token = str(uuid.uuid4())
        # TODO: adjust URL
        session.invite_link = f'http://localhost:5173/sessions/join/{session.invite_token}'

        await self.repo.set_session(session)
        await self.repo.set_session_by_invite(session)

        await manager.publish(channel=self.repo.get_session_key(session.id), message="New session created")

        return session

    async def get_all_sessions(self) -> List[Session]:
        session_keys = [session_id async for session_id in self.repo.get_all_sessions_by_pattern()]
        sessions = []
        for session_key in session_keys:
            result = await self.repo.get_session_by_key(session_key)
            sessions.append(Session.model_validate_json(result))

        return sessions

    async def add_guest_to_session(self, guest_id: str, session_id: str, invite_token: str) -> Session:
        if invite_token:
            session_id = await self.repo.get_session_by_invite(invite_token)
        result = await self.repo.get_session_by_id(session_id)
        session = Session.model_validate_json(result)

        if guest_id not in session.guests:
            session.guests.append(guest_id)
            await self.repo.set_session(session)
            await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest_id} has joined the session")

        return session

    async def remove_guest_from_session(self, host_id: str, guest_id: str, session_id: str) -> None:
        result = await self.repo.get_session_by_id(session_id)
        session = Session.model_validate_json(result)

        if host_id and session.host != str(host_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not host of session.")

        if guest_id in session.guests:
            session.guests.remove(guest_id)
            await self.repo.set_session(session)
            await manager.publish(channel=self.repo.get_session_key(session.id), message=f"Guest {guest_id} was removed from session")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest not part of session.")

    async def validate_session(self, session_id: str) -> None:
        await self.repo.validate_session_by_id(session_id)

    async def validate_invite(self, invite_token: str) -> None:
        await self.repo.validate_invite_by_token(invite_token)

    async def establish_ws_connection_to_session(self, websocket: WebSocket, session_id: str) -> None:
        channel = self.repo.get_session_key(session_id)

        async with manager.subscribe(channel=channel) as subscriber:
            try:
                async for event in subscriber:
                    await websocket.send_text(event.message)
            except WebSocketDisconnect:
                pass
