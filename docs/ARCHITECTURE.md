## Architecture

### Overview
The project separates concerns into transport (MIDI I/O), scheduling (timing), theory helpers (content generation), and orchestration (entrypoint).

```
main.py → Sequencer → MidiPlayer → mido → OS MIDI → GarageBand
           ↑
        theory
```

### Modules and responsibilities
- `midi_player.py`
  - Opens a mido output port by name.
  - Sends `note_on`, waits, then `note_off`.
  - Handles failure by printing available ports.

- `sequencer.py`
  - Stores note events as dicts:
    - `pitch: int`, `velocity: int`, `start_beat: float`, `duration_beats: float`.
  - Converts beats to seconds with `seconds_per_beat = 60 / BPM`.
  - Sorts by `start_beat` and sleeps between events before triggering `MidiPlayer`.

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
- New content: add functions to `theory.py` (arpeggios, chords, rhythms).
- Alternate output: subclass or replace `MidiPlayer` (e.g., different backend or network MIDI).
- Advanced scheduling: add a non-blocking scheduler that overlaps notes, or quantization/latency compensation.


