import asyncio

from langchain_core.messages import HumanMessage, SystemMessage

from graphs.graph import get_components, graph
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def agent_setup_and_execution(
    input_text: str = "can you prefix the word 'michael'",
) -> str:
    """Process text using LangGraph workflow"""
    llm, tools = await get_components()
    llm_with_tools = llm.bind_tools(tools)

    # Create the tool node
    from langgraph.prebuilt import ToolNode

    tool_node = ToolNode(tools)
    # Define your system message
    system_message = """You are a helpful assistant that uses tools for all operations.
    For math problems like addition, multiplication, etc., you MUST use the appropriate tools.
    Even if you know the answer, always call the relevant tool instead of answering directly."""

    # Create messages with system prompt and user input
    messages = [SystemMessage(content=system_message), HumanMessage(content=input_text)]
    initial_state = {
        "messages": [],
        "initial_prompt": messages,
    }
    # Run the graph
    result = await graph.ainvoke(
        initial_state, context={"llm": llm_with_tools, "toolNode": tool_node}
    )
    # Extract the final response from the result
    # The exact way to extract depends on your graph structure
    # Typically, the result will contain the final messages
    final_message = result.get("messages", [])[-1] if result.get("messages") else None

    if final_message:
        logger.info(
            "Response type: %s", getattr(final_message, "type", "Unknown")
        )  # Changed from print
        logger.info(
            "Tool calls: %s", getattr(final_message, "tool_calls", None)
        )  # Changed from print
        logger.info(
            "Response content: %s", getattr(final_message, "content", "No content")
        )  # Changed from print
        return final_message.content
    else:
        logger.warning("No final message in result: %s", result)  # Changed from print
        return result


if __name__ == "__main__":
    # For testing the agentgateway_llm function directly
    from langchain.globals import set_verbose

    set_verbose(True)
    asyncio.run(agent_setup_and_execution())
