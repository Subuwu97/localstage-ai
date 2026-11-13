# Architecture and deployment

```text
Text input / future microphone or livestream connector
                       |
                Character gateway
        prompt + bounded caller-owned history
                       |
          OpenAI-compatible model server
            local machine / datacenter
                       |
              Text and app events
                       |
       VTuber app: subtitles + TTS + avatar
```

The gateway owns character instructions and the app contract. A model server owns inference, tokenization, quantization, hardware acceleration, and scheduling. The VTuber app owns rendering, voice playback, lip sync, and user interaction. This allows a lightweight client to use a model hosted on another machine without embedding a model engine in every client.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| LOCALSTAGE_BACKEND | mock | `mock` fixed reply or `model` inference |
| MODEL_BASE_URL | http://127.0.0.1:8080/v1 | Trusted model endpoint, including `/v1` |
| MODEL_NAME | local-model | Backend model identifier |
| MODEL_API_KEY | unset | Optional credential for the model server |
| LOCALSTAGE_API_KEY | unset | Gateway bearer key; required for non-loopback binding |
| CHARACTER_PROMPT | built-in Aster prompt | Operator-controlled character instruction |

The process reads environment variables. Do not accept model URLs, keys, or character prompts from untrusted callers. The gateway does not execute model-generated commands or fetch model-generated URLs.

## Datacenter path

This standard-library HTTP server is a development reference, not an Internet-facing production service. For a datacenter prototype, put it on a private network behind a reverse proxy with TLS, request timeouts, connection limits, body limits, authentication, and rate limits. Set a strong `LOCALSTAGE_API_KEY` and bind deliberately with `--host 0.0.0.0`. Keep model servers private. Gateway concurrency is two requests per process; extra requests get 429. It does not provide a distributed scheduler, autoscaling, tenant isolation, or a bounded HTTP connection pool.

For production, migrate the same API contract to a maintained production server, add per-user authorization and cancellation, load tests, a bounded request queue, model readiness checks, monitoring, and a deployment-specific threat review. Do not expose the reference server directly to the public Internet. Bearer keys alone are not a complete deployment security system.

## Performance measurement

Record model/version/license, quantization, context, prompt size, output tokens, backend version, OS, CPU, GPU, RAM/VRAM, concurrency, and warm/cold state. Measure time to first token once streaming exists, full reply latency (p50/p95), tokens/sec, memory peak, and energy if instrumentation is available. Compare quality as well as speed. No real-model speed or hardware claims have been benchmarked in this starter.

Use small models and shorter context for constrained devices. On larger machines, benchmark GPU offload and backend batching. Model capability, memory use, and latency involve tradeoffs; selecting a hardware backend does not remove them.

## Privacy and character behavior

No telemetry or conversation persistence is implemented. The reference server suppresses access logs. Model servers, reverse proxies, browsers, and voice engines may have their own logging or network behavior. Browser speech may use remote services; choose a verified offline speech engine for strict offline use. Prompt instructions are behavior guidance, not a security boundary or moderation system. Add application-specific input/output moderation and operator interruption before unattended public performance.

## Upstream references

- [llama.cpp hardware support and builds](https://github.com/ggml-org/llama.cpp)
- [llama.cpp server API](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
- [VTube Studio Public API and authentication](https://github.com/DenchiSoft/VTubeStudio)
