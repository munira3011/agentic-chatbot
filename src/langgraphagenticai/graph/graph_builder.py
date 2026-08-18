from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import create_tool_node,get_tools
from src.langgraphagenticai.nodes.chat_with_tool_node import ChatWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
from langgraph.prebuilt import tools_condition

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_builder(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """

        tools = get_tools()
        tool_node = create_tool_node(tools)

        obj_chat_with_tools = ChatWithToolNode(self.llm)
        chat_wit_tool_node = obj_chat_with_tools.create_chatbot(tools)


        self.graph_builder.add_node("chatbot",chat_wit_tool_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_build_graph(self):
       
       # Initialize the AINewsNode
        ai_news_node = AINewsNode(self.llm)
        
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result", END)
 

    def setup_graph(self, usecase: str):
        """
            set up the graph based on the selected usecase
        """
        if usecase == "Basic Chatbot":
           self.basic_chatbot_builder()
        if usecase == "Chatbot with Web":
           self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
           self.ai_news_build_graph()

        return self.graph_builder.compile()


