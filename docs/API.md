# App API v0 (experimental)

`GET /health` reports gateway availability and configured backend. It does not check model readiness. `GET /` serves the demo. No CORS support is enabled. Serve browser clients from the same origin, or use a trusted backend proxy.

`POST /v1/chat` accepts JSON:

```json
{"messages":[{"role":"user","content":"Hello, Aster!"}]}
```

If `LOCALSTAGE_API_KEY` is configured, include `Authorization: Bearer <key>`. Native clients can connect through HTTP; use HTTPS when crossing a network trust boundary.

Successful response:

```json
{
  "text": "Hello!",
  "events": [
    {"type":"expression","name":"neutral"},
    {"type":"subtitle","text":"Hello!"},
    {"type":"speech.request","text":"Hello!"}
  ],
  "metrics":{"response_ms":123}
}
```

`response_ms` measures backend completion time, excluding network delivery, speech generation, and playback. Events arrive together after generation; token streaming is not implemented. Expression is always neutral in v0. A speech request contains text, not audio. Clients must ignore unknown event types for forward compatibility, render text safely, and own speech cancellation and avatar lifecycle.

Messages must contain 1–16 turns, roles `user` or `assistant`, 1–4000 characters per turn, at most 12000 characters total, and end with a user turn. The gateway prepends a configurable character system prompt. History is supplied by the client and never persisted by the gateway. Keep client history within limits.

Errors return `{"error":"..."}`: 400 invalid input, 401 missing/wrong key, 403 cross-site browser request, 404 unknown route, 413 missing/oversized body, 429 concurrency limit, 502 model failure. Retry 429 with backoff. Model errors are intentionally returned without upstream response bodies.
