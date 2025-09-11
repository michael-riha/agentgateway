
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: List

def fake_llm_node(state: AgentState):
    """Simple LangGraph node for demonstration"""
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        return {"messages": [AIMessage(content=f"I received your message: {last_message.content}")]}
    return {"messages": [AIMessage(content="I'm not sure how to process that")]}

# Build LangGraph workflow
builder = StateGraph(AgentState)
builder.add_node("process", fake_llm_node)
builder.add_edge(START, "process")
builder.add_edge("process", END)
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="./data/graphs/simple.png")