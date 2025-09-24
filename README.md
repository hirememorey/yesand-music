# YesAnd Music

**AI-Powered Musical Collaborator with Conversational Intelligence**

Transform MIDI editing from technical manipulation to intelligent musical collaboration through natural language conversation that integrates seamlessly with existing DAW workflows.

## 🚀 Quick Start

Choose your path based on what you want to do:

### 🎵 **Live MIDI Streaming** (Recommended)
Generate and stream MIDI directly to your DAW in real-time:
```bash
# Setup (2 minutes)
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
# Enable IAC Driver in Audio MIDI Setup → Create "IAC Driver Bus 1"

# Start live streaming
python live_control_plane_cli.py
# Try: "Give me a funky bassline" → "Make it more complex"
```

### 💬 **Musical Conversation**
Chat with an AI musical collaborator:
```bash
# Setup (2 minutes)
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"

# Start conversation
python enhanced_control_plane_cli.py --conversation
# Try: "I need a funky bass line" → "Make it groove like Stevie Wonder"
```

### 🎛️ **Traditional Commands**
Use natural language commands for MIDI control:
```bash
# Setup (2 minutes)
pip install -r requirements.txt

# Start control plane
python control_plane_cli.py "play scale C major"
# Try: "analyze bass", "make this groove better"
```

### 🧠 **Musical Scribe** (NEW - Context-Aware AI)
AI that understands your entire project and provides contextually appropriate enhancements:
```bash
# Setup (2 minutes)
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"

# Start Musical Scribe
python control_plane_cli.py "musical scribe enhance add a funky bassline"
# Try: "musical scribe analyze", "musical scribe prompt create a jazz melody"
```

**📖 [Complete Setup Guide](QUICKSTART.md) | [Troubleshooting](TROUBLESHOOTING.md)**

## 🎯 What It Does

- **🎵 Live MIDI Streaming**: Generate and stream MIDI directly to Ardour tracks in real-time
- **💬 Musical Conversation**: Chat with AI musical collaborator in natural language
- **🧠 Musical Scribe**: Context-aware AI that understands your entire project and provides intelligent enhancements
- **🎯 Musical Intelligence**: Analyze bass lines, melodies, harmony, and rhythm with visual feedback
- **🛠️ Problem Solving**: "Make this groove better", "Fix the harmony", "Improve the arrangement"
- **🎨 Musical References**: "Make it groove like Stevie Wonder", "Give it that Motown feel"
- **🔄 Iterative Refinement**: "Make it more complex" → "This is too busy, simplify it"
- **🎚️ DAW Integration**: Works with Ardour, Logic Pro, and GarageBand
- **📚 Educational**: Learn musical concepts through AI explanations

## 🛤️ Common Paths

### 🎵 **I Want to Generate Music Live**
1. Start with [Live MIDI Streaming Setup](QUICKSTART.md#-live-midi-streaming-setup)
2. Learn more: [Live MIDI Streaming Guide](docs/guides/LIVE_MIDI_STREAMING_README.md)
3. Integrate with DAW: [Ardour Integration](docs/ARDOUR_INTEGRATION.md)

### 💬 **I Want to Chat About Music**
1. Start with [Musical Conversation Setup](QUICKSTART.md#-musical-conversation-setup)
2. Learn more: [Musical Conversation Guide](docs/guides/MUSICAL_CONVERSATION_README.md)
3. Try examples: "I need a funky bass line" → "Make it more complex"

### 🧠 **I Want Context-Aware AI Enhancement**
1. Start with [Musical Scribe Setup](QUICKSTART.md#-musical-scribe-setup)
2. Learn more: [Musical Scribe Architecture](MUSICAL_SCRIBE_ARCHITECTURE.md)
3. Try examples: "musical scribe enhance add a funky bassline" → "musical scribe analyze"

### 🛠️ **I Want to Develop Features**
1. Start with [Developer Setup](DEVELOPMENT.md#-quick-setup)
2. Understand architecture: [Architecture Overview](ARCHITECTURE.md)
3. Add new features: [Development Guide](DEVELOPMENT.md)

### 🐛 **I'm Having Issues**
1. Check [Quick Troubleshooting](TROUBLESHOOTING.md#quick-diagnostics)
2. Find your issue: [Common Issues](TROUBLESHOOTING.md#common-issues)
3. Get help: [Getting Help](TROUBLESHOOTING.md#getting-help)

## 📊 Current Status

✅ **Phase 4A Complete**: Live MIDI streaming system working  
✅ **Phase 3C Complete**: Musical conversation system working  
🚨 **CRITICAL GAP IDENTIFIED**: Context-aware architecture missing (Musical Scribe model)
🎯 **Next**: Implement Musical Scribe architecture for true context awareness

## 📚 Documentation

### 🚀 **Getting Started**
- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup guide with multiple paths
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

### 🎵 **Feature Guides**
- **[docs/guides/LIVE_MIDI_STREAMING_README.md](docs/guides/LIVE_MIDI_STREAMING_README.md)** - Live MIDI streaming and real-time editing
- **[docs/guides/MUSICAL_CONVERSATION_README.md](docs/guides/MUSICAL_CONVERSATION_README.md)** - Musical conversation system
- **[docs/ARDOUR_INTEGRATION.md](docs/ARDOUR_INTEGRATION.md)** - Ardour DAW integration

### 🛠️ **Development**
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer workflows and guides
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design
- **[MUSICAL_SCRIBE_ARCHITECTURE.md](MUSICAL_SCRIBE_ARCHITECTURE.md)** - 🚨 **CRITICAL**: Musical Scribe architecture (Sully.ai-inspired)
- **[docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md)** - JUCE plugin development

### 📋 **Reference**
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

## 🎯 Vision

Enable musicians to intelligently edit their music through **context-aware analysis**, **musical scribe architecture**, and natural language conversation that enhances rather than disrupts their creative workflow.

**🚨 CRITICAL ARCHITECTURAL EVOLUTION**: The project is evolving toward a **"Musical Scribe" architecture** inspired by Sully.ai's medical scribe model, where the system maintains full DAW project context awareness to provide truly intelligent musical assistance.

## 🎵 The Musical Scribe Architecture

### The Problem
The current YesAnd Music architecture is **command-driven** rather than **context-driven**, severely limiting its effectiveness:

**Current (Limited)**: User says "funky bass" → Generate generic funky bassline
**Needed (Context-Aware)**: User says "funky bass" → Analyze entire project → Generate contextually appropriate bassline

### The Solution (Inspired by Sully.ai)
Transform YesAnd Music to work like Sully.ai's medical scribe:

1. **DAW Project Input**: Full project state (tracks, regions, arrangements)
2. **Musical Context**: Project converted to structured JSON with musical analysis
3. **Contextual Prompt**: Musical context + specialized prompt sent to LLM
4. **Enhanced MIDI**: LLM returns contextually appropriate MIDI patterns

### Example Workflow
```
User: "Give me a funky bassline"
System: Analyzes entire project → "This is a jazz ballad in C major with complex piano chords and soft drums. The piano is busy and needs a supportive bass foundation. Generate 2-3 funky bassline options that complement the existing arrangement."
Result: Contextually appropriate bassline patterns that actually enhance the song
```

**📖 [Read the full Musical Scribe Architecture Guide](MUSICAL_SCRIBE_ARCHITECTURE.md)**

---

**💡 New to the project?** Start with [QUICKSTART.md](QUICKSTART.md)  
**🐛 Having issues?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
**🔧 Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)
