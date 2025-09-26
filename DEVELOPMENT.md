# Development Guide

Complete guide for developing and contributing to YesAnd Music's Enhanced Musical Conversation System.

## Current State

**✅ Production Ready Features:**
- **Enhanced Musical Conversation System**: Primary feature - natural dialogue with intent discovery
- **Intent Discovery Agent**: Captures musical vision through conversational dialogue
- **Creative Enhancement System**: Context-aware musical suggestions and improvements
- **Dynamic Question Generator**: Adaptive questioning based on musical context
- **Context-Aware Prompt Generation**: Rich prompts from full conversational context
- **Security-First Real-Time Enhancement**: Live LLM-powered track enhancement with built-in security
- **Real-Time Ardour Enhancement**: Live LLM-powered track enhancement with OSC monitoring and auto-import
- **Musical Scribe Architecture**: Context-aware AI for project-wide analysis
- **Live MIDI Streaming**: Real-time MIDI generation and streaming
- **DAW Integration**: File-based integration with professional DAWs
- **JUCE Plugin System**: Native DAW plugin integration

**🎯 Current Focus**: Production Ready - Advanced Features and Integration

**⚠️ Deprecated Systems**: The following systems have been deprecated and should not be used for new development:
- **Musical Quality First Generator**: Had critical issues with simple pattern generation
- **MVP User-Driven Generator**: Technical quality-focused approach
- **Legacy MVP MIDI Generator**: Basic AI MIDI generation
- **Rigid Schema-Based Systems**: Replaced by conversation-driven approach

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
python enhanced_musical_conversation_cli.py --demo
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
├── enhanced_musical_conversation_engine.py    # Main conversation engine
├── enhanced_musical_conversation_cli.py       # CLI interface
├── intent_discovery_agent.py                  # Intent discovery through conversation
├── intent_parser.py                          # Conversational intent parsing
├── question_generator.py                     # Dynamic question generation
├── creative_enhancement.py                   # Creative enhancement system
├── schemas.py                                # Dynamic intent schemas
├── commands/                                 # Control plane system
├── musical_scribe/                           # Musical Scribe architecture
├── midi_io.py                               # MIDI file I/O
├── analysis.py                              # Musical analysis functions
├── theory.py                                # Music theory helpers
└── tests/                                   # Test suite
```

## Architecture Overview

YesAnd Music follows a **Conversation-First Architecture** that prioritizes natural musical dialogue over rigid technical interfaces.

### Core Principles

#### 1. Conversation-First Design
- **Natural Dialogue**: All interaction through musical conversation
- **Intent Discovery**: Musical vision emerges through guided questions
- **Context Preservation**: Rich musical context maintained throughout
- **Psychological Approach**: Focus on musical understanding, not technical data

#### 2. Dynamic Intent System
- **Flexible Schemas**: Intent captured as flexible, context-aware objects
- **Musical Relationships**: Understands how musical elements work together
- **Context Awareness**: Same musical term means different things in different contexts
- **Extensible Design**: Grows organically with new musical concepts

#### 3. Creative Enhancement
- **Musical Understanding**: Enhancements based on musical principles, not random mutations
- **Context-Aware Suggestions**: Creative ideas that fit the musical context
- **Style-Specific Intelligence**: Different approaches for different musical styles
- **Relationship-Based**: Considers how musical elements interact

#### 4. Real-Time Safety
- No memory allocation in audio-critical paths
- No blocking operations in MIDI processing
- Thread-safe communication between components
- Background analysis doesn't interfere with audio

#### 5. Security-First Design
- Security built into every component from the ground up
- Input validation, output sanitization, rate limiting
- Fail-fast design with graceful degradation
- 95%+ test coverage with security validation

## Key Components

### Enhanced Musical Conversation Engine
**Purpose**: Main orchestrator for natural musical conversation
**Key Files**: `enhanced_musical_conversation_engine.py`, `enhanced_musical_conversation_cli.py`
**Status**: ✅ Production ready

### Intent Discovery Agent
**Purpose**: Captures musical vision through conversational dialogue
**Key Files**: `intent_discovery_agent.py`, `intent_parser.py`
**Status**: ✅ Production ready

### Creative Enhancement System
**Purpose**: Context-aware musical suggestions and improvements
**Key Files**: `creative_enhancement.py`, `question_generator.py`
**Status**: ✅ Production ready

### Dynamic Intent Schemas
**Purpose**: Flexible, context-aware musical intent representation
**Key Files**: `schemas.py`
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

### Adding a New Musical Intent Type
1. Add intent type to `IntentType` enum in `schemas.py`
2. Add patterns to `intent_parser.py`
3. Add enhancement logic to `creative_enhancement.py`
4. Add question patterns to `question_generator.py`

### Adding Creative Enhancement Patterns
1. Add patterns to `MusicalCreativityEngine` in `creative_enhancement.py`
2. Add style-specific patterns
3. Add reasoning logic for why enhancements make musical sense
4. Test with different musical contexts

### Adding Question Patterns
1. Add patterns to `MusicalQuestionGenerator` in `question_generator.py`
2. Add context-aware question generation
3. Add follow-up question logic
4. Test with different conversation stages

### Adding Musical Analysis
1. Extend `MusicalElement` enum in `contextual_intelligence.py`
2. Implement analysis method
3. Add to analysis pipeline
4. Add to creative enhancement suggestions

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

### Test Individual Systems
```bash
# Test enhanced conversation system
python enhanced_musical_conversation_cli.py --demo

# Test intent discovery
python test_intent_discovery.py

# Test creative enhancement
python test_creative_enhancement.py

# Test question generation
python test_question_generator.py

# Test security-first system
python secure_enhancement_cli.py --status

# Test real-time enhancement
python real_time_enhancement_cli.py --status
```

### Manual Testing
```bash
# Test musical conversation system
python enhanced_musical_conversation_cli.py --interactive

# Test with initial input
python enhanced_musical_conversation_cli.py --interactive --input "I'm working on a jazz piece"

# Test security-first system
python secure_enhancement_cli.py --interactive

# Test real-time enhancement
python real_time_enhancement_cli.py --interactive
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

### Conversation Performance
- Intent discovery is optimized for natural flow
- Creative enhancement suggestions are cached
- Context is preserved efficiently throughout conversation

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
- Conversation systems must preserve context
- Creative enhancements must be musically meaningful

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
- Maintain conversation-first approach
- Preserve musical context throughout

### Quality Gates
The project includes a comprehensive validation system that must pass before submitting changes:

```bash
# Run the complete validation suite
./validate.sh
```

This checks:
- Code quality and style (flake8)
- Unit tests (45+ tests)
- Architectural purity (Conversation-First)
- Integration tests
- Documentation consistency
- Dependencies
- File structure

### New Feature Guidelines
- **Conversation-First**: All new features should work through natural dialogue
- **Context Preservation**: Maintain rich musical context throughout
- **Musical Understanding**: Base features on musical principles, not technical manipulation
- **Extensible Design**: Allow features to grow with new musical concepts
- **Security-First**: Build security into features from the ground up

---

**Ready to contribute?** Start with the [README.md](README.md) to understand the system, then check out the [Quick Start Guide](QUICK_START.md) for setup instructions.