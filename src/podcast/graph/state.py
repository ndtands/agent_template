from typing import Optional

from langgraph.graph import MessagesState

from src.podcast.types import Script


class PodcastState(MessagesState):
    """State for the podcast generation."""

    # Input
    input: str = ""

    # Output
    output: Optional[bytes] = None

    # Assets
    script: Optional[Script] = None
    audio_chunks: list[bytes] = []
