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

**📖 [Complete Setup Guide](QUICKSTART.md) | [Troubleshooting](TROUBLESHOOTING.md)**

## 🎯 What It Does

- **🎵 Live MIDI Streaming**: Generate and stream MIDI directly to Ardour tracks in real-time
- **💬 Musical Conversation**: Chat with AI musical collaborator in natural language
- **🧠 Musical Intelligence**: Analyze bass lines, melodies, harmony, and rhythm with visual feedback
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
🎯 **Next**: Advanced features and multi-user collaboration

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
- **[docs/JUCE_PLUGIN_DEVELOPMENT.md](docs/JUCE_PLUGIN_DEVELOPMENT.md)** - JUCE plugin development

### 📋 **Reference**
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

## 🎯 Vision

Enable musicians to intelligently edit their music through background analysis, contextual intelligence, and natural language conversation that enhances rather than disrupts their creative workflow.

---

**💡 New to the project?** Start with [QUICKSTART.md](QUICKSTART.md)  
**🐛 Having issues?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
**🔧 Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)
