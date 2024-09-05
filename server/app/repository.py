import os

from databases import Database
from fastapi import HTTPException, status
from models.session import Session
from models.user import User
from redis.asyncio import Redis
from sqlalchemy import Column, Table, MetaData, Integer, String, ARRAY, Float, Date, insert, select, func
from typing import Optional

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

postgres = Database(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}")

metadata = MetaData()
songs = Table(
    "songs",
    metadata,
    Column("id", String, primary_key=True),
    Column("track_name", String),
    Column("album", String),
    Column("album_id", String),
    Column("artists", ARRAY(String)),
    Column("artist_ids", ARRAY(String)),
    Column("danceability", Float),
    Column("energy", Float),
    Column("speechiness", Float),
    Column("valence", Float),
    Column("tempo", Float),
    Column("duration_ms", Integer),
    Column("release_date", Date),
    Column("popularity", Float, nullable=True)
)

class Repository:
    def __init__(self):
        self.redis = Redis(host="redis", port=6379, decode_responses=True)

    @staticmethod
    def get_user_key(user_id) -> str:
        return f'user:{user_id}'

    @staticmethod
    def get_session_key(session_id) -> str:
        return f'session:{session_id}'

    async def set_user(self, user: User) -> None:
        await self.redis.set(self.get_user_key(user.id), user.model_dump_json())

    async def get_user_by_id(self, user_id: str) -> Optional[bytes]:
        return await self.redis.get(self.get_user_key(user_id))

    async def verify_user_by_id(self, user_id: str) -> None:
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

    async def verify_session_by_id(self, session_id: str) -> None:
        if await self.redis.exists(self.get_session_key(session_id)) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid session ID.")

    async def delete_session_by_id(self, session_id: str) -> None:
        await self.redis.delete(self.get_session_key(session_id))
