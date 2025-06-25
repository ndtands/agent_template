import logging
import os

import grpc
from dotenv import load_dotenv

from tts import text_to_speech_api_pb2, text_to_speech_api_pb2_grpc

# Set up logging
logger = logging.getLogger(__name__)


def create_tts_client(text, gender, output_file=None):
    """
    Creates a TTS client and generates speech from text.

    Args:
        text (str): The text to convert to speech
        gender (str): The voice gender ("male" or "female")
        output_file (str, optional): If provided, saves audio to file

    Returns:
        bytes: The audio data
    """
    # Load environment variables
    load_dotenv()
    host = os.getenv("TTS_HOST", "localhost:50051")

    try:
        with grpc.insecure_channel(host) as channel:
            stub = text_to_speech_api_pb2_grpc.TextToSpeechStub(channel)

            # Create request
            request = text_to_speech_api_pb2.SpeechRequest(text=text, gender=gender)

            # Generate speech
            response = stub.GenerateSpeech(request)
            audio_data = response.audio

            # Save to file if output_file is specified
            if output_file:
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Audio saved to {output_file}")

            return audio_data
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        return None
