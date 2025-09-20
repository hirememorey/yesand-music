## Changelog

This project follows a lightweight semantic versioning approach (MAJOR.MINOR.PATCH).

### [Unreleased]
#### Python OSC Integration (Phase A: Complete)
- **OSC Sender Implementation**: Created complete `OSCSender` class for Python-to-JUCE plugin communication
  - Thread-safe design for non-real-time thread usage
  - Automatic parameter validation and clamping
  - Connection management with automatic reconnection
  - Comprehensive error handling and logging
- **Natural Language OSC Commands**: Added 8 new command types for style parameter control via OSC
  - `set swing to [0-1]` - Control swing ratio
  - `set accent to [0-50]` - Control accent amount
  - `set humanize timing to [0-1]` - Control timing humanization
  - `set humanize velocity to [0-1]` - Control velocity humanization
  - `set osc enabled to [on/off]` - Enable/disable OSC control
  - `set osc port to [PORT]` - Set OSC port
  - `set style to [PRESET]` - Apply style presets
  - `reset osc` - Reset all parameters to defaults
- **Style Preset System**: Implemented built-in presets (jazz, classical, electronic, blues, straight)
  - Each preset configures multiple parameters for coherent musical styles
  - Easy to extend with new presets
  - Natural language access via "make it jazzier" commands
- **Control Plane Integration**: Seamless integration of OSC commands with existing MIDI control
  - Unified command interface for both MIDI and OSC operations
  - Combined MIDI playback with real-time style control
  - Error isolation - OSC failures don't affect MIDI functionality
- **Dependencies**: Added `python-osc>=1.7.4` to requirements.txt
- **Configuration**: Added OSC settings to config.py (IP, port, message addresses)
- **Testing**: Created comprehensive test suite and demo scripts
  - `test_osc_sender.py` - OSC functionality validation
  - `demo_osc_integration.py` - Complete feature demonstration
- **Documentation**: Updated all documentation to reflect OSC integration capabilities

#### Vision & Roadmap
- **Semantic MIDI Editing Vision**: Updated project vision to enable natural language commands like "make the bass beat from measures 8-12 jazzier"
- **Comprehensive Roadmap**: Created detailed implementation plan across 5 phases for semantic MIDI editing
- **Enhanced Documentation**: Updated all markdown files to reflect the new vision and technical architecture
- **Ardour-Focused Development**: Shifted primary target from GarageBand to Ardour for deeper integration capabilities
- **JUCE Plugin Development**: Initiated development of real-time MIDI effect plugin for style transformations

#### JUCE Plugin OSC Integration (Phase A: Complete)
- **OSC Dependency Integration**: Added liblo (Lightweight OSC) library for real-time safe remote control
- **Thread-Safe Architecture**: Implemented FIFO queue pattern for non-real-time OSC message processing
- **Timer-Based Processing**: Added 30 Hz timer callback for safe OSC message processing
- **Parameter Control**: Added OSC control for swing ratio, accent amount, humanization parameters, and OSC enable/port settings
- **Real-Time Safety**: Ensured OSC operations never interfere with audio thread processing
- **DAW Integration**: Implemented setParameterNotifyingHost() for proper DAW and UI updates
- **Plugin Structure**: Created complete JUCE plugin with CMakeLists.txt, PluginProcessor, and PluginEditor
- **Documentation**: Added comprehensive OSC_INTEGRATION.md with usage examples and troubleshooting
- **Test Scripts**: Created Python test script for OSC message validation

#### Critical Real-Time Safety Guidelines
- **Real-Time Safety Documentation**: Added comprehensive guidelines for JUCE plugin development to prevent common audio thread bugs
- **Velocity Preservation Pattern**: Documented the critical difference between overwriting vs. modifying velocity to preserve human musical expression
- **Parameter Management Best Practices**: Added AudioProcessorValueTreeState guidelines to prevent thread-safety crashes
- **Common Bug Prevention**: Documented the most destructive real-time audio bugs and their prevention strategies

#### JUCE Plugin Development
- **Style Transfer Plugin**: Created JUCE-based MIDI effect plugin for real-time style transformations
- **Real-Time Safety**: Implemented real-time safe MIDI processing with no memory allocation or blocking calls
- **Swing Transformation**: Added swing feel transformation for off-beat note timing adjustment
- **Accent Transformation**: Added down-beat velocity enhancement for musical emphasis
- **Humanization Feature**: Added subtle timing and velocity variations for authentic human feel
  - Timing humanization: ±5ms maximum variation for natural timing feel
  - Velocity humanization: ±10 units maximum variation for natural dynamics
  - Critical velocity preservation: Modifies original values, never overwrites
  - Real-time safe random number generation with pre-seeded Random generator
- **Modular Architecture**: Refactored into pure transformation functions for testability and extensibility
- **Plugin Architecture**: Designed modular architecture supporting VST3 and AudioUnit formats
- **Documentation**: Created comprehensive documentation for JUCE plugin development approach

#### Added
- **Data Core Foundation**: Created universal MIDI data structures for semantic MIDI editing
  - **`midi_io.py`**: Pure Python MIDI file I/O using lightweight mido library
    - `parse_midi_file()`: Converts MIDI files to universal note dictionary format
    - `save_midi_file()`: Saves note dictionaries back to MIDI files
    - Universal data structure: `{'pitch': int, 'velocity': int, 'start_time_seconds': float, 'duration_seconds': float, 'track_index': int}`
    - No heavy dependencies - avoids "Black Box Dependency Problem"
    - Comprehensive validation and error handling
  - **`project.py`**: Clean Project class for musical data management
    - `Project` class as container for musical data and metadata
    - `load_from_midi()` and `save_to_midi()` methods using midi_io functions
    - Query methods: `get_notes_by_track()`, `get_notes_in_time_range()`, `get_duration()`
    - Separation of concerns - pure data management without musical analysis logic
    - Prevents "Spaghetti Code Problem" through clean, focused design
  - **`analysis.py`**: Musical analysis and transformation functions
    - `filter_notes_by_pitch()`: Filter notes by pitch range for bass line analysis
    - `apply_swing()`: Apply swing feel by delaying off-beat notes
    - Pure functions with no side effects - avoids "Spaghetti Code Problem"
    - Foundation for semantic MIDI editing transformations
    - Testable in isolation - each function can be tested independently
- **Complete Control Plane Implementation**: Full chat-driven MIDI control system with natural language commands
  - Command parser with regex patterns for all major command types
  - Session state management with persistent file-based storage
  - Pattern engine supporting scales, arpeggios, and random note generation
  - **Non-blocking sequencer with timer-based note-off events** (critical fix for real-time performance)
  - CLI interface ready for chat integration (`control_plane_cli.py`)
  - Interactive mode in main.py (`python main.py --interactive`)
  - Comprehensive test suite with mocked MIDI components
  - **Implementation verification script** (`verify_implementation.py`) for end-to-end testing
- **Extended Music Theory**: Added support for all major modes, chord types, arpeggios, and rhythmic patterns
- **Advanced Pattern Generation**: Density control, randomness application, and configurable note timing
- **Control Commands**: CC messages, modulation wheel, tempo, key, density, and randomness controls
- **Session Persistence**: State survives between commands with atomic file updates
- **Multiple Entry Points**: Original demo, interactive mode, CLI, and chat integration ready
- **ROADMAP.md**: Comprehensive implementation plan for semantic MIDI editing across 5 phases

#### Fixed
- **Critical: Non-blocking MIDI Playback**: Fixed blocking issue where `MidiPlayer.send_note()` used `time.sleep()` preventing real-time operation. Now uses timer-based note-off events for truly non-blocking playback.
- **CC Command Execution**: Fixed mido import issue in control commands (CC and modulation wheel now work correctly).
- **Ardour panner plugin discovery**: Resolved "No panner found" fatal error by adding the missing `ARDOUR_PANNER_PATH` environment variable. Ardour uses a dedicated `ARDOUR_PANNER_PATH` variable (not just `ARDOUR_DLL_PATH`) to discover panner plugins. The launch script now correctly sets both variables for complete plugin discovery.
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


