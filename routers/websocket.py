import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router_websocket = APIRouter()


class WebSocketManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: dict[str, str]):
        for connection in self.connections:
            await connection.send_json(json.dumps(message, ensure_ascii=False))


websocket_manager = WebSocketManager()


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket_manager.connect(websocket)
    await websocket_manager.broadcast({
        "type": f"notification",
        "message": f"Пользователь {client_id} зашел на сайт",
        "time": f"{datetime.now()}"
    })
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast({
                "type": "message",
                "message": f"Пользователь {client_id}: {data}",
                "time": f"{datetime.now()}"
            })
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        await websocket_manager.broadcast({
            "type": "notification",
            "message": f"Пользователь {client_id} покинул сайт",
            "time": f"{datetime.now()}"
        })

