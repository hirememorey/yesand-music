## Chat-driven Control Plane for GarageBand

### Purpose
Use Cursor chat as a real-time control plane to influence GarageBand via MIDI. Precision sync is not required; nondeterministic, improvisatory output is desirable. Optional project context (key, track names) may inform behavior.

### Principles
- Embrace nondeterminism and simplicity: minimal timing guarantees, fast iteration.
- Never depend on undocumented DAW APIs for correctness; always provide a manual fallback.
- Make the system transparent: show current assumptions (key, target, randomness).

### Layers
1. Core control plane (baseline, always works)
   - Parse chat into intents (play/pattern/cc/settings).
   - Maintain session state (key/scale, density, register, velocity, randomness).
   - Send MIDI to `IAC Driver Bus 1` toward the armed track in GarageBand.
2. Declarative project manifest (opt-in)
   - `project.yaml` or `project.json` describing key/scale, logical parts (piano, bass, pad), and suggested MIDI channels or track nicknames.
   - Chat can reference logical parts; the control plane maps intents to targets.
3. Best-effort DAW context (optional)
   - Use macOS Accessibility or AppleScript UI scripting to read track names and armed/selected state; optionally toggle arm/solo.
   - Fail gracefully; if unavailable or denied, continue with Layers 1–2.
4. Audio-derived suggestions (optional)
   - With a loopback device (e.g., BlackHole), capture brief audio and run lightweight key estimation for hints, not authority.

### MVP Scope
- Single-armed track model; user arms the target in GarageBand.
- Intents: play scale/arp/random-walk; set key/scale; adjust density/register/velocity/randomness; send CC; stop.
- Patterns are simple, timed with `sleep`, and may randomize timing/velocity/pitch within constraints.

### Intent Grammar (initial)
- play: "play [scale|arp|random] in [KEY MODE] for [DURATION]"
- set: "set key to [KEY MODE]", "set density to [low|med|high]", "set randomness to [0..1]"
- cc: "cc [1-119] to [0-127]", "mod wheel [0-127]"
- target (with manifest or UI read): "target [piano|bass|pad]"
- stop: "stop", "silence"

### Project Manifest (optional)
Example `project.yaml`:
```yaml
key: D minor
tempo: 100
parts:
  - name: piano
    channel: 1
    track_hint: "Soft Piano"
  - name: bass
    channel: 2
    track_hint: "Electric Bass"
cc_map:
  cutoff: 74
  resonance: 71
randomness: 0.35
```

### Developer Plan
1. Core
   - Parse intents from chat text (simple regex/keywords first).
   - Maintain session state in memory.
   - Map intents to MIDI events and patterns via existing `sequencer.py` and `midi_player.py`.
2. Manifest
   - Load optional `project.yaml`/`project.json`; expose logical parts and CC names.
   - If missing, operate with sensible defaults.
3. Optional UI read (macOS only)
   - Use Accessibility to read selected track name and armed flags.
   - Feature-flag and handle permission errors; never block core behavior.
4. Audio hints (off by default)
   - If loopback available, provide a key suggestion command.

### Risks and Mitigations
- GarageBand lacks public APIs → Use manual arming and a manifest; UI scripting is optional and resilient to failure.
- Track targeting ambiguity → Rely on armed track; surface current assumption to the user.
- Timing jitter → Accept as design; keep patterns short and reactive.

### Testing
- Unit: intent parsing, manifest loading, pattern generation.
- Integration: fake mido output to capture messages; manual DAW test.
- Optional: UI read smoke test guarded by platform checks.

### Next Steps
- Implement Layer 1 (core control plane) and ship simple commands.
- Add manifest support and a few CC aliases.
- Explore UI read for track names/armed state as an optional enhancement.


