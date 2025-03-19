from ast import Dict
from typing_extensions import TypedDict
from typing import Annotated, List, Literal,Any, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
import operator
from nuverlan.Schema.schema import Section

# class State(TypedDict):
#     user_requirement:str
#     #user_story:Annotated[list,add_messages]
#     product_owner: str
#     design_document:str
#     graph:StateGraph
#     thread:Any
#     user_story: Annotated[list,add_messages] #List[str,add_messages]  # User-provided requirements
#     project_structure: Optional[Dict[str, Dict[str, str]]] = None  # Folder & file structure
#     generated_files: Optional[Dict[str, Dict[str, str]]] = None  # Code files
#     review_feedback: Optional[Dict[str, Dict[str, List[str]]]] = None  # AI review feedback

# # Worker state
# class WorkerState(TypedDict):
#     section: Section
#     completed_sections: Annotated[list, operator.add]


# Graph state
class State(TypedDict):
    topic: str  # Report topic
    sections: list[Section]  # List of report sections
    completed_sections: Annotated[
        list, operator.add
    ]  # All workers write to this key in parallel
    final_report: str  # Final report
    user_story: Annotated[list,add_messages] #List[str,add_messages]  # User-provided requirements
    # project_structure: Optional[Dict[str, Dict[str, str]]] = None  # Folder & file structure
    # generated_files: Optional[Dict[str, Dict[str, str]]] = None  # Code files
    # review_feedback: Optional[Dict[str, Dict[str, str]]] = None  # Code files
    user_requirement:str
    #user_story:Annotated[list,add_messages]
    product_owner: str
    design_document:str
    graph:StateGraph
    thread:Any


# Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]
