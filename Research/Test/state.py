from typing import Annotated, List
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt
from langchain.schema import HumanMessage

from typing_extensions import TypedDict

class ChatState(TypedDict):
    messages: Annotated[List[HumanMessage], add_messages]
