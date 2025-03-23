# websocket_handler.py

from fastapi import WebSocket

class WebSocketHandler:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def receive_message(self, user_id: str) -> str:
        websocket = self.active_connections.get(user_id)
        if websocket:
            # This will be blocking, so ideally this should run in a different thread or task
            data = await websocket.receive_text()
            return data
        return ""
