# YesAnd Music

**AI-Powered Musical Collaborator with Context-Aware Intelligence**

Transform MIDI editing from technical manipulation to intelligent musical collaboration through natural language conversation that integrates seamlessly with existing DAW workflows.

## 🚀 Quick Start (2 minutes)

### Prerequisites
- **macOS** (tested on macOS 15.5)
- **Python 3.8+**
- **OpenAI API key** (for AI features)
- **IAC Driver** enabled in Audio MIDI Setup

### Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Enable IAC Driver
# Open Audio MIDI Setup → Window → Show MIDI Studio
# Double-click IAC Driver → check "Device is online"
# Create port named "IAC Driver Bus 1"
```

### Try It Now
```bash
# Live MIDI Streaming (Recommended)
python live_control_plane_cli.py
# Try: "Give me a funky bassline" → "Make it more complex"

# Musical Conversation
python enhanced_control_plane_cli.py --conversation
# Try: "I need a funky bass line" → "Make it groove like Stevie Wonder"

# Traditional Commands
python control_plane_cli.py "play scale C major"
# Try: "analyze bass", "make this groove better"
```

## 🎯 What It Does

**YesAnd Music** is a context-aware AI musical collaborator that understands your entire project and provides intelligent enhancements through natural language conversation.

### Core Capabilities
- **🎵 Live MIDI Streaming**: Generate and stream MIDI directly to Ardour tracks in real-time
- **💬 Musical Conversation**: Chat with AI musical collaborator in natural language
- **🧠 Musical Scribe**: Context-aware AI that understands your entire project and provides intelligent enhancements
- **🎯 Musical Intelligence**: Analyze bass lines, melodies, harmony, and rhythm with visual feedback
- **🛠️ Problem Solving**: "Make this groove better", "Fix the harmony", "Improve the arrangement"
- **🎨 Musical References**: "Make it groove like Stevie Wonder", "Give it that Motown feel"
- **🔄 Iterative Refinement**: "Make it more complex" → "This is too busy, simplify it"
- **🎚️ DAW Integration**: Works with Ardour, Logic Pro, and GarageBand
- **📚 Educational**: Learn musical concepts through AI explanations

### Key Features
- **Context-Aware Intelligence**: Understands entire musical projects, not just individual tracks
- **Sully.ai-Inspired Architecture**: Uses specialized prompts for different musical roles
- **Real-Time Performance**: Live MIDI streaming with professional audio safety
- **Non-Intrusive Integration**: Preserves existing DAW workflows while adding intelligence

## 📚 Documentation

### For Users
- **[Features Guide](FEATURES.md)** - Complete guide to all features and capabilities
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Reference](REFERENCE.md)** - Complete command and API reference

### For Developers
- **[Development Guide](DEVELOPMENT.md)** - Complete development and contribution guide
- **[Architecture](ARCHITECTURE.md)** - Technical architecture and design details

## 🎵 Example Workflows

### Live MIDI Creation
1. **Generate**: "Give me a funky bassline" → MIDI streams to Ardour
2. **Refine**: "Make it more complex" → Real-time modification
3. **Style**: "Make it groove like Bootsy Collins" → Style transformation
4. **Polish**: "Add some swing" → Final touches

### Musical Conversation
1. **Start**: "I need help with my jazz ballad"
2. **Analyze**: AI analyzes your entire project context
3. **Suggest**: "The piano is busy, try a simpler bassline"
4. **Generate**: Creates contextually appropriate bassline
5. **Refine**: "Make it darker" → Iterative improvement

### Problem Solving
1. **Load**: `load my_song.mid`
2. **Analyze**: `analyze all` → Complete musical analysis
3. **Improve**: `make this groove better` → Enhanced version
4. **Compare**: Listen to original vs. improved

## 🏗️ Architecture

YesAnd Music follows a "Brain vs. Hands" architecture:
- **Musical Intelligence (Brain)**: Pure algorithmic functions, testable and reliable
- **MIDI I/O (Hands)**: Simple data conversion without musical logic
- **Context Awareness**: Full project understanding for intelligent suggestions

## 🚀 Current Status

**✅ Production Ready Features:**
- Live MIDI streaming to Ardour
- Musical conversation system with OpenAI integration
- Context-aware Musical Scribe architecture
- Comprehensive musical problem solvers
- File-based DAW integration
- Real-time MIDI editing capabilities

**🎯 Next Priorities:**
- Test Musical Scribe with real projects
- Refine musical analysis algorithms
- Performance optimization
- Multi-DAW support expansion

## 🤝 Contributing

We welcome contributions! See our [Development Guide](DEVELOPMENT.md) for:
- Development setup and workflows
- Code style and testing requirements
- Pull request process
- Architecture guidelines

## 📄 License

This project is part of YesAnd Music. See [LICENSE](LICENSE) for details.

---

**Ready to start?** Check out the [Features Guide](FEATURES.md) for detailed usage instructions, or jump straight to [Troubleshooting](TROUBLESHOOTING.md) if you run into issues.