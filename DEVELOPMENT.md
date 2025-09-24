# Development Guide

Complete guide for developing and contributing to YesAnd Music.

## Table of Contents

- [Current State](#current-state)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Key Components](#key-components)
- [Common Development Tasks](#common-development-tasks)
- [Testing](#testing)
- [JUCE Plugin Development](#juce-plugin-development)
- [Performance Considerations](#performance-considerations)
- [Code Quality](#code-quality)
- [Contributing](#contributing)

---

## Current State

**✅ Production Ready Features:**
- Live MIDI streaming to Ardour
- Musical conversation system with OpenAI integration
- Context-aware Musical Scribe architecture
- Comprehensive musical problem solvers
- File-based DAW integration
- Real-time MIDI editing capabilities

**🎯 CRITICAL PRIORITY: Musical Quality-First Implementation**

**The Problem**: Current system can generate MIDI patterns, but musical quality is often mediocre. Users abandon the product because generated music doesn't sound professional.

**The Solution**: Implement Musical Quality-First Architecture that prioritizes musical excellence above all else.

**Implementation Plan**: See [MUSICAL_QUALITY_IMPLEMENTATION_PLAN.md](MUSICAL_QUALITY_IMPLEMENTATION_PLAN.md) for detailed roadmap.

**Key Insight**: Musical quality is not a feature - it's the foundation. Everything else is secondary to making music that actually sounds good.

---

## Musical Quality-First Development

### Core Principles

#### 1. Musical Quality First
- Every technical decision is evaluated against its impact on musical output quality
- Build quality assessment tools before generation tools
- Test with real musical examples, not synthetic test cases
- Focus on what makes music sound good, not just technically correct

#### 2. Rhythm is King
- Groove and timing are more important than harmony
- Different styles have distinct rhythmic characteristics
- Poor rhythm makes everything sound amateur
- Good rhythm can make simple harmony sound professional

#### 3. Expert Knowledge Integration
- Use musical expertise in prompts, not generic AI instructions
- Role-specific prompts with musical knowledge are essential
- Understanding musical conventions is more important than technical complexity
- Learn from successful patterns and expert feedback

#### 4. Quality Validation
- Every generated pattern must meet quality standards
- Patterns below threshold are rejected and regenerated
- Quality feedback drives prompt refinement
- Only high-quality patterns reach the user

### Development Phases

#### Phase 1: Musical Quality Foundation (Weeks 1-3)
1. **Week 1**: Build Musical Quality Assessment Engine
2. **Week 2**: Implement Groove Engine (rhythm and timing)
3. **Week 3**: Add Musical Quality Validation

#### Phase 2: Specialized Musical Engines (Weeks 4-6)
1. **Week 4**: Build Harmonic Intelligence Engine
2. **Week 5**: Create Style Engine for genre-specific patterns
3. **Week 6**: Integration and testing with real musical projects

#### Phase 3: Expert Prompt System (Weeks 7-8)
1. **Week 7**: Replace generic prompts with musical expertise
2. **Week 8**: Add user feedback integration and iterative refinement

#### Phase 4: Technical Integration (Weeks 9-10)
1. **Week 9**: Connect quality system to Ardour
2. **Week 10**: User experience and performance optimization

### Success Metrics

#### Musical Quality
- Generated patterns sound professional and authentic
- Patterns work well together musically
- Users actually want to use the generated music

#### User Satisfaction
- Users prefer generated patterns to generic alternatives
- Users can easily provide musical feedback
- Users learn musical concepts through interaction

#### Technical Performance
- Generation happens in real-time
- Quality assessment is fast and accurate
- System integrates seamlessly with Ardour

### Critical Success Factors

1. **Start with Musical Quality**: Don't build technical infrastructure until you can generate good music
2. **Rhythm is King**: Focus on groove and timing first - everything else is secondary
3. **Test with Real Examples**: Use actual musical patterns, not synthetic test cases
4. **Expert Knowledge**: Use musical expertise in prompts, not generic AI instructions
5. **Quality Validation**: Every generated pattern must meet quality standards

---

## Development Setup

### Prerequisites
- **macOS** (tested on macOS 15.5)
- **Python 3.8+**
- **Xcode Command Line Tools**
- **CMake 3.31.7+**
- **OpenAI API key** (for conversational AI features)

### Environment Setup
```bash
# Clone and setup
git clone <repository>
cd music_cursor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Verify setup
python control_plane_cli.py status
python enhanced_control_plane_cli.py --help-enhanced
```

### MIDI Setup
```bash
# Enable IAC Driver in Audio MIDI Setup
# Create port named "IAC Driver Bus 1"
python -c "import mido; print('Ports:', mido.get_output_names())"
```

---

## Project Structure

```
music_cursor/
├── commands/                    # Control plane system
│   ├── control_plane.py        # Main orchestrator
│   ├── parser.py              # Command parsing
│   ├── pattern_engine.py      # Musical pattern generation
│   ├── session.py             # State management
│   └── types.py               # Command type definitions
├── musical_conversation_engine.py    # LLM integration for conversation
├── iterative_musical_workflow.py     # Conversational workflow management
├── enhanced_control_plane.py         # Enhanced control plane with AI
├── enhanced_control_plane_cli.py     # Enhanced CLI interface
├── contextual_intelligence.py        # Musical analysis engine
├── visual_feedback_display.py        # Visual feedback system
├── musical_solvers.py               # Problem-solving algorithms
├── ardour_integration.py            # Ardour file-based integration
├── musical_scribe/                  # Musical Scribe architecture
│   ├── project_state_parser.py      # Full DAW project analysis
│   ├── musical_context_engine.py    # Project-wide musical analysis
│   ├── contextual_prompt_builder.py # Specialized prompt generation
│   └── musical_scribe_engine.py     # Main orchestrator
├── musical_scribe_integration.py    # Integration layer
├── midi_io.py                      # MIDI file I/O
├── project.py                      # Project data management
├── analysis.py                     # Musical analysis functions
├── theory.py                       # Music theory helpers
├── osc_sender.py                   # OSC communication
├── main.py                         # Entry point
├── control_plane_cli.py            # CLI interface
├── live_control_plane_cli.py       # Live MIDI streaming CLI
├── demo_*.py                       # Demo and testing scripts
├── test_*.py                       # Unit tests
└── tests/                          # Test suite
```

---

## Architecture Overview

YesAnd Music follows a "Brain vs. Hands" architecture that separates core musical intelligence from DAW integration, enabling focus on musical intelligence without being constrained by DAW-specific APIs.

### Core Principles

#### 1. Separation of Concerns
- **Musical Intelligence**: Pure algorithmic functions, testable and reliable
- **MIDI I/O**: Simple data conversion without musical logic
- **Visual Feedback**: Display logic separate from analysis
- **DAW Integration**: File-based workflow separate from real-time processing
- **Control Plane**: Orchestration without implementation details

#### 2. Real-Time Safety
- No memory allocation in audio-critical paths
- No blocking operations in MIDI processing
- Thread-safe communication between components
- Background analysis doesn't interfere with audio

#### 3. Extensibility
- Easy to add new command types
- Simple to extend musical analysis
- Modular visual feedback system
- Clear interfaces between components

#### 4. Educational Value
- Every feature provides learning value
- Clear explanations of musical concepts
- Visual feedback helps understanding
- AI reasoning is transparent and explainable

### System Architecture

```
Natural Language → Command Parser → Control Plane → Contextual Intelligence → Visual Feedback Display
       ↓                ↓                ↓              ↓                        ↓
   "analyze bass"   Command Types    Pattern Gen    Musical Analysis        Color-Coded
   "show melody"    (40+ types)      + OSC Sender   + Smart Suggestions      Highlighting
   "ardour tracks"  + Ardour Int.    + MIDI Player  + Educational Content    + Explanations
   "get suggestions" + Visual        (IAC Driver)   + Background Analysis    + Real-Time Updates
                     Feedback         + File I/O     + DAW Integration        + DAW State
```

---

## Key Components

### Control Plane (`commands/`)
**Purpose**: Natural language command processing and orchestration

**Key Files**:
- `control_plane.py`: Main orchestrator coordinating all components
- `parser.py`: Natural language command parsing with regex patterns
- `pattern_engine.py`: Musical pattern generation from commands
- `session.py`: Persistent state management with file-based storage

**Responsibilities**:
- Parse natural language commands into structured operations
- Maintain session state across command executions
- Coordinate between MIDI generation and visual feedback
- Handle error isolation and graceful degradation

### Musical Intelligence Engine
**Purpose**: Core musical analysis and problem-solving algorithms

**Key Files**:
- `contextual_intelligence.py`: Main analysis orchestrator
- `musical_solvers.py`: Problem-solving algorithms (groove, harmony, arrangement)
- `analysis.py`: Pure functions for musical analysis and transformation
- `theory.py`: Music theory helpers and generators

**Responsibilities**:
- Analyze musical elements (bass, melody, harmony, rhythm)
- Generate smart suggestions for musical improvements
- Apply musical transformations and problem-solving
- Provide educational content and explanations

### Musical Scribe Architecture
**Purpose**: Context-aware AI enhancement system

**Key Files**:
- `musical_scribe/project_state_parser.py`: Converts entire DAW projects to structured JSON
- `musical_scribe/musical_context_engine.py`: Analyzes project-wide musical relationships
- `musical_scribe/contextual_prompt_builder.py`: Creates specialized prompts like Sully.ai's medical scribe
- `musical_scribe/musical_scribe_engine.py`: Main orchestrator coordinating all components
- `musical_scribe_integration.py`: Integration layer with existing system

**Responsibilities**:
- Analyze entire musical projects for context
- Generate contextually appropriate musical suggestions
- Maintain musical coherence and style consistency
- Provide multiple enhancement options

### MIDI Processing Layer
**Purpose**: Universal MIDI data handling and real-time processing

**Key Files**:
- `midi_io.py`: Universal MIDI file I/O with consistent data format
- `project.py`: Project data management and querying
- `midi_player.py`: Real-time MIDI output
- `sequencer.py`: Non-blocking MIDI playback

**Responsibilities**:
- Convert MIDI files to universal note format
- Handle MIDI format constraints and validation
- Provide real-time MIDI output without blocking
- Manage project data and metadata

### Visual Feedback System
**Purpose**: On-demand visual feedback and educational display

**Key Files**:
- `visual_feedback_display.py`: Color-coded visual feedback system
- `osc_sender.py`: Python-to-JUCE plugin communication

**Responsibilities**:
- Display color-coded musical element highlighting
- Provide educational overlays and explanations
- Handle real-time visual updates without blocking audio
- Communicate with JUCE plugin via OSC

### DAW Integration System
**Purpose**: File-based integration with DAWs for state awareness

**Key Files**:
- `ardour_integration.py`: File-based Ardour DAW integration
- Project file parsing for track/region information
- Export/import workflow for MIDI data exchange

**Responsibilities**:
- Discover and parse DAW project files
- Export selected regions for analysis
- Import improved MIDI back to DAW
- Generate automation scripts (Lua for Ardour)
- Provide DAW state awareness through file-based workflow

---

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

### Adding MIDI Transformations

1. **Implement pure function** in `analysis.py`:
```python
def new_transformation(notes: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
    """Apply new transformation to notes."""
    # Implementation
    return transformed_notes
```

2. **Add command type and parsing**:
```python
# In commands/types.py
NEW_TRANSFORMATION = "new_transformation"

# In commands/parser.py
CommandType.NEW_TRANSFORMATION: [
    r"apply\s+new\s+transformation",
    r"transform\s+with\s+new",
],
```

3. **Integrate with control plane**:
```python
# In commands/control_plane.py
elif command.type == CommandType.NEW_TRANSFORMATION:
    transformed_notes = analysis.new_transformation(notes, **parameters)
    # Apply transformation
```

4. **Add visual feedback for changes**:
```python
# In visual_feedback_display.py
def _display_transformation_feedback(self, changes: List[Dict]) -> None:
    # Show what was changed
```

---

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
# Test traditional control plane
python control_plane_cli.py "play scale C major"
python control_plane_cli.py "analyze bass"

# Test musical solvers
python control_plane_cli.py "make this groove better"

# Test Ardour integration
python control_plane_cli.py "ardour connect"
python control_plane_cli.py "ardour tracks"

# Test musical conversation system
python enhanced_control_plane_cli.py --conversation
# Try: "I need a funky bass line", "Make it more complex"

# Test Musical Scribe
python control_plane_cli.py "musical scribe status"
python control_plane_cli.py "musical scribe analyze"
python control_plane_cli.py "musical scribe enhance add a funky bassline"

# Test live MIDI streaming
python live_control_plane_cli.py
# Try: "Give me a funky bassline", "Make it more complex"
```

### Integration Testing
```bash
# End-to-end verification
python verify_implementation.py

# Demo scripts
python demo_control_plane.py
python demo_contextual_intelligence.py
python demo_musical_solvers.py
python demo_ardour_integration.py
python demo_musical_conversation.py
python demo_musical_scribe.py
```

---

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

### Common Issues
- **Plugin not loading**: Check installation paths and AudioUnit type configuration
- **Build errors**: Check CMake version and Xcode Command Line Tools
- **Real-time crashes**: Avoid memory allocation and locking in audio thread

---

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

---

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

---

## Contributing

### Development Workflow
1. **Fork and clone** the repository
2. **Create feature branch** from `main`
3. **Make changes** following code style guidelines
4. **Add tests** for new functionality
5. **Run validation** suite: `./validate.sh`
6. **Submit pull request** with clear description

### Code Style
- Prefer clear, descriptive names over abbreviations
- Keep functions small and focused; avoid deep nesting
- Add concise docstrings explaining purpose and behavior
- Follow existing patterns and conventions

### Commit Messages
- Use imperative style: "Add X", "Fix Y"
- Reference issues when applicable: `Fixes #123`
- Keep first line under 50 characters
- Add detailed description if needed

### Pull Request Process
1. **Keep PRs small and focused** with clear description
2. **Note any platform-specific testing** (macOS, Apple Silicon, DAW versions)
3. **Include testing steps** for reviewers
4. **Update documentation** if adding new features

### Quality Gates
The project includes a comprehensive validation system that must pass before submitting changes:

```bash
# Run the complete validation suite
./validate.sh
```

This checks:
- Code quality and style (flake8)
- Unit tests (45+ tests)
- Architectural purity (Brain vs. Hands)
- Integration tests
- Documentation consistency
- Dependencies
- File structure

---

## Getting Help

### Documentation
- **Features Guide**: [FEATURES.md](FEATURES.md) - Complete feature documentation
- **Reference**: [REFERENCE.md](REFERENCE.md) - Commands and APIs
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

### Development Resources
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture details
- **JUCE Plugin Development**: [docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md)
- **Ardour Integration**: [docs/ARDOUR_INTEGRATION.md](docs/ARDOUR_INTEGRATION.md)

### Common Issues
- **MIDI not working**: Check IAC Driver setup and DAW configuration
- **Commands not parsing**: Check regex patterns and command types
- **Plugin not loading**: Check build and installation paths
- **Tests failing**: Check dependencies and environment setup

---

**Ready to contribute?** Start with the [Features Guide](FEATURES.md) to understand the system, then check out the [Reference](REFERENCE.md) for technical details.