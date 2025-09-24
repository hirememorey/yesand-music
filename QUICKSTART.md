# Quick Start Guide

Get YesAnd Music running in 5 minutes.

## What This Is

YesAnd Music is an AI-powered musical collaborator that provides contextual intelligence and musical problem-solving through natural language conversation. It works with your existing DAW workflow, including direct integration with Ardour DAW, and can engage in musical dialogue to help you create, improve, and understand music.

## Prerequisites

- macOS (tested on macOS 15.5)
- Python 3.8+
- OpenAI API key (for conversational AI features)
- A DAW (GarageBand, Logic Pro, or Ardour with file-based integration)

## 1. Setup (2 minutes)

### Enable MIDI Port
```bash
# Open Audio MIDI Setup and enable IAC Driver
# Create a port named "IAC Driver Bus 1"
python -c "import mido; print('Available ports:', mido.get_output_names())"
```

### Install Dependencies
```bash
cd /path/to/music_cursor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Set OpenAI API Key
```bash
# Get your API key from https://platform.openai.com/
export OPENAI_API_KEY="your-api-key-here"
```

## 2. Run It (1 minute)

### Musical Conversation (Recommended)
```bash
# Start conversation mode
python enhanced_control_plane_cli.py --conversation

# Try these examples:
"I need a funky bass line for my song"
"Make it groove like Stevie Wonder"
"This chorus sounds flat, brighten it up"
"Make it more complex"
```

### Traditional Commands
```bash
# Basic demo
python main.py
# Expected: "Playing C Major Scale..." and 8 notes in your DAW

# Interactive mode
python main.py --interactive
# Try: "play scale D minor", "set tempo to 140", "stop"

# CLI commands
python control_plane_cli.py "play scale F# lydian"
python control_plane_cli.py "make it jazz"

# Ardour Integration (if Ardour is installed)
python control_plane_cli.py "ardour connect"
python control_plane_cli.py "ardour tracks"
```

### Musical Scribe (Context-Aware AI)
```bash
# Check Musical Scribe status
python control_plane_cli.py "musical scribe status"

# Analyze entire project context
python control_plane_cli.py "musical scribe analyze"

# Enhance with context-aware AI
python control_plane_cli.py "musical scribe enhance add a funky bassline"
python control_plane_cli.py "musical scribe enhance improve the arrangement"
python control_plane_cli.py "musical scribe enhance add some drums"

# Generate contextual prompts
python control_plane_cli.py "musical scribe prompt create a jazz melody"
python control_plane_cli.py "musical scribe prompt add a walking bass line"
```

## 3. Test Musical Intelligence (2 minutes)

### Musical Conversation Examples
```bash
# Start conversation mode
python enhanced_control_plane_cli.py --conversation

# Generate musical content
"I need a funky bass line for my song"
"Create a jazz melody in C major"
"Make a blues chord progression"

# Use musical references
"Make it groove like Stevie Wonder"
"Give it that Motown feel"
"I want something dark and moody"

# Provide feedback and refinement
"Make it more complex"
"This is too busy, simplify it"
"Make it swing more"
"I want it in a different key"
```

### Traditional Analysis
```bash
# Load and analyze MIDI files
python control_plane_cli.py "load test_simple.mid"
python control_plane_cli.py "analyze bass"
python control_plane_cli.py "analyze melody"
python control_plane_cli.py "analyze all"

# Solve musical problems
python control_plane_cli.py "make this groove better"
python control_plane_cli.py "fix the harmony"
python control_plane_cli.py "improve the arrangement"

# With Ardour Integration
python control_plane_cli.py "ardour export selected"
python control_plane_cli.py "ardour analyze selected"
python control_plane_cli.py "ardour improve selected"
```

### Musical Scribe Examples
```bash
# Context-aware enhancement
python control_plane_cli.py "musical scribe enhance add a funky bassline"
python control_plane_cli.py "musical scribe enhance improve the arrangement"
python control_plane_cli.py "musical scribe enhance add some drums"

# Project analysis
python control_plane_cli.py "musical scribe analyze"

# Contextual prompt generation
python control_plane_cli.py "musical scribe prompt create a jazz melody"
python control_plane_cli.py "musical scribe prompt add a walking bass line"

# System status
python control_plane_cli.py "musical scribe status"
```

## 4. What You Should See

- **Musical Conversation**: Natural dialogue with AI musical collaborator
- **Musical Scribe**: Context-aware AI that understands your entire project
- **Generated Content**: MIDI files created from your requests
- **Contextual Enhancement**: AI-generated patterns that fit your existing musical context
- **Iterative Refinement**: Back-and-forth conversation to perfect ideas
- **Musical References**: AI understanding of artists, styles, and techniques
- **MIDI Output**: Notes playing in your DAW
- **Visual Feedback**: Color-coded analysis (Blue=bass, Green=melody, Purple=harmony, Orange=rhythm)
- **Musical Improvements**: Better-sounding versions saved as new MIDI files
- **Educational Content**: Explanations of what the AI changed and why

## 5. Next Steps

- **For Users**: See [README.md](README.md) for full features
- **For Musical Conversation**: See [MUSICAL_CONVERSATION_README.md](MUSICAL_CONVERSATION_README.md) for detailed conversation guide
- **For Developers**: See [DEVELOPMENT.md](DEVELOPMENT.md) for development workflows
- **For Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- **For Ardour Integration**: See [docs/ARDOUR_INTEGRATION.md](docs/ARDOUR_INTEGRATION.md) for detailed Ardour workflow

## Troubleshooting

**No sound?**
- Check IAC Driver is enabled and port is named "IAC Driver Bus 1"
- Verify DAW track is armed and monitoring is on
- Run: `python control_plane_cli.py status`

**Commands not working?**
- Check you're in the virtual environment: `source .venv/bin/activate`
- Verify dependencies: `pip list | grep mido`

**Need help?**
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development issues
