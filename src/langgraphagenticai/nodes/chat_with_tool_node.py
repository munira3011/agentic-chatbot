from src.langgraphagenticai.state.state import State

class ChatWithToolNode:
    
    """
        Chatbot logic with tool integration
    """
    def __init__(self, model):
        self.llm = model
   
    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response with tool integration.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user", "content":user_input}])

        tools_response = f"Tools integration for:'{user_input}'"

        return {"messages": [llm_response, tools_response]}

    def create_chatbot(self, tools):
        """
        Return a chatbot node function
        """
        llm_with_tool = self.llm.bind_tools(tools)

        def chatbotNode(state: State):
            """
                chatbot logic for processing input and returning state
            """
            return {"messages": llm_with_tool.invoke(state["messages"])}
        return chatbotNode