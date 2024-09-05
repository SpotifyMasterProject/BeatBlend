from fastapi import FastAPI, status, Depends, WebSocket, WebSocketDisconnect
from service import Service, lifespan
from models.token import Token
from models.user import User, SpotifyUser
from models.session import Session
from models.song import Song
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from recommender.songs_dataset import SongsDataset

service = Service()
songsDataset = SongsDataset("./recommender/dataset.csv")

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
    host.username = service.get_spotify_name()
    host = await service.create_user(host)
    token_info = service.spotify_oauth.get_access_token(host.auth_code)
    return service.generate_token(host, Token(**token_info))


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


# TODO: used for getting all artifacts
# @app.get("/sessions", status_code=status.HTTP_200_OK, response_model=list[Session])
# async def get_all_user_sessions(user_id: Annotated[str, Depends(service.verify_token)]) -> list[Session]:
#     await service.validate_user(user_id)
#     user = await service.get_user(user_id)
#     return await service.get_user_sessions(user)


@app.post("/sessions/{session_id}/guests", status_code=status.HTTP_200_OK, response_model=Session)
async def add_guest(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> Session:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    return await service.add_guest_to_session(guest_id, session_id)


# TODO: this will be adapted once we have the postgres database
# @app.patch("/sessions/{session_id}/songs", status_code=status.HTTP_200_OK)
# async def add_song(user_id: Annotated[str, Depends(service.verify_token)], session_id: str, song_id: str) -> Session:
#     await service.validate_user(user_id)
#     await service.validate_session(session_id)
#     return await service.add_song_to_session(user_id, session_id, song_id)


# TODO: this will be adapted once we have the postgres database
@app.get("/songs/{pattern}", status_code=status.HTTP_200_OK, response_model=list[Song])
async def get_songs(user_id: Annotated[str, Depends(service.verify_token)], pattern: str) -> list[Song]:
    await service.verify_instances(user_ids=user_id)
    return songsDataset.get_matching_songs(pattern)


@app.delete("/sessions/{session_id}", status_code=status.HTTP_200_OK)
async def end_existing_session(host_id: Annotated[str, Depends(service.verify_token)], session_id: str):
    await service.verify_instances(user_ids=host_id, session_id=session_id)
    return await service.end_session(host_id, session_id)


@app.delete("/sessions/{session_id}/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_guest(host_id: Annotated[str, Depends(service.verify_token)], session_id: str, guest_id: str) -> None:
    await service.verify_instances(user_ids=[host_id, guest_id], session_id=session_id)
    await service.remove_guest_from_session(host_id, guest_id, session_id)


@app.delete("/sessions/{session_id}/guests", status_code=status.HTTP_204_NO_CONTENT)
async def leave_session(guest_id: Annotated[str, Depends(service.verify_token)], session_id: str) -> None:
    await service.verify_instances(user_ids=guest_id, session_id=session_id)
    await service.remove_guest_from_session("", guest_id, session_id)


@app.websocket("/ws/{session_id}")
async def websocket_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        await service.establish_ws_connection_to_session(websocket, session_id)
    except WebSocketDisconnect:
        print(f'WebSocket for session {session_id} disconnected')
    finally:
        await service.end_ws_connection_to_session(session_id)


# This WS code is inspired by the encode/broadcaster package.
# If something needs to be fixed or changed, look at their GitHub repo.
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # This endpoint only serves a simplex operation.
#     # If the future desires duplex operations, look at the encode/broadcaster example.
#     await websocket.accept()
#
#     async with manager.subscribe(channel="test") as subscriber:
#         try:
#             async for event in subscriber:
#                 await websocket.send_text(event.message)
#         except WebSocketDisconnect:
#             pass
#
#
# async def test_websocket():
#     event = asyncio.Event()
#     asyncio.create_task(set_websocket_test_task(event))
#     await handle_test_event(event)
#
#
# async def set_websocket_test_task(event):
#     while True:
#         await asyncio.sleep(2)
#         event.set()
#         event.clear()
#
#
# async def handle_test_event(event):
#     while True:
#         await event.wait()
#         await manager.publish(channel="test", message="WEBSOCKET TEST MESSAGE")
