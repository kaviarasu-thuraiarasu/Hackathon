from langgraph.graph import StateGraph,START,END
from nuverlan.State.state import State
from nuverlan.Node.node import node
from langgraph.checkpoint.memory import MemorySaver
class graph:
    def __init__(self):
        self.graph = StateGraph(State)
        self.child_node= node()

    def create_graph(self):
        self.graph.add_node('generate_user_story',self.child_node.generate_user_stories)
        self.graph.add_node('product_owner_review',self.child_node.product_owner)
        self.graph.add_node('create_design_document',self.child_node.create_design_document)
        self.graph.add_node('revise_user_stories',self.child_node.revise_user_stories)
        self.graph.add_node('review_design',self.child_node.design_review)
        self.graph.add_node('human',self.child_node.human_assistance)
        self.graph.add_node('generate_source_code',self.child_node.generate_code)
        
        self.graph.add_edge(START,'generate_user_story')
        self.graph.add_edge('generate_user_story','product_owner_review')
        #self.graph.add_edge('human','product_owner_review')
        self.graph.add_conditional_edges('product_owner_review',self.child_node.product_owner_status,{'Approved':'create_design_document','FeedBack':'revise_user_stories'})
        self.graph.add_edge('revise_user_stories','generate_user_story')
        self.graph.add_edge('create_design_document','review_design')

        self.graph.add_conditional_edges('review_design',self.child_node.validate_design_review,{"FeedBack":"create_design_document","Approved":"generate_source_code"})


    
    def setup_graph(self):
        memory = MemorySaver()
        return self.graph.compile(checkpointer=memory)