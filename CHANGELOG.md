## Changelog

This project follows a lightweight semantic versioning approach (MAJOR.MINOR.PATCH).

### [Unreleased]
#### Added
- Control plane design doc: `docs/CONTROL_PLANE.md` (layered approach, manifest spec, intents).
- README section introducing the chat-driven control plane vision.
- Architecture updates outlining planned control plane components.
- Usage, Setup, Troubleshooting, and Contributing updated with control plane notes.
- Ardour build & integration guide: `docs/ARDOUR_SETUP.md` (MacPorts-based macOS build, dependency list, current blocker, and next steps).
#### Changed
- `docs/ARDOUR_SETUP.md`: Phase 1 completed. Installed GTK2/gtkmm 2.4 and `liblrdf` via MacPorts; verified via pkg-config. `suil` not in MacPorts and skipped for now. Updated Phase 2 instructions (clean env configure with `--no-ytk`) and status snapshot.

### [0.1.0] - 2025-09-06
#### Added
- Initial modular framework: `midi_player.py`, `sequencer.py`, `theory.py`, `config.py`, `main.py`.
- Demo playing C Major scale via IAC into GarageBand.
- Documentation: README, Setup, Architecture, Usage, Troubleshooting, Contributing, Changelog.


