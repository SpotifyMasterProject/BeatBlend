from fastapi import WebSocket, WebSocketDisconnect

from ws.websocket_manager import WebsocketManager


class WebSocketService:
    def __init__(self, websocket_manager: WebsocketManager):
        self._manager = websocket_manager
        self._active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str, ws_type: str) -> None:
        if session_id not in self._active_connections:
            self._active_connections[session_id] = set()
        self._active_connections[session_id].add(websocket)

        async with self._manager.subscribe(channel=f"{ws_type}:{session_id}") as subscriber:
            try:
                async for event in subscriber:
                    await websocket.send_text(event.message)
            except WebSocketDisconnect:
                pass

    async def disconnect(self, session_id: str) -> None:
        for websocket in self._active_connections[session_id]:
            await websocket.close(code=1001, reason='Session ended.')
        del self._active_connections[session_id]