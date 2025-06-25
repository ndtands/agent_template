import grpc
import text_to_speech_api_pb2
import text_to_speech_api_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = text_to_speech_api_pb2_grpc.TextToSpeechStub(channel)

        # Example request
        request = text_to_speech_api_pb2.SpeechRequest(
            text="Hey, how are you doing today?", gender="male"
        )

        response = stub.GenerateSpeech(request)

        # Save the audio to a file
        with open("output.wav", "wb") as f:
            f.write(response.audio)
        print("Audio saved to output.wav")


if __name__ == "__main__":
    run()
