# Development Guide

Complete guide for developing and contributing to YesAnd Music.

## Current State

**✅ Production Ready Features:**
- **Musical Conversation System**: Primary feature - fully working with Interview-First Architecture
- **Security-First Real-Time Enhancement**: Live LLM-powered track enhancement with built-in security
- **Real-Time Ardour Enhancement**: Live LLM-powered track enhancement with OSC monitoring and auto-import
- **Musical Scribe Architecture**: Context-aware AI for project-wide analysis
- **Live MIDI Streaming**: Real-time MIDI generation and streaming
- **DAW Integration**: File-based integration with professional DAWs
- **JUCE Plugin System**: Native DAW plugin integration

**🎯 Current Focus**: Production Ready - User Testing and Feature Enhancement

**⚠️ Deprecated Systems**: The following systems have been deprecated and should not be used for new development:
- **Musical Quality First Generator**: Had critical issues with simple pattern generation
- **MVP User-Driven Generator**: Technical quality-focused approach
- **Legacy MVP MIDI Generator**: Basic AI MIDI generation

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
python test_simple_functionality.py
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
├── commands/                    # Control plane system
├── musical_conversation_engine.py    # LLM integration for conversation
├── musical_scribe/                  # Musical Scribe architecture
├── midi_io.py                      # MIDI file I/O
├── analysis.py                     # Musical analysis functions
├── theory.py                       # Music theory helpers
├── musical_conversation_cli.py     # Main CLI interface
├── secure_enhancement_cli.py       # Security-first enhancement
├── real_time_enhancement_cli.py    # Real-time enhancement
└── tests/                          # Test suite
```

## Architecture Overview

YesAnd Music follows a "Brain vs. Hands" architecture that separates core musical intelligence from DAW integration.

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

#### 3. Security-First Design
- Security built into every component from the ground up
- Input validation, output sanitization, rate limiting
- Fail-fast design with graceful degradation
- 95%+ test coverage with security validation

## Key Components

### Musical Conversation System
**Purpose**: Natural language musical collaboration
**Key Files**: `musical_conversation_cli.py`, `musical_conversation_engine.py`
**Status**: ✅ Production ready

### Security-First Enhancement
**Purpose**: Secure AI-powered track enhancement
**Key Files**: `secure_enhancement_cli.py`, `secure_enhancement_system.py`
**Status**: ✅ Production ready

### Real-Time Enhancement
**Purpose**: Live LLM-powered track enhancement with auto-import
**Key Files**: `real_time_enhancement_cli.py`, `real_time_ardour_enhancer.py`
**Status**: ✅ Production ready

### Musical Scribe Architecture
**Purpose**: Context-aware AI for project-wide analysis
**Key Files**: `musical_scribe/` directory
**Status**: ✅ Production ready

## Common Development Tasks

### Adding a New Command
1. Add command type to `commands/types.py`
2. Add regex patterns to `commands/parser.py`
3. Add command handling to `commands/control_plane.py`

### Adding Musical Analysis
1. Extend `MusicalElement` enum in `contextual_intelligence.py`
2. Implement analysis method
3. Add to analysis pipeline

### Adding Visual Feedback
1. Extend `VisualFeedbackType` enum
2. Implement feedback generation
3. Add to display system

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
# Test musical conversation system
python musical_conversation_cli.py --demo

# Test security-first system
python secure_enhancement_cli.py --status

# Test real-time enhancement
python real_time_enhancement_cli.py --status
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

### Real-Time Safety
- **NEVER** allocate memory in `processBlock()`
- **NEVER** use locking mechanisms in audio thread
- **NEVER** make blocking calls in audio thread
- Use `AudioProcessorValueTreeState` for thread-safe parameter access

## Performance Considerations

### Real-Time Safety
- Visual feedback runs in separate thread
- No blocking operations in audio-critical paths
- Background analysis doesn't interfere with MIDI playback

### Memory Management
- Visual feedback queue has size limits
- Analysis results are cached to avoid recomputation
- Old feedback is automatically cleaned up

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

**Ready to contribute?** Start with the [README.md](README.md) to understand the system, then check out the [Quick Start Guide](QUICK_START.md) for setup instructions.