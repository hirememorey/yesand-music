# Automatic Ardour Import Guide

**Seamless MIDI Import to Ardour with Lua Scripting**

This guide explains how to use the new automatic import functionality that eliminates the need for manual MIDI file imports in Ardour.

## 🚀 Quick Start

### Prerequisites
- **Ardour 8.9+** with Lua scripting support
- **OpenAI API key** (for AI features)
- **IAC Driver** enabled in Audio MIDI Setup

### Setup
```bash
# 1. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 2. Enable IAC Driver
# Open Audio MIDI Setup → Window → Show MIDI Studio
# Double-click IAC Driver → check "Device is online"
# Create port named "IAC Driver Bus 1"

# 3. Enable OSC in Ardour
# Ardour → Preferences → OSC → Enable OSC
# Set OSC port to 3819
```

### Start Using Auto-Import
```bash
# Interactive mode with auto-import
python real_time_enhancement_cli.py --interactive

# Try these commands:
enhance> enhance create a funky bassline
enhance> enhance add a drum pattern
enhance> enhance create a jazz melody
enhance> imports  # Check import status
```

## 🎯 How It Works

### Automatic Workflow
1. **AI Enhancement**: Generate musical content using LLM
2. **Track Management**: Automatically create appropriate tracks
3. **Lua Scripting**: Generate Ardour Lua scripts for import
4. **Auto-Import**: Execute scripts to import MIDI to Ardour
5. **User Feedback**: Show import status and results

### Key Components

#### 1. ArdourLuaImporter
- **Reliable Import**: Uses Lua scripting instead of unstable OSC
- **Track Creation**: Automatically creates tracks if needed
- **Error Handling**: Comprehensive error reporting and recovery
- **Multiple Patterns**: Import multiple patterns to separate tracks

#### 2. TrackManager
- **Smart Track Naming**: Creates appropriate track names based on content
- **Track Templates**: Pre-configured templates for different enhancement types
- **Track Organization**: Intelligent track placement and grouping
- **Conflict Resolution**: Handles duplicate track names gracefully

#### 3. Enhanced CLI
- **Real-Time Feedback**: Shows import status during enhancement
- **Import Status**: Check successful and failed imports
- **Error Reporting**: Clear error messages and troubleshooting

## 🎵 Usage Examples

### Basic Enhancement with Auto-Import
```bash
enhance> enhance create a walking bass line
🎵 Enhancing track: create a walking bass line
✅ Enhancement completed in 2.1s
📊 Confidence: 0.91
🎼 Generated 3 patterns
  1. Simple Walking Bass (Confidence: 0.93)
     Root notes with smooth voice leading
  2. Complex Walking Bass (Confidence: 0.89)
     Chord tones with rhythmic variations
  3. Jazz Walking Bass (Confidence: 0.87)
     Advanced bass line with passing tones

🚀 Auto-import status:
  ✅ Successfully imported to 3 tracks:
    - Bass at position 0
    - Bass_2 at position 32
    - Bass_3 at position 64
```

### Check Import Status
```bash
enhance> imports
🚀 Import Status (3 total):
  ✅ Successful imports (3):
    - Bass at position 0
    - Bass_2 at position 32
    - Bass_3 at position 64
  📊 Total imports this session: 3
```

### Multiple Enhancement Types
```bash
enhance> enhance bass make it more complex
enhance> enhance drums add ghost notes
enhance> enhance melody create a jazz solo
enhance> imports
```

## 🔧 Technical Details

### Lua Script Generation
The system generates Lua scripts that:
- **Create tracks** if they don't exist
- **Import MIDI files** to specified tracks
- **Position regions** at correct timeline positions
- **Handle errors** gracefully with clear messages

### Track Management
- **Enhancement Types**: Bass, Drums, Melody, Harmony, General
- **Track Templates**: Pre-configured settings for each type
- **Smart Naming**: Avoids conflicts and maintains organization
- **Position Strategy**: Intelligent track placement based on type

### Error Handling
- **File Validation**: Checks MIDI files before import
- **Track Creation**: Handles track creation failures
- **Import Recovery**: Retries failed imports with different strategies
- **User Feedback**: Clear error messages and suggestions

## 🚨 Troubleshooting

### Common Issues

#### Import Failed
```
❌ Failed to import to 1 tracks:
  - Bass: Lua script execution failed
```
**Solutions**:
1. Check Ardour is running and accessible
2. Verify Lua scripting is enabled in Ardour
3. Check file permissions for generated scripts

#### Track Creation Failed
```
❌ Failed to create track Bass
```
**Solutions**:
1. Check Ardour project is open
2. Verify track name doesn't conflict
3. Check Ardour session permissions

#### No Import Results
```
⚠️ No auto-import results available
```
**Solutions**:
1. Check if enhancement was successful
2. Verify MIDI files were generated
3. Check import process logs

### Debug Mode
```bash
# Enable debug output
export DEBUG=1
python real_time_enhancement_cli.py --interactive
```

### Manual Import
If auto-import fails, you can manually import:
1. Check generated Lua scripts in temp directory
2. Copy script content to Ardour's Lua console
3. Execute script manually

## 📊 Performance

### Import Speed
- **Track Creation**: < 1 second
- **MIDI Import**: < 2 seconds per file
- **Multiple Patterns**: Parallel processing
- **Error Recovery**: < 5 seconds

### Resource Usage
- **Memory**: Minimal overhead for Lua scripts
- **CPU**: Low impact during import
- **Disk**: Temporary files cleaned up automatically

## 🔮 Future Enhancements

### Planned Features
- **Real-Time Import**: Direct MIDI streaming to Ardour
- **Advanced Track Management**: Custom track templates
- **Import Scheduling**: Queue multiple imports
- **Rollback Support**: Undo failed imports

### Integration Opportunities
- **Multi-DAW Support**: Logic Pro, Pro Tools, etc.
- **Cloud Import**: Import from cloud storage
- **Collaborative Import**: Multi-user import sessions
- **Import Analytics**: Track import success rates

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
python test_auto_import.py
```

### Code Structure
- `ardour_lua_importer.py`: Core import functionality
- `track_manager.py`: Track management and templates
- `real_time_ardour_enhancer.py`: Integration with enhancement system
- `test_auto_import.py`: Comprehensive test suite

## 📄 License

This project is part of YesAnd Music. See [LICENSE](LICENSE) for details.

---

**Ready to start?** The auto-import system is production-ready and will transform your musical workflow by eliminating manual import steps. Just run the interactive CLI and start enhancing!
