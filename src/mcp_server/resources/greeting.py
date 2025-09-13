from mcp.server.fastmcp import FastMCP


def setup_greeting_resources(mcp: FastMCP):
    """Setup greeting resources as shown in the article"""

    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting"""
        return f"Hello, {name}! Welcome to the MCP Server with LangGraph integration."
