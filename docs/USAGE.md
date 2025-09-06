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


