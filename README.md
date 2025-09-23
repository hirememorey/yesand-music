## YesAnd Music: Visual-First Semantic MIDI Editing

The goal of this project is to enable musicians to intelligently edit their music through **visual analysis, interactive manipulation, and smart suggestions** that integrate seamlessly with their existing DAW workflows.

## 🔄 Strategic Pivot: From Command-Based to Visual-First

**Critical Insight from Pre-Mortem Analysis**: Musicians are visual, immediate feedback creatures who work in familiar DAW environments. A command-based interface breaks their fundamental workflow of see-hear-adjust.

**New Vision**: Transform MIDI editing from technical manipulation to visual, intelligent interaction that enhances rather than disrupts existing creative workflows.

## The Solution

To achieve this, YesAnd Music is composed of three primary systems:

### Part 1: The Real-Time Control Plane (Live/Generative) ✅ COMPLETE
A tool for real-time, interactive music creation. This system is currently functional and allows you to generate MIDI patterns (scales, arpeggios) on the fly via chat commands.

**Current Features:**
- Interactive MIDI control via natural language commands
- Real-time session state management with persistent storage
- Multiple pattern types: scales, arpeggios, random notes with configurable density and randomness
- Control commands: CC messages, modulation wheel, tempo, key, and more
- CLI interface ready for chat integration: `python control_plane_cli.py "play scale D minor"`
- JUCE Plugin Development: Real-time MIDI effect plugin with swing, accent, and humanization transformations
- OSC Integration: Complete Python-to-JUCE plugin communication with real-time parameter control
- Style Control: Natural language control of plugin parameters via OSC messages

### Part 2: The Visual MIDI Analysis Engine (Next Focus) 🎯
A visual-first system for intelligent MIDI editing that integrates seamlessly with existing DAW workflows.

**Phase 3A Features (Visual Foundation):**
- **Visual Pattern Recognition**: Real-time MIDI analysis with color-coded highlighting
- **Interactive MIDI Manipulation**: Drag-and-drop interface with immediate audio feedback
- **DAW Integration**: Seamless overlay on existing DAW piano roll interfaces
- **Musical Element Highlighting**: Bass lines, melodies, chord progressions, rhythmic patterns

**Phase 3B Features (Smart Suggestions):**
- **Smart Suggestion Engine**: Analyze patterns and suggest musical improvements
- **Visual Feedback System**: Real-time highlighting of suggested changes
- **One-Click Application**: Single-click application with immediate feedback
- **Musical Intelligence Display**: Show musical theory behind suggestions

**Phase 3C Features (Advanced Visual):**
- **Advanced Visual Analysis**: Harmonic, rhythmic, melodic, and dynamic analysis
- **Multi-DAW Support**: Logic Pro, Pro Tools, Cubase integration
- **Advanced Interaction**: Multi-touch, gestures, keyboard shortcuts
- **Performance Optimization**: Real-time performance with GPU acceleration

### Part 3: The Command-Line Editor (Offline/Editorial) ✅ PHASE 1 COMPLETE
A tool for intelligent, offline music editing of existing MIDI files from a DAW. Phase 1 MVP is now complete and functional.

**Phase 1 Features (✅ Complete):**
- Command-line MIDI editor: `python edit.py --input song.mid --output swung.mid --command "apply_swing"`
- Swing transformation: Apply swing feel to off-beat notes
- MIDI file I/O: Load and save MIDI files using universal note format
- Constraint handling: Automatic sorting and overlap resolution for MIDI format compliance
- Comprehensive testing plan: Step-by-step validation workflow

## The Architecture

Our architectural philosophy is to separate the core intelligence from the DAW integration while prioritizing visual, immediate feedback for musicians.

**The "Brain"** is a standalone Python application that handles all musical analysis and transformation. It takes a MIDI file as input and produces a new MIDI file as output.

**The "Eyes"** are the visual analysis and highlighting systems that show musicians what's happening in their music in real-time.

**The "Hands"** are the simple integration points that get MIDI data to and from the DAW.

**The "Heart"** is the visual interface that provides immediate feedback and integrates seamlessly with existing DAW workflows.

This separation allows us to:
- Focus on musical intelligence without being constrained by DAW-specific APIs
- Provide visual, immediate feedback that musicians expect
- Test and develop the core functionality independently
- Support multiple DAWs through simple integration points
- Maintain real-time safety and performance standards
- Preserve familiar DAW workflows while adding intelligent features

## The Roadmap

Our development is focused on de-risking the biggest challenges first, with a strategic pivot to visual-first approach based on pre-mortem analysis.

### Phase 1: The "Manual Roundtrip" MVP ✅ COMPLETE
Built the core "Brain" and proved the end-to-end editing loop works via a simple command-line interface.
- ✅ Enhanced MIDI file I/O for DAW integration
- ✅ Basic musical analysis functions (swing transformation)
- ✅ Simple command-line interface for testing transformations
- ✅ Proof of concept for the full editing workflow
- ✅ MIDI format constraint handling (sorting, overlaps)
- ✅ Comprehensive testing plan and validation

### Phase 2A: JUCE Plugin Development ✅ COMPLETE
Successfully created a testable JUCE plugin for immediate DAW integration with real-time MIDI processing.
- ✅ Real-time MIDI effect plugin for DAW integration (installed and working)
- ✅ Swing and accent transformations (real-time safe algorithms implemented)
- ✅ Production-ready plugin for immediate testing (AudioUnit & VST3 formats)
- ✅ OSC control integration with existing Python control plane
- **Implementation Strategy**: Hybrid approach (70% Pragmatic CTO + 20% Security Engineer + 10% Staff Engineer)
- **Timeline**: Completed ahead of schedule
- **Success Criteria**: ✅ All achieved - Plugin loads in Logic Pro, processes MIDI, real-time safe
- **Approach**: Successfully balanced speed with essential safety requirements

### Phase 2B: OSC Integration & Enhanced Features ✅ COMPLETE
Complete Python-to-JUCE plugin communication with style presets and natural language control.
- ✅ Complete OSC integration with Python-to-JUCE plugin communication
- ✅ Style presets (jazz, classical, electronic, blues, straight) operational
- ✅ Natural language commands (8 OSC command types) parsing and executing correctly
- ✅ Thread-safe design with error isolation
- ✅ Parameter validation and clamping working properly

### Phase 3: Visual MIDI Analysis Engine 🎯 NEXT FOCUS
**Strategic Pivot**: Transform from command-based to visual-first approach based on pre-mortem insights.

**Phase 3A: Visual Foundation (Weeks 1-2)**
- Visual pattern recognition with real-time highlighting
- Interactive MIDI manipulation with drag-and-drop
- DAW integration preserving familiar workflows
- Basic visual interface with immediate feedback

**Phase 3B: Smart Visual Suggestions (Weeks 3-4)**
- Smart suggestion engine with visual indicators
- One-click application with immediate feedback
- Musical intelligence display with educational content
- A/B comparison interface for testing changes

**Phase 3C: Advanced Visual Features (Weeks 5-6)**
- Advanced visual analysis (harmonic, rhythmic, melodic, dynamic)
- Multi-DAW support (Logic Pro, Pro Tools, Cubase)
- Advanced interaction features (multi-touch, gestures, shortcuts)
- Performance optimization with GPU acceleration

## Current Development Status

### ✅ **Phase 1 Complete: Control Plane & MIDI Editor**
- **Python Control Plane**: 23+ command types with OSC integration
- **Semantic MIDI Editor**: Command-line tool with swing transformation
- **OSC Integration**: Python-to-JUCE plugin communication ready
- **Style Presets**: Jazz, classical, electronic, blues, straight

### ✅ **Phase 2A Complete: JUCE Plugin Development**
- **Production-Ready Plugin**: AudioUnit & VST3 formats installed and working
- **Real-Time Safe Algorithms**: Swing and accent transformations implemented
- **Thread-Safe Parameters**: APVTS integration for real-time control
- **Plugin UI**: Basic parameter controls for swing and accent
- **Comprehensive Testing**: Full test suite with validation
- **DAW Integration**: ✅ **VERIFIED WORKING** in Logic Pro, GarageBand, and Reaper
- **Plugin Validation**: ✅ **PASSED** AudioUnit validation with all tests

### ✅ **Phase 2B Complete: OSC Integration & Enhanced Features**
- **OSC Integration**: Complete Python-to-JUCE plugin communication working
- **Style Presets**: 5 presets (jazz, classical, electronic, blues, straight) operational
- **Natural Language Commands**: 8 OSC command types parsing and executing correctly
- **Thread-Safe Design**: OSC operations run in non-real-time thread
- **Error Isolation**: OSC failures don't affect MIDI functionality
- **Parameter Validation**: All OSC parameters properly clamped and validated

### 🎯 **Phase 3 Next Focus: Musical Analysis Engine**
**Goal**: Build the core musical intelligence for semantic MIDI editing

**Implementation Strategy**:
- Bass line analysis and pattern recognition
- Chord progression analysis and harmonic understanding
- Rhythmic pattern analysis (swing, syncopation, groove)
- Musical context understanding and element relationships

**Success Criteria**:
- Can analyze existing MIDI and identify musical elements
- Understands musical relationships and context
- Provides meaningful musical insights

## Quick Start: Complete System

Both Phase 1 and Phase 2A are complete and ready for use. Here's how to get started:

### 🎵 JUCE Plugin (Phase 2A & 2B Complete)
The plugin is already built, installed, and validated! Use it in your DAW:

#### **GarageBand Instructions:**
1. **Open GarageBand** and create a new project
2. **Create a Software Instrument track**
3. **Load the "Style Transfer" plugin**:
   - Click on the track to select it
   - In Smart Controls panel, look for "MIDI Effects" section
   - Click the MIDI Effects slot and select "Style Transfer"
   - Alternative: Track > Show Track Inspector > MIDI Effects > Style Transfer
4. **Adjust parameters**:
   - Swing Ratio: 0.5 = straight, > 0.5 = swing feel
   - Accent Amount: Velocity boost for down-beat notes (0-50)
   - OSC Enabled: Toggle for remote control
   - OSC Port: Set port for Python control (default: 3819)
5. **Play MIDI notes** to hear real-time transformations

#### **Logic Pro Instructions:**
1. **Open Logic Pro** and create a new project
2. **Create a Software Instrument track**
3. **Add "Style Transfer" plugin** in the MIDI Effects section
4. **Adjust parameters** and play MIDI notes

#### **Test the plugin:**
```bash
# Run comprehensive test suite
python test_plugin.py

# Test OSC control
python control_plane_cli.py "set swing to 0.7"
python control_plane_cli.py "make it jazz"
```

### 📝 Semantic MIDI Editor (Phase 1 Complete)
```bash
# Apply swing transformation to a MIDI file
python edit.py --input song.mid --output swung.mid --command "apply_swing"

# See all available options
python edit.py --help
```

**What it does:**
- Loads MIDI files using the universal note format
- Applies swing transformation to off-beat notes
- Handles MIDI format constraints automatically
- Saves transformed MIDI files ready for DAW import

**Testing:**
- See `TESTING_PLAN.md` for complete validation workflow
- Export MIDI from your DAW → transform → import back to verify

## Developer Quickstart: Real-Time Control Plane

The Real-Time Control Plane is currently functional and ready for use. Here's how to get started:

### Quick Setup (time-to-first-note)

1) Create and activate a virtualenv
```bash
cd "/path/to/yesand-music"
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip3 install --upgrade pip setuptools wheel
pip3 install mido python-rtmidi python-osc
```

3) Enable IAC Driver and create a port named "IAC Driver Bus 1"
- Open: Audio MIDI Setup → Window → Show MIDI Studio → double‑click IAC Driver → Enable.
- Add or rename a port to: `IAC Driver Bus 1`.

4) Prepare GarageBand to receive MIDI
- Create a Software Instrument track.
- Arm the track for recording and enable input monitoring (so it listens to external MIDI).

5) Run the demo
```bash
# Original demo
python3 main.py

# New control plane (interactive)
python3 main.py --interactive

# Control plane CLI (for chat integration)
python3 control_plane_cli.py "play scale D minor"
```
Expected: Terminal prints "Playing C Major Scale..." and GarageBand plays 8 notes.

### Control Plane Commands

#### Interactive Mode
```bash
python3 main.py --interactive

# Then try these commands:
play scale D minor          # Play a D minor scale
play arp C major           # Play a C major arpeggio  
play random 8              # Play 8 random notes
set key to F# lydian       # Change key and mode
set tempo to 140           # Change tempo
set density to high        # Change note density
set randomness to 0.3      # Add some randomness
cc 74 to 64               # Send control change
mod wheel 32              # Send modulation wheel
status                    # Show current state
stop                      # Stop playback
help                      # Show all commands
```

#### OSC Style Control (JUCE Plugin) ✅ WORKING
```bash
# Style parameter control (tested and working)
python control_plane_cli.py "set swing to 0.7"          # Set swing ratio (0.0-1.0)
python control_plane_cli.py "set accent to 25"          # Set accent amount (0-50)
python control_plane_cli.py "set humanize timing to 0.3" # Set timing humanization (0.0-1.0)
python control_plane_cli.py "set humanize velocity to 0.4" # Set velocity humanization (0.0-1.0)

# Style presets (tested and working)
python control_plane_cli.py "set style to jazz"         # Apply jazz style preset
python control_plane_cli.py "make it classical"         # Apply classical style
python control_plane_cli.py "set style to electronic"   # Apply electronic style
python control_plane_cli.py "set style to blues"        # Apply blues style
python control_plane_cli.py "set style to straight"     # Apply straight (no effects) style

# OSC control (tested and working)
python control_plane_cli.py "set osc enabled to on"     # Enable OSC control
python control_plane_cli.py "set osc port to 3819"      # Set OSC port
python control_plane_cli.py "reset osc"                 # Reset all parameters to defaults
```

### Configuration

Edit `config.py`:
- `MIDI_PORT_NAME` (default: `IAC Driver Bus 1`)
- `BPM` (default: 120)

### Troubleshooting

- **Port not found**: If you see a message listing available ports, ensure one is exactly `IAC Driver Bus 1`, then re‑run.
- **No sound but script runs**: In GarageBand, confirm the track is armed, monitoring is on, and an instrument is loaded. Watch input meters.
- **Wrong device**: If you use a different port name, change `MIDI_PORT_NAME` in `config.py`.
- **Backend not working**: Ensure `python-rtmidi` installed correctly (`pip show python-rtmidi`). Apple Silicon users should use native Python.
- **Latency**: This simple sequencer is blocking and sleep‑based; DAW buffer size and system load affect timing.

### How It Works

- `MidiPlayer`: opens a mido output port and sends note_on → sleep → note_off.
- `Sequencer`: stores notes as dicts with `start_beat` and `duration_beats`, converts beats to seconds using BPM, and schedules playback.
- `theory.create_major_scale(60)`: returns `[60, 62, 64, 65, 67, 69, 71, 72]`.
- `main.py`: wires components, schedules quarter notes of the C Major scale, and plays.

### Quality Assurance

**Comprehensive Validation System**: The project includes a robust quality gate system to ensure code quality and architectural integrity.

```bash
# Run the complete validation suite
./validate.sh
```

**What it checks:**
- ✅ **Code Quality & Style**: Flake8 linting with `.flake8` configuration (120 char lines, E501/W503 ignored)
- ✅ **Unit Tests**: Comprehensive test suite execution (45+ tests)
- ✅ **Architectural Purity**: Enhanced custom checks for "Brain vs. Hands" architecture
  - Enforces forbidden imports: `analysis.py` cannot import MIDI I/O, `midi_io.py` cannot import analysis
  - Validates pure functions in analysis.py (no side effects, no argument modification)
  - Prevents heavy dependencies in core modules
- ✅ **Integration Tests**: Main entry point functionality verification
- ✅ **Documentation Consistency**: Docstring and documentation checks
- ✅ **Dependencies**: Required package availability verification
- ✅ **File Structure**: Required files and project structure validation

**Developer Workflow:**
1. Make code changes
2. Run `./validate.sh` to check quality
3. Fix any issues found
4. Commit when all checks pass

### Next Steps

- **Try the control plane**: `python3 main.py --interactive`
- **Chat integration**: Use `python3 control_plane_cli.py "command"` in chat
- **Launch Ardour**: Use `./launch_ardour.sh` for easy Ardour startup with proper backend detection.
- **Explore the roadmap**: See [ROADMAP.md](ROADMAP.md) for the semantic MIDI editing vision
- **JUCE Plugin Development**: See [docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md) for real-time MIDI style transformations
- **OSC Integration**: See [OSC_INTEGRATION.md](OSC_INTEGRATION.md) for remote control capabilities

### Deep Dive Documentation

- [Setup](docs/SETUP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Usage](docs/USAGE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [GarageBand Setup](docs/GARAGEBAND_SETUP.md) — Complete guide for loading and using the Style Transfer plugin in GarageBand
- [Ardour Integration Setup](docs/ARDOUR_SETUP.md) — Ardour 8.9 now builds and launches successfully on macOS with internal YTK (SDK 14.x, arm64). Backend detection resolved.
- [JUCE Plugin Development](docs/JUCE_PLUGIN_DEVELOPMENT.md) — Real-time MIDI effect plugin for style transformations
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)


