
from nuverlan.llm.model import model
from docx import Document
from nuverlan.Utils.util import generate_comprehensive_spec
from langchain_core.tools import tool
from langgraph.types import Command, interrupt
from langchain_core.messages import HumanMessage

class node:
    def __init__(self):
        self.model = model()
        # https://github.com/gotohuman/examples-langgraph-py/tree/main/sales-lead-agent
  
    def human_assistance(self,query: str) -> str:
        """Request assistance from a human."""
        print("before")
        location = interrupt("Please provide your location:")
        tool_message ="Approved"
        return 'Approved'
    
    def generate_user_stories(self,state):
        print("***********Generate User Story***********")
        prompt = f"Generate a list of 3 user stories for an {state['user_requirement']}, with each user story formatted as: 'As a [type of user], I want [goal] so that [reason].' Please return the response as a list (array format)."
        data = self.model.stream_llm_response(prompt)
        print(data)
        # return {"user_story":[self.model.process().invoke(state["user_requirement"] + "Create the list of user stories with acceptence critera")]}
        return {"user_story":data}

    def product_owner(self,state):
        print("***********Product Owner***********")
        review = interrupt("Review the user story:")
        print(review)
        return {"product_owner": review}

    def product_owner_status(self,state):
       print("***********Product Owner Status***********")
       
       return state["product_owner"]
    
    def create_design_document(self,state):
        print("***********create Design Document***********")
        # comprehensive_spec = generate_comprehensive_spec(state['user_story'])
        
        # doc = Document()
        # doc.add_heading('Design Documentation', 0)

        # # Add the generated content to the Word document
        # doc.add_paragraph(comprehensive_spec)

        # # Save the DOCX document
        # doc.save('comprehensive_specification.docx')
        return {"design_document":"Created"}
       


    def revise_user_stories(self,state):
        print("***********Revise User Story***********")



    def design_review(self,state):
        print("***********Review Design***********")

    def validate_design_review(self,state):
        print("***********VALIDATE DESIGN REVIEW***********")
        status = input("Validate the document?")
        return status

    def generate_code(self,state):
        print("***********Generate Code***********")
        return state    
    
    def assistant(self,state):
        return {"messages": [self.model.process().invoke(state["messages"])]}