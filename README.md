# LocalStage AI

A lightweight foundation for a self-hosted AI character: run the character gateway on a personal computer or next to a model server in a datacenter, and connect a VTuber application through a small JSON API.

**Status: early development starter.** This is an inference application scaffold, not a newly trained foundation model or a finished autonomous VTuber. No model weights, avatar assets, or voices are bundled. Inspired by the general idea of AI performers such as Neuro-sama and Riko Project; no affiliation, copied identity, code, or assets.

## Working today

- Python standard-library gateway with no third-party Python dependencies.
- Fixed-response mock mode for testing without a GPU or model download.
- Adapter for a model server's OpenAI-compatible `/v1/chat/completions` endpoint.
- Browser text demo with optional browser speech synthesis.
- App events for subtitles, a neutral expression, and speech requests.
- Bounded conversation input, two concurrent model requests, timeouts, optional bearer authentication, and loopback binding by default.
- Automated tests and a Windows/Linux/macOS CI configuration.

## Try it

Use Python 3.11 or newer. From the repository directory:

```sh
python -m localstage.server
```

Open http://127.0.0.1:8765 in your browser. Mock mode is explicitly a fixed reply, not AI inference. Stop with Ctrl+C.

### Connect a local model

Install a suitable build of [llama.cpp](https://github.com/ggml-org/llama.cpp), obtain a compatible GGUF chat model whose license permits your use, and start its server. Illustrative command; adjust model path and hardware options using the upstream documentation:

```sh
llama-server -m models/your-chat-model.gguf --host 127.0.0.1 --port 8080 -c 4096
```

Then in another terminal, select the model backend.

PowerShell:

```powershell
$env:LOCALSTAGE_BACKEND = 'model'
$env:MODEL_BASE_URL = 'http://127.0.0.1:8080/v1'
$env:MODEL_NAME = 'local-model'
python -m localstage.server
```

Linux/macOS:

```sh
LOCALSTAGE_BACKEND=model MODEL_BASE_URL=http://127.0.0.1:8080/v1 MODEL_NAME=local-model python -m localstage.server
```

Set `MODEL_NAME` to the identifier accepted by your backend. The gateway uses the API format; it does not require an OpenAI account or cloud connection. It can target other compatible servers, but those have not been verified here. `.env.example` is a reference, not an automatically loaded configuration file.

## Efficiency and hardware

The design separates a small character gateway from the inference engine. llama.cpp offers different hardware backends; actual support depends on your build, drivers, and model. There is no promise of fast inference on every device. The mock gateway can run without a GPU; a real model needs adequate memory and compute.

Start with a small quantized model that fits comfortably in available memory, keep context short, and measure before increasing model size. The starter caps each generated reply at 128 tokens and accepts at most 16 conversation turns totaling 12000 characters. Character limits are not token limits: your backend context must fit the prompt plus output.

See [architecture and deployment](docs/ARCHITECTURE.md), [app API](docs/API.md), and [development roadmap](docs/ROADMAP.md).

## VTuber integration

A client sends text to `/v1/chat`, shows subtitle events, passes speech requests to its own speech engine, and maps expression names to its own avatar controls. The included demo only displays text and optionally speaks it. It does not create or animate a Live2D/VRM model.

A future VTube Studio bridge should use its documented [Public API](https://github.com/DenchiSoft/VTubeStudio), including plugin authentication and user approval. This starter's JSON events are **not** VTube Studio protocol messages. Microphone input, local STT/TTS, lip sync, expression inference, streaming chat, and livestream connectors are planned.

## Tests

```sh
python -m unittest discover -s tests -v
```

## Contributing

Small changes with clear reproduction steps and meaningful tests are welcome. Start with the roadmap. Keep inference, voice, avatar rendering, and platform connectors modular. Never commit credentials, personal conversations, model weights, or unlicensed character assets. Submit security concerns privately to the repository owner rather than posting secrets in issues.

## License

MIT for this repository's original code. Models, voices, inference engines, and avatar assets retain their own licenses.
