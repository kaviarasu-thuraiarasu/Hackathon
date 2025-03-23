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
        prompt = """
                    You are a code generator. Based on the user's request, generate the code required to implement the described functionality. Provide only the generated code, followed by the appropriate **relative file path** and **file extension type**, considering the standard project structure **inside the specified root directory**.

### Guidelines:

1. **Root Directory Specification:** Assume the root directory is explicitly specified as `E:/AgenticAI/Hackathon/Output`. All generated file paths should be relative to this root directory.

2. **Identify the Programming Language:** Determine the language from the user's request.

3. **Standard Project Structure:** Within the root directory, organize the code using common subdirectories for the identified language:
   - **`src/`**: Core source code.
     - **`services/`**: Business logic and service classes.
     - **`constants/`**: Constant values and configurations.
     - **`utilities/` or `utils/`**: Helper functions and utilities.
     - **`models/`**: Data structures or entities.
     - **`controllers/`**: Request and response logic (MVC pattern).
     - **`repositories/`**: Data access and database interactions.
     - **`middlewares/`**: Middleware components (commonly used in web applications).
     - **`adapters/`**: Integration with external systems or libraries.
   - **`tests/`**: Unit tests and test cases.
   - **`docs/`**: Project documentation.

4. **Language-Specific Examples:**
   - **Python:** 
     - `E:/AgenticAI/Hackathon/Output/src/services/`, `E:/AgenticAI/Hackathon/Output/src/constants/`
   - **Java (using Maven):**
     - `E:/AgenticAI/Hackathon/Output/src/main/java/com/yourcompany/yourproject/services/`
   - **JavaScript/TypeScript:**
     - `E:/AgenticAI/Hackathon/Output/src/services/`, `E:/AgenticAI/Hackathon/Output/src/constants/`
   - **Go:**
     - `E:/AgenticAI/Hackathon/Output/pkg/services/`, `E:/AgenticAI/Hackathon/Output/pkg/constants/`

5. **Response Format:**
   - **Generated Code:** Only the relevant code.
   - **File Path:** A relative path starting from the **root directory**.
   - **Filename:** Include the correct file extension based on the programming language.

### Request Example:

"Write Python code for a function that allows a user to search for books in a library by title or author using an in-memory list of books."

### Response Format:

<Generated Code>

Path: `E:/AgenticAI/Hackathon/Output/<relative file path inside standard subdirectory>`
Filename: `<filename.ext>`  # The appropriate file extension based on the language



                    For the following task
                """
        

        section = self.llm.invoke(f"{state['section'].task}")
        print("************CODE GENRATION******************")
        print(section.content)
        # Generate and save code to the file
        path, filename,fullPath = generate_and_save_code(section.content)
        return {"generated_files": [str(fullPath)]}


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


