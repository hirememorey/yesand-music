# OSC Integration for StyleTransfer JUCE Plugin

## Overview

This document describes the OSC (Open Sound Control) integration for the StyleTransfer JUCE plugin, enabling remote control of style parameters via OSC messages.

## Architecture

### Real-Time Safety Design

The OSC integration follows strict real-time safety principles:

1. **Thread Separation**: OSC processing runs in the non-real-time thread only
2. **FIFO Queue**: Thread-safe message queue for communication between threads
3. **Timer-Based Processing**: 30 Hz timer callback processes OSC messages safely
4. **Parameter Management**: All parameter changes go through `AudioProcessorValueTreeState` (APVTS)
5. **No Audio Thread Blocking**: OSC operations never block the audio thread

### Key Components

- **`OSCMessage`**: Lightweight structure for OSC message data
- **`oscMessageFifo`**: Thread-safe FIFO queue for message passing
- **`OSCListenerThread`**: Background thread for OSC message reception
- **`timerCallback()`**: 30 Hz timer callback for processing OSC messages
- **`setParameterNotifyingHost()`**: Ensures DAW and UI are updated

## OSC Message Protocol

### Supported Messages

| Address | Type | Range | Description |
|---------|------|-------|-------------|
| `/style/swing` | float | 0.0 - 1.0 | Swing ratio (0.5 = straight, >0.5 = swing) |
| `/style/accent` | float | 0.0 - 50.0 | Accent amount (velocity boost) |
| `/style/humanizeTiming` | float | 0.0 - 1.0 | Timing humanization amount |
| `/style/humanizeVelocity` | float | 0.0 - 1.0 | Velocity humanization amount |
| `/style/enable` | bool | true/false | Enable/disable OSC control |

### Example OSC Messages

```bash
# Set swing ratio to 0.7 (moderate swing)
oscsend localhost 3819 /style/swing 0.7

# Set accent amount to 25
oscsend localhost 3819 /style/accent 25.0

# Set humanization parameters
oscsend localhost 3819 /style/humanizeTiming 0.3
oscsend localhost 3819 /style/humanizeVelocity 0.5

# Enable OSC control
oscsend localhost 3819 /style/enable true
```

## Dependencies

### liblo (Lightweight OSC)

The plugin uses **liblo** as the OSC library:

- **Real-time safe**: No memory allocation in audio thread
- **Lightweight**: Minimal overhead
- **Cross-platform**: Works on macOS, Windows, Linux
- **Well-tested**: Used in many professional audio applications

### Installation on macOS

```bash
# Using MacPorts
sudo port install liblo

# Using Homebrew
brew install liblo

# Verify installation
pkg-config --modversion liblo
```

## Build Configuration

### CMakeLists.txt

The CMakeLists.txt includes:

```cmake
# Find liblo (Lightweight OSC library)
pkg_check_modules(LIBLO REQUIRED liblo)

# Link libraries
target_link_libraries(StyleTransfer
    PRIVATE
        # ... other libraries
        ${LIBLO_LIBRARIES}
)

# Compiler flags
target_compile_options(StyleTransfer
    PRIVATE
        ${LIBLO_CFLAGS_OTHER}
)
```

## Usage

### 1. Enable OSC in Plugin

1. Load the plugin in your DAW
2. Open the plugin editor
3. Enable "OSC Enabled" checkbox
4. Set desired OSC port (default: 3819)

### 2. Send OSC Commands

```bash
# Test OSC connection
oscsend localhost 3819 /style/swing 0.5

# Real-time parameter control
oscsend localhost 3819 /style/swing 0.8
oscsend localhost 3819 /style/accent 30.0
```

### 3. Integration with Music Cursor

The OSC integration enables the Music Cursor control plane to remotely control the plugin:

```python
# From Music Cursor control plane
python control_plane_cli.py "set swing to 0.7"
python control_plane_cli.py "set accent to 25"
```

## Real-Time Safety Validation

### ✅ Safe Operations (Non-Real-Time Thread)

- OSC message reception
- Parameter updates via APVTS
- Message queue management
- String operations
- Memory allocation

### ❌ Forbidden Operations (Audio Thread)

- Direct OSC operations
- Parameter updates without APVTS
- Memory allocation
- String operations
- Blocking calls

## Future Enhancements

### Phase 2: Full OSC Implementation

- [x] Implement `juce::OSCReceiver` integration
- [x] Add OSC message validation
- [x] Implement OSC error handling
- [x] Add timer-based message processing
- [x] Add humanization parameter support

### Phase 3: Advanced OSC Features

- [ ] Bidirectional OSC communication
- [ ] OSC parameter automation
- [ ] OSC preset management
- [ ] OSC tempo synchronization

## Troubleshooting

### Common Issues

1. **OSC Not Receiving Messages**
   - Check firewall settings
   - Verify port number
   - Ensure plugin OSC is enabled

2. **Build Errors**
   - Install liblo: `sudo port install liblo`
   - Verify pkg-config: `pkg-config --modversion liblo`
   - Check CMakeLists.txt configuration

3. **Parameter Not Updating**
   - Verify OSC message format
   - Check parameter ranges
   - Ensure APVTS is properly configured

### Debug Commands

```bash
# Check if OSC port is listening
lsof -nP -iUDP:3819

# Test OSC message
oscsend localhost 3819 /style/swing 0.5

# Monitor OSC traffic
tcpdump -i lo0 udp port 3819
```

## Conclusion

The OSC integration provides a robust, real-time safe way to remotely control the StyleTransfer plugin. The architecture ensures that OSC operations never interfere with audio processing while providing responsive parameter control for the Music Cursor semantic MIDI editing system.
