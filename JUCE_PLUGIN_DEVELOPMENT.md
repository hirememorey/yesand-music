# JUCE Plugin Development: YesAnd Music AI Collaborator

This document outlines the development of a native DAW plugin using the JUCE framework to support the YesAnd Music AI-powered musical collaboration vision.

## Project Overview

**Plugin Name**: YesAnd Music AI Collaborator  
**Type**: MIDI Effect Plugin with AI Integration  
**Formats**: VST3, AudioUnit (AU), Ardour Plugin  
**Purpose**: Native DAW integration for AI-powered musical collaboration

## Vision Integration

This JUCE plugin represents the **future direction** of YesAnd Music, providing:

- **Native DAW Integration**: Text input directly in Ardour interface
- **AI-Powered Generation**: Real-time MIDI generation from natural language prompts
- **Automatic Track Management**: Create and modify tracks based on user requests
- **Zero Context Switching**: Stay in the DAW, never leave for external tools
- **Professional Workflow**: Feels like a built-in DAW feature

## Future Architecture

### Target User Experience
```
User opens Ardour → Loads YesAnd Music plugin → Types "a bass line that wouldn't feel out of place in a Red Hot Chili Peppers song" → Clicks Send → Plugin creates new MIDI track with generated bass line
```

### Core Components (Planned)
- **Text Input UI**: Native text input field in plugin interface
- **Send Button**: Triggers AI generation and track creation
- **AI Integration**: Real-time LLM processing within the plugin
- **Track Management**: Direct Ardour track creation and modification
- **MIDI Generation**: Real-time MIDI pattern creation and import

## Technical Architecture

### Real-Time Safety Constraints

#### ✅ Allowed in Audio Thread
- Simple arithmetic operations
- Array access with fixed bounds
- Function calls to real-time safe functions
- Reading from pre-allocated buffers
- Writing to pre-allocated output buffers

#### ❌ Forbidden in Audio Thread
- Memory allocation (`new`, `malloc`, `std::vector::push_back`)
- Locking mechanisms (`std::mutex`, `CriticalSection`)
- File I/O operations
- Blocking calls (`sleep`, `wait`)
- Dynamic container resizing
- String operations that allocate memory
- **Console output** (`std::cout`, `printf`, `juce::Logger::writeToLog`)
- **Any logging or debugging output**

### Critical Real-Time Safety Guidelines

#### The Most Common Bugs That Destroy Performance

**1. Console Output in processBlock**
```cpp
// ❌ NEVER DO THIS - Will cause audio dropouts
void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) {
    std::cout << "Processing MIDI..." << std::endl;  // FORBIDDEN!
}
```

**2. Memory Allocation in processBlock**
```cpp
// ❌ NEVER DO THIS - Will cause audio dropouts
void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) {
    std::vector<int> notes;  // FORBIDDEN!
    notes.push_back(60);     // FORBIDDEN!
}
```

**3. Thread-Unsafe Parameter Access**
```cpp
// ❌ NEVER DO THIS - Will cause crashes
class PluginProcessor {
    float swingRatio = 0.5f;  // NOT thread-safe!
    
    void processBlock(...) {
        if (swingRatio > 0.5f) {  // CRASH RISK!
            // process
        }
    }
};
```

**4. The Velocity Overwriting Bug (Most Destructive)**
```cpp
// ❌ DESTROYS HUMAN PERFORMANCE
if (isDownBeat) {
    newVelocity = 127;  // Overwrites original velocity!
} else {
    newVelocity = 80;   // Overwrites original velocity!
}

// ✅ PRESERVES HUMAN PERFORMANCE
float newVelocity = originalVelocity;
if (isDownBeat) {
    newVelocity += style.accentAmount;  // Modifies, not overwrites
}
newVelocity = juce::jlimit(0.0f, 127.0f, newVelocity);
```

### Core Components

1. **PluginProcessor** - Main audio/MIDI processing class
2. **StyleTransferEngine** - Real-time safe MIDI transformation engine
3. **PluginEditor** - UI for parameter control
4. **AudioProcessorValueTreeState** - Thread-safe parameter management system

### Critical Parameter Management

#### ❌ WRONG: Simple Member Variables
```cpp
class PluginProcessor {
    float swingRatio = 0.5f;      // NOT thread-safe!
    float accentAmount = 20.0f;    // Will cause crashes!
    
    void processBlock(...) {
        if (swingRatio > 0.5f) {  // CRASH RISK!
            // process
        }
    }
};
```

#### ✅ CORRECT: AudioProcessorValueTreeState
```cpp
class PluginProcessor : public juce::AudioProcessor {
    AudioProcessorValueTreeState parameters;
    
    // Parameter IDs
    static constexpr const char* SWING_RATIO_ID = "swingRatio";
    static constexpr const char* ACCENT_AMOUNT_ID = "accentAmount";
    
    void processBlock(...) {
        // Thread-safe parameter access
        float swingRatio = *parameters.getRawParameterValue(SWING_RATIO_ID);
        float accentAmount = *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
        
        // Safe to use in audio thread
        if (swingRatio > 0.5f) {
            // process
        }
    }
};
```

## Implementation Status

### ✅ Completed (Phase 1)

#### Basic Plugin Structure
- [x] JUCE project setup with Projucer
- [x] VST3 and AudioUnit plugin formats configured
- [x] MIDI input/output channels set to 16
- [x] Basic plugin framework implemented

#### Core Style Transformation Engine
- [x] **StyleParameters struct** - Defines swing ratio, accent amount, and humanization parameters
- [x] **Modular transformation functions** - Pure, testable transformation functions
- [x] **Swing transformation** - Off-beat note timing adjustment
- [x] **Accent transformation** - Down-beat velocity enhancement
- [x] **Humanization transformation** - Subtle timing and velocity variations for authentic feel
- [x] **Real-time safety** - No memory allocation or blocking calls

#### Key Features Implemented
```cpp
struct StyleParameters {
    float swingRatio = 0.5f; // 0.5 = straight, > 0.5 = swing
    float accentAmount = 20.0f; // Velocity to add to accented beats
    float humanizeTimingAmount = 0.0f; // 0.0 = no timing variation, 1.0 = maximum
    float humanizeVelocityAmount = 0.0f; // 0.0 = no velocity variation, 1.0 = maximum
};
```

**Swing Logic**:
- Detects off-beat notes (8th note positions)
- Applies configurable swing delay based on `swingRatio`
- Converts beat delay to sample offset for real-time processing

**Accent Logic**:
- Detects down-beat notes (close to integer beat positions)
- Adds `accentAmount` to velocity for emphasis
- Clips final velocity to valid MIDI range (0-127)

**Humanization Logic**:
- Adds subtle timing variations (±5ms maximum) for natural feel
- Adds subtle velocity variations (±10 units maximum) for natural dynamics
- Critical velocity preservation: Modifies original values, never overwrites
- Real-time safe random number generation with pre-seeded Random generator

### 🔄 In Progress (Phase 2)

#### Parameter Control System
- [ ] **UI Parameters** - Real-time parameter control
- [ ] **Parameter Smoothing** - Smooth parameter changes to avoid clicks
- [ ] **MIDI Learn** - Map parameters to MIDI controllers
- [ ] **Preset Management** - Save/load style configurations

#### Advanced Style Transformations
- [x] **Humanization** - Subtle timing and velocity variations for authentic human feel
- [ ] **Velocity Curves** - Dynamic shaping of note velocities
- [ ] **Rhythmic Patterns** - Complex accent and swing patterns
- [ ] **Style Presets** - Jazz, classical, electronic, etc.

### 📋 Planned (Phase 3)

#### Integration Features
- [ ] **OSC Control** - Remote control via Open Sound Control
- [ ] **Tempo Detection** - Automatic tempo detection from host DAW
- [ ] **MIDI Channel Routing** - Process specific MIDI channels
- [ ] **Bypass Functionality** - Real-time bypass without artifacts

#### Advanced Features
- [ ] **Multi-Style Processing** - Apply different styles to different channels
- [ ] **Real-time Analysis** - Analyze incoming MIDI for style suggestions
- [ ] **Automation Support** - Full DAW automation integration
- [ ] **Performance Monitoring** - CPU usage and latency monitoring

## Code Implementation

### Core Transformation Function

```cpp
void StyleTransferAudioProcessor::applyStyle(juce::MidiBuffer& midiMessages, 
                                           const StyleParameters& style, 
                                           double beatsPerMinute, 
                                           double sampleRate)
{
    juce::MidiBuffer processedBuffer;
    
    juce::MidiBuffer::Iterator iterator(midiMessages);
    juce::MidiMessage message;
    int samplePosition;
    
    while (iterator.getNextEvent(message, samplePosition))
    {
        if (!message.isNoteOn()) {
            processedBuffer.addEvent(message, samplePosition);
            continue;
        }
        
        // Get original properties
        int originalSamplePosition = samplePosition;
        int noteNumber = message.getNoteNumber();
        int originalVelocity = message.getVelocity();
        
        // Calculate position in beats
        double positionInBeats = message.getTimeStamp() / sampleRate * (beatsPerMinute / 60.0);
        double beatFraction = positionInBeats - floor(positionInBeats);
        
        // Apply swing to off-beat notes
        int newSamplePosition = originalSamplePosition;
        if (beatFraction > 0.4 && beatFraction < 0.6) {
            double swingDelay = (style.swingRatio - 0.5f) * 0.25;
            int delayInSamples = static_cast<int>(swingDelay * sampleRate * 60.0 / beatsPerMinute);
            newSamplePosition = originalSamplePosition + delayInSamples;
        }
        
        // Apply accent to down-beat notes
        int newVelocity = originalVelocity;
        if (beatFraction < 0.1 || beatFraction > 0.9) {
            newVelocity = originalVelocity + static_cast<int>(style.accentAmount);
        }
        
        // Clip velocity to valid range
        newVelocity = juce::jlimit(0, 127, newVelocity);
        
        // Create modified message
        juce::MidiMessage newMessage = juce::MidiMessage::noteOn(
            message.getChannel(), noteNumber, static_cast<juce::uint8>(newVelocity)
        );
        
        processedBuffer.addEvent(newMessage, newSamplePosition);
    }
    
    // Replace original buffer with processed messages
    midiMessages.clear();
    midiMessages.addEvents(processedBuffer, 0, -1, 0);
}
```

## Integration with YesAnd Music

### Command Integration
The plugin can be controlled via YesAnd Music commands:

```bash
# Set swing ratio
python control_plane_cli.py "set swing to 0.7"

# Set accent amount  
python control_plane_cli.py "set accent to 25"

# Apply jazz style
python control_plane_cli.py "make it jazzier"
```

### OSC Control
Future integration will support OSC commands:

```bash
# Real-time parameter control
oscsend localhost 3819 /style/swing 0.7
oscsend localhost 3819 /style/accent 25
```

## Development Workflow

### 1. Project Setup
```bash
# Open JUCE Projucer
# Create new project: "Basic MIDI Effect Plugin"
# Name: StyleTransfer
# Formats: VST3, AudioUnit
# MIDI Channels: 16 in, 16 out
```

### 2. Build and Test
```bash
# Build in Xcode
# Test in DAW (Logic Pro, GarageBand, etc.)
# Verify real-time performance
# Check CPU usage
```

### 3. Integration Testing
```bash
# Test with YesAnd Music control plane
# Verify parameter changes work in real-time
# Test with different MIDI sequences
# Validate swing and accent effects
```

## Performance Considerations

### Real-Time Safety
- **No memory allocation** in audio thread
- **No locking mechanisms** for thread safety
- **Fixed-size buffers** for predictable memory usage
- **Efficient algorithms** for minimal CPU overhead

### Optimization Strategies
- **Pre-calculated values** where possible
- **Minimal branching** in hot code paths
- **Efficient MIDI parsing** with single-pass iteration
- **Parameter smoothing** to avoid clicks

## Testing Strategy

### Unit Tests
- [ ] Test swing calculation accuracy
- [ ] Test accent velocity clipping
- [ ] Test real-time safety compliance
- [ ] Test parameter range validation

### Integration Tests
- [ ] Test with various DAWs
- [ ] Test with different MIDI sequences
- [ ] Test parameter automation
- [ ] Test bypass functionality

### Performance Tests
- [ ] CPU usage under load
- [ ] Latency measurements
- [ ] Memory usage monitoring
- [ ] Real-time safety validation

## Future Enhancements

### Phase 4: Advanced Style Transformations
- **Jazz Style**: Complex swing patterns, chord substitutions
- **Classical Style**: Rubato timing, dynamic phrasing
- **Electronic Style**: Quantized timing, velocity curves
- **Blues Style**: Micro-timing variations, blue notes

### Phase 5: Machine Learning Integration
- **Style Learning**: Learn from user preferences
- **Pattern Recognition**: Detect musical patterns for transformation
- **Adaptive Processing**: Adjust transformations based on input
- **Style Transfer**: Apply learned styles to new material

## Conclusion

The JUCE Style Transfer plugin provides the foundational MIDI processing capabilities needed for the YesAnd Music semantic editing vision. By implementing real-time safe style transformations, we create a bridge between high-level natural language commands and low-level MIDI manipulation.

The modular architecture allows for incremental development while maintaining the critical real-time safety requirements for professional audio applications. This plugin will serve as the core MIDI processing engine for the broader YesAnd Music ecosystem.
