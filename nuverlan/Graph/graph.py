from langgraph.graph import StateGraph,START,END
from nuverlan.State.state import State
from nuverlan.Node.node import node
from langgraph.checkpoint.memory import MemorySaver
from nuverlan.Node.Orchestrator import Orchestrator
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
        self.graph.add_node('orchestrator',run_orchestrator)
        self.graph.add_node('CodeReview',self.child_node.code_review)
        self.graph.add_node('FixCode',self.child_node.fix_code)
        
        self.graph.add_edge(START,'generate_user_story')
        self.graph.add_edge('generate_user_story','product_owner_review')
        #self.graph.add_edge('human','product_owner_review')
        self.graph.add_conditional_edges('product_owner_review',self.child_node.product_owner_status,{'Approved':'create_design_document','FeedBack':'revise_user_stories'})
        self.graph.add_edge('revise_user_stories','generate_user_story')
        self.graph.add_edge('create_design_document','review_design')

        self.graph.add_conditional_edges('review_design',self.child_node.validate_design_review,{"FeedBack":"create_design_document","Approved":"generate_source_code"})
        self.graph.add_edge('generate_source_code','orchestrator')
        self.graph.add_edge('orchestrator','CodeReview')
        self.graph.add_conditional_edges('CodeReview',self.child_node.code_review_status,{"Approved":"FixCode","FeedBack":"FixCode"})

    
    def setup_graph(self):
        memory = MemorySaver()
        return self.graph.compile(checkpointer=memory)
    

class OrchestratorGraph:
    def __init__(self):
        self.graph = StateGraph(State)
        self.child_node = Orchestrator()

    def create_graph(self):
        
        self.graph.add_node("orchestrator", self.child_node.orchestrator)
        self.graph.add_node("llm_call", self.child_node.llm_call)
        self.graph.add_node("synthesizer", self.child_node.synthesizer)

        # Add edges to connect nodes
        self.graph.add_edge(START, "orchestrator")
        self.graph.add_conditional_edges(
            "orchestrator", self.child_node.assign_workers, ["llm_call"]
        )
        self.graph.add_edge("llm_call", "synthesizer")
        self.graph.add_edge("synthesizer", END)

        # Compile the workflow
        #orchestrator_worker = self.graph.compile()

        # Show the workflow
        #display(Image(orchestrator_worker.get_graph().draw_mermaid_png()))

        # Invoke
        # prompt = [
        #     "As a library member, I want to be able to search for books by various criteria such as title, author, or genre. This feature will help me quickly find the books I am interested in, making it easier for me to borrow them. Whether I want a specific title or I'm just browsing for something new to read, having an effective search functionality will enhance my library experience..",
        #     "As a library member, I want to be able to view the books I currently have checked out and see their due dates. This feature will allow me to keep track of when my borrowed items are due back, helping me avoid late fees. It will also give me a better understanding of what I have in hand and when to return them, making the borrowing process more organized.",
        #     "As a library administrator, I want the ability to add new books, update existing book information, or remove books from the inventory. This feature is crucial for maintaining an up-to-date and accurate catalog of the library’s collection. It ensures that members can access accurate information when searching for books and allows the library to manage its resources efficiently."
        # ]
        # state = orchestrator_worker.invoke({"topic": prompt})
    
    def setup_graph(self):
        memory = MemorySaver()
        return self.graph.compile(checkpointer=memory)
    

def run_orchestrator(state):
    """Calls the Orchestrator Workflow."""
    # if not state.requirements:
    #     raise ValueError("Requirements not provided!")
    g = OrchestratorGraph()
    g.create_graph()
    final_graph = g.setup_graph()
 
    orchestrator_state = final_graph.invoke(
        {"task": state["user_story"]}
    )
    #print(orchestrator_state)
    # Store the generated project path in the main workflow
    #state.generated_project_path = orchestrator_state["generated_project_path"]
    return orchestrator_state
    