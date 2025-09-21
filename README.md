## YesAnd Music: Semantic MIDI Editing

The goal of this project is to enable a musician to use a simple, natural language command like **"Make the bass beat from measures 8-12 jazzier"** to intelligently edit their music.

## The Solution

To achieve this, YesAnd Music is composed of two primary systems:

### Part 1: The Real-Time Control Plane (Live/Generative)
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

### Part 2: The Semantic Editor (Offline/Editorial) ✅ PHASE 1 COMPLETE
A tool for intelligent, offline music editing of existing MIDI files from a DAW. Phase 1 MVP is now complete and functional.

**Phase 1 Features (✅ Complete):**
- Command-line MIDI editor: `python edit.py --input song.mid --output swung.mid --command "apply_swing"`
- Swing transformation: Apply swing feel to off-beat notes
- MIDI file I/O: Load and save MIDI files using universal note format
- Constraint handling: Automatic sorting and overlap resolution for MIDI format compliance
- Comprehensive testing plan: Step-by-step validation workflow

**Phase 2+ Features (Planned):**
- "Make the bass beat from measures 8-12 jazzier" - Intelligent musical modifications
- Deep musical analysis - Understand bass lines, chord progressions, rhythmic patterns
- DAW integration - Read existing MIDI, analyze, modify, and write back
- Style transformations - Apply musical concepts like "jazzier", "simpler", "more aggressive"
- Context-aware editing - Preserve musical relationships while making changes

## The Architecture

Our architectural philosophy is to separate the core intelligence from the DAW integration.

**The "Brain"** is a standalone Python application that handles all musical analysis and transformation. It takes a MIDI file as input and produces a new MIDI file as output.

**The "Hands"** are the simple integration points that get MIDI data to and from the DAW.

This separation allows us to:
- Focus on musical intelligence without being constrained by DAW-specific APIs
- Test and develop the core functionality independently
- Support multiple DAWs through simple integration points
- Maintain real-time safety and performance standards

## The Roadmap

Our development is focused on de-risking the biggest challenges first.

### Phase 1: The "Manual Roundtrip" MVP ✅ COMPLETE
Built the core "Brain" and proved the end-to-end editing loop works via a simple command-line interface.
- ✅ Enhanced MIDI file I/O for DAW integration
- ✅ Basic musical analysis functions (swing transformation)
- ✅ Simple command-line interface for testing transformations
- ✅ Proof of concept for the full editing workflow
- ✅ MIDI format constraint handling (sorting, overlaps)
- ✅ Comprehensive testing plan and validation

### Phase 2: The Analysis Engine
Teach the "Brain" to identify musical concepts like "bass lines" and "chords" within a MIDI file.
- Bass line analysis and pattern recognition
- Chord progression analysis and harmonic understanding
- Rhythmic pattern analysis (swing, syncopation, groove)
- Musical context understanding and element relationships

### Phase 3: The Semantic Layer
Build the full natural language parser and a simple "Controller" plugin for a seamless user experience.
- Extended command parser for complex musical modifications
- Style transformation engine with context preservation
- Real-time DAW integration with OSC communication
- Complete natural language interface for musicians

## Quick Start: Phase 1 MVP (Semantic MIDI Editor)

The Phase 1 MVP is complete and ready for use. Here's how to get started:

### Semantic MIDI Editor (Phase 1)
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
- ✅ **Code Quality & Style**: Flake8 linting with critical error detection
- ✅ **Unit Tests**: Comprehensive test suite execution (45+ tests)
- ✅ **Architectural Purity**: Custom checks for "Brain vs. Hands" architecture
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
- [Ardour Integration Setup](docs/ARDOUR_SETUP.md) — Ardour 8.9 now builds and launches successfully on macOS with internal YTK (SDK 14.x, arm64). Backend detection resolved.
- [JUCE Plugin Development](docs/JUCE_PLUGIN_DEVELOPMENT.md) — Real-time MIDI effect plugin for style transformations
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)


