# Real-Time Ardour Enhancement System

**LLM-Powered Track Enhancement with Real-Time Project Context**

This system provides real-time track enhancement in Ardour using OpenAI's GPT models, with live project state monitoring and intelligent musical suggestions.

## 🚀 Quick Start

### Prerequisites
- **macOS** (tested on macOS 15.5)
- **Python 3.8+**
- **OpenAI API key**
- **Ardour 8.9+** with OSC enabled
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

# 4. Enable OSC in Ardour
# Ardour → Preferences → OSC → Enable OSC
# Set OSC port to 3819
```

### Start Real-Time Enhancement
```bash
# Interactive mode (recommended)
python real_time_enhancement_cli.py --interactive

# Single command
python real_time_enhancement_cli.py --command enhance --request "make the bassline groovier"

# Show project status
python real_time_enhancement_cli.py --status
```

## 🎵 How It Works

### Real-Time Architecture
```
Ardour OSC → Project State Capture → LLM Enhancement → MIDI Generation → Ardour Import
     ↓              ↓                      ↓                ↓              ↓
Live Project    Musical Context      AI Analysis      MIDI Patterns    Import Script
State          Analysis             & Generation     & Validation      & Automation
```

### Key Components

1. **OSC Monitor** (`ardour_osc_monitor.py`): Real-time monitoring of Ardour project state
2. **State Capture** (`project_state_capture.py`): Musical context analysis and enhancement opportunities
3. **MIDI Analyzer** (`midi_stream_analyzer.py`): Real-time MIDI stream analysis
4. **LLM Enhancer** (`llm_track_enhancer.py`): OpenAI-powered track enhancement
5. **Pattern Parser** (`midi_pattern_parser.py`): MIDI pattern generation and validation
6. **Integration** (`real_time_ardour_enhancer.py`): Complete system orchestration

## 🎯 Features

### Real-Time Project Monitoring
- **Live State Capture**: Monitors Ardour project changes in real-time via OSC
- **Musical Context Analysis**: Analyzes harmonic progression, rhythm, and style
- **Enhancement Opportunities**: Identifies areas for improvement
- **Track Analysis**: Individual track analysis with musical role detection

### LLM-Powered Enhancement
- **Context-Aware Suggestions**: Uses full project context for intelligent enhancements
- **Multiple Enhancement Types**: Bass, drums, melody, harmony, and general enhancements
- **Musical Justification**: Explains musical choices and reasoning
- **Confidence Scoring**: Provides confidence levels for generated patterns

### MIDI Pattern Generation
- **Universal MIDI Format**: Consistent MIDI data structure
- **Pattern Validation**: Validates generated patterns for correctness
- **Ardour Optimization**: Optimizes patterns for Ardour import
- **Import Automation**: Generates Lua scripts for Ardour automation

## 🎼 Usage Examples

### Interactive Mode
```bash
python real_time_enhancement_cli.py --interactive

enhance> enhance make the bassline groovier
🎵 Enhancing track: make the bassline groovier
✅ Enhancement completed in 2.34s
📊 Confidence: 0.87
🎼 Generated 3 patterns
  1. Walking Bass Pattern (Confidence: 0.89)
     Provides solid rhythmic foundation with root notes
  2. Syncopated Bass Pattern (Confidence: 0.85)
     Adds rhythmic interest with off-beat emphasis
  3. Complex Bass Pattern (Confidence: 0.82)
     Advanced bass line with chord tones and rhythm variations

enhance> enhance drums add ghost notes
🎵 Enhancing track: add ghost notes
✅ Enhancement completed in 1.98s
📊 Confidence: 0.91
🎼 Generated 2 patterns
  1. Ghost Note Pattern (Confidence: 0.93)
     Adds subtle ghost notes for realistic drum feel
  2. Complex Ghost Pattern (Confidence: 0.89)
     Advanced ghost note pattern with dynamic variation
```

### Command Line Mode
```bash
# Enhance bass line
python real_time_enhancement_cli.py --command enhance --request "make the bassline groovier" --enhancement-type bass

# Enhance specific track
python real_time_enhancement_cli.py --command enhance --request "add more complexity" --track-id "1"

# Show suggestions
python real_time_enhancement_cli.py --suggestions

# Show project status
python real_time_enhancement_cli.py --status
```

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key"  # Required for LLM features
export MIDI_PORT_NAME="IAC Driver Bus 1"     # MIDI port name
export OSC_IP_ADDRESS="127.0.0.1"           # OSC IP address
export OSC_PORT=3819                         # OSC port number
export DEBUG=1                               # Enable debug output
```

### Ardour OSC Setup
1. **Enable OSC in Ardour**:
   - Ardour → Preferences → OSC
   - Check "Enable OSC"
   - Set port to 3819

2. **Configure OSC Messages**:
   - Enable track information
   - Enable region information
   - Enable selection information
   - Enable MIDI data

### MIDI Setup
1. **Enable IAC Driver**:
   - Audio MIDI Setup → Window → Show MIDI Studio
   - Double-click IAC Driver
   - Check "Device is online"
   - Create port named "IAC Driver Bus 1"

2. **Configure Ardour MIDI**:
   - Create MIDI track in Ardour
   - Set input to "IAC Driver Bus 1"
   - Enable track monitoring

## 📊 API Reference

### RealTimeArdourEnhancer
```python
from real_time_ardour_enhancer import RealTimeArdourEnhancer

# Initialize enhancer
enhancer = RealTimeArdourEnhancer(openai_api_key="your-key")

# Start session
session_id = enhancer.start_enhancement_session()

# Enhance track
result = enhancer.enhance_track("make the bassline groovier", enhancement_type="bass")

# Get suggestions
suggestions = enhancer.get_enhancement_suggestions()

# Stop session
enhancer.stop_enhancement_session()
```

### EnhancementRequest
```python
from llm_track_enhancer import EnhancementRequest

request = EnhancementRequest(
    user_request="make the bassline groovier",
    track_id="1",
    enhancement_type="bass",
    context=project_context
)
```

### MIDIPattern
```python
from llm_track_enhancer import MIDIPattern

pattern = MIDIPattern(
    name="Walking Bass Pattern",
    description="Provides solid rhythmic foundation",
    midi_data=[
        {"pitch": 36, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0}
    ],
    confidence_score=0.89,
    enhancement_type="bass",
    musical_justification="Root notes provide harmonic foundation"
)
```

## 🧪 Testing

### Run Integration Tests
```bash
python test_real_time_integration.py
```

### Test Individual Components
```bash
# Test OSC monitor
python -c "from ardour_osc_monitor import ArdourOSCMonitor; print('OSC Monitor OK')"

# Test state capture
python -c "from project_state_capture import ProjectStateCapture; print('State Capture OK')"

# Test LLM enhancer
python -c "from llm_track_enhancer import LLMTrackEnhancer; print('LLM Enhancer OK')"
```

## 🚨 Troubleshooting

### Common Issues

#### OSC Connection Failed
```
❌ Failed to start OSC monitoring
```
**Solution**: 
1. Enable OSC in Ardour (Preferences → OSC)
2. Check Ardour is running
3. Verify OSC port (default: 3819)

#### No Project State
```
❌ No project state available
```
**Solution**:
1. Open a project in Ardour
2. Ensure OSC is enabled
3. Check OSC message configuration

#### LLM Enhancement Failed
```
❌ Enhancement failed: OpenAI API error
```
**Solution**:
1. Check OpenAI API key: `echo $OPENAI_API_KEY`
2. Verify API key is valid
3. Check internet connection

#### MIDI Import Failed
```
❌ Failed to import MIDI to Ardour
```
**Solution**:
1. Check IAC Driver is enabled
2. Verify MIDI port name
3. Check Ardour MIDI track configuration

### Debug Mode
```bash
export DEBUG=1
python real_time_enhancement_cli.py --interactive
```

## 📁 File Structure

```
real_time_enhancement/
├── ardour_osc_monitor.py          # Real-time OSC monitoring
├── project_state_capture.py       # Project state analysis
├── midi_stream_analyzer.py        # MIDI stream analysis
├── llm_track_enhancer.py          # LLM enhancement engine
├── midi_pattern_parser.py         # MIDI pattern generation
├── real_time_ardour_enhancer.py   # Main integration system
├── real_time_enhancement_cli.py   # CLI interface
├── test_real_time_integration.py  # Integration tests
└── generated_patterns/            # Generated MIDI files
    ├── pattern_1.mid
    ├── pattern_2.mid
    └── ...
```

## 🔮 Future Enhancements

### Planned Features
- **Real-Time MIDI Streaming**: Direct MIDI output to Ardour
- **Advanced Pattern Recognition**: ML-based musical pattern analysis
- **Multi-DAW Support**: Support for Logic Pro, Pro Tools, etc.
- **Collaborative Features**: Multi-user enhancement sessions
- **Pattern Library**: Save and reuse enhancement patterns

### Integration Opportunities
- **VST Plugin**: Real-time MIDI effect plugin
- **Web Interface**: Browser-based enhancement interface
- **Mobile App**: iOS/Android companion app
- **API Server**: REST API for external integrations

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd music_cursor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_real_time_integration.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all functions
- Write tests for new features

## 📄 License

This project is part of YesAnd Music. See [LICENSE](LICENSE) for details.

---

**Ready to enhance your tracks?** Start with the [Quick Start](#-quick-start) guide and begin creating amazing music with AI-powered assistance!
