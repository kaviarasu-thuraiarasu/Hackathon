from langgraph.constants import Send
from typing_extensions import TypedDict

from typing import List, Annotated,Optional,Dict
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import START,StateGraph,END,add_messages
import operator
from nuverlan.Schema.schema import Sections,Section
from nuverlan.State.state import State,WorkerState

from langchain_openai import ChatOpenAI
from nuverlan.Utils.util import generate_and_save_code
from nuverlan.llm.model import model
from typing import Annotated, List
import operator

class Orchestrator:

    def __init__(self):
        self.llm = model().llm #ChatOpenAI(model="gpt-4o",stream_usage=True)
        self.planner = self.llm.with_structured_output(Sections)


    # Nodes
    def orchestrator(self,state: State):
        """Orchestrator that generates a plan for the report"""

        # Generate queries
        report_sections = self.planner.invoke( f"We are creating microservice,Give me the list of task for the user story : {state['task']}")
        return {"sections": report_sections.sections}



    def llm_call(self,state: WorkerState):
        """Worker writes a section of the report"""
        prompt = f"""
    Using the following user story, generate the complete source code. Return the response as a structured JSON object with details about each file's path, filename, and the corresponding code.

    Requirements:
    1. Follow standard best practices for the chosen language or framework.
       - Organize code into appropriate directories (e.g., components, modules, views, helpers, styles).
       - Implement state management, routing, and styling as required.
       - Include comments in the code where helpful.
    2. Assume necessary dependencies and environment setup are already in place.
    3. Return the output strictly in the following JSON format:
    [
      {{
        "filePath": "[Relative Path]",
        "fileName": "[Filename]",
        "code": "[Code]"
      }}
    ]
    User Story: {state['section'].task}

    Provide the response strictly in the requested JSON format without additional explanations or commentary or single line of description.
    """
            
        
        

        section = self.llm.invoke(prompt)
        print("************CODE GENRATION******************")
        print(section.content)
        # Generate and save code to the file
        #path, filename,fullPath = generate_and_save_code(section.content)
        file_list = generate_and_save_code(section.content)
        #return {"generated_files": [str(fullPath)]}
        return {"generated_files": [*file_list]}


    def synthesizer(self,state: State):
        """Synthesize full report from sections"""
        completed_sections = state["completed_sections"]
        completed_report_sections = "\n\n---\n\n".join(completed_sections)
        return {"final_report": "CODE GENERATED"}


    # Conditional edge function to create llm_call workers that each write a section of the report
    def assign_workers(self,state: State):
        """Assign a worker to each section in the plan"""
        
        # Kick off section writing in parallel via Send() API
        return [Send("llm_call", {"section": s}) for s in state["sections"]]


