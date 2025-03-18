from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class model:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4",streaming=True,api_key="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")

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
        for chunk in response:
            if chunk.content:
                streamed_text += chunk.content
                print(chunk.content, end="", flush=True)  # ✅ Stream output in real-time
        print("\n")  # New line for readability
        return streamed_text  # Return full response
