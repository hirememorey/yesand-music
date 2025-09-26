# Quick Start Guide

This guide will get you up and running with the Enhanced Musical Conversation System in minutes.

## What Works

### 1. Enhanced Musical Conversation System (PRIMARY)
```bash
python enhanced_musical_conversation_cli.py --demo
python enhanced_musical_conversation_cli.py --interactive
```
- **Status**: ✅ Fully working
- **Purpose**: Natural musical conversation with intent discovery
- **Key Features**: Conversational discovery, creative enhancement, prompt generation

### 2. Security-First Real-Time Enhancement
```bash
python secure_enhancement_cli.py --status
python secure_enhancement_cli.py --interactive
```
- **Status**: ✅ Working (requires OpenAI API key)
- **Purpose**: Secure AI-powered track enhancement
- **Key Features**: Built-in security, rate limiting, health monitoring

### 3. Real-Time Ardour Enhancement
```bash
python real_time_enhancement_cli.py --status
python real_time_enhancement_cli.py --interactive
```
- **Status**: ⚠️ Requires OpenAI API key and Ardour setup
- **Purpose**: Live LLM-powered track enhancement with auto-import
- **Key Features**: OSC monitoring, context analysis, automatic MIDI import

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (for AI features)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd music_cursor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Test Everything Works
```bash
# Test the enhanced conversation system
python enhanced_musical_conversation_cli.py --demo

# Test security-first system
python secure_enhancement_cli.py --status

# Test core functionality
python test_simple_functionality.py
```

## Getting Started

### 1. Try the Demo
```bash
python enhanced_musical_conversation_cli.py --demo
```
This runs a simulated conversation showing how the system works.

### 2. Start Interactive Mode
```bash
python enhanced_musical_conversation_cli.py --interactive
```
This starts an interactive conversation where you can describe your musical vision.

### 3. With Initial Input
```bash
python enhanced_musical_conversation_cli.py --interactive --input "I'm working on a jazz piece"
```
This starts with your initial musical idea.

## How It Works

### 1. Intent Discovery
The system asks questions to understand your musical vision:
- What style/genre are you working in?
- What tempo and key signature?
- What instrument are you generating for?
- What mood or feeling should it convey?

### 2. Creative Enhancement
Based on your responses, the system suggests creative enhancements:
- Rhythmic improvements
- Harmonic extensions
- Melodic development
- Timbral enhancements

### 3. Prompt Generation
The system creates rich, contextual prompts for MIDI generation that capture your complete musical vision.

## Example Conversation

```
🎵 You: I'm working on a jazz piece
🤖 AI: Welcome to your musical discovery session! I'm here to help you explore and clarify your musical vision...

🎵 You: It's in G minor at 120 BPM
🤖 AI: I understand you're working on G minor at 120 for harmonic...

🎵 You: I want a mysterious, dark sound like Miles Davis
🤖 AI: I picked up several musical ideas from what you said:
     - Timbral: mysterious, dark sound like Miles
     - Emotional: want a mysterious, dark sound
     
     💡 Musical Insights: Harmonic elements are well-defined, Emotional character is clear

🎵 You: Swung eighths for the rhythm
🤖 AI: I picked up several musical ideas from what you said:
     - Rhythmic: for the rhythm, Swung eighths for, Swung eighths for the
     
     💡 Musical Insights: You have a clear rhythmic vision, Harmonic elements are well-defined
```

## Available Commands

### Interactive Mode Commands
- `help` - Show available commands
- `status` - Show system status
- `context` - Show current musical context
- `discovery` - Show intent discovery summary
- `suggestions` - Show musical suggestions
- `enhancements` - Show creative enhancement suggestions
- `prompt` - Show generated MIDI prompt
- `generate <type>` - Generate specific suggestions
- `enhance <level>` - Apply creative enhancements
- `quit` - Exit the system

### Command Examples
```bash
# Show current context
context

# Show discovery summary
discovery

# Generate prompt
prompt

# Apply high-level enhancements
enhance high
```

## Troubleshooting

### Common Issues

1. **EOF Error**: If you get an EOF error, use demo mode instead:
   ```bash
   python enhanced_musical_conversation_cli.py --demo
   ```

2. **Missing OpenAI API Key**: Set your API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Import Errors**: Make sure you're in the correct directory and have activated the virtual environment:
   ```bash
   source .venv/bin/activate
   cd music_cursor
   ```

### Getting Help

- Check the [Development Guide](DEVELOPMENT.md) for detailed setup
- Look at the test files for usage examples
- Run the demo mode to see how the system works

## Next Steps

1. **Explore the System**: Try different musical ideas and see how the system responds
2. **Read the Code**: Check out the source code to understand how it works
3. **Contribute**: See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines
4. **Extend**: Add new features or improve existing ones

The Enhanced Musical Conversation System is designed to be intuitive and natural - just describe your musical vision and let the system guide you through the discovery process!