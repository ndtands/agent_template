from langgraph.prebuilt import create_react_agent

from src.llms import LLM
from src.prompts import apply_prompt_template


# Create agents using configured LLM types
def create_agent(agent_name: str, agent_type: str, tools: list, prompt_template: str):
    """Factory function to create agents with consistent configuration."""
    return create_react_agent(
        name=agent_name,
        model=LLM[agent_type],
        tools=tools,
        prompt=lambda state: apply_prompt_template(prompt_template, state),
    )
