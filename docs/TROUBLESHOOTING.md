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

### 7) Control plane automation issues (optional features)
- UI reading fails or is inconsistent:
  - Verify Accessibility permissions in System Settings → Privacy & Security → Accessibility.
  - GarageBand UI labels may vary; the feature is optional and will auto-disable on failure.
- Project manifest not applied:
  - Ensure `project.yaml` or `project.json` is in the project root and valid YAML/JSON.
  - Fall back to the armed-track baseline; target selection via manual arming still works.
- Audio-derived key suggestions missing:
  - Install and route via a loopback device (e.g., BlackHole) and retry the command.
  - This feature is off by default and is only advisory.

### 8) Alternative DAWs / OS
- If using another DAW, ensure the track input source is the virtual MIDI port and the track is armed.
- Windows: create a virtual port with loopMIDI and set `MIDI_PORT_NAME` accordingly.
- Linux: use ALSA/JACK virtual MIDI; verify with `mido.get_output_names()`.

### 9) Ardour crashes on launch (macOS build)

Launching a self-built Ardour instance is complex. The application is a system of interacting components that must all be configured correctly. Refer to `docs/ARDOUR_SETUP.md` for the full explanation and the correct launch script.

Common fatal errors and their root causes:

- **`Gtk-WARNING **: Unable to locate theme engine in module_path: "clearlooks"`**:
  - **Symptom**: The GTK UI framework cannot find the library needed to render its theme.
  - **Solution**: The `GTK_PATH` environment variable must point to the directory containing `libclearlooks.dylib`.

- **`Ardour - : Fatal Error | No panner found`**:
  - **Symptom**: Ardour cannot find its critical internal plugins for audio panning.
  - **Solution**: The `ARDOUR_DLL_PATH` environment variable is not just a single path; it must be an **exhaustive, colon-separated list of every single subdirectory** where a plugin (`.dylib`) is located. It is not recursive.

- **`[ERROR]: Default keybindings not found` or `Invalid symbolic color 'bases'`**:
  - **Symptom**: Ardour crashes late in startup because it can't find essential resources like keymaps, fonts, or color definitions.
  - **Solution**: This is a two-part problem. First, Ardour has a pre-flight check and expects some files (`ardour.keys`, `ardour.menus`) to be present in its config directory (`~/Library/Preferences/Ardour8`) before launch. Second, the `ARDOUR_DATA_PATH` must be a composite path that points to *both* the build artifacts in the `build` tree and source assets (like fonts) in the source tree.

The `./launch_ardour.sh` script is designed to handle all of these cases correctly.


