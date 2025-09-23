# Quick Start Guide

Get YesAnd Music running in 5 minutes with clear paths for different use cases.

## 🎯 Choose Your Path

### 🎵 **Live MIDI Streaming** (Musicians & Producers)
Generate and stream MIDI directly to your DAW in real-time
→ [Jump to Live MIDI Setup](#-live-midi-streaming-setup)

### 💬 **Musical Conversation** (Songwriters & Composers)  
Chat with an AI musical collaborator for creative assistance
→ [Jump to Conversation Setup](#-musical-conversation-setup)

### 🎛️ **Traditional Commands** (Developers & Technical Users)
Use natural language commands for MIDI control and analysis
→ [Jump to Traditional Setup](#-traditional-commands-setup)

---

## 📋 Prerequisites

- **macOS** (tested on macOS 15.5)
- **Python 3.8+**
- **OpenAI API key** (for conversational AI features)
- **DAW** (Ardour for live streaming, any DAW for traditional features)

## 🚀 Universal Setup (2 minutes)

### 1. Install Dependencies
```bash
cd /path/to/music_cursor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
# Get your API key from https://platform.openai.com/
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Enable MIDI Port
```bash
# Open Audio MIDI Setup → Window → Show MIDI Studio
# Double-click IAC Driver → check "Device is online"
# Create port named "IAC Driver Bus 1"
python -c "import mido; print('Available ports:', mido.get_output_names())"
```

---

## 🎵 Live MIDI Streaming Setup

**Perfect for:** Musicians, producers, live performers

### 1. Start Ardour DAW
```bash
# Open Ardour and create a new project
# Create a Software Instrument track
# Arm the track for recording and enable monitoring
```

### 2. Start Live Streaming
```bash
python live_control_plane_cli.py
```

### 3. Try Live Generation
```
"Give me a funky bassline"
"Make it more complex" 
"Add some swing to it"
"Make it brighter"
"Stop" to end the session
```

**✅ Success:** You should see MIDI notes appearing in Ardour in real-time!

---

## 💬 Musical Conversation Setup

**Perfect for:** Songwriters, composers, creative exploration

### 1. Start Conversation Mode
```bash
python enhanced_control_plane_cli.py --conversation
```

### 2. Try Musical Dialogue
```
"I need a funky bass line for my song"
"Make it groove like Stevie Wonder"
"This chorus sounds flat, brighten it up"
"Make it more complex"
```

**✅ Success:** You should have a natural conversation with AI about music!

---

## 🎛️ Traditional Commands Setup

**Perfect for:** Developers, technical users, automation

### 1. Basic Demo
```bash
python main.py
# Expected: "Playing C Major Scale..." and 8 notes in your DAW
```

### 2. Interactive Mode
```bash
python main.py --interactive
# Try: "play scale D minor", "set tempo to 140", "stop"
```

### 3. CLI Commands
```bash
python control_plane_cli.py "play scale F# lydian"
python control_plane_cli.py "make it jazz"
python control_plane_cli.py "analyze bass"
```

**✅ Success:** You should hear MIDI notes and see command responses!

---

## 🧪 Test Your Setup

### Quick Tests for Each Path

**Live MIDI Streaming:**
```bash
python live_control_plane_cli.py
# Try: "Give me a C major scale"
# Expected: Notes appear in Ardour in real-time
```

**Musical Conversation:**
```bash
python enhanced_control_plane_cli.py --conversation
# Try: "Create a simple melody"
# Expected: Natural conversation with musical generation
```

**Traditional Commands:**
```bash
python control_plane_cli.py "play scale C major"
# Expected: Hear 8 notes in your DAW
```

---

## 🎯 What You Should See

### ✅ Live MIDI Streaming Success
- MIDI notes appear in Ardour in real-time as you speak
- Existing MIDI content changes immediately in Ardour
- Natural dialogue with AI that controls live MIDI

### ✅ Musical Conversation Success
- Natural dialogue with AI musical collaborator
- Generated MIDI files created from your requests
- Back-and-forth conversation to perfect ideas

### ✅ Traditional Commands Success
- MIDI notes playing in your DAW
- Command responses and feedback
- Visual analysis (Blue=bass, Green=melody, Purple=harmony, Orange=rhythm)

---

## 🚨 Quick Troubleshooting

**No sound?**
- Check IAC Driver is enabled and port is named "IAC Driver Bus 1"
- Verify DAW track is armed and monitoring is on
- Run: `python control_plane_cli.py status`

**Commands not working?**
- Check you're in the virtual environment: `source .venv/bin/activate`
- Verify dependencies: `pip list | grep mido`

**Need more help?**
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development issues

---

## 📚 Next Steps

### 🎵 **Live MIDI Streaming**
- [docs/guides/LIVE_MIDI_STREAMING_README.md](docs/guides/LIVE_MIDI_STREAMING_README.md) - Detailed live streaming guide
- [docs/ARDOUR_INTEGRATION.md](docs/ARDOUR_INTEGRATION.md) - Ardour DAW integration

### 💬 **Musical Conversation**
- [docs/guides/MUSICAL_CONVERSATION_README.md](docs/guides/MUSICAL_CONVERSATION_README.md) - Detailed conversation guide

### 🛠️ **Development**
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer workflows and guides
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture and design

### 📋 **Reference**
- [README.md](README.md) - Full project overview
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes
