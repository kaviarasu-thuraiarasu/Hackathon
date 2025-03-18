from langgraph.constants import Send
from typing_extensions import TypedDict
from pydantic import BaseModel,Field
from typing import List, Annotated,Optional,Dict
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import START,StateGraph,END,add_messages
import operator

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o",stream_usage=True)

# Schema for structured output to use in planning
class Section(BaseModel):
    # file_name: str = Field(
    #     description="Name for this section of the report.",
    # )
    # file_path: str = Field(
    #     description="Brief overview of the main topics and concepts to be covered in this section.",
    # )
    task: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )





class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )


# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)

# Graph state
class State(TypedDict):
    topic: str  # Report topic
    sections: list[Section]  # List of report sections
    completed_sections: Annotated[
        list, operator.add
    ]  # All workers write to this key in parallel
    final_report: str  # Final report
    user_story: Annotated[list,add_messages] #List[str,add_messages]  # User-provided requirements
    project_structure: Optional[Dict[str, Dict[str, str]]] = None  # Folder & file structure
    generated_files: Optional[Dict[str, Dict[str, str]]] = None  # Code files
    review_feedback: Optional[Dict[str, Dict[str, str]]] = None  # Code files


# Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]

from typing import Annotated, List
import operator




# Nodes
def orchestrator(state: State):
    """Orchestrator that generates a plan for the report"""

    # Generate queries
    report_sections = planner.invoke( f"We are creating microservice,Give me the list of task for the user story : {state['topic']}")
    return {"sections": report_sections.sections}


import os

# Function to generate the Python code and save it to a file
def generate_and_save_code(response):
    # Assuming `response` is the output of the LangChain agent
    # Example format of response:
    # "<generated Python code>\n\nPath: <absolute file path>\nFilename: <filename.py>"

    # Split the response into code, path, and filename
    code, path_filename = response.strip().split("\n\nPath: ")
    path, filename = path_filename.split("\nFilename: ")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create and write the code to the specified file
    with open(path, 'w') as file:
        file.write(code)
    
    # Return the saved file path and filename
    return path, filename

def llm_call(state: WorkerState):
    """Worker writes a section of the report"""

    # Generate section
    print(state['section'])
    prompt = """
       You are a Python code generator. Based on the user request, generate the Python code required to implement the functionality described in the request. Do not provide any explanation or commentary—only the generated Python code should be returned, followed by the **relative file path** where the code should be saved in the current directory, and the **file extension type** (e.g., .py for Python files, .js for JavaScript files).

Request: "Write Python code for a function that allows a user to search for books in a library by title or author. The code should use a simple in-memory list of books for searching."

Response should be only the code, relative file path (including the extension), and filename in the following format:

<Generated Python Code>

Path: <relative file path in the current directory>
Filename: <filename.ext>  # The file extension (e.g., .py for Python files, .js for JavaScript files)

        For the following task
"""

    section = llm.invoke(f"{prompt} : {state['section'].task}")
    print("************CODE GENRATION******************")
    #print(section.content)
    # Generate and save code to the file
    path, filename = generate_and_save_code(section.content)
    print(path +"======="+ filename)
    # Write the updated section to completed sections
    return {"completed_sections": [section.content]}


def synthesizer(state: State):
    """Synthesize full report from sections"""

    # List of completed sections
    completed_sections = state["completed_sections"]

    # Format completed section to str to use as context for final sections
    completed_report_sections = "\n\n---\n\n".join(completed_sections)

    return {"final_report": completed_report_sections}


# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
    """Assign a worker to each section in the plan"""
    
    # Kick off section writing in parallel via Send() API
    return [Send("llm_call", {"section": s}) for s in state["sections"]]


# Build workflow
orchestrator_worker_builder = StateGraph(State)

# Add the nodes
orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("llm_call", llm_call)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)

# Add edges to connect nodes
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator", assign_workers, ["llm_call"]
)
orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile the workflow
orchestrator_worker = orchestrator_worker_builder.compile()

# Show the workflow
#display(Image(orchestrator_worker.get_graph().draw_mermaid_png()))

# Invoke
prompt = [
  "As a library member, I want to be able to search for books by various criteria such as title, author, or genre. This feature will help me quickly find the books I am interested in, making it easier for me to borrow them. Whether I want a specific title or I'm just browsing for something new to read, having an effective search functionality will enhance my library experience..",
   "As a library member, I want to be able to view the books I currently have checked out and see their due dates. This feature will allow me to keep track of when my borrowed items are due back, helping me avoid late fees. It will also give me a better understanding of what I have in hand and when to return them, making the borrowing process more organized.",
   "As a library administrator, I want the ability to add new books, update existing book information, or remove books from the inventory. This feature is crucial for maintaining an up-to-date and accurate catalog of the library’s collection. It ensures that members can access accurate information when searching for books and allows the library to manage its resources efficiently."
  
]
state = orchestrator_worker.invoke({"topic": prompt})
#print(state)

from IPython.display import Markdown
Markdown(state["final_report"])