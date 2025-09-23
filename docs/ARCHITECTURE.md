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

### Vision: Contextual Intelligence Architecture with On-Demand Visual Feedback
```
MIDI Input → Background Intelligence Engine → Contextual Intelligence → Visual Feedback Display → DAW Integration
     ↓              ↓                           ↓                        ↓                        ↓
  DAW Track    Silent Pattern              On-Demand Visual         Color-Coded              Seamless
  (Piano Roll)  Recognition &               Feedback System          Highlighting             DAW Workflow
                Analysis                     + Educational            + Explanations           Integration
                (Harmonic, Rhythmic,        Content                  + Smart Suggestions      (Non-Intrusive
                Melodic, Style)             + Natural Language       + Real-Time Updates      Visual Feedback)
                                         Commands
```

### LLM Integration Pattern: Natural Language Interface and Orchestrator
```
User Chat → LLM Chat Interface → Musical Intelligence Engine → Invisible + Audio Feedback
     ↓            ↓                      ↓                           ↓
"Make this    Parse conversation,    Apply specific            Provide assistance,
beat jazzier"  understand context,    transformations,          explain reasoning
              plan actions,          analyze results           + Chat response
              coordinate
```

### Current: Contextual Intelligence with Visual Feedback (Primary)
```
Natural Language → Command Parser → Control Plane → Contextual Intelligence → Visual Feedback Display
       ↓                ↓                ↓              ↓                        ↓
   "analyze bass"   Command Types    Pattern Gen    Musical Analysis        Color-Coded
   "show melody"    (33+ types)      + OSC Sender   + Smart Suggestions      Highlighting
   "get suggestions" + Visual        + MIDI Player  + Educational Content    + Explanations
                     Feedback         (IAC Driver)  + Background Analysis    + Real-Time Updates
```

### Secondary: Chat-driven Control with OSC Integration
```
Natural Language → Command Parser → Control Plane → MIDI Output + OSC Control
       ↓                ↓                ↓              ↓           ↓
   "play scale     Command Types    Pattern Gen    MIDI Player   JUCE Plugin
    with jazz"     (23+ types)      + OSC Sender   (IAC Driver)  (Style Effects)
```

### Future: Invisible Intelligence with Natural Language Chat Interface (Primary)
```
Natural Language → LLM Chat Interface → Musical Intelligence → Invisible Assistance → DAW Integration
       ↓                ↓                      ↓                    ↓                    ↓
   "Make the bass   Parse conversation,    Apply musical        Provide contextual   Seamless
    line jazzier"   understand context,    transformations,     help and            DAW workflow
                    plan actions,          analyze results      explanations        integration
                    coordinate                                    (on-demand)         (no visual
                                                                                      interference)
```

### JUCE Plugin Architecture (Real-Time MIDI Processing)
```
MIDI Input → Style Transfer Plugin → Real-Time Transformations → MIDI Output
     ↓              ↓                        ↓                      ↓
  DAW Track    Swing/Accent            Real-Time Safe         Transformed
  (Ardour)     Transformations         Processing             MIDI to DAW
```

### Implemented: Chat-driven control plane with OSC integration
- **Core components** (all implemented):
  - **Command Parser** (`commands/parser.py`): Converts natural language into structured commands using regex patterns
  - **Session Manager** (`commands/session.py`): Persistent state management with file-based storage
  - **Pattern Engine** (`commands/pattern_engine.py`): Generates musical patterns from commands and session state
  - **Control Plane** (`commands/control_plane.py`): Main orchestrator that coordinates all components
  - **Non-blocking Sequencer**: Timer-based note-off events for real-time performance
  - **OSC Sender** (`osc_sender.py`): Python-to-JUCE plugin communication via OSC messages
- **Key features**:
  - Natural language command parsing (23+ command types including OSC)
  - Persistent session state across command executions
  - Multiple pattern types (scales, arpeggios, random notes)
  - Control commands (CC, modulation wheel, tempo, key)
  - OSC style control (swing, accent, humanization, style presets)
  - CLI interface ready for chat integration
  - Combined MIDI playback with real-time style effects
- **OSC Integration** (newly implemented):
  - **Style Parameter Control**: Real-time control of plugin parameters via natural language
  - **Style Presets**: Built-in presets (jazz, classical, electronic, blues, straight)
  - **Thread-Safe Design**: OSC operations run in non-real-time thread
  - **Parameter Validation**: Automatic clamping and validation of all values
  - **Error Isolation**: OSC failures don't affect MIDI functionality
- **Future extensions** (planned):
  - **Enhanced Musical Intelligence Engine**: Deep analysis of bass lines, chord progressions, rhythmic patterns
  - **LLM Reasoning Layer**: Natural language understanding and orchestration of musical operations
  - **Visual MIDI Editor**: Interactive piano roll with real-time visualization and editing
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

## Contextual Intelligence Components (Phase 3A Complete)

### Contextual Intelligence Engine (`contextual_intelligence.py`)
**Purpose**: Core musical analysis and smart suggestion generation

**Key Components**:
- `ContextualIntelligence` class: Main orchestrator
- `MusicalAnalysis` dataclass: Comprehensive musical analysis results
- `VisualFeedback` dataclass: Structured feedback for display
- `MusicalElement` enum: Bass, melody, harmony, rhythm, drums
- `VisualFeedbackType` enum: Highlight, diff, explanation, suggestion, analysis

**Musical Analysis Capabilities**:
- **Bass Line Detection**: Identifies low-pitch notes (≤C4) as bass elements
- **Melody Recognition**: Finds highest-pitch notes in each time segment
- **Harmony Analysis**: Identifies supporting chord tones
- **Rhythm Analysis**: Calculates swing, syncopation, and complexity
- **Style Classification**: Detects jazz, classical, electronic, blues, pop styles
- **Confidence Scoring**: Provides reliability metrics for each analysis

### Visual Feedback Display System (`visual_feedback_display.py`)
**Purpose**: Non-intrusive visual feedback display

**Key Components**:
- `VisualFeedbackDisplay` class: Main display window
- Color-coded highlighting system
- Real-time updates without blocking audio
- Educational overlays and explanations
- Thread-safe operation

**Visual Features**:
- **Color Coding**: Blue (bass), Green (melody), Purple (harmony), Orange (rhythm), Red (drums)
- **Educational Content**: Musical theory explanations and AI reasoning
- **Smart Suggestions**: Actionable improvement recommendations
- **Real-Time Updates**: Live feedback as users interact
- **Non-Intrusive Design**: Separate window that doesn't interfere with DAW

### Extended Command System
**New Command Types** (10 additional commands):
- `load [FILE]` - Load MIDI project for analysis
- `analyze bass` - Show bass line analysis and highlighting
- `analyze melody` - Show melody analysis and highlighting
- `analyze harmony` - Show harmony analysis and highlighting
- `analyze rhythm` - Show rhythm analysis and highlighting
- `analyze all` - Complete musical analysis
- `get suggestions` - Get improvement suggestions
- `apply suggestion [ID]` - Apply a specific suggestion
- `show feedback` - Show visual feedback summary
- `clear feedback` - Clear all visual feedback

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

- `analysis.py` (Musical Intelligence Engine Foundation)
  - **Pure functions** for musical data analysis and transformation
  - `filter_notes_by_pitch()`: Filter notes by pitch range for bass line analysis
  - `apply_swing()`: Apply swing feel by delaying off-beat notes
  - **No side effects** - creates new data instead of modifying original
  - **Foundation for semantic MIDI editing** - implements transformations that will be used in JUCE plugin
  - **Testable in isolation** - each function can be tested independently
  - **Future extensions**: Harmonic analysis, rhythmic analysis, style classification, intelligent suggestions

### LLM Integration Layer (Future Component)
- `llm_agent.py` (Planned)
  - **Natural language conversation** for musical guidance and commands
  - **Chat interface** that responds to visual selections and provides contextual help
  - **Orchestration layer** that coordinates musical intelligence engine
  - **Command parsing and planning** for complex musical operations
  - **Reasoning and explanation** for musical decisions
  - **Voice integration** for hands-free operation while playing
  - **Context awareness** for understanding current musical selection and project state
  - **Integration with existing musical intelligence engine** (analysis.py, theory.py)

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


