import logging
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.graph.nodes.utils import _setup_and_execute_agent_step
from src.graph.types import State
from src.tools import python_repl_tool

logger = logging.getLogger(__name__)


async def coder_node(
    state: State, config: RunnableConfig
) -> Command[Literal["research_team"]]:
    """Coder node that do code analysis."""
    logger.info("Coder node is coding.")

    return await _setup_and_execute_agent_step(
        state, config, "coder", [python_repl_tool]
    )
