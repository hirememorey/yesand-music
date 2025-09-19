## Changelog

This project follows a lightweight semantic versioning approach (MAJOR.MINOR.PATCH).

### [Unreleased]
#### Fixed
- **Ardour panner plugin discovery**: Resolved "No panner found" fatal error by adding the missing `ARDOUR_PANNER_PATH` environment variable. Ardour uses a dedicated `ARDOUR_PANNER_PATH` variable (not just `ARDOUR_DLL_PATH`) to discover panner plugins. The launch script now correctly sets both variables for complete plugin discovery.

#### Added
- Control plane design doc: `docs/CONTROL_PLANE.md` (layered approach, manifest spec, intents).
- README section introducing the chat-driven control plane vision.
- Architecture updates outlining planned control plane components.
- Usage, Setup, Troubleshooting, and Contributing updated with control plane notes.
- Ardour build & integration guide: `docs/ARDOUR_SETUP.md` (proven macOS build path: internal YTK, SDKROOT pinned to 14.x, alias/visibility flags, arm64; logs and launch instructions).
- **Ardour launch success**: Resolved fatal startup errors ("No panner found", Gtk theme engine failures, missing keybindings) by creating a robust, evidence-based launch script (`launch_ardour.sh`) that correctly orchestrates all of Ardour's interacting sub-systems.
- OSC integration testing: Verified `oscsend` commands work; documented OSC enablement steps in Ardour preferences.
#### Changed
- `docs/ARDOUR_SETUP.md`: Replaced `--no-ytk` external GTK route with the successful internal YTK path on macOS. Documented clean configure with `env - i`, `--keepflags`, `CFLAGS/CXXFLAGS="-DNO_SYMBOL_RENAMING -DNO_SYMBOL_EXPORT -DDISABLE_VISIBILITY"`, SDKROOT=14.x, deployment target 11.0, and proof gates ("Use YTK instead of GTK: True"). Added artifact locations and run commands.
- `docs/ARDOUR_SETUP.md`: Overhauled the launch section with a detailed explanation of the multi-system environment (Ardour vs. GTK), the need for pre-flight configuration, and the construction of exhaustive, non-recursive search paths for data and plugins.
- `launch_ardour.sh`: The script is now a definitive system orchestrator that correctly sets up the GTK, Ardour Data, and Ardour DLL environments for a stable launch.
- `docs/TROUBLESHOOTING.md`: Added a new section for diagnosing common Ardour launch failures, explaining the root cause of each and pointing to the correct solution.

### [0.1.0] - 2025-09-06
#### Added
- Initial modular framework: `midi_player.py`, `sequencer.py`, `theory.py`, `config.py`, `main.py`.
- Demo playing C Major scale via IAC into GarageBand.
- Documentation: README, Setup, Architecture, Usage, Troubleshooting, Contributing, Changelog.


