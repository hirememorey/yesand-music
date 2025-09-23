## Control Plane for Invisible Intelligence Semantic MIDI Editing

### Purpose
Provide a real-time control plane for MIDI generation and style control, with the primary focus on invisible intelligence semantic MIDI editing with natural language conversation that integrates seamlessly with existing DAW workflows.

### Vision: Invisible Intelligence Semantic MIDI Editing with Natural Language Interface
The ultimate goal is to enable intelligent, non-intrusive musical assistance through:
- **Background Musical Analysis**: Silent, continuous analysis that doesn't interrupt workflow
- **Contextual Intelligence**: Understand what musicians are working on without visual intrusion
- **Smart Suggestions**: Provide musical improvements only when requested
- **Natural Language Conversation**: Chat with AI assistant for musical guidance and complex operations
- **Seamless DAW Integration**: Work within familiar DAW workflows, not against them

### Strategic Pivot: From Visual-First to Invisible Intelligence
**Critical Insight from Pre-Mortem Analysis**: Musicians are creatures of habit who have spent years perfecting their DAW workflow. Any visual overlay or new interface feels invasive and disrupts their sacred "see-hear-adjust" workflow.

**New Approach**: The control plane now serves as a secondary interface, with the primary focus on invisible intelligence and natural language conversation that integrates seamlessly with existing DAW workflows without visual interference.

### Principles
- Embrace nondeterminism and simplicity: minimal timing guarantees, fast iteration.
- Never depend on undocumented DAW APIs for correctness; always provide a manual fallback.
- Make the system transparent: show current assumptions (key, target, randomness).

### Layers

#### Primary: Invisible Intelligence Interface with Natural Language Chat (Next Focus)
1. **Background MIDI Analysis Engine + Chat Interface** (Phase 3A - Weeks 1-2)
   - Silent MIDI analysis without visual interference
   - Background musical element detection (bass, melody, harmony, rhythm, drums)
   - Natural language chat interface for musical guidance and commands
   - DAW integration preserving familiar workflows
   - Contextual intelligence that understands current musical work

2. **Smart Invisible Suggestions + LLM Integration** (Phase 3B - Weeks 3-4)
   - Analyze patterns and suggest musical improvements only when requested
   - Contextual assistance for potential enhancements
   - Natural language application with immediate feedback
   - Musical intelligence display with educational content
   - Conversational AI assistant for complex musical operations
   - Natural language commands: "Make the bass line more jazzy", "Simplify the drums in the chorus"

3. **Advanced Invisible Intelligence Features + Advanced Chat** (Phase 3C - Weeks 5-6)
   - Advanced background analysis (harmonic, rhythmic, melodic, dynamic)
   - Multi-DAW support (Logic Pro, Pro Tools, Cubase)
   - Advanced interaction features (keyboard shortcuts, voice commands, contextual menus)
   - Voice integration for hands-free operation while playing
   - Collaborative chat for multiple musicians
   - Performance optimization without impacting DAW operation

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
   - Fail gracefully; invisible intelligence works without this
8. **Audio-derived suggestions** (optional)
   - Lightweight key estimation for visual analysis hints

### Current Scope (Implemented)
- Single-armed track model; user arms the target in Ardour/GarageBand.
- Intents: play scale/arp/random-walk; set key/scale; adjust density/register/velocity/randomness; send CC; stop.
- Patterns are simple, timed with `sleep`, and may randomize timing/velocity/pitch within constraints.

### Future Scope (Invisible Intelligence Semantic MIDI Editing with Natural Language Interface)
- **Background Pattern Recognition**: Silent analysis of musical elements without visual interference
- **Contextual Assistance**: Invisible help with immediate feedback
- **Smart Suggestions**: Natural language indicators for musical improvements
- **Natural Language Conversation**: Chat with AI assistant for musical guidance and complex operations
- **DAW Integration**: Seamless background operation within existing DAW workflows
- **Educational Value**: Natural language explanations of musical theory and concepts with conversational guidance
- **Multi-DAW Support**: Logic Pro, Pro Tools, Cubase integration
- **Advanced Features**: Keyboard shortcuts, voice commands, contextual menus
- **Collaborative Features**: Multiple musicians can chat with the same AI assistant

### Intent Grammar (Current)
- play: "play [scale|arp|random] in [KEY MODE] for [DURATION]"
- set: "set key to [KEY MODE]", "set density to [low|med|high]", "set randomness to [0..1]"
- cc: "cc [1-119] to [0-127]", "mod wheel [0-127]"
- target (with manifest or UI read): "target [piano|bass|pad]"
- stop: "stop", "silence"

### Intent Grammar (Future - Semantic MIDI Editing with Natural Language Conversation)
- modify: "make [element] [style]", "modify [element] from [location] [transformation]"
- analyze: "analyze [element]", "show [element] pattern", "what's the [element] doing"
- transform: "make it [style]", "add [characteristic]", "simplify [element]"
- context: "in [location]", "from [measure] to [measure]", "in the [section]"
- conversation: "How can I improve this?", "What would make this more interesting?", "Explain what's happening here"
- voice: Voice-to-text commands for hands-free operation while playing
- Examples:
  - "make the bass beat from measures 8-12 jazzier"
  - "simplify the harmony in the chorus"
  - "add more syncopation to the drums"
  - "make it more aggressive"
  - "How can I make this section more dynamic?"
  - "What's the harmonic function of this chord progression?"
  - "Show me alternative voicings for this chord"

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


