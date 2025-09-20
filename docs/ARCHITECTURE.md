## Architecture

### Overview
The project separates concerns into transport (MIDI I/O), scheduling (timing), theory helpers (content generation), musical analysis, and orchestration (entrypoint).

```
main.py → Sequencer → MidiPlayer → mido → OS MIDI → Ardour/GarageBand
           ↑
        theory
           ↑
    musical_analysis (future)
```

### Vision: Semantic MIDI Editing Architecture
```
Natural Language → Command Parser → Musical Analysis → Style Transform → Ardour Integration
       ↓                ↓                ↓                ↓                ↓
   "make bass      Command Types    Bass Pattern    Jazz Style      Write MIDI
    jazzier"       (existing)       Analysis        Application     Back to DAW
```

### Implemented: Chat-driven control plane
- **Core components** (all implemented):
  - **Command Parser** (`commands/parser.py`): Converts natural language into structured commands using regex patterns
  - **Session Manager** (`commands/session.py`): Persistent state management with file-based storage
  - **Pattern Engine** (`commands/pattern_engine.py`): Generates musical patterns from commands and session state
  - **Control Plane** (`commands/control_plane.py`): Main orchestrator that coordinates all components
  - **Non-blocking Sequencer**: Timer-based note-off events for real-time performance
- **Key features**:
  - Natural language command parsing (15+ command types)
  - Persistent session state across command executions
  - Multiple pattern types (scales, arpeggios, random notes)
  - Control commands (CC, modulation wheel, tempo, key)
  - CLI interface ready for chat integration
- **Future extensions** (planned):
  - **Musical Analysis Engine**: Deep analysis of bass lines, chord progressions, rhythmic patterns
  - **Semantic MIDI Editing**: "Make bass jazzier", "simplify harmony", "add syncopation"
  - **Ardour Integration**: Read existing MIDI, analyze, modify, write back
  - **Style Transformations**: Apply musical concepts and maintain context
  - Manifest loader: `project.yaml`/`project.json` for logical parts and CC aliases
  - UI reader: macOS Accessibility API for track names and armed state
- See: `docs/CONTROL_PLANE.md` for detailed design and implementation.
- See: `ROADMAP.md` for the semantic MIDI editing vision and implementation phases.

### Modules and responsibilities
- `midi_player.py`
  - Opens a mido output port by name.
  - Sends `note_on`, waits, then `note_off`.
  - Handles failure by printing available ports.

- `sequencer.py`
  - Stores note events as dicts:
    - `pitch: int`, `velocity: int`, `start_beat: float`, `duration_beats: float`.
  - Converts beats to seconds with `seconds_per_beat = 60 / BPM`.
  - **Non-blocking playback**: Uses timer-based note-off events for real-time performance
  - **Async support**: `play_async()` method for background playback with stop controls
  - Sorts by `start_beat` and triggers notes via `MidiPlayer.send_note_on()` immediately

- `theory.py`
  - Provides musical generators, e.g., `create_major_scale(root)` → 8 MIDI notes including octave.

- `config.py`
  - Global settings: `MIDI_PORT_NAME`, `BPM`.

- `main.py`
  - Wires everything together for the demo (C Major quarter notes).

### Timing model
- Beat-based scheduling.
- Blocking loop: `sleep((next_start - current_beat) * seconds_per_beat)`.
- Note triggering is synchronous: `note_on` → sleep → `note_off`.

### Design trade-offs
- Simplicity over precision: relies on `time.sleep`, which is adequate for a demo but not sample-accurate.
- Single-threaded: easy to reason about; overlapping long notes still work because `send_note` blocks for the note duration (polyphony limited per step).
- Extensibility: additional generators or alternate players can be added without touching the core scheduling logic.

### Extension points
- **Musical Analysis**: Add functions to `theory.py` for pattern recognition, harmonic analysis, style classification
- **Semantic Commands**: Extend `commands/parser.py` with new command types for musical modifications
- **Ardour Integration**: Add MIDI file I/O, project structure parsing, OSC communication
- **Style Engine**: Create style transformation modules for "jazzier", "simpler", "more aggressive"
- New content: add functions to `theory.py` (arpeggios, chords, rhythms).
- Alternate output: subclass or replace `MidiPlayer` (e.g., different backend or network MIDI).
- Advanced scheduling: add a non-blocking scheduler that overlaps notes, or quantization/latency compensation.


