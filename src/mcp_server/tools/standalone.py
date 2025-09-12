# add a Standalone Tool witnhout any MCP for testing and debugging
from langchain_core.tools import tool


@tool()
def prefix(word: str) -> str:
    """Add a prefix_ to a word"""
    print(f"called Standalone prefix with {word}")
    return "prefix_" + word
