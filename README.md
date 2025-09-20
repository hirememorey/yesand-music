## Music Cursor: Semantic MIDI Editing for Ardour

A sophisticated Python framework for **natural language control of music creation and editing** in Ardour. Generate MIDI patterns, analyze existing music, and make intelligent modifications through chat commands.

### Current: Chat-driven MIDI control (implemented!)
- **Interactive MIDI control via natural language commands**. Send commands to generate patterns, tweak dynamics, and modulate instruments via MIDI, embracing nondeterminism over tight sync.
- **Real-time session state management** with persistent storage across commands.
- **Multiple pattern types**: scales, arpeggios, random notes with configurable density and randomness.
- **Control commands**: CC messages, modulation wheel, tempo, key, and more.
- **CLI interface** ready for chat integration: `python control_plane_cli.py "play scale D minor"`
- **JUCE Plugin Development**: Real-time MIDI effect plugin with swing, accent, and humanization transformations
- **OSC Integration**: Complete timer-based OSC receiver for real-time parameter control with DAW integration
- See: [Control Plane](docs/CONTROL_PLANE.md)

### Vision: Semantic MIDI Editing (roadmap)
- **"Make the bass beat from measures 8-12 jazzier"** - Intelligent musical modifications
- **Deep musical analysis** - Understand bass lines, chord progressions, rhythmic patterns
- **Ardour integration** - Read existing MIDI, analyze, modify, and write back
- **Style transformations** - Apply musical concepts like "jazzier", "simpler", "more aggressive"
- **Context-aware editing** - Preserve musical relationships while making changes

### What this is
- **Goal**: Semantic MIDI editing framework for intelligent music creation and modification.
- **Data Core**: `midi_io.py` (universal MIDI I/O), `project.py` (musical data container) - foundation for semantic editing
- **Core Modules**: `midi_player.py` (I/O), `sequencer.py` (timing), `theory.py` (music theory), `commands/` (control plane).
- **Platform focus**: macOS with Ardour integration. IAC Driver support for GarageBand compatibility.
- **Architecture**: Modular design supporting both real-time control and deep musical analysis.

### Quickstart (time-to-first-note)
1) Create and activate a virtualenv
```bash
cd "/Users/harrisgordon/Documents/Development/Python/not_sports/music_cursor"
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip3 install --upgrade pip setuptools wheel
pip3 install mido python-rtmidi
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

### Inline troubleshooting (top 5)
- **Port not found**: If you see a message listing available ports, ensure one is exactly `IAC Driver Bus 1`, then re‑run.
- **No sound but script runs**: In GarageBand, confirm the track is armed, monitoring is on, and an instrument is loaded. Watch input meters.
- **Wrong device**: If you use a different port name, change `MIDI_PORT_NAME` in `config.py`.
- **Backend not working**: Ensure `python-rtmidi` installed correctly (`pip show python-rtmidi`). Apple Silicon users should use native Python.
- **Latency**: This simple sequencer is blocking and sleep‑based; DAW buffer size and system load affect timing.

### Configure
Edit `config.py`:
- `MIDI_PORT_NAME` (default: `IAC Driver Bus 1`)
- `BPM` (default: 120)

### How it works
- `MidiPlayer`: opens a mido output port and sends note_on → sleep → note_off.
- `Sequencer`: stores notes as dicts with `start_beat` and `duration_beats`, converts beats to seconds using BPM, and schedules playback.
- `theory.create_major_scale(60)`: returns `[60, 62, 64, 65, 67, 69, 71, 72]`.
- `main.py`: wires components, schedules quarter notes of the C Major scale, and plays.

### Control Plane Commands
```bash
# Interactive mode
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

### Next steps
- **Try the control plane**: `python3 main.py --interactive`
- **Chat integration**: Use `python3 control_plane_cli.py "command"` in chat
- **Launch Ardour**: Use `./launch_ardour.sh` for easy Ardour startup with proper backend detection.
- **Explore the roadmap**: See [ROADMAP.md](ROADMAP.md) for the semantic MIDI editing vision
- **JUCE Plugin Development**: See [docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md) for real-time MIDI style transformations
- **OSC Integration**: See [OSC_INTEGRATION.md](OSC_INTEGRATION.md) for remote control capabilities
- **Deep dive docs**:
  - [Setup](docs/SETUP.md)
  - [Architecture](docs/ARCHITECTURE.md)
  - [Usage](docs/USAGE.md)
  - [Troubleshooting](docs/TROUBLESHOOTING.md)
  - [Ardour Integration Setup](docs/ARDOUR_SETUP.md) — Ardour 8.9 now builds and launches successfully on macOS with internal YTK (SDK 14.x, arm64). Backend detection resolved.
  - [JUCE Plugin Development](docs/JUCE_PLUGIN_DEVELOPMENT.md) — Real-time MIDI effect plugin for style transformations
  - [Contributing](CONTRIBUTING.md)
  - [Changelog](CHANGELOG.md)


