## MIDI Sequencing to GarageBand (macOS)

Generate MIDI in Python and play it in real time through a virtual MIDI port into GarageBand.

### New: Chat-driven control plane (vision)
- Use Cursor chat as a live control surface for GarageBand. Send natural-language commands to generate patterns, tweak dynamics, and modulate instruments via MIDI, embracing nondeterminism over tight sync.
- Start with a simple baseline (user arms a target track; we send MIDI via IAC). Optionally add a small project manifest and best-effort UI reading for track names.
- See: [Control Plane](docs/CONTROL_PLANE.md)

### What this is
- **Goal**: Minimal, modular framework for generating MIDI and scheduling playback.
- **Modules**: `midi_player.py` (I/O), `sequencer.py` (timing), `theory.py` (scales), `main.py` (demo), `config.py` (settings).
- **Platform focus**: macOS with IAC Driver and GarageBand. Others may work with minor changes.

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
python3 main.py
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

### Next steps
- Change tempo or port in `config.py` and re‑run.
- Add notes via `Sequencer.add_note()` or build new patterns in `theory.py`.
- Explore deeper docs:
  - [Setup](docs/SETUP.md)
  - [Architecture](docs/ARCHITECTURE.md)
  - [Usage](docs/USAGE.md)
  - [Troubleshooting](docs/TROUBLESHOOTING.md)
  - [Ardour Integration Setup](docs/ARDOUR_SETUP.md) — Phase 1 complete; start at "Continue here" for Phase 2 (clean reconfigure with `--no-ytk`).
  - [Contributing](CONTRIBUTING.md)
  - [Changelog](CHANGELOG.md)


