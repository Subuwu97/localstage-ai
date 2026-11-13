# Development roadmap

## Phase 1: working conversation

- [x] No-model demo and model-server adapter.
- [x] Browser demo and documented character event contract.
- [ ] Verify a licensed small chat model on CPU and a GPU machine.
- [ ] Incremental token streaming, cancellation, and turn interruption.
- [ ] Reproducible latency/memory benchmark harness and published results.
- [ ] Configurable token budgets with tokenizer-aware history trimming.

## Phase 2: VTuber application

- [ ] Offline microphone transcription and voice activity detection.
- [ ] Pluggable offline TTS with sentence-by-sentence synthesis.
- [ ] Audio-driven mouth movement and timestamped visemes.
- [ ] Authenticated VTube Studio bridge and/or VRM renderer.
- [ ] User-created character profiles, expression mapping, and asset import.
- [ ] Desktop control panel with mute, stop, and performance indicators.

## Phase 3: persistent character

- [ ] Opt-in local memory with inspection, deletion, and retrieval limits.
- [ ] Livestream chat connectors with platform authentication and rate limits.
- [ ] Moderation, operator approval controls, and adversarial testing.
- [ ] Permission-scoped tools; no arbitrary command execution by default.

## Phase 4: scale and optimization

- [ ] Production HTTP/WebSocket service and deployment manifests.
- [ ] Tenant isolation, model routing, bounded queues, and GPU scheduling.
- [ ] Hardware profiles based on measured capacity, not universal speed claims.
- [ ] Optional fine-tuning pipeline using properly licensed and consented data.

Training a competitive foundation model from scratch is a separate research and compute program. Begin by building a reliable, measurable character system around an existing licensed model, then evaluate whether fine-tuning improves the specific character tasks.
