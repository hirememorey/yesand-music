## Setup (macOS + GarageBand)

Follow these steps to enable a virtual MIDI port and get GarageBand receiving input.

### 1) Enable IAC Driver and create the port
1. Open Audio MIDI Setup (Spotlight → "Audio MIDI Setup").
2. Window → Show MIDI Studio.
3. Double‑click IAC Driver → check "Device is online".
4. In Ports, create or rename a port to: `IAC Driver Bus 1`.

Verification:
```bash
python - <<'PY'
import mido
print('\n'.join(mido.get_output_names()))
PY
```
You should see `IAC Driver Bus 1` in the list.

### 2) Prepare GarageBand to receive MIDI
1. Create a Software Instrument track.
2. Arm the track for recording.
3. Enable input monitoring.
4. Load any software instrument patch.

Verification:
- When the Python script runs later, you should see the instrument track input meter move.

### 3) Set up Python environment
```bash
cd "/Users/harrisgordon/Documents/Development/Python/not_sports/music_cursor"
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip setuptools wheel
pip3 install mido python-rtmidi
```

### 4) Configure (optional)
Edit `config.py` if your port name or tempo differ:
- `MIDI_PORT_NAME = "IAC Driver Bus 1"`
- `BPM = 120`

### 5) Run and test
```bash
python3 main.py
```
Expected: Terminal prints "Playing C Major Scale..." and GarageBand plays 8 notes.

### Other platforms / DAWs
- Logic Pro: identical IAC setup; ensure the track is record‑enabled and monitoring.
- Ableton Live: set track input from IAC port and arm the track.
- Windows: use loopMIDI (create a virtual port) and set `MIDI_PORT_NAME` accordingly.
- Linux: use ALSA/JACK virtual MIDI ports; confirm with `mido.get_output_names()`.


