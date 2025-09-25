# MVP User-Driven MIDI Generator

**High-Quality AI Musical Generation with Built-in User Feedback Integration**

This is the MVP implementation of the user-driven MIDI generator that allows you to type in any musical prompt and get back a high-quality MIDI file, with built-in user evaluation and feedback loops for continuous improvement.

## 🎯 What This MVP Does

Given a prompt like:
> "Create a funky jazz bass line in G minor at 120 BPM for 8 measures"

The system will:
1. **Extract Musical Context** - Parse key, tempo, style, instrument, length, mood, and complexity
2. **Generate with Quality Gates** - Use AI to create MIDI with built-in quality assessment
3. **Validate Musical Quality** - Ensure the output meets professional standards
4. **Learn from Feedback** - Record user ratings and comments for continuous improvement
5. **Output Professional MIDI** - Save a high-quality MIDI file ready for any DAW

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
```bash
# Install dependencies
pip install -r requirements_mvp.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

#### Single Generation
```bash
python mvp_user_driven_generator.py "Create a jazz bass line in C major"
```

#### Interactive Mode
```bash
python mvp_user_driven_generator.py --interactive
```

#### With User ID for Feedback Tracking
```bash
python mvp_user_driven_generator.py "Generate a funky drum pattern" --user-id "musician_123"
```

## 🎵 Example Prompts

The system understands natural language and extracts musical context:

### Basic Prompts
- `"Create a bass line in C major"`
- `"Generate a jazz piano melody"`
- `"Make a rock drum pattern"`

### Detailed Prompts
- `"Create a complex jazz bass line in G minor at 120 BPM for 8 measures"`
- `"Generate a melancholic piano melody in F# major at 80 BPM"`
- `"Make a funky drum pattern with ghost notes"`

### Style References
- `"Create a bass line like Jeff Ament of Pearl Jam"`
- `"Generate jazz piano in the style of Bill Evans"`
- `"Make a funky drum pattern like James Brown"`

## 🏗️ Architecture

### Core Components

#### 1. Musical Context Extractor
- **Purpose**: Parse natural language prompts to extract musical context
- **Features**: Key detection, tempo extraction, style recognition, instrument identification
- **Example**: "jazz bass line in C major at 120 BPM" → `{key: "C major", tempo: 120, style: "jazz", instrument: "bass"}`

#### 2. Musical Quality Gate
- **Purpose**: Assess and ensure musical quality of generated content
- **Criteria**: Musical coherence, style accuracy, technical quality, user preference
- **Features**: Multi-pass generation, quality validation, user feedback learning

#### 3. MIDI Generator
- **Purpose**: Generate MIDI using OpenAI with quality validation
- **Features**: Context-aware prompts, quality-driven generation, error handling
- **Integration**: OpenAI GPT-4, quality gates, user feedback

#### 4. User Feedback System
- **Purpose**: Learn from user feedback to improve future generations
- **Features**: Rating collection, comment analysis, preference learning
- **Integration**: Quality model updates, user profiling

### Quality Assessment Engine

The system uses a sophisticated quality assessment engine with four criteria:

1. **Musical Coherence (30%)** - Does the music make musical sense?
2. **Style Accuracy (25%)** - Does it match the requested style?
3. **Technical Quality (20%)** - Is it technically well-formed?
4. **User Preference (25%)** - Does it match the user's taste?

### Multi-Pass Generation

If quality is below threshold (0.7/1.0), the system:
1. Analyzes quality feedback
2. Refines the prompt based on weaknesses
3. Regenerates with improved context
4. Repeats up to 3 times for optimal quality

## 🎯 Key Features

### Musical Quality First
- **Quality Gates**: Every generation must meet professional standards
- **Multi-Pass Generation**: Automatic refinement for better quality
- **Musical Validation**: Ensures output is musically coherent and technically correct

### User Feedback Integration
- **Rating System**: Users rate generations 1-5 stars
- **Comment Collection**: Users provide detailed feedback
- **Learning System**: System learns from feedback to improve future generations
- **User Profiling**: Builds profiles of user preferences over time

### Context-Aware Generation
- **Natural Language**: Understands complex musical requests
- **Context Extraction**: Automatically extracts key, tempo, style, mood, etc.
- **Style Recognition**: Identifies musical styles and instruments
- **Length Parsing**: Understands measure, bar, and beat requirements

### Professional Output
- **MIDI Format**: Standard MIDI files compatible with any DAW
- **Quality Validation**: Ensures technical correctness
- **Descriptive Naming**: Files named based on content and timestamp
- **Ready to Use**: Generated MIDI is immediately usable in projects

## 📊 User Feedback System

### How It Works
1. **Generation**: User requests MIDI generation
2. **Quality Check**: System validates musical quality
3. **User Rating**: User rates the generation 1-5 stars
4. **Comments**: User provides optional feedback
5. **Learning**: System updates quality models based on feedback
6. **Improvement**: Future generations improve based on user preferences

### Feedback Integration
- **Real-time Learning**: System learns from each user interaction
- **Preference Modeling**: Builds models of what each user likes
- **Quality Refinement**: Improves quality assessment based on user feedback
- **Style Adaptation**: Adapts to user's preferred musical styles

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python test_mvp_user_driven.py

# Run specific test categories
python -m pytest test_mvp_user_driven.py::TestMusicalQualityGate -v
```

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Quality Tests**: Musical quality assessment validation
- **User Feedback Tests**: Feedback system functionality

### Demo Suite
```bash
# Run comprehensive demo
python demo_mvp_user_driven.py
```

## 📁 File Structure

```
mvp_user_driven_generator.py    # Main MVP system
test_mvp_user_driven.py        # Comprehensive test suite
demo_mvp_user_driven.py        # Demo and showcase script
requirements_mvp.txt           # Minimal dependencies
MVP_USER_DRIVEN_README.md      # This documentation
```

## 🎯 Success Metrics

### Quality Metrics
- **Quality Score**: Average quality score across all generations (target: 0.8+/1.0)
- **Generation Success Rate**: Percentage of high-quality generations (target: 80%+)
- **User Satisfaction**: Average user rating (target: 4.0+/5.0)

### User Engagement
- **User Retention**: Percentage of users who return (target: 60%+)
- **Feedback Rate**: Percentage of generations with user feedback (target: 50%+)
- **Generation Frequency**: Average generations per user session (target: 3+)

### Technical Performance
- **Response Time**: Average generation time (target: <10 seconds)
- **Quality Validation**: Percentage of generations passing quality gates (target: 80%+)
- **Error Rate**: Percentage of failed generations (target: <5%)

## 🔧 Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-api-key-here"
export MVP_OUTPUT_DIR="generated_midi"  # Optional: custom output directory
```

### Quality Thresholds
```python
# Adjustable in MusicalQualityGate class
quality_criteria = {
    'musical_coherence': 0.3,  # Weight for musical coherence
    'style_accuracy': 0.25,    # Weight for style accuracy
    'technical_quality': 0.2,  # Weight for technical quality
    'user_preference': 0.25    # Weight for user preference
}

quality_threshold = 0.7  # Minimum quality score for acceptance
max_attempts = 3         # Maximum generation attempts
```

## 🚀 Future Enhancements

### Short Term
- **More Style Recognition**: Expand style database and recognition
- **Advanced Quality Models**: Machine learning-based quality assessment
- **User Preference Learning**: More sophisticated preference modeling
- **Batch Generation**: Generate multiple variations at once

### Long Term
- **Real-time Generation**: Live MIDI streaming to DAWs
- **Collaborative Features**: Share and rate generations with other users
- **Advanced Context**: Harmonic analysis, rhythm pattern recognition
- **Custom Models**: User-specific AI models trained on their preferences

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository>
cd music_cursor

# Install dependencies
pip install -r requirements_mvp.txt

# Run tests
python test_mvp_user_driven.py

# Run demo
python demo_mvp_user_driven.py
```

### Code Quality
- **Testing**: All new features must include tests
- **Quality Gates**: Maintain high quality standards
- **User Feedback**: Consider user experience in all changes
- **Documentation**: Update documentation for new features

## 📄 License

This project is part of YesAnd Music. See the main project for license details.

---

## 🎉 Ready to Generate Music!

The MVP User-Driven MIDI Generator is ready for production use. It provides:

✅ **High-Quality Generation** - Professional-quality MIDI output
✅ **User Feedback Integration** - Continuous improvement through user input
✅ **Context-Aware Intelligence** - Understands complex musical requests
✅ **Quality-First Design** - Ensures every generation meets standards
✅ **Easy to Use** - Simple command-line interface
✅ **Production Ready** - Comprehensive testing and validation

**Start generating music now:**
```bash
export OPENAI_API_KEY="your-api-key-here"
python mvp_user_driven_generator.py --interactive
```
