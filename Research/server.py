from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from langchain.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain

from typing import List

import os

import asyncio

 

# Load your OpenAI API key from the environment variable

openai_api_key = "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" # os.getenv("OPENAI_API_KEY")

 

# Initialize the FastAPI application

app = FastAPI()

 

# Store active WebSocket connections in a list

active_connections: List[WebSocket] = []

 

# Initialize LangChain components (GPT-3/4 model using OpenAI API)

chat_model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key,stream=True)

 

# async def async_stream():

#     loop = asyncio.get_event_loop()

#     return await loop.run_in_executor(None, lambda: list(chat_model.stream()))  # wrap the sync stream

 

# This function should yield tokens asynchronously

async def async_stream(user_input):

        # Creating a simple conversational prompt

    prompt = f"Human: {user_input}\nAI:"

 

    print(prompt)

    # Assuming chat_model.stream() is a synchronous generator (you should modify this to async if possible)

    for token in chat_model.stream(prompt):  # Example synchronous generator

        await asyncio.sleep(0)  # Yield control back to the event loop to simulate async behavior

        yield token

# Define a function to process the incoming message using LangChain and stream the response

async def stream_gpt_response(user_input: str, websocket: WebSocket):

 

    # Using OpenAI's stream parameter to get a streamed response

    async for token in async_stream(user_input):  # stream=True enables token-by-token response

        # Send each token as it is generated

        await websocket.send_text(f"{token.content}")

 

@app.websocket("/ws")

async def websocket_endpoint(websocket: WebSocket):

    # Accept the WebSocket connection

    await websocket.accept()

    active_connections.append(websocket)

    try:

        while True:

            # Receive a message from the client

            message = await websocket.receive_text()

 

            # Process the message using LangChain and stream the response

            await stream_gpt_response(message, websocket)

 

            # Optionally, broadcast the message to all other connected clients

            for connection in active_connections:

                if connection != websocket:

                    await connection.send_text(f"User: {message}")

    except WebSocketDisconnect:

        # Remove the WebSocket from the active connections when disconnected

        active_connections.remove(websocket)

        print("Client disconnected")