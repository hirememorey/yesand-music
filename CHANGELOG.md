## Changelog

This project follows a lightweight semantic versioning approach (MAJOR.MINOR.PATCH).

### [Unreleased]
#### Added
- Control plane design doc: `docs/CONTROL_PLANE.md` (layered approach, manifest spec, intents).
- README section introducing the chat-driven control plane vision.
- Architecture updates outlining planned control plane components.
- Usage, Setup, Troubleshooting, and Contributing updated with control plane notes.
- Ardour build & integration guide: `docs/ARDOUR_SETUP.md` (proven macOS build path: internal YTK, SDKROOT pinned to 14.x, alias/visibility flags, arm64; logs and launch instructions).
- **Ardour launch success**: Resolved "No audio/MIDI backends detected" error by setting `ARDOUR_BACKEND_PATH` to specific subdirectories (`coreaudio` and `dummy`). Ardour now launches with full CoreAudio and MIDI device detection.
- OSC integration testing: Verified `oscsend` commands work; documented OSC enablement steps in Ardour preferences.
#### Changed
- `docs/ARDOUR_SETUP.md`: Replaced `--no-ytk` external GTK route with the successful internal YTK path on macOS. Documented clean configure with `env - i`, `--keepflags`, `CFLAGS/CXXFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY"`, SDKROOT=14.x, deployment target 11.0, and proof gates ("Use YTK instead of GTK: True"). Added artifact locations and run commands.
- `docs/ARDOUR_SETUP.md`: Added working launch command with correct environment variables and backend path configuration. Documented OSC integration steps and testing commands.

### [0.1.0] - 2025-09-06
#### Added
- Initial modular framework: `midi_player.py`, `sequencer.py`, `theory.py`, `config.py`, `main.py`.
- Demo playing C Major scale via IAC into GarageBand.
- Documentation: README, Setup, Architecture, Usage, Troubleshooting, Contributing, Changelog.


