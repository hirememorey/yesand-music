## Control Plane for Visual-First Semantic MIDI Editing

### Purpose
Provide a real-time control plane for MIDI generation and style control, with the primary focus on visual-first semantic MIDI editing that integrates seamlessly with existing DAW workflows.

### Vision: Visual-First Semantic MIDI Editing
The ultimate goal is to enable visual, immediate feedback musical editing through:
- **Visual Pattern Recognition**: Highlight bass lines, melodies, chord progressions in real-time
- **Interactive MIDI Manipulation**: Drag-and-drop musical elements with instant audio feedback
- **Smart Visual Suggestions**: Show musical improvements with one-click application
- **Seamless DAW Integration**: Work within familiar DAW workflows, not against them

### Strategic Pivot: From Command-Based to Visual-First
**Critical Insight from Pre-Mortem Analysis**: Musicians are visual, immediate feedback creatures who work in familiar DAW environments. A command-based interface breaks their fundamental workflow of see-hear-adjust.

**New Approach**: The control plane now serves as a secondary interface, with the primary focus on visual analysis and manipulation that integrates seamlessly with existing DAW workflows.

### Principles
- Embrace nondeterminism and simplicity: minimal timing guarantees, fast iteration.
- Never depend on undocumented DAW APIs for correctness; always provide a manual fallback.
- Make the system transparent: show current assumptions (key, target, randomness).

### Layers

#### Primary: Visual-First Interface (Next Focus)
1. **Visual MIDI Analysis Engine** (Phase 3A - Weeks 1-2)
   - Real-time MIDI analysis with color-coded highlighting
   - Interactive drag-and-drop manipulation with immediate audio feedback
   - DAW integration preserving familiar workflows
   - Musical element highlighting (bass, melody, harmony, rhythm, drums)

2. **Smart Visual Suggestions** (Phase 3B - Weeks 3-4)
   - Analyze patterns and suggest musical improvements
   - Visual indicators for potential enhancements
   - One-click application with immediate feedback
   - Musical intelligence display with educational content

3. **Advanced Visual Features** (Phase 3C - Weeks 5-6)
   - Advanced visual analysis (harmonic, rhythmic, melodic, dynamic)
   - Multi-DAW support (Logic Pro, Pro Tools, Cubase)
   - Advanced interaction features (multi-touch, gestures, shortcuts)
   - Performance optimization with GPU acceleration

#### Secondary: Control Plane (Current - Maintained)
4. **Core control plane** (implemented, always works)
   - Parse chat into intents (play/pattern/cc/settings)
   - Maintain session state (key/scale, density, register, velocity, randomness)
   - Send MIDI to `IAC Driver Bus 1` toward the armed track in Ardour/GarageBand
   - OSC integration for real-time parameter control

5. **JUCE Plugin Integration** (implemented)
   - Real-time MIDI effect plugin with swing, accent, humanization
   - Thread-safe parameter management with APVTS
   - Style presets (jazz, classical, electronic, blues, straight)
   - Production-ready AudioUnit & VST3 formats

#### Optional: Enhanced Features
6. **Declarative project manifest** (opt-in)
   - `project.yaml` or `project.json` describing key/scale, logical parts
   - Visual interface can reference logical parts for highlighting
7. **Best-effort DAW context** (optional)
   - Use macOS Accessibility for track names and armed state
   - Fail gracefully; visual interface works without this
8. **Audio-derived suggestions** (optional)
   - Lightweight key estimation for visual analysis hints

### Current Scope (Implemented)
- Single-armed track model; user arms the target in Ardour/GarageBand.
- Intents: play scale/arp/random-walk; set key/scale; adjust density/register/velocity/randomness; send CC; stop.
- Patterns are simple, timed with `sleep`, and may randomize timing/velocity/pitch within constraints.

### Future Scope (Visual-First Semantic MIDI Editing)
- **Visual Pattern Recognition**: Real-time highlighting of musical elements
- **Interactive Manipulation**: Drag-and-drop interface with immediate feedback
- **Smart Suggestions**: Visual indicators for musical improvements
- **DAW Integration**: Seamless overlay on existing DAW interfaces
- **Educational Value**: Visual explanations of musical theory and concepts
- **Multi-DAW Support**: Logic Pro, Pro Tools, Cubase integration
- **Advanced Features**: Multi-touch, gestures, keyboard shortcuts

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
- **Phase 3A**: Visual MIDI Analysis Foundation (Weeks 1-2)
  - Visual pattern recognition with real-time highlighting
  - Interactive MIDI manipulation with drag-and-drop
  - DAW integration preserving familiar workflows
- **Phase 3B**: Smart Visual Suggestions (Weeks 3-4)
  - Smart suggestion engine with visual indicators
  - One-click application with immediate feedback
  - Musical intelligence display with educational content
- **Phase 3C**: Advanced Visual Features (Weeks 5-6)
  - Advanced visual analysis (harmonic, rhythmic, melodic, dynamic)
  - Multi-DAW support (Logic Pro, Pro Tools, Cubase)
  - Advanced interaction features and performance optimization
- See [ROADMAP.md](../ROADMAP.md) for detailed implementation phases


