from langchain_core.messages import HumanMessage
from mcp.server.fastmcp import FastMCP

from utils.logger import setup_logger

logger = setup_logger(__name__)
# Initialize MCP server
mcp = FastMCP("Math Server", host="0.0.0.0", port=8000)

from prompts.system_prompts import setup_system_prompts
from resources.greeting import setup_greeting_resources

# Import tools, resources, and prompts
from tools.calculator import setup_calculator_tools

# Setup all Tools available (Tools, Resources, Prompts)
setup_calculator_tools(mcp)
setup_greeting_resources(mcp)
setup_system_prompts(mcp)


# Example Graphs to be called via MCP as Tool
@mcp.tool()
async def simple_langgraph(input_text: str) -> str:
    """Process text using LangGraph workflow"""
    from graphs.simple import graph

    result = graph.invoke({"messages": [HumanMessage(content=input_text)]})
    return result["messages"][-1].content


@mcp.tool()
async def execute_graph(input_text: str = "add 3+5") -> str:
    """Run example Graph over MCP"""
    from agent import agent_setup_and_execution

    result = await agent_setup_and_execution(input_text)
    return result


# Run the MCP-Server
if __name__ == "__main__":
    # For testing the agentgateway_llm function directly
    from langchain.globals import set_verbose

    logger.info("Starting MCP Server with streamable-http transport")  # Added logging
    set_verbose(True)
    mcp.run(transport="streamable-http")
