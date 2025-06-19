from src.config.agents import LLMType
from src.config.llms import base_model


def get_llm_by_type(
    llm_type: LLMType,
):
    """
    Get LLM instance by type. Returns cached instance if available.
    """
    if llm_type == "basic":
        return base_model
