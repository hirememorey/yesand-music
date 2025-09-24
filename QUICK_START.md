# Quick Start Guide - Security-First YesAnd Music

## 🚀 Get Started in 5 Minutes

This guide will get you up and running with the new security-first YesAnd Music system quickly.

## Prerequisites

- **macOS** (tested on macOS 15.5)
- **Python 3.8+**
- **OpenAI API key** (for AI features)
- **IAC Driver** enabled in Audio MIDI Setup

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/yesand-music.git
cd yesand-music

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 4. Enable IAC Driver (macOS only)
# Open Audio MIDI Setup → Window → Show MIDI Studio
# Double-click IAC Driver → check "Device is online"
# Create port named "IAC Driver Bus 1"
```

## Quick Test

### Test Security-First System
```bash
# Test the security-first system
python secure_enhancement_cli.py --status

# Expected output:
# 🔒 SECURE ENHANCEMENT SYSTEM - Security-First Architecture
# ✅ Enhancement system initialized
# 📊 SYSTEM STATUS
# Mode: offline
# Healthy: ✅
```

### Test MIDI to JSON Workflow (NEW)
```bash
# Test basic MIDI generation
python music_generator_cli.py "generate a simple bass line in C major"

# Test style reference generation
python music_generator_cli.py "generate a bass pattern like Alice In Chains in GMinor"

# Test context extraction
python music_generator_cli.py --extract-context
```

## Interactive Mode

```bash
# Start interactive mode
python secure_enhancement_cli.py --interactive

# Try these commands:
# enhance create a funky bassline
# status
# help
# quit
```

## Single Command Mode

```bash
# Single enhancement command
python secure_enhancement_cli.py --request "create a jazz melody" --type melody

# With specific parameters
python secure_enhancement_cli.py --request "add drums" --type drums --track-id "2" --security-level high
```

## System Modes

The system automatically detects the best available mode:

1. **Real-Time Mode**: OSC communication with Ardour (requires Ardour running)
2. **File-Based Mode**: File-based workflow (requires project files)
3. **Offline Mode**: LLM-only processing (always available)
4. **Demo Mode**: Fallback for testing (always available)

## Security Features

The system includes built-in security features:

- **Input Validation**: All inputs are validated before processing
- **Output Sanitization**: All outputs are sanitized before delivery
- **Rate Limiting**: Built-in rate limiting for all external communications
- **Encryption**: Message encryption for sensitive data
- **Quarantine**: Suspicious files automatically quarantined
- **Health Monitoring**: Continuous health checks and monitoring

## Troubleshooting

### System Not Healthy
```bash
# Check system status
python secure_enhancement_cli.py --status

# Check component health
python -c "from secure_enhancement_system import FailFastEnhancer; e = FailFastEnhancer(); print(e.get_system_status())"
```

### Rate Limiting
```bash
# Check rate limit status
python -c "from secure_llm_client import SecureLLMClient, LLMConfig; c = SecureLLMClient(LLMConfig('test')); print(c.get_rate_limit_status())"
```

### Security Errors
```bash
# Enable debug output
export DEBUG=1
python secure_enhancement_cli.py --interactive
```

## Development Setup

### Run Tests
```bash
# Run all tests
python test_security_first_system.py

# Run specific test categories
python -m unittest test_security_first_system.TestSecurityFirstArchitecture
```

### Code Structure
```
security_first_architecture.py      # Core security framework
secure_osc_client.py               # Secure OSC communication
secure_file_parser.py              # Secure file processing
secure_llm_client.py               # Secure LLM communication
secure_enhancement_system.py       # Integration layer
secure_enhancement_cli.py          # Command-line interface
test_security_first_system.py     # Comprehensive test suite
```

### Key Components

1. **SecurityFirstComponent**: Base class for all secure components
2. **SecureOSCClient**: Secure OSC communication with validation
3. **SecureFileParser**: Secure file processing with quarantine
4. **SecureLLMClient**: Secure LLM communication with sanitization
5. **FailFastEnhancer**: Main enhancement orchestrator

## Configuration

### Environment Variables
```bash
export OPENAI_API_KEY="your-api-key-here"
export OSC_HOST="127.0.0.1"
export OSC_PORT="3819"
export SECURITY_LEVEL="medium"
export DEBUG="false"
```

### Configuration Files
```python
# OSC Configuration
from secure_osc_client import OSCConfig
osc_config = OSCConfig(
    host="127.0.0.1",
    port=3819,
    rate_limit_per_second=100,
    encryption_key="your-encryption-key"
)

# File Configuration
from secure_file_parser import FileConfig
file_config = FileConfig(
    max_file_size=10 * 1024 * 1024,  # 10MB
    allowed_extensions=['.mid', '.midi', '.json'],
    quarantine_dir="/tmp/quarantine"
)

# LLM Configuration
from secure_llm_client import LLMConfig
llm_config = LLMConfig(
    api_key="your-api-key",
    model="gpt-3.5-turbo",
    rate_limit_per_minute=60,
    max_prompt_length=4000
)
```

## Performance Characteristics

- **Response Times**: < 10ms for OSC, < 100ms for files, < 2000ms for LLM
- **Throughput**: 100+ OSC messages/sec, 10+ files/sec, 30+ LLM requests/min
- **Resource Usage**: < 100MB base memory, < 5% CPU idle

## Next Steps

1. **Read the Documentation**: Check out [SECURITY_FIRST_IMPLEMENTATION.md](SECURITY_FIRST_IMPLEMENTATION.md)
2. **Implement MIDI to JSON Workflow**: Follow [MIDI_TO_JSON_IMPLEMENTATION.md](MIDI_TO_JSON_IMPLEMENTATION.md)
3. **Explore Features**: Try different enhancement types and security levels
4. **Run Tests**: Ensure everything is working correctly
5. **Contribute**: See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines

## Support

- **Documentation**: [SECURITY_FIRST_IMPLEMENTATION.md](SECURITY_FIRST_IMPLEMENTATION.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Features**: [FEATURES.md](FEATURES.md)

## Quick Reference

### Commands
```bash
# Interactive mode
python secure_enhancement_cli.py --interactive

# Single command
python secure_enhancement_cli.py --request "enhancement request" --type enhancement_type

# System status
python secure_enhancement_cli.py --status

# Help
python secure_enhancement_cli.py --help
```

### Enhancement Types
- `bass` - Bass line enhancements
- `drums` - Drum pattern enhancements
- `melody` - Melodic enhancements
- `harmony` - Harmonic enhancements
- `general` - General enhancements

### Security Levels
- `low` - Basic security
- `medium` - Standard security (default)
- `high` - Enhanced security
- `critical` - Maximum security

---

**Ready to start?** Run `python secure_enhancement_cli.py --interactive` and try `enhance create a funky bassline`!
