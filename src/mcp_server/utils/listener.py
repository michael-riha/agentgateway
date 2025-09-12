# https://python.langchain.com/docs/how_to/custom_callbacks/
from typing import Any  # Add the missing imports for type hints

from langchain_core.callbacks import BaseCallbackHandler


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs
    ) -> None:
        print(f"My custom handler, LLM started with prompts: {prompts}")

    def on_llm_end(self, response: dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, LLM ended with response: {response}")

    def on_chain_start(
        self, serialized: dict[str, Any], inputs: dict[str, Any], **kwargs
    ) -> None:
        print(f"My custom handler,  chain started with inputs: {inputs}")

    def on_tool_start(
        self, serialized: dict[str, Any], input_str: str, **kwargs
    ) -> None:
        print(f"My custom handler, tool started with input: {input_str}")

    def on_agent_action(self, action: dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, agent action: {action}")

    def on_agent_finish(self, finish: dict[str, Any], **kwargs) -> None:
        print(f"My custom handler, agent finished: {finish}")
