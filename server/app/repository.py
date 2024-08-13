from redis.asyncio import Redis
from fastapi import HTTPException, status
from models.session import Session
from typing import Optional
from models.user import User


class Repository:
    def __init__(self):
        self.redis = Redis(host="redis", port=6379, decode_responses=True)

    @staticmethod
    def get_user_key(user_id) -> str:
        return f'user:{user_id}'

    @staticmethod
    def get_session_key(session_id) -> str:
        return f'session:{session_id}'

    @staticmethod
    def get_invite_key(invite_token) -> str:
        return f'invite:{invite_token}'

    async def set_user(self, user: User) -> None:
        await self.redis.set(self.get_user_key(user.id), user.model_dump_json())

    async def get_user_by_id(self, user_id: str) -> Optional[bytes]:
        return await self.redis.get(self.get_user_key(user_id))

    async def validate_user_by_id(self, user_id: str) -> None:
        if await self.redis.exists(self.get_user_key(user_id)) == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized! Invalid user ID.")

    async def set_session(self, session: Session) -> None:
        await self.redis.set(self.get_session_key(session.id), session.model_dump_json())

    async def get_session_by_id(self, session_id: str) -> Optional[bytes]:
        return await self.redis.get(self.get_session_key(session_id))

    async def get_session_by_key(self, session_key: str) -> Optional[bytes]:
        return await self.redis.get(session_key)

    def get_all_sessions_by_pattern(self):
        return self.redis.scan_iter(match='session:*')

    async def validate_session_by_id(self, session_id: str) -> None:
        if await self.redis.exists(self.get_session_key(session_id)) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid session ID.")

    async def set_session_by_invite(self, session: Session) -> None:
        await self.redis.set(self.get_invite_key(session.invite_token), session.id)

    async def get_session_by_invite(self, invite_token: str) -> Optional[str]:
        return await self.redis.get(self.get_invite_key(invite_token))

    async def validate_invite_by_token(self, invite_token: str) -> None:
        if await self.redis.exists(self.get_invite_key(invite_token)) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite link.")

