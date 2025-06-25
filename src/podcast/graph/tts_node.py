import logging

from tqdm import tqdm

from src.podcast.graph.state import PodcastState
from tts import create_tts_client

logger = logging.getLogger(__name__)


def tts_node(state: PodcastState):
    logger.info("Generating audio chunks for podcast...")
    # Ensure audio_chunks is initialized
    if "audio_chunks" not in state:
        state["audio_chunks"] = []

    for line in tqdm(state["script"].lines[:2], desc="run audio chunks"):
        # Map speaker to gender
        gender = "male" if line.speaker.lower() == "male" else "female"

        # Generate audio using create_tts_client
        audio_data = create_tts_client(text=line.paragraph, gender=gender)

        if audio_data:
            # Encode audio data to base64 to match original output format
            state["audio_chunks"].append(audio_data)
        else:
            logger.error(f"Failed to generate audio for line: {line.paragraph}")

    return {
        "audio_chunks": state["audio_chunks"],
    }
