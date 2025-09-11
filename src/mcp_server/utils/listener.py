# https://python.langchain.com/docs/how_to/custom_callbacks/
from typing import Dict, List, Any  # Add the missing imports for type hints
from langchain_core.callbacks import BaseCallbackHandler
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        print(f"My custom handler, LLM started with prompts: {prompts}")
    
    def on_llm_end(self, response: Dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, LLM ended with response: {response}")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        print(f"My custom handler,  chain started with inputs: {inputs}")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        print(f"My custom handler, tool started with input: {input_str}")
    
    def on_agent_action(self, action: Dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, agent action: {action}")
    
    def on_agent_finish(self, finish: Dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, agent finished: {finish}")
