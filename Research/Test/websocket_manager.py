import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.human_input = None  # Stores human input or commands
        self.command = None  # Stores commands like /stop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        """Send messages to all active WebSocket connections."""
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def wait_for_human_input(self):
        """Wait for human input asynchronously."""
        while self.human_input is None:
            await asyncio.sleep(0.5)
        return self.human_input

manager = ConnectionManager()
