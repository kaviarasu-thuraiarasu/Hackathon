from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from nuverlan.websocket.websocket import WebSocketHandler

class model:
    def __init__(self):
        # self.llm = ChatOpenAI(model="gpt-4",streaming=True,api_key="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")
        self.llm = ChatGroq(model="llama3-70b-8192",streaming=True,api_key="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")
        self.websocket_handler = WebSocketHandler()

    def process(self):
        try:
            
            return self.llm
        except Exception as e:
            print(e)

    def stream_llm_response(self,prompt):
        """Streams the response from an LLM."""
        messages = [HumanMessage(content=prompt)]
        response = self.llm.stream(messages)
        
        streamed_text = ""
        # print("@@@@@@@@@@@@@@@@")
        # print(response)
        for chunk in response:
            
            if chunk.content:
                streamed_text += chunk.content
                #self.websocket_handler.send_message("1", f"Message received: {chunk.content}")
                #print(chunk.content, end="", flush=True)  # ✅ Stream output in real-time
        #print("\n")  # New line for readability
        return streamed_text  # Return full response
    
