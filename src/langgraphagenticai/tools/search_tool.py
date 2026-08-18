from langgraph.prebuilt.tool_node import ToolNode
from langchain_community.tools import TavilySearchResults

def get_tools():
    """
    Return the list of tools
    """
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
        Create and return tool node for the graph 
    """
    return ToolNode(tools)



