from nuverlan.Node.node import node
from nuverlan.Graph.graph import graph
from langgraph.types import Command

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Enable CORS to allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
g = graph()
g.create_graph()
final_graph = g.setup_graph()
thread={"configurable":{"thread_id":"1"}}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#      await websocket.accept()
#      print("hllo")
#      await websocket.send_text("Hello! WebSocket is working.")
#      for event in final_graph.stream({"user_requirement":"Library management Application."},thread,stream_mode="values"):
   
#         print(event)

#      if final_graph.get_state(thread).tasks[0].interrupts:

#       interrupted_state = final_graph.get_state(thread)[0]
#       handle_interruption(final_graph, interrupted_state)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Open WebSocket connection
    print("WebSocket connected! Waiting for input...")  # Debugging

    while True:
        try:
            message = await websocket.receive_text()  # Wait for UI input
            print(f"Received: {message}")  # Debugging

            for event in final_graph.stream({"user_requirement":message},thread,stream_mode="values"):

                print(event)

            if final_graph.get_state(thread).tasks[0].interrupts:

                interrupted_state = final_graph.get_state(thread)[0]
                handle_interruption(final_graph, interrupted_state)

            # Process only after receiving input
            response = f"Processed: {message.upper()}"  # Example transformation

            await websocket.send_text(response)  # Send response to React
        except Exception as e:
            print("WebSocket Error:", e)
            break  # Stop if error occurs


def handle_interruption(graph, interrupted_state):
    """Handles each interruption and resumes execution."""
   
    thread_config = {"configurable": {"thread_id": "1"}}
    while interrupted_state:
       
        user_input = input(graph.get_state(thread_config).tasks[0].interrupts[0].value + " ")  
        # Inject user input into the interrupted state
        # key = "user_feedback" if "feedback" in interrupted_state["input"] else "confirmation"

        # Resume execution with updated state
        stream = graph.stream(Command(resume=user_input), thread_config, stream_mode="values")
       
        interrupted_state = None  # Reset interruption tracking
        for next_event in stream:
            print("Event:", next_event)
        
        if graph.get_state(thread_config).tasks and graph.get_state(thread_config).tasks[0].interrupts:
            interrupted_state = graph.get_state(thread_config)[0]
        else:
            break
        
if __name__ =="__main__":
   
  
   for event in final_graph.stream({"user_requirement":"Library management Application."},thread,stream_mode="values"):
   
    print(event)

   if final_graph.get_state(thread).tasks[0].interrupts:

        interrupted_state = final_graph.get_state(thread)[0]
        handle_interruption(final_graph, interrupted_state)
