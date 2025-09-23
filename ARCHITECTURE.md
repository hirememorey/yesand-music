# Architecture

Technical architecture and design decisions for YesAnd Music.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
  - [Traditional Architecture (File-Based)](#traditional-architecture-file-based)
  - [Live MIDI Streaming Architecture (Phase 4A)](#live-midi-streaming-architecture-phase-4a)
- [Core Components](#core-components)
  - [Control Plane](#control-plane-commands)
  - [Musical Intelligence Engine](#musical-intelligence-engine)
  - [MIDI Processing Layer](#midi-processing-layer)
  - [Visual Feedback System](#visual-feedback-system)
  - [DAW Integration System](#daw-integration-system)
  - [Live MIDI Streaming System](#live-midi-streaming-system-phase-4a)
- [Data Flow](#data-flow)
- [Design Principles](#design-principles)
- [Key Design Decisions](#key-design-decisions)
- [Extension Points](#extension-points)
- [Performance Characteristics](#performance-characteristics)
- [Integration Points](#integration-points)
- [Future Architecture](#future-architecture)
- [Quality Assurance](#quality-assurance)

---

## Overview

YesAnd Music follows a "Brain vs. Hands" architecture that separates core musical intelligence from DAW integration, enabling focus on musical intelligence without being constrained by DAW-specific APIs.

## System Architecture

### Traditional Architecture (File-Based)
```
Natural Language → Command Parser → Control Plane → Contextual Intelligence → Visual Feedback Display
       ↓                ↓                ↓              ↓                        ↓
   "analyze bass"   Command Types    Pattern Gen    Musical Analysis        Color-Coded
   "show melody"    (40+ types)      + OSC Sender   + Smart Suggestions      Highlighting
   "ardour tracks"  + Ardour Int.    + MIDI Player  + Educational Content    + Explanations
   "get suggestions" + Visual        (IAC Driver)   + Background Analysis    + Real-Time Updates
                     Feedback         + File I/O     + DAW Integration        + DAW State
```

### Live MIDI Streaming Architecture (Phase 4A)
```
Natural Language → Live Conversation → Live Editing → MIDI Stream → Real-Time → Ardour DAW
       ↓                ↓                ↓              ↓            ↓           ↓
   "funky bass"    AI Analysis      Live Commands   MIDI Events   IAC Driver   Live Track
   "make complex"   + Context        + Operations   + Timing      + Streaming   + Playback
   "add swing"      + References     + History      + Velocity    + Real-Time   + Visual
   "brighter"       + Session        + Undo/Redo    + Channel     + Safety      + Editing
```

## Core Components

### Control Plane (`commands/`)
**Purpose**: Natural language command processing and orchestration

**Key Files**:
- `control_plane.py`: Main orchestrator coordinating all components
- `parser.py`: Natural language command parsing with regex patterns
- `pattern_engine.py`: Musical pattern generation from commands
- `session.py`: Persistent state management with file-based storage

**Responsibilities**:
- Parse natural language commands into structured operations
- Maintain session state across command executions
- Coordinate between MIDI generation and visual feedback
- Handle error isolation and graceful degradation

### Musical Intelligence Engine
**Purpose**: Core musical analysis and problem-solving algorithms

**Key Files**:
- `contextual_intelligence.py`: Main analysis orchestrator
- `musical_solvers.py`: Problem-solving algorithms (groove, harmony, arrangement)
- `analysis.py`: Pure functions for musical analysis and transformation
- `theory.py`: Music theory helpers and generators

**Responsibilities**:
- Analyze musical elements (bass, melody, harmony, rhythm)
- Generate smart suggestions for musical improvements
- Apply musical transformations and problem-solving
- Provide educational content and explanations

### MIDI Processing Layer
**Purpose**: Universal MIDI data handling and real-time processing

**Key Files**:
- `midi_io.py`: Universal MIDI file I/O with consistent data format
- `project.py`: Project data management and querying
- `midi_player.py`: Real-time MIDI output
- `sequencer.py`: Non-blocking MIDI playback

**Responsibilities**:
- Convert MIDI files to universal note format
- Handle MIDI format constraints and validation
- Provide real-time MIDI output without blocking
- Manage project data and metadata

### Visual Feedback System
**Purpose**: On-demand visual feedback and educational display

**Key Files**:
- `visual_feedback_display.py`: Color-coded visual feedback system
- `osc_sender.py`: Python-to-JUCE plugin communication

**Responsibilities**:
- Display color-coded musical element highlighting
- Provide educational overlays and explanations
- Handle real-time visual updates without blocking audio
- Communicate with JUCE plugin via OSC

### DAW Integration System
**Purpose**: File-based integration with DAWs for state awareness

**Key Files**:
- `ardour_integration.py`: File-based Ardour DAW integration
- Project file parsing for track/region information
- Export/import workflow for MIDI data exchange

**Responsibilities**:
- Discover and parse DAW project files
- Export selected regions for analysis
- Import improved MIDI back to DAW
- Generate automation scripts (Lua for Ardour)
- Provide DAW state awareness through file-based workflow

### Live MIDI Streaming System (Phase 4A)
**Purpose**: Real-time MIDI generation and streaming to DAWs

**Key Files**:
- `ardour_live_integration.py`: Real-time MIDI streaming to Ardour DAW
- `live_editing_engine.py`: Real-time MIDI modification and editing
- `live_conversation_workflow.py`: Natural language control of live operations
- `live_control_plane_cli.py`: Interactive CLI for live MIDI streaming

**Responsibilities**:
- Stream MIDI events directly to DAW tracks in real-time
- Provide live editing capabilities for existing MIDI content
- Manage live editing sessions and track state
- Handle real-time MIDI port communication
- Coordinate between conversation AI and live operations

### Live Editing Engine
**Purpose**: Real-time MIDI modification and editing operations

**Key Files**:
- `live_editing_engine.py`: Core live editing functionality
- Live edit commands and operations
- Edit history and undo/redo management

**Responsibilities**:
- Apply real-time MIDI modifications (velocity, swing, accent, humanization)
- Manage edit history and provide undo/redo functionality
- Ensure real-time performance and thread safety
- Coordinate with live conversation workflow
- Provide structured command interface for live operations

## Data Flow

### Command Processing
```
User Input → Parser → Control Plane → Musical Intelligence → Visual Feedback → Display
     ↓         ↓          ↓              ↓                    ↓
"analyze"  Command    Orchestrate    Analyze Music      Show Results
"bass"     Types      Components     + Generate         + Educational
                                    Suggestions        Content
```

### MIDI Processing
```
MIDI File → Universal Format → Analysis → Transformations → Visual Feedback
     ↓            ↓              ↓            ↓               ↓
  Raw MIDI    Consistent      Musical     Improved        Color-Coded
  Data        Structure       Analysis    Versions        Display
```

### Real-Time Processing
```
MIDI Input → Control Plane → Pattern Engine → MIDI Output → DAW
     ↓            ↓              ↓              ↓
  Commands    Session State   Musical       Real-Time
  Parsing     Management      Patterns      Playback
```

### DAW Integration Processing
```
DAW Project → File Parser → Export/Import → Musical Analysis → Improved MIDI → DAW
     ↓            ↓             ↓              ↓                ↓
  .ardour     Track/Region   MIDI Files    Contextual        Enhanced
  Files       Discovery      Exchange     Intelligence       Versions
```

### Live MIDI Streaming Processing (Phase 4A)
```
User Input → Live Conversation → Live Editing → MIDI Stream → Real-Time → Ardour DAW
     ↓              ↓                ↓              ↓            ↓           ↓
"funky bass"   AI Analysis      Live Commands   MIDI Events   IAC Driver   Live Track
"make complex" + Context        + Operations   + Timing      + Streaming   + Playback
"add swing"    + References     + History      + Velocity    + Real-Time   + Visual
"brighter"     + Session        + Undo/Redo    + Channel     + Safety      + Editing
```

### Live Editing Processing
```
Existing MIDI → Live Edit Command → Real-Time Modification → Updated MIDI → DAW Track
     ↓               ↓                      ↓                    ↓            ↓
  Current Track   Operation Type        Apply Changes        New Version   Live Update
  + Content      + Parameters          + History            + Feedback    + Playback
  + State        + Intensity           + Undo/Redo          + Validation  + Visual
```

## Design Principles

### 1. Separation of Concerns
- **Musical Intelligence**: Pure algorithmic functions, testable and reliable
- **MIDI I/O**: Simple data conversion without musical logic
- **Visual Feedback**: Display logic separate from analysis
- **DAW Integration**: File-based workflow separate from real-time processing
- **Control Plane**: Orchestration without implementation details

### 2. Real-Time Safety
- No memory allocation in audio-critical paths
- No blocking operations in MIDI processing
- Thread-safe communication between components
- Background analysis doesn't interfere with audio

### 3. Extensibility
- Easy to add new command types
- Simple to extend musical analysis
- Modular visual feedback system
- Clear interfaces between components

### 4. Educational Value
- Every feature provides learning value
- Clear explanations of musical concepts
- Visual feedback helps understanding
- AI reasoning is transparent and explainable

### 5. DAW Integration
- File-based workflow for reliability
- No real-time dependencies on DAW APIs
- Automatic project discovery and parsing
- Seamless export/import workflow

## Key Design Decisions

### Universal Note Format
**Decision**: Use consistent dictionary format for all MIDI data
```python
{
    'pitch': int,                    # MIDI note number
    'velocity': int,                 # Note velocity (0-127)
    'start_time_seconds': float,     # Start time in seconds
    'duration_seconds': float,       # Note duration in seconds
    'track_index': int              # Track number
}
```

**Rationale**: 
- Avoids "Black Box Dependency Problem" with heavy MIDI libraries
- Enables pure functions in analysis layer
- Simplifies testing and debugging
- Provides consistent interface across all components

### Command Parser Architecture
**Decision**: Regex-based parsing with fallback to LLM for complex commands

**Rationale**:
- Fast parsing for common commands
- Natural language support for complex operations
- Easy to extend with new command types
- Maintains real-time performance

### Visual Feedback System
**Decision**: On-demand visual feedback with color-coded highlighting

**Rationale**:
- Addresses pre-mortem insight about visual learning
- Non-intrusive integration with DAW workflows
- Educational value through visual explanations
- Thread-safe operation without audio interference

### Musical Problem Solvers
**Decision**: One-command problem solving for specific musical challenges

**Rationale**:
- Solves real problems musicians face daily
- Maintains creative flow with immediate results
- Educational value through explanations
- Natural language interface matching musical vocabulary

### DAW Integration Architecture
**Decision**: File-based workflow instead of real-time API integration

**Rationale**:
- Avoids unstable DAW APIs and version dependencies
- Provides reliable state access through project files
- Maintains performance without real-time polling
- Enables cross-platform compatibility
- Allows offline analysis and improvement

## Extension Points

### Adding New Commands
1. Add command type to `CommandType` enum
2. Add regex patterns to parser
3. Implement command handling in control plane
4. Add visual feedback if needed

### Adding Musical Analysis
1. Extend `MusicalElement` enum
2. Implement analysis method
3. Add to analysis pipeline
4. Create visual feedback method

### Adding Visual Feedback
1. Extend `VisualFeedbackType` enum
2. Implement feedback generation
3. Add to display system
4. Update color coding

### Adding MIDI Transformations
1. Implement pure function in `analysis.py`
2. Add command type and parsing
3. Integrate with control plane
4. Add visual feedback for changes

### Adding DAW Integration
1. Extend `ArdourIntegration` class with new functionality
2. Add command types for new DAW operations
3. Implement file parsing for additional DAW data
4. Add export/import methods for new data types
5. Create automation scripts for DAW-specific operations

## Performance Characteristics

### Real-Time Processing
- MIDI playback: Non-blocking with timer-based note-off events
- Command parsing: < 10ms for common commands
- Visual feedback: Background thread, no audio interference
- OSC communication: Non-blocking with error isolation

### Memory Usage
- Visual feedback queue: Limited size with automatic cleanup
- Analysis results: Cached to avoid recomputation
- MIDI data: Universal format minimizes memory overhead
- Session state: File-based persistence with atomic updates

### Thread Safety
- Audio thread: Only MIDI processing, no allocation or locking
- Visual feedback: Separate thread with thread-safe queues
- Control plane: Synchronized access to shared state
- OSC communication: Non-real-time thread only

## Integration Points

### DAW Integration
- **MIDI I/O**: Via IAC Driver (macOS) or similar virtual ports
- **Plugin Integration**: JUCE plugin with AudioUnit/VST3 support
- **OSC Communication**: Real-time parameter control
- **File Exchange**: Standard MIDI file import/export
- **Ardour Integration**: File-based workflow with project parsing
- **State Awareness**: Track/region information from DAW project files

### External Dependencies
- **Python**: Core runtime and libraries
- **mido**: Lightweight MIDI I/O
- **python-rtmidi**: Real-time MIDI output
- **python-osc**: OSC communication
- **JUCE**: C++ plugin framework

## Future Architecture

### Phase 3C: LLM Integration
```
User Chat → LLM Agent → Musical Intelligence Engine → Invisible Assistance → DAW Integration
     ↓         ↓              ↓                           ↓                    ↓
"Make this  Parse intent,   Apply specific            Provide assistance,   Seamless
beat jazzier"  plan actions,   transformations,         explain reasoning    DAW workflow
              coordinate      analyze results           + Chat response      + File-based
                                                                             + State awareness
```

### Key Changes
- **LLM Agent**: Natural language understanding and orchestration
- **Command Orchestration**: Complex command decomposition and planning
- **Reasoning Engine**: Musical decision justification and explanation
- **Invisible Intelligence**: Background assistance without visual interference
- **Enhanced DAW Integration**: Real-time state access and seamless workflow

## Quality Assurance

### Architecture Validation
- **Brain vs. Hands**: Enforced separation between analysis and I/O
- **Pure Functions**: Analysis functions have no side effects
- **Real-Time Safety**: No blocking operations in audio paths
- **Thread Safety**: Proper synchronization between components

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Performance Tests**: Real-time safety validation
- **User Tests**: End-to-end workflow validation

## Conclusion

The architecture successfully separates concerns while maintaining real-time performance and educational value. The modular design enables easy extension while preserving the core principles of musical intelligence, non-intrusive integration, and user learning.

The system is ready for Phase 3C LLM integration, which will add natural language understanding and orchestration while maintaining the existing architectural principles.

---

## 📚 See Also

### 🚀 **Getting Started**
- [README.md](README.md) - Project overview and quick start
- [QUICKSTART.md](QUICKSTART.md) - Complete setup guide with multiple paths
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer workflows and guides

### 🎵 **Feature Guides**
- [docs/guides/LIVE_MIDI_STREAMING_README.md](docs/guides/LIVE_MIDI_STREAMING_README.md) - Live MIDI streaming and real-time editing
- [docs/guides/MUSICAL_CONVERSATION_README.md](docs/guides/MUSICAL_CONVERSATION_README.md) - Musical conversation system
- [docs/ARDOUR_INTEGRATION.md](docs/ARDOUR_INTEGRATION.md) - Ardour DAW integration

### 🛠️ **Development**
- [docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md) - JUCE plugin development
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

### 📋 **Reference**
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
