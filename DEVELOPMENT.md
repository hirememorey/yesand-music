# Development Guide

Everything you need to know to develop YesAnd Music.

## Current State

**Phase 3B Complete**: Musical problem solvers working  
**Next Phase**: Phase 3C - Advanced LLM integration

## Development Setup

### Prerequisites
- macOS (tested on macOS 15.5)
- Python 3.8+
- Xcode Command Line Tools
- CMake 3.31.7+

### Environment Setup
```bash
# Clone and setup
git clone <repository>
cd music_cursor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Verify setup
python control_plane_cli.py status
```

### MIDI Setup
```bash
# Enable IAC Driver in Audio MIDI Setup
# Create port named "IAC Driver Bus 1"
python -c "import mido; print('Ports:', mido.get_output_names())"
```

## Project Structure

```
music_cursor/
├── commands/           # Control plane system
│   ├── control_plane.py    # Main orchestrator
│   ├── parser.py          # Command parsing
│   ├── pattern_engine.py  # Musical pattern generation
│   └── session.py         # State management
├── contextual_intelligence.py  # Musical analysis engine
├── visual_feedback_display.py  # Visual feedback system
├── musical_solvers.py    # Problem-solving algorithms
├── midi_io.py           # MIDI file I/O
├── project.py           # Project data management
├── analysis.py          # Musical analysis functions
├── theory.py            # Music theory helpers
├── osc_sender.py        # OSC communication
├── main.py              # Entry point
├── control_plane_cli.py # CLI interface
└── tests/               # Test suite
```

## Key Components

### Control Plane (`commands/`)
- **control_plane.py**: Main orchestrator, handles all commands
- **parser.py**: Natural language command parsing with regex patterns
- **pattern_engine.py**: Generates musical patterns from commands
- **session.py**: Persistent state management

### Musical Intelligence
- **contextual_intelligence.py**: Core analysis engine for musical elements
- **musical_solvers.py**: Problem-solving algorithms (groove, harmony, arrangement)
- **analysis.py**: Pure functions for musical analysis and transformation
- **theory.py**: Music theory helpers and generators

### MIDI Processing
- **midi_io.py**: Universal MIDI file I/O with consistent data format
- **project.py**: Project data management and querying
- **midi_player.py**: Real-time MIDI output
- **sequencer.py**: Non-blocking MIDI playback

### Visual Feedback
- **visual_feedback_display.py**: Color-coded visual feedback system
- **osc_sender.py**: Python-to-JUCE plugin communication

## Common Development Tasks

### Adding a New Command

1. **Add command type** in `commands/types.py`:
```python
class CommandType(Enum):
    # ... existing types ...
    NEW_COMMAND = "new_command"
```

2. **Add regex patterns** in `commands/parser.py`:
```python
CommandType.NEW_COMMAND: [
    r"new\s+command",
    r"do\s+something",
],
```

3. **Add parameter extraction** in `commands/parser.py`:
```python
elif cmd_type == CommandType.NEW_COMMAND:
    # Extract parameters if needed
    pass
```

4. **Add command handling** in `commands/control_plane.py`:
```python
elif command.type == CommandType.NEW_COMMAND:
    # Implement command logic
    return "Command executed"
```

### Adding Musical Analysis

1. **Extend MusicalElement enum** in `contextual_intelligence.py`:
```python
class MusicalElement(Enum):
    # ... existing elements ...
    NEW_ELEMENT = "new_element"
```

2. **Implement analysis method**:
```python
def _analyze_new_element(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze new musical element."""
    # Implementation
    return analyzed_notes
```

3. **Add to analysis pipeline**:
```python
def _analyze_project(self) -> None:
    # ... existing analysis ...
    new_element_notes = self._analyze_new_element(notes)
```

### Adding Visual Feedback

1. **Extend VisualFeedbackType enum**:
```python
class VisualFeedbackType(Enum):
    # ... existing types ...
    NEW_FEEDBACK = "new_feedback"
```

2. **Implement feedback generation**:
```python
def _get_new_feedback(self) -> List[VisualFeedback]:
    """Get visual feedback for new element."""
    # Implementation
    return feedback_list
```

3. **Add to display system** in `visual_feedback_display.py`:
```python
def _display_feedback(self, feedback: VisualFeedback) -> None:
    # ... existing display logic ...
    if feedback.type == VisualFeedbackType.NEW_FEEDBACK:
        # New feedback display logic
```

## Testing

### Run All Tests
```bash
# Full test suite
python -m pytest tests/

# Specific test file
python -m pytest tests/test_control_plane.py

# With coverage
python -m pytest --cov=. tests/
```

### Manual Testing
```bash
# Test control plane
python control_plane_cli.py "play scale C major"
python control_plane_cli.py "analyze bass"

# Test musical solvers
python control_plane_cli.py "make this groove better"

# Test plugin
python test_plugin.py
```

### Integration Testing
```bash
# End-to-end verification
python verify_implementation.py

# Demo scripts
python demo_control_plane.py
python demo_contextual_intelligence.py
python demo_musical_solvers.py
```

## JUCE Plugin Development

### Build Plugin
```bash
# Build the plugin
make -C build_minimal
# or
./build_minimal.sh
```

### Plugin Location
- **AudioUnit**: `/Users/harrisgordon/Library/Audio/Plug-Ins/Components/Style Transfer.component`
- **VST3**: `/Users/harrisgordon/Library/Audio/Plug-Ins/VST3/Style Transfer.vst3`

### Key Files
- `StyleTransferAudioProcessor.cpp/h`: Main plugin logic
- `StyleTransferAudioProcessorEditor.cpp/h`: Plugin UI
- `CMakeLists.txt`: Build configuration

### Real-Time Safety
- **NEVER** allocate memory in `processBlock()`
- **NEVER** use locking mechanisms in audio thread
- **NEVER** make blocking calls in audio thread
- Use `AudioProcessorValueTreeState` for thread-safe parameter access

## Debugging

### Common Issues

**MIDI not working:**
```bash
# Check port availability
python -c "import mido; print(mido.get_output_names())"

# Check session state
python control_plane_cli.py status
```

**Plugin not loading:**
- Check installation paths
- Verify AudioUnit type configuration
- Check build logs in `build_minimal/`

**Commands not parsing:**
- Check regex patterns in `commands/parser.py`
- Verify command type enum values
- Test with simple commands first

### Debug Mode
```bash
# Enable debug output
export DEBUG=1
python control_plane_cli.py "your command"
```

## Performance Considerations

### Real-Time Safety
- Visual feedback runs in separate thread
- No blocking operations in audio-critical paths
- Background analysis doesn't interfere with MIDI playback

### Memory Management
- Visual feedback queue has size limits
- Analysis results are cached to avoid recomputation
- Old feedback is automatically cleaned up

### Thread Safety
- All visual feedback operations are thread-safe
- MIDI I/O operations are isolated from visual feedback
- Control plane operations are synchronized

## Code Quality

### Validation
```bash
# Run quality checks
./validate.sh
```

### Architecture Rules
- `analysis.py` cannot import MIDI I/O modules
- `midi_io.py` cannot import analysis modules
- Pure functions in `analysis.py` (no side effects)
- No heavy dependencies in core modules

### Testing Requirements
- Unit tests for all new functions
- Integration tests for new features
- Manual testing for user-facing changes
- Performance testing for real-time components

## Next Steps

### Phase 3C: Advanced LLM Integration
- LLM agent implementation
- Command orchestration system
- Reasoning and explanation engine
- DAW workflow integration

### Development Priorities
1. **LLM Integration**: Natural language understanding and orchestration
2. **Performance Optimization**: Real-time analysis and memory efficiency
3. **Multi-DAW Support**: Logic Pro, Pro Tools, Cubase integration
4. **Advanced Features**: Voice integration, collaborative features

## Getting Help

- **Architecture Questions**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Setup Issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Code Issues**: Check test suite and validation output
