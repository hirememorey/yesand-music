## Troubleshooting

Work through these checks in order; stop when the issue is resolved.

### 1) Verify the MIDI port exists
```bash
python - <<'PY'
import mido
print('\n'.join(mido.get_output_names()))
PY
```
Expected: `IAC Driver Bus 1` listed (or your configured name). If missing:
- Enable IAC Driver and create the port (see docs/SETUP.md).
- Restart GarageBand and re-run the command.

### 2) Confirm the script opens the correct port
Run:
```bash
python3 main.py
```
If it prints an error with available ports, update `MIDI_PORT_NAME` in `config.py`.

### 3) GarageBand receives but no sound
- Track must be record‑armed and input monitoring enabled.
- Ensure a software instrument is loaded (not an audio track).
- Check that instrument volume and master volume are up, and no mute/solo conflict.

### 4) No meters, still silent
- In GarageBand Preferences → Audio/MIDI, confirm MIDI input is active.
- Try creating a new empty project and adding a fresh Software Instrument track.
- Reboot GarageBand after changing IAC settings.

### 5) Backend or install issues
- Confirm dependencies:
  ```bash
  pip show mido python-rtmidi
  ```
- On Apple Silicon, ensure you use a native Python (not Rosetta) matching your wheels.
- If `python-rtmidi` fails to import, reinstall it and verify your Python version.

### 6) Timing / latency / jitter
- This demo uses a blocking `time.sleep` scheduler; small drift is expected.
- Reduce DAW buffer size (with care) and minimize system load to improve responsiveness.

### 7) Alternative DAWs / OS
- If using another DAW, ensure the track input source is the virtual MIDI port and the track is armed.
- Windows: create a virtual port with loopMIDI and set `MIDI_PORT_NAME` accordingly.
- Linux: use ALSA/JACK virtual MIDI; verify with `mido.get_output_names()`.


