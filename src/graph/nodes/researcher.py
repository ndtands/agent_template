import logging
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.config.configuration import Configuration
from src.graph.nodes.utils import _setup_and_execute_agent_step
from src.graph.types import State
from src.tools import crawl_tool, get_web_search_tool

logger = logging.getLogger(__name__)


# TO DO Add RAG into researcher team
async def researcher_node(
    state: State, config: RunnableConfig
) -> Command[Literal["research_team"]]:
    """Researcher node that do research"""
    logger.info("Researcher node is researching.")
    configurable = Configuration.from_runnable_config(config)
    tools = [get_web_search_tool(configurable.max_search_results), crawl_tool]
    logger.info(f"Researcher tools: {tools}")
    return await _setup_and_execute_agent_step(
        state,
        config,
        "researcher",
        tools,
    )
