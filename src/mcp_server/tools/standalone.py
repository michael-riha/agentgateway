# add a Standalone Tool without any MCP for testing and debugging
from langchain_core.tools import tool

from utils.logger import setup_logger

logger = setup_logger(__name__)


@tool()
def prefix(word: str) -> str:
    """Add a prefix_ to a word"""
    logger.info("Called Standalone prefix with %s", word)  # Changed from print
    return "prefix_" + word
