from typing import Annotated
from langchain_openai import ChatOpenAI


from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from langchain_core.messages import HumanMessage
from websocket_manager import manager
from state import ChatState
checkpointer = MemorySaver()
# Initialize the graph
graph_builder = StateGraph(ChatState)

# Tavily Search Tool (Web Search)
search_tool = TavilySearchResults(max_results=2)

# Human Assistance (Interrupt AI)
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    manager.human_input = None  # Reset previous input
    manager.human_input = interrupt({"query": query})
    return manager.human_input["data"]

# Add tools (Search + Human Assist)
tools = [search_tool, human_assistance]

# Claude 3.5 with Tool Handling
llm = ChatOpenAI(model="gpt-4",stream_usage=True)
llm_with_tools = llm.bind_tools(tools)

# AI Chatbot Node
def chatbot(state: ChatState):
    """Handles AI responses & tool invocation."""
    message = llm_with_tools.invoke(state["messages"])

    # Check if the AI requests a tool (e.g., Search or Human Assist)
    assert len(message.tool_calls) <= 1  # Only allow one tool at a time

    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

# Tool Execution Node
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Define Edges for AI → Tool Execution → AI
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,  # If tools are needed, execute them
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile the workflow graph
graph = graph_builder.compile(checkpointer=checkpointer)
