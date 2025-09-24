# Reference

Complete command and API reference for YesAnd Music.

## Table of Contents

- [Command Line Interfaces](#command-line-interfaces)
- [Traditional Commands](#traditional-commands)
- [Musical Conversation Commands](#musical-conversation-commands)
- [Musical Scribe Commands](#musical-scribe-commands)
- [Live MIDI Streaming Commands](#live-midi-streaming-commands)
- [DAW Integration Commands](#daw-integration-commands)
- [Visual Feedback Commands](#visual-feedback-commands)
- [Musical Problem Solvers](#musical-problem-solvers)
- [Configuration Options](#configuration-options)
- [API Reference](#api-reference)

---

## Command Line Interfaces

### Main Entry Points

#### Traditional Control Plane
```bash
python control_plane_cli.py [COMMAND]
```
- **Purpose**: Traditional command-based interface
- **Features**: MIDI control, analysis, problem solving
- **Best for**: Scripting and automation

#### Enhanced Control Plane (Musical Conversation)
```bash
python enhanced_control_plane_cli.py [OPTIONS] [COMMAND]
```
- **Purpose**: Conversational AI interface
- **Features**: Natural language conversation, iterative refinement
- **Best for**: Interactive musical collaboration

#### Live MIDI Streaming
```bash
python live_control_plane_cli.py [OPTIONS] [COMMAND]
```
- **Purpose**: Real-time MIDI generation and editing
- **Features**: Live streaming to Ardour, real-time editing
- **Best for**: Live musical creation and performance

### Command Line Options

#### Enhanced Control Plane Options
```bash
--conversation          # Start in conversation mode
--openai-key KEY        # Set OpenAI API key
--verbose               # Enable verbose output
--help-enhanced         # Show enhanced help
```

#### Live MIDI Streaming Options
```bash
--command COMMAND       # Execute single command
--track-name NAME       # Set custom track name
--verbose               # Enable verbose output
```

---

## Traditional Commands

### Basic MIDI Control

#### Scale Commands
```bash
play scale [KEY] [MODE]     # Play musical scale
# Examples:
play scale C major
play scale D minor
play scale F# lydian
play scale Bb dorian
```

#### Arpeggio Commands
```bash
play arpeggio [KEY] [CHORD] [OCTAVES]  # Play chord arpeggio
# Examples:
play arpeggio C major 2
play arpeggio Dm7 3
play arpeggio F#maj7 1
```

#### Random Note Commands
```bash
play random [COUNT] [OCTAVE]  # Play random notes
# Examples:
play random 8 4
play random 16 3
```

#### Control Commands
```bash
set tempo [BPM]           # Set tempo
set key [KEY] [MODE]      # Set key and mode
set density [0.0-1.0]     # Set note density
set velocity [0-127]      # Set note velocity
set randomness [0.0-1.0]  # Set randomness level
stop                      # Stop playback
```

### MIDI File Operations

#### File Loading
```bash
load [FILENAME]           # Load MIDI file
# Examples:
load my_song.mid
load test_simple.mid
load demo_jazz_melody.mid
```

#### File Saving
```bash
save [FILENAME]           # Save current project
# Examples:
save my_improved_song.mid
save enhanced_groove.mid
```

### Status and Information

#### System Status
```bash
status                    # Show system status
help                      # Show available commands
version                   # Show version information
```

---

## Musical Conversation Commands

### Conversation Control

#### Starting Conversations
```bash
start conversation        # Start conversation mode
conversation mode         # Alternative start command
```

#### Project Management
```bash
project status            # Show current project status
show project              # Display project details
current project           # Show current project info
```

#### Project Control
```bash
clear project             # Clear current project
new project               # Start new project
reset project             # Reset project state
```

### Natural Language Commands

#### Musical Generation
```bash
# Generate musical content
"I need a funky bass line"
"Create a jazz melody"
"Make a blues chord progression"
"Generate a rock drum pattern"
```

#### Style and Feel
```bash
# Apply musical styles
"Make it groove like Stevie Wonder"
"Give it that Motown feel"
"I want something dark and moody"
"Make it sound like Miles Davis"
```

#### Feedback and Refinement
```bash
# Provide feedback
"Make it more complex"
"This is too busy, simplify it"
"Make it swing more"
"I want it in a different key"
"Make it brighter"
"Add some reverb"
```

#### Analysis and Explanation
```bash
# Ask for explanations
"Explain what you just did"
"Why did you choose that chord?"
"What makes this funky?"
"How can I improve this?"
```

---

## Musical Scribe Commands

### Context-Aware Enhancement

#### Enhancement Commands
```bash
musical scribe enhance [REQUEST]    # Enhance project with contextual AI
# Examples:
musical scribe enhance add a funky bassline
musical scribe enhance improve the arrangement
musical scribe enhance add some drums
musical scribe enhance make the bass more supportive
musical scribe enhance add a walking bass line
```

#### Analysis Commands
```bash
musical scribe analyze              # Analyze entire project context
musical scribe status               # Show Musical Scribe system status
```

#### Prompt Generation
```bash
musical scribe prompt [REQUEST]     # Generate contextual prompt
# Examples:
musical scribe prompt create a jazz melody
musical scribe prompt add a walking bass line
musical scribe prompt improve the harmony
```

### How Musical Scribe Works

1. **Project Analysis**: Analyzes entire DAW project for context
2. **Musical Context**: Understands key, tempo, style, and relationships
3. **Contextual Prompt**: Creates specialized prompt with project context
4. **Enhanced Generation**: Generates contextually appropriate suggestions
5. **Multiple Options**: Provides 2-3 different approaches

---

## Live MIDI Streaming Commands

### Real-Time Generation

#### Basic Generation
```bash
# Generate musical content
"Give me a funky bassline"
"Create a jazz melody"
"Make a blues chord progression"
"Generate a rock drum pattern"
```

#### Style-Based Generation
```bash
# Different musical styles
"Give me a funky bassline"
"Create a jazz melody"
"Make a blues progression"
"Generate a rock drum pattern"
"Create a classical string section"
```

### Real-Time Editing

#### Live Modifications
```bash
# Modify existing content
"Make it more complex"
"Add some swing to it"
"Make it brighter"
"Simplify it a bit"
"Change the rhythm pattern"
```

#### Style Changes
```bash
# Transform musical style
"Make it groove like Stevie Wonder"
"Give it that Motown feel"
"Change to jazz style"
"Make it sound like Miles Davis"
```

#### Technical Modifications
```bash
# Specific technical changes
"Make the bass higher"
"Add more accent to the downbeats"
"Humanize the timing"
"Change the tempo"
"Add more reverb"
```

### Live Editing Operations

#### Velocity Control
```bash
"Make it louder"          # Increase velocity
"Make it softer"          # Decrease velocity
"Add more dynamics"       # Increase velocity variation
```

#### Timing Modifications
```bash
"Add some swing"          # Apply swing feel
"Make it more straight"   # Remove swing
"Humanize the timing"     # Add natural timing variations
```

#### Harmonic Changes
```bash
"Make it brighter"        # Transpose up
"Make it darker"          # Transpose down
"Add harmony"             # Add harmonic elements
"Simplify the chords"     # Reduce chord complexity
```

---

## DAW Integration Commands

### Ardour Integration

#### Connection Commands
```bash
ardour connect            # Connect to Ardour DAW
ardour disconnect         # Disconnect from Ardour
ardour tracks            # List Ardour tracks
```

#### Export/Import Commands
```bash
ardour export selected    # Export selected region to MIDI file
ardour import [FILE]     # Import MIDI file to Ardour
# Examples:
ardour import my_song.mid
ardour import improved_groove.mid
```

#### Analysis Commands
```bash
ardour analyze selected   # Analyze exported region
ardour improve selected   # Improve exported region
```

### Workflow Example
```bash
# 1. Connect to Ardour
ardour connect

# 2. List available tracks
ardour tracks

# 3. Export selected region
ardour export selected

# 4. Analyze the region
ardour analyze selected

# 5. Improve the region
ardour improve selected

# 6. Import improved version
ardour import improved_region.mid
```

---

## Visual Feedback Commands

### Analysis Commands
```bash
analyze bass              # Show bass line analysis
analyze melody            # Show melody analysis
analyze harmony           # Show harmony analysis
analyze rhythm            # Show rhythm analysis
analyze all               # Complete musical analysis
```

### Visual Feedback Control
```bash
show feedback             # Show visual feedback summary
clear feedback            # Clear all visual feedback
```

### Suggestion Commands
```bash
get suggestions           # Get improvement suggestions
apply suggestion [ID]     # Apply specific suggestion
# Examples:
apply suggestion 1
apply suggestion 2
```

### Color Coding
- **🔵 Blue**: Bass line elements
- **🟢 Green**: Melody elements
- **🟣 Purple**: Harmony elements
- **🟠 Orange**: Rhythm elements
- **🔴 Red**: Drum elements

---

## Musical Problem Solvers

### Groove Improver
```bash
make this groove better   # Improve rhythm and timing
```
**What it does**:
- Applies swing feel improvements
- Adds timing humanization
- Enhances velocity variation
- Adds syncopation for interest

### Harmony Fixer
```bash
fix the harmony           # Fix harmonic issues
```
**What it does**:
- Analyzes chord progressions
- Fixes poor voice leading
- Adjusts harmonic rhythm
- Reduces dissonance

### Arrangement Improver
```bash
improve the arrangement   # Enhance song structure
```
**What it does**:
- Analyzes song structure
- Adds melodic and rhythmic variation
- Optimizes note density
- Enhances dynamic variation

---

## Configuration Options

### Environment Variables

#### Required
```bash
export OPENAI_API_KEY="your-openai-api-key"  # For AI features
```

#### Optional
```bash
export MIDI_PORT_NAME="IAC Driver Bus 1"     # MIDI port name
export OSC_IP_ADDRESS="127.0.0.1"           # OSC IP address
export OSC_PORT=3819                         # OSC port number
export ARDOUR_PATH="/Applications/Ardour.app/Contents/MacOS/ardour"  # Ardour path
export DEBUG=1                               # Enable debug output
```

### Configuration Files

#### requirements.txt
```
mido>=1.2.10
python-rtmidi>=1.5.0
python-osc>=1.7.4
openai>=1.0.0
```

#### config.py
```python
# MIDI Configuration
MIDI_PORT_NAME = "IAC Driver Bus 1"
MIDI_CHANNEL = 0

# OSC Configuration
OSC_IP_ADDRESS = "127.0.0.1"
OSC_PORT = 3819

# Ardour Configuration
ARDOUR_PATH = "/Applications/Ardour.app/Contents/MacOS/ardour"
```

---

## API Reference

### Core Classes

#### ControlPlane
```python
class ControlPlane:
    def execute(self, command: str) -> str
    def get_status(self) -> Dict[str, Any]
    def load_project(self, filename: str) -> bool
    def save_project(self, filename: str) -> bool
```

#### MusicalConversationEngine
```python
class MusicalConversationEngine:
    def process_conversation(self, user_input: str) -> MusicalResponse
    def get_musical_context(self) -> Dict[str, Any]
    def add_musical_reference(self, reference: MusicalReference) -> None
```

#### MusicalScribeEngine
```python
class MusicalScribeEngine:
    def enhance_music(self, project_path: str, user_request: str) -> MusicalScribeResult
    def analyze_project(self, project_path: str) -> ProjectAnalysis
    def generate_prompt(self, context: Dict, request: str) -> str
```

#### ArdourIntegration
```python
class ArdourIntegration:
    def connect(self) -> bool
    def disconnect(self) -> None
    def list_tracks(self) -> List[Track]
    def export_selected_region(self) -> Optional[str]
    def import_midi_file(self, filename: str) -> bool
```

### Data Structures

#### Universal Note Format
```python
{
    'pitch': int,                    # MIDI note number
    'velocity': int,                 # Note velocity (0-127)
    'start_time_seconds': float,     # Start time in seconds
    'duration_seconds': float,       # Note duration in seconds
    'track_index': int              # Track number
}
```

#### MusicalResponse
```python
class MusicalResponse:
    success: bool
    message: str
    generated_content: Optional[List[Dict]]
    suggestions: List[str]
    confidence: float
```

#### ProjectAnalysis
```python
class ProjectAnalysis:
    project_info: Dict[str, Any]
    tracks: List[Track]
    musical_context: Dict[str, Any]
    enhancement_opportunities: List[str]
```

### Utility Functions

#### MIDI I/O
```python
def parse_midi_file(filename: str) -> List[Dict[str, Any]]
def save_midi_file(notes: List[Dict[str, Any]], filename: str) -> bool
def validate_midi_notes(notes: List[Dict[str, Any]]) -> bool
```

#### Musical Analysis
```python
def analyze_bass_line(notes: List[Dict[str, Any]]) -> BassAnalysis
def analyze_melody(notes: List[Dict[str, Any]]) -> MelodyAnalysis
def analyze_harmony(notes: List[Dict[str, Any]]) -> HarmonyAnalysis
def analyze_rhythm(notes: List[Dict[str, Any]]) -> RhythmAnalysis
```

#### Musical Transformations
```python
def apply_swing(notes: List[Dict[str, Any]], swing_ratio: float) -> List[Dict[str, Any]]
def apply_humanization(notes: List[Dict[str, Any]], intensity: float) -> List[Dict[str, Any]]
def transpose_notes(notes: List[Dict[str, Any]], semitones: int) -> List[Dict[str, Any]]
def adjust_velocity(notes: List[Dict[str, Any]], factor: float) -> List[Dict[str, Any]]
```

---

## Error Handling

### Common Error Messages

#### MIDI Errors
```
"Port not found"          # IAC Driver not enabled
"MIDI file not found"     # File doesn't exist
"Invalid MIDI format"     # Corrupted or invalid file
```

#### Command Errors
```
"Unknown command"         # Command not recognized
"Invalid parameters"      # Wrong parameter format
"Command failed"          # Execution error
```

#### AI Errors
```
"OpenAI API key not set"  # Missing API key
"LLM response error"      # AI service error
"Context analysis failed" # Musical context error
```

### Debug Mode
```bash
export DEBUG=1
python control_plane_cli.py "your command"
```

---

## Performance Characteristics

### Response Times
- **Traditional Commands**: < 100ms
- **LLM Conversations**: 1-3 seconds
- **Pattern Generation**: < 500ms
- **Live MIDI Streaming**: < 100ms
- **Musical Analysis**: < 1 second

### Memory Usage
- **Base System**: ~50MB
- **LLM Integration**: +50MB
- **Live Streaming**: +25MB
- **Visual Feedback**: +10MB

### Real-Time Safety
- **Audio Thread**: No blocking operations
- **MIDI Processing**: Non-blocking with timer-based events
- **Visual Feedback**: Separate thread
- **Background Analysis**: Non-interfering

---

**Need more help?** Check out the [Features Guide](FEATURES.md) for detailed usage examples, or see [Troubleshooting](TROUBLESHOOTING.md) for common issues and solutions.
