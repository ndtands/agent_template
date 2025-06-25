from concurrent import futures

import grpc
import soundfile as sf
import text_to_speech_api_pb2
import text_to_speech_api_pb2_grpc
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


class TextToSpeechService(text_to_speech_api_pb2_grpc.TextToSpeechServicer):
    def __init__(self):
        self.device = "cpu"
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            "parler-tts/parler-tts-mini-v1"
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

        # Define gender-specific prompts
        self.prompts = {
            "male": "A male speaker delivers a clear and expressive speech with a moderate speed and deep pitch. The recording is of very high quality, with the speaker's voice sounding crisp and close-up.",
            "female": "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up.",
        }

    def GenerateSpeech(self, request, context):
        text = request.text
        gender = request.gender.lower()

        if gender not in self.prompts:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Gender must be 'male' or 'female'")
            return text_to_speech_api_pb2.SpeechResponse()

        description = self.prompts[gender]

        # Tokenize inputs
        input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(
            self.device
        )
        prompt_input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(
            self.device
        )

        # Generate audio
        with torch.no_grad():
            generation = self.model.generate(
                input_ids=input_ids, prompt_input_ids=prompt_input_ids
            )

        audio_arr = generation.cpu().numpy().squeeze()

        # Save audio to bytes
        import io

        buffer = io.BytesIO()
        sf.write(buffer, audio_arr, self.model.config.sampling_rate, format="WAV")
        audio_data = buffer.getvalue()

        return text_to_speech_api_pb2.SpeechResponse(audio=audio_data)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_to_speech_api_pb2_grpc.add_TextToSpeechServicer_to_server(
        TextToSpeechService(), server
    )
    server.add_insecure_port("[::]:50051")
    print("Server starting on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
