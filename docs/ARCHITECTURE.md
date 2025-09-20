## Architecture

### Overview
The project separates concerns into data core (MIDI I/O), transport (MIDI I/O), scheduling (timing), theory helpers (content generation), musical analysis, and orchestration (entrypoint).

```
Data Core: midi_io.py → project.py → Universal Note Format
    ↓
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

### JUCE Plugin Architecture (Real-Time MIDI Processing)
```
MIDI Input → Style Transfer Plugin → Real-Time Transformations → MIDI Output
     ↓              ↓                        ↓                      ↓
  DAW Track    Swing/Accent            Real-Time Safe         Transformed
  (Ardour)     Transformations         Processing             MIDI to DAW
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

### Implemented: JUCE Plugin (Real-Time MIDI Processing)
- **Core components** (implemented):
  - **StyleTransferAudioProcessor**: Main plugin class handling MIDI processing
  - **StyleParameters**: Real-time safe parameter structure for swing, accent, and humanization control
  - **Modular transformation functions**: Pure, testable functions for each transformation type
  - **Real-time Safety**: All MIDI processing code follows strict real-time safety constraints
  - **OSC Integration**: Remote control via Open Sound Control with thread-safe architecture
- **Key features**:
  - **Swing Transformation**: Off-beat note timing adjustment based on configurable swing ratio
  - **Accent Transformation**: Down-beat velocity enhancement for musical emphasis
  - **Humanization Transformation**: Subtle timing and velocity variations for authentic human feel
  - **Real-time Processing**: No memory allocation, locking, or blocking calls in audio thread
  - **Plugin Formats**: VST3 and AudioUnit support for cross-platform compatibility
  - **Parameter Control**: Real-time parameter adjustment for all transformation parameters
  - **OSC Control**: Remote parameter control via OSC messages (`/style/swing`, `/style/accent`, `/style/enable`)
- **Future extensions** (planned):
  - **Advanced Style Transformations**: Jazz, classical, electronic, blues styles
  - **Velocity Curves**: Dynamic shaping of note velocities
  - **Advanced OSC Features**: Bidirectional communication, parameter automation, preset management
  - **Machine Learning**: Style learning and adaptive processing
- See: `docs/JUCE_PLUGIN_DEVELOPMENT.md` for detailed implementation and development approach.

### Data Core (New Foundation)
- `midi_io.py`
  - **Pure Python MIDI I/O** using lightweight mido library
  - `parse_midi_file()`: Converts MIDI files to universal note dictionary format
  - `save_midi_file()`: Saves note dictionaries back to MIDI files
  - Universal data structure: `{'pitch': int, 'velocity': int, 'start_time_seconds': float, 'duration_seconds': float, 'track_index': int}`
  - **No heavy dependencies** - avoids "Black Box Dependency Problem"
  - Comprehensive validation and error handling

- `project.py`
  - **Project class** as container for musical data and metadata
  - `load_from_midi()` and `save_to_midi()` methods using midi_io functions
  - Query methods: `get_notes_by_track()`, `get_notes_in_time_range()`, `get_duration()`
  - **Separation of concerns** - pure data management without musical analysis logic
  - Prevents "Spaghetti Code Problem" through clean, focused design

- `analysis.py`
  - **Pure functions** for musical data analysis and transformation
  - `filter_notes_by_pitch()`: Filter notes by pitch range for bass line analysis
  - `apply_swing()`: Apply swing feel by delaying off-beat notes
  - **No side effects** - creates new data instead of modifying original
  - **Foundation for semantic MIDI editing** - implements transformations that will be used in JUCE plugin
  - **Testable in isolation** - each function can be tested independently

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


