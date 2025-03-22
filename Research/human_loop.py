import asyncio
import json
from langgraph.graph import StateGraph
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.human_input = None  # Stores human input or commands
        self.command = None  # Stores special commands like /stop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        """Send messages to all active WebSocket connections."""
        for connection in self.active_connections:
            await connection.send_text(message)

    async def wait_for_human_input(self):
        """Wait for human input asynchronously."""
        while self.human_input is None:
            await asyncio.sleep(0.5)  # Check every 0.5 seconds
        return self.human_input

manager = ConnectionManager()

# Chat State Class
class ChatState:
    def __init__(self, history=None):
        self.history = history or []
        self.human_override = None  # Stores human intervention
        self.command = None  # Stores commands like /stop

# AI Processing with Interrupt Check
async def ai_response(state):
    model = ChatOpenAI(model_name="gpt-4-turbo")

    for i in range(5):  # Simulating AI processing in chunks
        await asyncio.sleep(1)  # Simulated processing delay
        
        # Check for human input or commands
        if manager.human_input:
            if manager.human_input.startswith("/"):  # Command detected
                state.command = manager.human_input  # Store command
                manager.human_input = None  # Reset input
                return state  # Stop AI and handle the command

            # If it's a normal message, switch to human review
            state.human_override = manager.human_input  
            manager.human_input = None
            return state  # Stop AI and switch to human review
    
    # AI completes its response
    response = model.predict_messages(state.history)
    state.history.append(response)
    
    await manager.send_message(json.dumps({"role": "ai", "text": response.content}))
    return state

# Human Review Node (Triggered by Interrupt)
async def human_review(state):
    await manager.send_message(json.dumps({"role": "system", "text": "Human override detected. Please respond..."}))
    
    # Wait for human input
    state.human_override = await manager.wait_for_human_input()
    
    # Store human response and reset override
    state.history.append(HumanMessage(content=state.human_override))
    state.human_override = None

    return state

# Command Handling Node
async def command_handler(state):
    if state.command == "/stop":
        await manager.send_message(json.dumps({"role": "system", "text": "AI has been stopped by human command."}))
        return None  # Stop workflow

    elif state.command.startswith("/override"):
        override_text = state.command.replace("/override ", "").strip()
        state.history.append(HumanMessage(content=override_text))
        await manager.send_message(json.dumps({"role": "system", "text": f"AI overridden with: {override_text}"}))

    state.command = None  # Reset command
    return state

# WebSocket for Human Interrupts & Commands
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            manager.human_input = data  # Store human input or command
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

# Define Workflow
workflow = StateGraph(ChatState)
workflow.add_node("ai", ai_response)
workflow.add_node("human", human_review)
workflow.add_node("command", command_handler)

workflow.set_entry_point("ai")

# **Interrupt Handling**
workflow.add_conditional_edges(
    "ai",
    lambda state: "command" if state.command else ("human" if state.human_override else "ai")
)

workflow.add_edge("human", "ai")  # Resume AI after human input
workflow.add_edge("command", "ai")  # Resume AI after command processing

graph = workflow.compile()
