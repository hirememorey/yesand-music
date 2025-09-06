## Architecture

### Overview
The project separates concerns into transport (MIDI I/O), scheduling (timing), theory helpers (content generation), and orchestration (entrypoint).

```
main.py → Sequencer → MidiPlayer → mido → OS MIDI → GarageBand
           ↑
        theory
```

### Planned: Chat-driven control plane
- High-level components:
  - Intent parser: converts chat text into structured commands (play/pattern/cc/settings/target/stop).
  - Session state: key/scale, density, register, velocity profile, randomness.
  - Manifest loader (optional): reads `project.yaml`/`project.json` describing parts and CC aliases.
  - Optional UI reader (macOS-only): best-effort read of track names and armed/selected state; feature-flagged.
  - MIDI dispatcher: maps intents to patterns/CCs and sends via `MidiPlayer` to the armed track.
- See: `docs/CONTROL_PLANE.md` for the layered design and risks.

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


