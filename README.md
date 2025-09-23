# YesAnd Music

**AI-Powered Musical Collaborator with Conversational Intelligence**

YesAnd Music transforms MIDI editing from technical manipulation to intelligent musical collaboration through natural language conversation that integrates seamlessly with existing DAW workflows.

## What It Does

- **Musical Conversation**: Chat with an AI musical collaborator in natural language
- **Intelligent Generation**: "Generate a funky bass line", "Make it groove like Stevie Wonder"
- **Iterative Refinement**: "Make it more complex" → "This is too busy, simplify it"
- **Musical Intelligence**: Analyzes bass lines, melodies, harmony, and rhythm with visual feedback
- **Problem Solving**: "Make this groove better", "Fix the harmony", "Improve the arrangement"
- **Real-Time Control**: Generate MIDI patterns via natural language commands
- **DAW Integration**: Works with GarageBand, Logic Pro, and Ardour (with file-based integration)
- **Educational**: Learn musical concepts through AI explanations and musical references

## Quick Start

```bash
# 1. Setup (2 minutes)
python -c "import mido; print('Available ports:', mido.get_output_names())"
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"

# 2. Start musical conversation
python enhanced_control_plane_cli.py --conversation

# 3. Try musical conversation
"I need a funky bass line for my song"
"Make it groove like Stevie Wonder"
"This chorus sounds flat, brighten it up"
```

**See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.**

## Current Status

✅ **Phase 3C Complete**: Musical conversation system working  
🎯 **Next**: Advanced features and multi-user collaboration

### What Works Now

- **Musical Conversation**: Chat with AI musical collaborator in natural language
- **Intelligent Generation**: Generate musical patterns through conversation
- **Iterative Refinement**: Refine musical ideas through feedback loops
- **Musical References**: Use artist and style references in conversation
- **Control Plane**: 23+ natural language commands for MIDI generation
- **JUCE Plugin**: Real-time MIDI effects (swing, accent, humanization)
- **Contextual Intelligence**: Musical analysis with visual feedback
- **Musical Solvers**: Groove improvement, harmony fixing, arrangement enhancement
- **OSC Integration**: Python-to-plugin communication
- **Ardour Integration**: File-based workflow with Ardour DAW

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[MUSICAL_CONVERSATION_README.md](MUSICAL_CONVERSATION_README.md)** - Musical conversation system guide
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development workflows and guides
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## Vision

Enable musicians to intelligently edit their music through background analysis, contextual intelligence, and natural language conversation that enhances rather than disrupts their creative workflow.
