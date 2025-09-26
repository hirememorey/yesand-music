# Quick Start Guide

This project has been cleaned up to contain only the essential, working systems.

## What Works

### 1. Musical Conversation System (PRIMARY)
```bash
python musical_conversation_cli.py --demo
python musical_conversation_cli.py --interactive
```
- **Status**: ✅ Fully working
- **Purpose**: Natural language musical collaboration
- **Key Features**: Context interview, suggestion generation, MIDI sketches

### 2. Security-First Real-Time Enhancement
```bash
python secure_enhancement_cli.py --status
python secure_enhancement_cli.py --interactive
```
- **Status**: ✅ Working (requires OpenAI API key)
- **Purpose**: Secure AI-powered track enhancement
- **Key Features**: Built-in security, rate limiting, health monitoring

### 3. Real-Time Ardour Enhancement
```bash
python real_time_enhancement_cli.py --status
python real_time_enhancement_cli.py --interactive
```
- **Status**: ⚠️ Requires OpenAI API key and Ardour setup
- **Purpose**: Live LLM-powered track enhancement with auto-import
- **Key Features**: OSC monitoring, context analysis, automatic MIDI import

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (for AI features)

### Installation
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
```

### Test Everything Works
```bash
python test_simple_functionality.py
python test_security_first_system.py
```

## What Was Removed

The following systems were removed because they were broken or deprecated:
- `control_plane_cli.py` - Missing `osc_sender.py` dependency
- `enhanced_control_plane_cli.py` - Missing `osc_sender.py` dependency
- `mvp_*` generators - Deprecated systems
- `demo_*.py` scripts - Referenced broken systems
- Generated MIDI files and context files
- Redundant test files and documentation

## Current Architecture

The project now contains only working systems organized by functionality:
- **Core Systems**: Musical conversation, security-first enhancement
- **Infrastructure**: MIDI I/O, analysis, music theory
- **DAW Integration**: Ardour integration, real-time enhancement
- **Plugin**: JUCE plugin for DAW integration
- **Tests**: Essential tests for working systems

## Next Steps

1. **Start with Musical Conversation**: `python musical_conversation_cli.py --demo`
2. **Try Security-First Enhancement**: `python secure_enhancement_cli.py --interactive`
3. **Read the documentation**: Check `README.md` and `DEVELOPMENT.md`
4. **Run tests**: `python test_simple_functionality.py`

The project is now clean, organized, and ready for new developers to contribute.