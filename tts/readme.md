# Hướng dẫn về gRPC: Cách hoạt động và triển khai cơ bản

## 1. Sự khác biệt giữa HTTP và gRPC

### HTTP

- **Giao thức**: HTTP (Hypertext Transfer Protocol) là giao thức truyền tải dữ liệu dựa trên văn bản, thường được sử dụng trong các API RESTful.
- **Cách hoạt động**:
  - Sử dụng các phương thức như GET, POST, PUT, DELETE để gửi yêu cầu và nhận phản hồi.
  - Dữ liệu thường được gửi dưới dạng JSON hoặc XML, dễ đọc nhưng có thể cồng kềnh.
  - Mỗi yêu cầu là một giao dịch độc lập, không duy trì trạng thái giữa các yêu cầu (stateless).
- **Ưu điểm**:
  - Dễ hiểu, dễ triển khai, đặc biệt với các ứng dụng web.
  - Hỗ trợ rộng rãi, tương thích với hầu hết các công cụ và trình duyệt.
  - Dễ debug vì dữ liệu ở dạng văn bản.
- **Nhược điểm**:
  - Hiệu suất có thể thấp hơn khi truyền dữ liệu lớn do kích thước payload lớn (JSON/XML).
  - Không hỗ trợ tốt cho các luồng dữ liệu hai chiều liên tục (bidirectional streaming).
  - Độ trễ có thể cao hơn trong các hệ thống yêu cầu hiệu suất cao.

### gRPC

- **Giao thức**: gRPC (gRPC Remote Procedure Call) là một framework RPC hiệu suất cao, dựa trên HTTP/2 và sử dụng Protocol Buffers (protobuf) để định dạng dữ liệu.
- **Cách hoạt động**:
  - Sử dụng các định nghĩa giao thức (`.proto`) để xác định dịch vụ và cấu trúc dữ liệu.
  - Dữ liệu được mã hóa dưới dạng nhị phân, nhỏ gọn hơn JSON/XML.
  - Hỗ trợ các kiểu giao tiếp: unary (một yêu cầu, một phản hồi), server streaming, client streaming, và bidirectional streaming.
- **Ưu điểm**:
  - Hiệu suất cao nhờ mã hóa nhị phân và HTTP/2 (hỗ trợ multiplexing, nén header).
  - Hỗ trợ streaming, phù hợp với các ứng dụng thời gian thực.
  - Tự động sinh mã code cho nhiều ngôn ngữ lập trình từ file `.proto`.
  - Kiểm tra kiểu nghiêm ngặt (type safety) nhờ protobuf.
- **Nhược điểm**:
  - Phức tạp hơn HTTP/REST khi thiết lập ban đầu.
  - Ít thân thiện với con người hơn do dữ liệu nhị phân khó đọc.
  - Yêu cầu công cụ bổ sung để debug (so với JSON trong HTTP).

### So sánh trong trường hợp của bạn (API Text-to-Speech)

Trong trường hợp của API Text-to-Speech sử dụng Parler-TTS:

- **gRPC phù hợp hơn** nếu:
  - Bạn cần hiệu suất cao, đặc biệt khi truyền dữ liệu âm thanh lớn (audio WAV).
  - Ứng dụng yêu cầu xử lý nhanh, chẳng hạn như tạo âm thanh trong thời gian thực.
  - Bạn muốn hỗ trợ streaming trong tương lai, ví dụ: gửi nhiều đoạn văn bản liên tiếp hoặc nhận audio theo luồng.
  - Hệ thống của bạn là nội bộ (microservices) và không cần tương thích với trình duyệt web.
- **HTTP/REST phù hợp hơn** nếu:
  - Bạn cần API dễ tích hợp với các ứng dụng web hoặc bên thứ ba.
  - Bạn ưu tiên tính đơn giản và khả năng debug dễ dàng.
  - Ứng dụng không yêu cầu hiệu suất cao hoặc streaming.

**Ý nghĩa của việc chọn gRPC trong trường hợp này**:

- gRPC giúp giảm độ trễ và kích thước dữ liệu khi truyền file âm thanh (do mã hóa nhị phân).
- Hỗ trợ tốt hơn nếu bạn muốn mở rộng API để xử lý streaming (ví dụ: gửi văn bản từng phần và nhận audio theo thời gian thực).
- Phù hợp với các hệ thống microservices, nơi hiệu suất và tính mở rộng là ưu tiên.

**Khuyến nghị**: Sử dụng gRPC trong trường hợp này vì API của bạn xử lý dữ liệu lớn (audio) và có thể cần mở rộng để hỗ trợ streaming trong tương lai. Tuy nhiên, nếu bạn cần tích hợp với các ứng dụng web hoặc ưu tiên sự đơn giản, hãy cân nhắc HTTP/REST.

## 2. gRPC hoạt động như thế nào?

gRPC là một framework gọi thủ tục từ xa (Remote Procedure Call) được phát triển bởi Google, dựa trên HTTP/2 và Protocol Buffers. Nó cho phép client và server giao tiếp hiệu quả, như thể gọi các hàm cục bộ.

### Cách hoạt động cơ bản

1. **Định nghĩa dịch vụ**:

   - Bạn tạo một file `.proto` để định nghĩa dịch vụ (các hàm có thể gọi) và cấu trúc dữ liệu (message).
   - Ví dụ: Định nghĩa một dịch vụ `TextToSpeech` với hàm `GenerateSpeech` nhận văn bản và trả về audio.
2. **Tạo mã code**:

   - Sử dụng công cụ `protoc` để sinh mã code (client và server) cho các ngôn ngữ như Python, Java, C++, v.v.
   - Mã code này bao gồm các lớp và hàm để gọi/gửi yêu cầu.
3. **Server triển khai logic**:

   - Server triển khai các hàm được định nghĩa trong file `.proto`.
   - Ví dụ: Server nhận văn bản, tạo audio bằng Parler-TTS, và trả về dữ liệu âm thanh.
4. **Client gửi yêu cầu**:

   - Client sử dụng mã code sinh ra để gọi hàm trên server, như thể gọi một hàm cục bộ.
   - Dữ liệu được mã hóa thành nhị phân và truyền qua HTTP/2.
5. **Giao tiếp qua HTTP/2**:

   - HTTP/2 hỗ trợ multiplexing (nhiều yêu cầu trên một kết nối), nén header, và streaming.
   - Dữ liệu được mã hóa bằng Protocol Buffers, nhỏ gọn và nhanh hơn JSON/XML.

### Ví dụ minh họa

Giả sử bạn muốn tạo một API chuyển văn bản thành giọng nói:

- Client gửi yêu cầu: `{ text: "Xin chào", gender: "female" }`.
- Server sử dụng Parler-TTS để tạo audio và trả về file WAV.
- gRPC đảm bảo truyền dữ liệu nhanh và hiệu quả.

## 3. Các bước triển khai gRPC cơ bản

Dưới đây là hướng dẫn từng bước để triển khai API Text-to-Speech sử dụng gRPC, dựa trên ví dụ trước.

### Bước 1: Cài đặt môi trường

Cài đặt các thư viện cần thiết:

```bash
pip install git+https://github.com/huggingface/parler-tts.git
pip install soundfile numpy grpcio-tools flash-attn
```

### Bước 2: Tạo file định nghĩa giao thức (`.proto`)

Tạo file `text_to_speech_api.proto`:

```proto
syntax = "proto3";

package tts;

service TextToSpeech {
  rpc GenerateSpeech(SpeechRequest) returns (SpeechResponse);
}

message SpeechRequest {
  string text = 1;
  string gender = 2; // "male" or "female"
}

message SpeechResponse {
  bytes audio = 1; // WAV audio data
}
```

### Bước 3: Sinh mã code từ file `.proto`

Chạy lệnh sau để sinh mã Python:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. text_to_speech_api.proto
```

Kết quả:

- `text_to_speech_api_pb2.py`: Chứa định nghĩa message (SpeechRequest, SpeechResponse).
- `text_to_speech_api_pb2_grpc.py`: Chứa định nghĩa dịch vụ và stub.

### Bước 4: Triển khai server

Tạo file `tts_server.py`:

```python
import grpc
import torch
import soundfile as sf
import numpy as np
from concurrent import futures
import text_to_speech_api_pb2
import text_to_speech_api_pb2_grpc
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

class TextToSpeechService(text_to_speech_api_pb2_grpc.TextToSpeechServicer):
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

        self.prompts = {
            "male": "A male speaker delivers a clear and expressive speech with a moderate speed and deep pitch. The recording is of very high quality, with the speaker's voice sounding crisp and close-up.",
            "female": "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
        }

    def GenerateSpeech(self, request, context):
        text = request.text
        gender = request.gender.lower()

        if gender not in self.prompts:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Gender must be 'male' or 'female'")
            return text_to_speech_api_pb2.SpeechResponse()

        description = self.prompts[gender]

        input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
        prompt_input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)

        with torch.no_grad():
            generation = self.model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)

        audio_arr = generation.cpu().numpy().squeeze()

        import io
        buffer = io.BytesIO()
        sf.write(buffer, audio_arr, self.model.config.sampling_rate, format="WAV")
        audio_data = buffer.getvalue()

        return text_to_speech_api_pb2.SpeechResponse(audio=audio_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_to_speech_api_pb2_grpc.add_TextToSpeechServicer_to_server(TextToSpeechService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### Bước 5: Triển khai client

Tạo file `tts_client.py`:

```python
import grpc
import text_toizard
import text_to_speech_api_pb2
import text_to_speech_api_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = text_to_speech_api_pb2_grpc.TextToSpeechStub(channel)

        request = text_to_speech_api_pb2.SpeechRequest(
            text="Xin chào, đây là bài kiểm tra giọng nói.",
            gender="female"
        )

        response = stub.GenerateSpeech(request)

        with open("output.wav", "wb") as f:
            f.write(response.audio)
        print("Audio saved to output.wav")

if __name__ == '__main__':
    run()
```

### Bước 6: Chạy server và client

1. Mở terminal, chạy server:

   ```bash
   python tts_server.py
   ```
2. Mở terminal khác, chạy client:

   ```bash
   python tts_client.py
   ```

### Kết quả

- Server sẽ nhận văn bản và giới tính ("male" hoặc "female"), tạo audio bằng Parler-TTS, và trả về file WAV.
- Client lưu audio vào file `output.wav`.

## 4. Lợi ích của gRPC trong ví dụ này

- **Hiệu suất**: File âm thanh được truyền dưới dạng nhị phân, giảm kích thước và tăng tốc độ.
- **Tính mở rộng**: Dễ dàng thêm các tính năng như streaming trong tương lai.
- **Tính bảo mật**: gRPC hỗ trợ SSL/TLS, phù hợp với các hệ thống nội bộ.

## 5. Debug và mở rộng

- **Debug**: Sử dụng công cụ như `BloomRPC` để kiểm tra các yêu cầu gRPC.
- **Mở rộng**:
  - Thêm các tùy chọn khác (giọng nói, tốc độ, cao độ).
  - Hỗ trợ streaming để gửi văn bản từng phần và nhận audio theo luồng.

---
Text-to-Speech!
