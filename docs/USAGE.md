## Usage

### Configure
Edit `config.py`:
- `MIDI_PORT_NAME`: must match your virtual MIDI port name (default: `IAC Driver Bus 1`).
- `BPM`: beats per minute used for beat→seconds conversion.

### Run the demo
```bash
source .venv/bin/activate
python3 main.py
```
Expected: "Playing C Major Scale..." and an 8‑note C Major scale in GarageBand.

### Chat-driven control plane (implemented!)
- **Interactive natural language MIDI control** via Cursor chat or command line.
- **Real-time session management** with persistent state across commands.
- **Multiple pattern types**: scales, arpeggios, random notes with configurable density and randomness.
- **Control commands**: CC messages, modulation wheel, tempo, key, and more.

#### Usage Examples
```bash
# Interactive mode
python main.py --interactive

# CLI for chat integration  
python control_plane_cli.py "play scale D minor"
python control_plane_cli.py "set tempo to 140"
python control_plane_cli.py "play arp C major"
```

#### Available Commands
- `play scale [KEY] [MODE]` - Play scales in any key/mode
- `play arp [KEY] [CHORD]` - Play arpeggios  
- `play random [COUNT]` - Play random notes
- `set key to [KEY] [MODE]` - Change session key
- `set tempo to [BPM]` - Change tempo
- `set density to [low|med|high]` - Change note density
- `set randomness to [0-1]` - Add randomness
- `cc [NUMBER] to [VALUE]` - Send control changes
- `mod wheel [VALUE]` - Send modulation wheel
- `status` - Show current state
- `stop` - Stop playback
- `help` - Show all commands

#### Chat Integration
- Use `python control_plane_cli.py "command"` in Cursor chat
- Commands execute immediately and return status
- Session state persists between chat interactions
- See details and examples: `docs/CONTROL_PLANE.md`.

### Add notes programmatically
Inside `main.py` or your own script:
```python
# Assume midi_player and seq already created
seq.add_note(pitch=60, velocity=90, start_beat=0.0, duration_beats=1.0)
seq.add_note(pitch=64, velocity=90, start_beat=1.0, duration_beats=1.0)
seq.play()
```

Note event schema stored by `Sequencer`:
- `pitch: int` (0–127)
- `velocity: int` (0–127)
- `start_beat: float`
- `duration_beats: float`

### Use theory helpers
```python
from theory import create_major_scale
scale = create_major_scale(60)  # C4
for i, note in enumerate(scale):
    seq.add_note(pitch=note, velocity=90, start_beat=float(i), duration_beats=1.0)
```

### Common workflows
- Change tempo: set `BPM` in `config.py`.
- Change output port: set `MIDI_PORT_NAME` in `config.py` to match your IAC/virtual port.
- Change instrument: select a different software instrument in GarageBand.
- Adjust dynamics: modify `velocity` values (higher = louder).

### Extending the framework
- New scales/chords: add functions to `theory.py` that return MIDI note lists.
- New patterns: generate sequences of note dicts and feed them to `Sequencer`.
- Alternative backends: swap `MidiPlayer` implementation if you need another mido backend or network MIDI.


