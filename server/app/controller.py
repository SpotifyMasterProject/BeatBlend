import os
import time

from contextlib import asynccontextmanager
from databases import Database
from fastapi import FastAPI, status, Depends, WebSocket
from redis.asyncio import Redis
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

from models.artifact import Artifact, AverageFeatures
from models.token import Token
from models.user import User, SpotifyUser
from models.session import Session
from models.song import Song, SongList, Playlist
from models.recommendation import RecommendationList
from repository import Repository
from service import Service
from websocket_service import WebSocketService
from ws.websocket_manager import WebsocketManager

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

manager = WebsocketManager()
postgres = Database(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}")
redis = Redis(host="redis", port=6379, decode_responses=True)
repository = Repository(postgres, redis)
service = Service(repository, manager)
ws_service = WebSocketService(repository, manager)

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

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post("/auth-codes", status_code=status.HTTP_201_CREATED, response_model=Token)
async def authorize_spotify(host: SpotifyUser) -> Token:
    spotify_token = service.get_spotify_token(host)
    host.username = service.get_display_name(spotify_token)
    host = await service.create_user(host)
    return service.generate_token(host, spotify_token)


@app.post("/token", status_code=status.HTTP_201_CREATED, response_model=Token)
async def authorize(guest: User) -> Token:
    guest = await service.create_user(guest)
    return service.generate_token(guest)


@app.get("/", status_code=status.HTTP_200_OK, response_model=User)
async def read_root(user_id: Annotated[str, Depends(service.verify_token)]) -> User:
    await service.verify_instances(user_ids=user_id)
    return await service.get_user(user_id)


@app.post("/sessions", status_code=status.HTTP_201_CREATED, response_model=Session)
async def create_new_session(host_id: Annotated[str, Depends(service.verify_token)], session: Session) -> Session:
    await service.verify_instances(user_ids=host_id)
    return await service.create_session(host_id, session)


@app.get("/sessions/{session_id}", status_code=status.HTTP_200_OK, response_model=Session)
async def get_specific_session(session_id: str) -> Session:
    await service.verify_instances(session_id=session_id)
    return await service.get_session(session_id)


@app.delete("/sessions/{session_id}", status_code=status.HTTP_200_OK, response_model=Artifact)
async def end_existing_session(host_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> Artifact:
    await service.verify_instances(user_ids=host_id, session_id=session_id)
    await ws_service.disconnect(session_id)
    await service.end_session(host_id, session_id)
    # TODO: change/remove temporary return
    return Artifact(
    songs_played=69,
    songs_added_manually=42,
    most_songs_added_by="de_gueggeli_maa",
    most_votes_by="haudrauf_hans",
    most_significant_feature_overall="energy",
    first_recommendation_vote_percentage=75.5,
    average_features=AverageFeatures(
        danceability=0.567568,
        energy=0.8956756,
        speechiness=0.0564,
        valence=0.755,
        tempo=120.0
    ),
    genre_start=["pop", "hip-hop"],
    genre_end=["jazz", "rock"]
)


# TODO: used for getting all artifacts
# @app.get("/sessions", status_code=status.HTTP_200_OK, response_model=list[Session])
# async def get_all_user_sessions(user_id: Annotated[str, Depends(service.verify_token)]) -> list[Session]:
#     await service.validate_user(user_id)
#     user = await service.get_user(user_id)
#     return await service.get_user_sessions(user)


@app.patch("/sessions/{session_id}/guests", status_code=status.HTTP_200_OK, response_model=Session)
async def add_guest(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> Session:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    return await service.add_guest_to_session(guest_id, session_id)


@app.delete("/sessions/{session_id}/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_guest(host_id: Annotated[str, Depends(service.verify_token)], session_id: str, guest_id: str) -> None:
    await service.verify_instances(user_ids=[host_id, guest_id], session_id=session_id)
    await service.remove_guest_from_session(host_id, guest_id, session_id)


@app.delete("/sessions/{session_id}/guests", status_code=status.HTTP_204_NO_CONTENT)
async def leave_session(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> None:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    await service.remove_guest_from_session("", guest_id, session_id)


@app.patch("/sessions/{session_id}/songs", status_code=status.HTTP_200_OK, response_model=Playlist)
async def add_song(user_id: Annotated[str, Depends(service.verify_token)], session_id: str, song_id: str) -> Playlist:
    await service.verify_instances(user_ids=user_id, session_id=session_id)
    return await service.add_song_to_session(user_id, session_id, song_id)


@app.delete("/sessions/{session_id}/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_song(host_id: Annotated[str, Depends(service.verify_token)], session_id: str, song_id: str) -> None:
    await service.verify_instances(user_ids=host_id, session_id=session_id)
    await service.remove_song_from_session(host_id, session_id, song_id)


@app.patch("/sessions/{session_id}/recommendations", status_code=status.HTTP_200_OK, response_model=RecommendationList)
async def generate_and_get_recommendations(user_id: Annotated[str, Depends(service.verify_token)], session_id: str, limit: int = 3) -> RecommendationList:
    await service.verify_instances(user_ids=user_id, session_id=session_id)
    return await service.generate_and_get_recommendations_from_database(session_id, limit)


@app.get("/sessions/{session_id}/recommendations", status_code=status.HTTP_200_OK, response_model=Song)
async def get_popular_recommendation(user_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> Song:
    await service.verify_instances(user_ids=user_id, session_id=session_id)
    return await service.get_most_popular_recommendation(session_id)


@app.patch("/sessions/{session_id}/recommendations/{song_id}/vote", status_code=status.HTTP_200_OK, response_model=RecommendationList)
async def add_vote(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str, song_id: str) -> RecommendationList:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    return await service.add_vote_to_recommendation(guest_id, session_id, song_id)


@app.delete("/sessions/{session_id}/recommendations/{song_id}/vote", status_code=status.HTTP_204_NO_CONTENT)
async def remove_vote(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str, song_id: str) -> None:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    await service.remove_vote_from_recommendation(guest_id, session_id, song_id)


@app.get("/songs", status_code=status.HTTP_200_OK, response_model=SongList)
async def get_matching_songs(user_id: Annotated[str, Depends(service.verify_token)], pattern: str, limit: int = 10) -> SongList:
    await service.verify_instances(user_ids=user_id)
    return await service.get_matching_songs_from_database(pattern, limit)


# @app.post("/songs/{song_id}", status_code=status.HTTP_200_OK, response_model=Song)
# async def add_song(song_id: str) -> Song:
#     return await service.add_song_to_database(song_id)


@app.get("/songs/{song_id}", status_code=status.HTTP_200_OK, response_model=Song)
async def get_specific_song(song_id: str) -> Song:
    return await service.get_song(song_id)


# @app.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_song(song_id: str) -> None:
#     await service.delete_song_from_database(song_id)


@app.websocket("/sessions/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    try:
        await service.verify_instances(session_id=session_id)
        await websocket.accept()
    except:
        await websocket.close(1001, "Session does not exist.")
    await ws_service.connect(websocket, session_id, ws_type="session")


@app.websocket("/playlist/{session_id}")
async def websocket_playlist(websocket: WebSocket, session_id: str):
    try:
        await service.verify_instances(session_id=session_id)
        await websocket.accept()
    except:
        await websocket.close(1001, "Session does not exist.")
    await ws_service.connect(websocket, session_id, ws_type="playlist")


@app.websocket("/recommendations/{session_id}")
async def websocket_recommendations(websocket: WebSocket, session_id: str):
    try:
        await service.verify_instances(session_id=session_id)
        await websocket.accept()
    except:
        await websocket.close(1001, "Session does not exist.")
    await ws_service.connect(websocket, session_id, ws_type="recommendations")
