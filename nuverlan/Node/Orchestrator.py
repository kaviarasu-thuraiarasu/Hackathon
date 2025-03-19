from langgraph.constants import Send
from typing_extensions import TypedDict

from typing import List, Annotated,Optional,Dict
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import START,StateGraph,END,add_messages
import operator
from nuverlan.Schema.schema import Sections,Section
from nuverlan.State.state import State,WorkerState

from langchain_openai import ChatOpenAI


from typing import Annotated, List
import operator

class Orchestrator:

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o",stream_usage=True)
        self.planner = self.llm.with_structured_output(Sections)


    # Nodes
    def orchestrator(self,state: State):
        """Orchestrator that generates a plan for the report"""

        # Generate queries
        report_sections = self.planner.invoke( f"We are creating microservice,Give me the list of task for the user story : {state['topic']}")
        return {"sections": report_sections.sections}



    def llm_call(self,state: WorkerState):
        """Worker writes a section of the report"""
        prompt = """
                    You are a Python code generator. Based on the user request, generate the Python code required to implement the functionality described in the request. Do not provide any explanation or commentary—only the generated Python code should be returned, followed by the **relative file path** where the code should be saved in the current directory, and the **file extension type** (e.g., .py for Python files, .js for JavaScript files).

                    Request: "Write Python code for a function that allows a user to search for books in a library by title or author. The code should use a simple in-memory list of books for searching."

                    Response should be only the code, relative file path (including the extension), and filename in the following format:

                    <Generated Python Code>

                    Path: <relative file path in the current directory>
                    Filename: <filename.ext>  # The file extension (e.g., .py for Python files, .js for JavaScript files)

                    For the following task
                """

        section = self.llm.invoke(f"{prompt} : {state['section'].task}")
        print("************CODE GENRATION******************")
        print(section.content)
        # Generate and save code to the file
        # path, filename = generate_and_save_code(section.content)
        # print(path +"======="+ filename)
        # Write the updated section to completed sections
        return {"completed_sections": [section.content]}


    def synthesizer(self,state: State):
        """Synthesize full report from sections"""
        completed_sections = state["completed_sections"]
        completed_report_sections = "\n\n---\n\n".join(completed_sections)
        return {"final_report": completed_report_sections}


    # Conditional edge function to create llm_call workers that each write a section of the report
    def assign_workers(self,state: State):
        """Assign a worker to each section in the plan"""
        
        # Kick off section writing in parallel via Send() API
        return [Send("llm_call", {"section": s}) for s in state["sections"]]


