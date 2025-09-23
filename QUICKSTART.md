# Quick Start Guide

Get YesAnd Music running in 5 minutes.

## What This Is

YesAnd Music is an AI-powered MIDI editing system that provides contextual intelligence and musical problem-solving through natural language commands. It works with your existing DAW workflow.

## Prerequisites

- macOS (tested on macOS 15.5)
- Python 3.8+
- A DAW (GarageBand, Logic Pro, or Ardour)

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

## 2. Run It (1 minute)

### Basic Demo
```bash
python main.py
# Expected: "Playing C Major Scale..." and 8 notes in your DAW
```

### Interactive Mode
```bash
python main.py --interactive
# Try: "play scale D minor", "set tempo to 140", "stop"
```

### CLI Commands
```bash
python control_plane_cli.py "play scale F# lydian"
python control_plane_cli.py "make it jazz"
```

## 3. Test Musical Intelligence (2 minutes)

### Load a MIDI File
```bash
python control_plane_cli.py "load test_simple.mid"
```

### Analyze Music
```bash
python control_plane_cli.py "analyze bass"
python control_plane_cli.py "analyze melody"
python control_plane_cli.py "analyze all"
```

### Solve Musical Problems
```bash
python control_plane_cli.py "make this groove better"
python control_plane_cli.py "fix the harmony"
python control_plane_cli.py "improve the arrangement"
```

## 4. What You Should See

- **MIDI Output**: Notes playing in your DAW
- **Visual Feedback**: Color-coded analysis (Blue=bass, Green=melody, Purple=harmony, Orange=rhythm)
- **Musical Improvements**: Better-sounding versions saved as new MIDI files
- **Educational Content**: Explanations of what the AI changed and why

## 5. Next Steps

- **For Users**: See [README.md](README.md) for full features
- **For Developers**: See [DEVELOPMENT.md](DEVELOPMENT.md) for development workflows
- **For Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

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
