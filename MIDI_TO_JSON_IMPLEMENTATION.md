# MIDI to JSON Implementation Guide

## Overview

This document provides a complete implementation guide for the MIDI to notation to JSON workflow that enables context-aware AI musical generation with Ardour integration.

## Target Workflow

```
User Prompt → Extract MIDI from Ardour → Convert to Musical Notation JSON → Send to OpenAI → Generate New MIDI → Import to Ardour
```

## Implementation Plan

### Phase 1: Basic MIDI Generation (MVP)

#### 1.1 Core MIDI Generator
**File**: `midi_generator.py`

**Purpose**: Generate MIDI files from natural language prompts using OpenAI

**Key Components**:
- OpenAI API integration
- MIDI file generation
- Style reference handling
- Error handling and validation

**API Structure**:
```python
class MIDIGenerator:
    def generate_midi(self, prompt: str, style_context: str = None) -> str
    def save_midi_file(self, midi_data: dict, filename: str) -> bool
    def validate_midi(self, midi_data: dict) -> bool
```

#### 1.2 Musical Notation Converter
**File**: `musical_notation_converter.py`

**Purpose**: Convert MIDI data to musical notation JSON format

**Key Components**:
- MIDI event parsing
- Pitch name conversion (MIDI numbers to note names)
- Timing normalization
- JSON structure creation

**JSON Format**:
```json
{
  "project": {
    "tempo": 120,
    "key": "G minor",
    "timeSignature": "4/4"
  },
  "tracks": [
    {
      "name": "Bass",
      "type": "midi",
      "notes": [
        {
          "pitch": "G2",
          "startTime": 0.0,
          "duration": 0.5,
          "velocity": 80,
          "channel": 0
        }
      ]
    }
  ]
}
```

#### 1.3 OpenAI Integration
**File**: `openai_music_client.py`

**Purpose**: Handle OpenAI API calls for musical generation

**Key Components**:
- Prompt construction
- API request handling
- Response parsing
- Error handling and retries

**Prompt Template**:
```
You are a professional bassist. Generate a bass pattern in {key} that sounds like {style_reference}.

Musical Context:
{musical_notation_json}

Requirements:
- Key: {key}
- Style: {style_reference}
- Pattern type: {pattern_type}
- Output format: JSON with musical notation

Generate the bass pattern as JSON in this format:
{
  "tracks": [
    {
      "name": "Bass",
      "notes": [
        {
          "pitch": "G2",
          "startTime": 0.0,
          "duration": 0.5,
          "velocity": 80
        }
      ]
    }
  ]
}
```

### Phase 2: Ardour Context Extraction

#### 2.1 Ardour MIDI Extractor
**File**: `ardour_midi_extractor.py`

**Purpose**: Extract MIDI data from Ardour projects

**Key Components**:
- Ardour project file parsing
- MIDI track identification
- MIDI data extraction
- Project metadata extraction

**Extraction Methods**:
1. **File-based**: Parse `.ardour` project files
2. **OSC-based**: Use existing OSC monitoring
3. **Export-based**: Export MIDI regions and parse

#### 2.2 Context Assembler
**File**: `context_assembler.py`

**Purpose**: Combine extracted MIDI with project context

**Key Components**:
- Musical analysis (key, tempo, style)
- Track role identification
- Harmonic progression analysis
- Rhythmic pattern analysis

### Phase 3: Ardour Integration

#### 3.1 MIDI File Importer
**File**: `ardour_midi_importer.py`

**Purpose**: Import generated MIDI files to Ardour

**Key Components**:
- Lua script generation
- Track creation
- MIDI region import
- Error handling

#### 3.2 Track Manager
**File**: `track_manager.py`

**Purpose**: Manage Ardour tracks for MIDI import

**Key Components**:
- Track type detection
- Track naming conventions
- Track creation logic
- Conflict resolution

### Phase 4: User Interface

#### 4.1 Command Line Interface
**File**: `music_generator_cli.py`

**Purpose**: Main command-line interface

**Usage**:
```bash
python music_generator_cli.py "generate a bass pattern like Alice In Chains in GMinor"
python music_generator_cli.py --interactive
python music_generator_cli.py --extract-context
```

#### 4.2 Interactive Mode
**Features**:
- Continuous conversation
- Context awareness
- Real-time feedback
- Error recovery

## Implementation Steps

### Step 1: Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Verify setup
python music_generator_cli.py --test
```

### Step 2: Basic MIDI Generation
```bash
# Test basic generation
python music_generator_cli.py "generate a simple bass line in C major"

# Test style reference
python music_generator_cli.py "generate a bass pattern like Alice In Chains in GMinor"
```

### Step 3: Context Extraction
```bash
# Extract context from Ardour project
python music_generator_cli.py --extract-context

# Generate with context
python music_generator_cli.py "add a bass line that fits with the existing music"
```

### Step 4: Ardour Integration
```bash
# Generate and import to Ardour
python music_generator_cli.py "generate a bass pattern like Alice In Chains in GMinor" --import-to-ardour
```

## File Structure

```
music_generator/
├── midi_generator.py              # Core MIDI generation
├── musical_notation_converter.py  # MIDI to JSON conversion
├── openai_music_client.py        # OpenAI integration
├── ardour_midi_extractor.py      # Ardour context extraction
├── context_assembler.py          # Context assembly
├── ardour_midi_importer.py       # Ardour import
├── track_manager.py              # Track management
├── music_generator_cli.py        # Main CLI interface
├── test_midi_generator.py        # Test suite
└── examples/                     # Example usage
    ├── basic_generation.py
    ├── context_extraction.py
    └── ardour_integration.py
```

## Dependencies

```txt
# Core dependencies
mido>=1.2.10
python-rtmidi>=1.4.9
python-osc>=1.7.4
openai>=1.0.0

# Additional dependencies for MIDI to JSON
music21>=8.0.0
numpy>=1.21.0

# Testing
pytest>=7.0.0
```

## Testing Strategy

### Unit Tests
- MIDI generation accuracy
- JSON conversion correctness
- OpenAI integration reliability
- Error handling coverage

### Integration Tests
- End-to-end workflow
- Ardour integration
- File I/O operations
- API communication

### Manual Tests
- User experience validation
- Musical quality assessment
- Performance testing
- Error recovery testing

## Success Criteria

1. **Basic Generation**: Generate valid MIDI files from prompts
2. **Style Accuracy**: Generated music matches style references
3. **Context Awareness**: Incorporate existing project context
4. **Ardour Integration**: Seamless import to Ardour
5. **User Experience**: Intuitive command-line interface

## Troubleshooting

### Common Issues
- OpenAI API key not set
- MIDI file generation failures
- Ardour project not found
- Import script execution errors

### Debug Mode
```bash
export DEBUG=1
python music_generator_cli.py "your prompt"
```

## Future Enhancements

1. **Real-time Generation**: Direct MIDI streaming
2. **Advanced Context**: Harmonic and rhythmic analysis
3. **Multi-track Support**: Generate multiple instruments
4. **Style Learning**: Learn from user preferences
5. **Cloud Integration**: Save and share generated patterns

## Getting Started

1. **Read this guide** completely
2. **Set up environment** with dependencies
3. **Test basic generation** with simple prompts
4. **Add context extraction** for existing projects
5. **Integrate with Ardour** for complete workflow

This implementation provides a complete, testable system for context-aware AI musical generation with Ardour integration.