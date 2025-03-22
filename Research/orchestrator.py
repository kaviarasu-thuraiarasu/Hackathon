from langgraph.graph import StateGraph
from pydantic import BaseModel
import os

# Import LLM Worker & File Writer Worker
from workers.llm_worker import generate_project_structure
from workers.file_writer import write_files_to_disk

# Define State for LLM-based Code Generation
class CodeGenState(BaseModel):
    user_stories: list[str]  # Input user stories
    project_structure: dict | None = None  # Folder & file structure
    generated_files: dict | None = None  # Generated code

# Define the Orchestrator Workflow
orchestrator_graph = StateGraph(CodeGenState)

# Add Nodes
orchestrator_graph.add_node("generate_project_structure", generate_project_structure)
orchestrator_graph.add_node("write_files_to_disk", write_files_to_disk)

# Set Execution Order
orchestrator_graph.set_entry_point("generate_project_structure")
orchestrator_graph.add_edge("generate_project_structure", "write_files_to_disk")

# Compile the Workflow
orchestrator_workflow = orchestrator_graph.compile()
