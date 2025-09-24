# Features Guide

Complete guide to all YesAnd Music features and capabilities.

## Table of Contents

- [Live MIDI Streaming](#live-midi-streaming)
- [Musical Conversation](#musical-conversation)
- [Musical Scribe (Context-Aware AI)](#musical-scribe-context-aware-ai)
- [Musical Problem Solvers](#musical-problem-solvers)
- [DAW Integration](#daw-integration)
- [Visual Feedback System](#visual-feedback-system)
- [Musical Intelligence](#musical-intelligence)

---

## Live MIDI Streaming

**Real-Time MIDI Generation and Editing with Ardour DAW Integration**

### What It Is
Live MIDI streaming enables you to generate and stream MIDI directly to your DAW in real-time, then modify it through natural language conversation. It's like having an AI musical collaborator that can generate and modify MIDI in real-time as you work.

### Key Features
- **Real-Time MIDI Generation**: Generate musical patterns and stream directly to Ardour tracks
- **Live Editing Engine**: Modify existing MIDI content in real-time through natural language
- **Natural Language Control**: "Give me a funky bassline" → instant MIDI generation
- **Multiple Musical Styles**: Funky, jazz, blues, rock, classical, electronic
- **Thread-Safe Operations**: Real-time audio thread safety for professional use

### How to Use

#### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Enable IAC Driver
# Open Audio MIDI Setup → Window → Show MIDI Studio
# Double-click IAC Driver → check "Device is online"
# Create port named "IAC Driver Bus 1"

# 4. Start Ardour and create a MIDI track
```

#### Basic Usage
```bash
# Start live streaming
python live_control_plane_cli.py

# Try these commands:
"Give me a funky bassline"
"Create a jazz melody"
"Make a blues chord progression"
```

#### Real-Time Editing
```bash
# Modify existing content
"Make it more complex"
"Add some swing to it"
"Make it brighter"
"Simplify it a bit"
```

#### Style References
```bash
# Use musical references
"Make it groove like Stevie Wonder"
"Give it that Motown feel"
"I want something dark and moody"
```

### Advanced Features

#### Live Editing Operations
- **Velocity Control**: Adjust note velocities
- **Swing Feel**: Apply swing timing to notes
- **Accent**: Emphasize downbeats
- **Humanization**: Add natural timing and velocity variations
- **Transpose**: Change pitch of notes
- **Rhythm Changes**: Modify rhythmic patterns
- **Style Transformation**: Change musical style
- **Harmony Addition**: Add harmonic elements

#### MIDI Stream Styles
- **Basslines**: Funky, Jazz, Rock, Classical, Electronic, Blues
- **Melodies**: Jazz, Classical, Blues, Pop with proper voice leading
- **Drums**: Rock, Jazz, Funk, Electronic with realistic patterns

### Workflow Example
1. **Generate**: "Give me a funky bassline" → MIDI streams to Ardour
2. **Refine**: "Make it more complex" → Real-time modification
3. **Style**: "Make it groove like Bootsy Collins" → Style transformation
4. **Polish**: "Add some swing" → Final touches

### Troubleshooting
- **No Sound**: Check IAC Driver is enabled and port is named "IAC Driver Bus 1"
- **MIDI Not Streaming**: Verify Ardour track is armed and monitoring
- **OpenAI Errors**: Check API key is set correctly

---

## Musical Conversation

**Natural Language Musical Collaboration with AI**

### What It Is
The Musical Conversation system transforms YesAnd Music from a command-based tool into a conversational musical collaborator. Users can engage in natural musical dialogue, describe what they want in their own words, and receive intelligent musical assistance.

### Key Features
- **Natural Language Understanding**: OpenAI GPT-4 integration for musical requests
- **Musical Context Management**: Tracks project state, preferences, and conversation history
- **Musical Reference Library**: Built-in references to artists, styles, and techniques
- **Iterative Refinement**: Back-and-forth conversation to perfect ideas
- **Educational Value**: Explains musical concepts and decisions

### How to Use

#### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Start conversation mode
python enhanced_control_plane_cli.py --conversation
```

#### Example Conversations
```
🎵 User: I need a funky bass line for my song
🤖 AI: I'll create a funky bass line for you! Let me generate something with that classic syncopated groove...

🎵 User: Make it more complex
🤖 AI: Adding more complexity with syncopated rhythms and chord tones...

🎵 User: This sounds too busy, simplify it
🤖 AI: I'll simplify it while keeping the funky feel...

🎵 User: Make it groove like Bootsy Collins
🤖 AI: Perfect! Bootsy Collins is the master of funk bass. I'll add that percussive, syncopated style...
```

#### Musical References
```bash
# Use artist references
"Make it groove like Stevie Wonder"
"Give it that Motown feel"
"I want something dark and moody"

# Provide feedback
"Make it more complex"
"This is too busy, simplify it"
"Make it swing more"
"I want it in a different key"
```

#### Project Management
```bash
# Check project status
"project status"
"show project"
"current project"

# Start fresh
"clear project"
"new project"
"reset project"
```

### Advanced Features

#### Musical Reference Library
The system includes built-in references to:
- **Artists**: Stevie Wonder, Bootsy Collins, Miles Davis, etc.
- **Styles**: Motown, Jazz, Funk, Blues, Rock, Classical
- **Techniques**: Swing, Syncopation, Voice Leading, etc.

#### Feedback Processing
- **Complexity**: "Make it more complex" / "Simplify it"
- **Style**: "Make it jazzier" / "Give it a rock feel"
- **Emotion**: "Make it brighter" / "Make it darker"
- **Technical**: "Add more swing" / "Fix the harmony"

### Integration
- **Traditional Commands**: All existing commands still work
- **Enhanced Control Plane**: Provides both traditional and conversational interfaces
- **DAW Integration**: Works with all existing DAW integrations

---

## Musical Scribe (Context-Aware AI)

**Sully.ai-Inspired Context-Aware Musical Enhancement**

### What It Is
Musical Scribe is a context-aware AI system inspired by Sully.ai's medical scribe model. It analyzes your entire musical project and provides contextually appropriate enhancements based on the full musical context, not just individual tracks.

### Key Features
- **Project-Wide Analysis**: Understands entire musical projects, not just individual tracks
- **Contextual Intelligence**: Generates suggestions that fit your existing musical context
- **Sully.ai-Inspired Workflow**: Uses specialized prompts for different musical roles
- **Multiple Enhancement Options**: Provides 2-3 different approaches for each request
- **Musical Coherence**: Maintains style consistency throughout enhancements

### How to Use

#### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Use Musical Scribe commands
python control_plane_cli.py "musical scribe status"
```

#### Available Commands
```bash
# Enhance project with contextual AI
musical scribe enhance [REQUEST]
# Examples:
musical scribe enhance add a funky bassline
musical scribe enhance improve the arrangement
musical scribe enhance add some drums

# Analyze entire project context
musical scribe analyze

# Generate contextual prompt
musical scribe prompt [REQUEST]
# Examples:
musical scribe prompt create a jazz melody
musical scribe prompt add a walking bass line

# Show system status
musical scribe status
```

### How It Works

#### 1. Project Analysis
The system analyzes your entire DAW project:
- **Track Information**: Names, types, and musical content
- **Musical Context**: Key, tempo, style, harmonic progression
- **Musical Relationships**: How tracks work together
- **Enhancement Opportunities**: Specific areas for improvement

#### 2. Contextual Prompt Generation
Based on your request, it creates specialized prompts:
```
You are an expert bassist brought in to enhance this musical project.

PROJECT CONTEXT:
- Song: "My Jazz Ballad"
- Key: C major
- Tempo: 120 BPM
- Style: Jazz ballad with complex chord progression

EXISTING TRACKS:
- Piano: Complex jazz chords, busy right hand
- Drums: Soft brush pattern
- Vocals: Melodic line in upper register

MUSICAL ANALYSIS:
- Harmonic progression: Cmaj7 - Am7 - Dm7 - G7
- Rhythmic patterns: Syncopated piano, straight drum groove
- Arrangement: Sparse, needs bass foundation

CLIENT REQUEST: "Give me a funky bassline"

Please generate 2-3 different MIDI patterns that enhance this track while maintaining musical coherence with the existing arrangement.
```

#### 3. Contextual Enhancement
The AI generates contextually appropriate suggestions that:
- Fit the existing musical style
- Complement other tracks
- Address specific enhancement opportunities
- Maintain musical coherence

### Example Workflow
1. **Analyze**: `musical scribe analyze` → Understands your project
2. **Enhance**: `musical scribe enhance add a funky bassline` → Generates contextually appropriate bassline
3. **Refine**: `musical scribe enhance make it simpler` → Refines based on context
4. **Compare**: Review multiple options and choose the best fit

### Benefits
- **Context-Aware Intelligence**: Understands your entire musical project
- **Musical Coherence**: All suggestions fit the existing musical context
- **Professional Quality**: Patterns sound like they were created by a professional musician
- **Multiple Options**: Provides 2-3 different approaches for each request
- **Educational Value**: Explains musical choices and provides learning opportunities

---

## Musical Problem Solvers

**One-Command Musical Problem Solving**

### What It Is
Musical Problem Solvers address specific musical challenges with immediate results. Each solver focuses on a particular aspect of music and provides intelligent improvements.

### Available Solvers

#### Groove Improver
**Command**: `make this groove better`

**What It Does**:
- Analyzes current rhythm and timing
- Applies swing feel improvements
- Adds timing humanization
- Enhances velocity variation
- Adds syncopation for interest

**Example**:
```bash
python control_plane_cli.py "load my_song.mid"
python control_plane_cli.py "make this groove better"
# Creates: improved_groove_my_song.mid
```

#### Harmony Fixer
**Command**: `fix the harmony`

**What It Does**:
- Analyzes chord progressions
- Fixes poor voice leading
- Adjusts harmonic rhythm
- Reduces dissonance
- Improves chord resolution

**Example**:
```bash
python control_plane_cli.py "load my_song.mid"
python control_plane_cli.py "fix the harmony"
# Creates: fixed_harmony_my_song.mid
```

#### Arrangement Improver
**Command**: `improve the arrangement`

**What It Does**:
- Analyzes song structure
- Adds melodic and rhythmic variation
- Optimizes note density
- Enhances dynamic variation
- Prevents monotony

**Example**:
```bash
python control_plane_cli.py "load my_song.mid"
python control_plane_cli.py "improve the arrangement"
# Creates: improved_arrangement_my_song.mid
```

### How to Use

#### Basic Workflow
1. **Load**: `load [filename.mid]`
2. **Analyze**: `analyze all` (optional)
3. **Improve**: `make this groove better` / `fix the harmony` / `improve the arrangement`
4. **Compare**: Listen to original vs. improved version

#### Advanced Usage
```bash
# Load and analyze
python control_plane_cli.py "load my_song.mid"
python control_plane_cli.py "analyze all"

# Apply multiple improvements
python control_plane_cli.py "make this groove better"
python control_plane_cli.py "fix the harmony"
python control_plane_cli.py "improve the arrangement"

# Get suggestions
python control_plane_cli.py "get suggestions"
python control_plane_cli.py "apply suggestion 1"
```

### Benefits
- **Immediate Results**: One command solves specific musical problems
- **Audio Preview**: Improved versions saved as MIDI files
- **Educational Value**: Clear explanations of what was changed and why
- **Non-Destructive**: Original files are preserved
- **Professional Quality**: Improvements sound like they were made by a professional musician

---

## DAW Integration

**File-Based Integration with Professional DAWs**

### Supported DAWs
- **Ardour**: Complete file-based integration with project parsing
- **Logic Pro**: VST3 plugin compatibility
- **GarageBand**: AudioUnit plugin support
- **Universal**: Works with any DAW via MIDI I/O

### Ardour Integration

#### Features
- **Project File Parsing**: Automatic discovery and parsing of Ardour project files
- **Track Information**: Extract track names, types, and armed states
- **Export/Import Workflow**: Seamless MIDI file exchange
- **Lua Script Generation**: Create automation scripts for Ardour operations

#### Available Commands
```bash
# Connection
ardour connect          # Connect to Ardour DAW
ardour disconnect       # Disconnect from Ardour
ardour tracks          # List Ardour tracks

# Export/Import
ardour export selected  # Export selected region to MIDI file
ardour import [FILE]   # Import MIDI file to Ardour

# Analysis
ardour analyze selected # Analyze exported region
ardour improve selected # Improve exported region
```

#### Workflow
1. **Start Ardour** and open your project
2. **Select a region** you want to analyze
3. **Connect**: `ardour connect`
4. **Export**: `ardour export selected`
5. **Analyze**: `ardour analyze selected`
6. **Improve**: `ardour improve selected`
7. **Import**: `ardour import improved_region.mid`

### Logic Pro Integration

#### Features
- **VST3 Plugin**: Real-time MIDI effect plugin
- **OSC Control**: Real-time parameter control
- **Style Presets**: Built-in musical style presets

#### Setup
1. **Build Plugin**: `make -C build_minimal`
2. **Install**: Plugin installs to `/Users/harrisgordon/Library/Audio/Plug-Ins/VST3/`
3. **Load**: Add as MIDI Effect in Logic Pro

### GarageBand Integration

#### Features
- **AudioUnit Plugin**: Native macOS plugin support
- **MIDI Effects**: Real-time MIDI processing
- **Style Control**: Natural language style commands

#### Setup
1. **Build Plugin**: `make -C build_minimal`
2. **Install**: Plugin installs to `/Users/harrisgordon/Library/Audio/Plug-Ins/Components/`
3. **Load**: Add as MIDI Effect in GarageBand

---

## Visual Feedback System

**On-Demand Visual Feedback and Educational Display**

### What It Is
The Visual Feedback System provides color-coded visual feedback and educational content without interfering with your DAW workflow.

### Features
- **Color-Coded Highlighting**: Blue (bass), Green (melody), Purple (harmony), Orange (rhythm), Red (drums)
- **Real-Time Updates**: Live feedback as users interact without blocking audio
- **Educational Overlays**: Musical theory explanations and AI reasoning
- **Non-Intrusive Design**: Separate window that doesn't interfere with DAW workflows
- **Thread-Safe Operation**: Background processing without audio disruption

### How to Use

#### Basic Commands
```bash
# Load and analyze
load [filename.mid]
analyze bass      # Show bass line analysis
analyze melody    # Show melody analysis
analyze harmony   # Show harmony analysis
analyze rhythm    # Show rhythm analysis
analyze all       # Complete musical analysis

# Visual feedback
show feedback     # Show visual feedback summary
clear feedback    # Clear all visual feedback
```

#### Advanced Usage
```bash
# Get suggestions
get suggestions
apply suggestion [ID]

# Background analysis
# Visual feedback appears automatically when needed
```

### Color Coding
- **🔵 Blue**: Bass line elements
- **🟢 Green**: Melody elements
- **🟣 Purple**: Harmony elements
- **🟠 Orange**: Rhythm elements
- **🔴 Red**: Drum elements

### Educational Value
- **Musical Theory**: Explains musical concepts and relationships
- **AI Reasoning**: Shows why the AI made specific suggestions
- **Visual Learning**: Helps understand musical structure through color coding
- **Real-Time Feedback**: Immediate visual response to musical changes

---

## Musical Intelligence

**Core Musical Analysis and Smart Suggestions**

### What It Is
The Musical Intelligence system provides deep musical analysis and generates smart suggestions for musical improvements.

### Analysis Capabilities

#### Musical Elements
- **Bass Line Analysis**: Root motion, harmonic function, rhythm patterns
- **Melody Analysis**: Contour, intervals, voice leading
- **Harmony Analysis**: Chord progressions, voice leading, resolution
- **Rhythm Analysis**: Patterns, syncopation, groove
- **Style Analysis**: Genre detection, characteristic elements

#### Smart Suggestions
- **Harmonic Improvements**: Better chord progressions and voice leading
- **Rhythmic Enhancements**: Improved groove and timing
- **Arrangement Suggestions**: Better song structure and density
- **Style Recommendations**: Genre-appropriate enhancements

### How to Use

#### Analysis Commands
```bash
# Load project
load [filename.mid]

# Analyze specific elements
analyze bass
analyze melody
analyze harmony
analyze rhythm
analyze all

# Get suggestions
get suggestions
apply suggestion [ID]
```

#### Advanced Analysis
```bash
# Background analysis
# Analysis runs automatically in background

# Detailed analysis
analyze all
# Shows comprehensive analysis of all musical elements
```

### Educational Content
- **Musical Theory**: Explains concepts like voice leading, chord progressions, etc.
- **AI Reasoning**: Shows why specific suggestions were made
- **Learning Opportunities**: Each interaction provides educational value
- **Visual Explanations**: Color-coded analysis helps understanding

### Integration
- **Works with all features**: Analysis integrates with all other YesAnd Music features
- **Real-time updates**: Analysis updates as you make changes
- **Context awareness**: Analysis considers the full musical context
- **Educational value**: Every analysis provides learning opportunities

---

## Getting Help

### Quick Start
- **New to YesAnd Music?** Start with the [README.md](README.md)
- **Need setup help?** Check [Troubleshooting](TROUBLESHOOTING.md)
- **Want to contribute?** See [Development Guide](DEVELOPMENT.md)

### Common Issues
- **No sound?** Check IAC Driver setup and DAW track configuration
- **Commands not working?** Verify virtual environment and dependencies
- **AI features not working?** Check OpenAI API key configuration

### Support
- **Documentation**: Comprehensive guides for all features
- **Troubleshooting**: Common issues and solutions
- **Reference**: Complete command and API reference
- **Development**: Technical details and contribution guidelines

---

**Ready to explore?** Start with [Live MIDI Streaming](#live-midi-streaming) for the most interactive experience, or try [Musical Conversation](#musical-conversation) for natural language collaboration.
