# YesAnd Music

**Contextual Intelligence for Semantic MIDI Editing with Visual Feedback**

YesAnd Music transforms MIDI editing from technical manipulation to intelligent assistance through natural language conversation that integrates seamlessly with existing DAW workflows.

## What It Does

- **Musical Intelligence**: Analyzes bass lines, melodies, harmony, and rhythm with visual feedback
- **Problem Solving**: "Make this groove better", "Fix the harmony", "Improve the arrangement"
- **Real-Time Control**: Generate MIDI patterns via natural language commands
- **DAW Integration**: Works with GarageBand, Logic Pro, and Ardour (with file-based integration)
- **Educational**: Learn musical concepts through AI explanations

## Quick Start

```bash
# 1. Setup (2 minutes)
python -c "import mido; print('Available ports:', mido.get_output_names())"
pip install -r requirements.txt

# 2. Run it
python main.py

# 3. Try musical intelligence
python control_plane_cli.py "load test_simple.mid"
python control_plane_cli.py "make this groove better"
```

**See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.**

## Current Status

✅ **Phase 3B Complete**: Musical problem solvers working  
🎯 **Next**: Phase 3C - Advanced LLM integration

### What Works Now

- **Control Plane**: 23+ natural language commands for MIDI generation
- **JUCE Plugin**: Real-time MIDI effects (swing, accent, humanization)
- **Contextual Intelligence**: Musical analysis with visual feedback
- **Musical Solvers**: Groove improvement, harmony fixing, arrangement enhancement
- **OSC Integration**: Python-to-plugin communication
- **Ardour Integration**: File-based workflow with Ardour DAW

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development workflows and guides
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## Vision

Enable musicians to intelligently edit their music through background analysis, contextual intelligence, and natural language conversation that enhances rather than disrupts their creative workflow.
