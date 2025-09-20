## Chat-driven Control Plane for Ardour

### Purpose
Use Cursor chat as a real-time control plane to influence Ardour via MIDI and eventually perform semantic MIDI editing. Precision sync is not required; nondeterministic, improvisatory output is desirable. Optional project context (key, track names) may inform behavior.

### Vision: Semantic MIDI Editing
The ultimate goal is to enable natural language commands like:
- **"Make the bass beat from measures 8-12 jazzier"** - Intelligent musical modifications
- **"Simplify the harmony in the chorus"** - Context-aware editing
- **"Add more syncopation to the drums"** - Style transformations
- **"Make it more aggressive"** - Musical concept application

### Principles
- Embrace nondeterminism and simplicity: minimal timing guarantees, fast iteration.
- Never depend on undocumented DAW APIs for correctness; always provide a manual fallback.
- Make the system transparent: show current assumptions (key, target, randomness).

### Layers
1. **Core control plane** (implemented, always works)
   - Parse chat into intents (play/pattern/cc/settings).
   - Maintain session state (key/scale, density, register, velocity, randomness).
   - Send MIDI to `IAC Driver Bus 1` toward the armed track in Ardour/GarageBand.
2. **Musical Analysis Engine** (planned)
   - Analyze existing MIDI data for bass lines, chord progressions, rhythmic patterns
   - Understand musical context and relationships
   - Identify musical elements and their functions
3. **Semantic MIDI Editing** (planned)
   - Parse complex musical commands ("make bass jazzier")
   - Apply style transformations while preserving context
   - Read, modify, and write MIDI data back to Ardour
4. **Ardour Integration** (partially implemented)
   - OSC communication for real-time control
   - MIDI file I/O for project data access
   - Project structure parsing (tracks, regions, measures)
5. **Declarative project manifest** (opt-in)
   - `project.yaml` or `project.json` describing key/scale, logical parts (piano, bass, pad), and suggested MIDI channels or track nicknames.
   - Chat can reference logical parts; the control plane maps intents to targets.
6. **Best-effort DAW context** (optional)
   - Use macOS Accessibility or AppleScript UI scripting to read track names and armed/selected state; optionally toggle arm/solo.
   - Fail gracefully; if unavailable or denied, continue with previous layers.
7. **Audio-derived suggestions** (optional)
   - With a loopback device (e.g., BlackHole), capture brief audio and run lightweight key estimation for hints, not authority.

### Current Scope (Implemented)
- Single-armed track model; user arms the target in Ardour/GarageBand.
- Intents: play scale/arp/random-walk; set key/scale; adjust density/register/velocity/randomness; send CC; stop.
- Patterns are simple, timed with `sleep`, and may randomize timing/velocity/pitch within constraints.

### Future Scope (Semantic MIDI Editing)
- **Musical Analysis**: Understand bass lines, chord progressions, rhythmic patterns
- **Complex Commands**: "Make bass jazzier", "simplify harmony", "add syncopation"
- **Context Preservation**: Maintain musical relationships during modifications
- **Ardour Integration**: Read existing MIDI, analyze, modify, write back
- **Style Transformations**: Apply musical concepts intelligently

### Intent Grammar (Current)
- play: "play [scale|arp|random] in [KEY MODE] for [DURATION]"
- set: "set key to [KEY MODE]", "set density to [low|med|high]", "set randomness to [0..1]"
- cc: "cc [1-119] to [0-127]", "mod wheel [0-127]"
- target (with manifest or UI read): "target [piano|bass|pad]"
- stop: "stop", "silence"

### Intent Grammar (Future - Semantic MIDI Editing)
- modify: "make [element] [style]", "modify [element] from [location] [transformation]"
- analyze: "analyze [element]", "show [element] pattern", "what's the [element] doing"
- transform: "make it [style]", "add [characteristic]", "simplify [element]"
- context: "in [location]", "from [measure] to [measure]", "in the [section]"
- Examples:
  - "make the bass beat from measures 8-12 jazzier"
  - "simplify the harmony in the chorus"
  - "add more syncopation to the drums"
  - "make it more aggressive"

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
- **Phase 1**: Enhanced MIDI file I/O for Ardour integration
- **Phase 2**: Musical analysis engine for bass lines, chord progressions, rhythmic patterns
- **Phase 3**: Semantic command parsing for complex musical modifications
- **Phase 4**: Style transformation engine for "jazzier", "simpler", "more aggressive"
- **Phase 5**: Advanced Ardour integration with real-time project awareness
- See [ROADMAP.md](../ROADMAP.md) for detailed implementation phases


