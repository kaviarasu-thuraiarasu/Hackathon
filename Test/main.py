from fastapi import FastAPI, WebSocket
from websocket_manager import manager
from workflow import graph
from state import ChatState, Command
import json
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
   await websocket.accept()
   session_id = None  # Track user session

   while True:
        data = await websocket.receive_text()
        #logging.debug(f"Received message: {data}")

        # If it's the first message, create a new session
        if session_id is None:
            session_id = '123'

        human_response = (
        "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
        " It's much more reliable and extensible than simple autonomous agents."
        )

        command = Command(resume={"data": human_response})
        events = graph.stream(command, config = {"configurable": {"thread_id": "1"}}, stream_mode="values")

        for event in events:
            #logging.debug(f"Sending response: {event}")
            await websocket.send_text(json.dumps(event))

@app.get("/start")
async def start_ai():
    """Start AI processing and listen for human interventions."""
    print("...................")
    state = ChatState(messages=["Explain machine learning"])
    events = graph.stream(state, config={}, stream_mode="values")

    async for event in events:
        await manager.send_message({"role": "ai", "text": event})

    return {"status": "AI processing started"}

@app.post("/human-input")
async def human_override(human_response: str):
    """Allows human input to override AI response."""
    command = Command(resume={"data": human_response})
    events = graph.stream(command,config = {"configurable": {"thread_id": "1"}}
, stream_mode="values")

    async for event in events:
        await manager.send_message({"role": "human", "text": event})

    return {"status": "Human intervention processed"}
