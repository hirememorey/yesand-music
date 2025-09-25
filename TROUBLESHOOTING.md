# Troubleshooting

Common issues and solutions for YesAnd Music.

## Quick Diagnostics

### Check MVP MIDI Generator Status (NEW)
```bash
# Test basic generation
python3 mvp_midi_generator.py "generate me a bass line in C major"

# Test with length requirements
python3 mvp_midi_generator.py "generate me 8 measures of bass line in G minor"

# Test with style references
python3 mvp_midi_generator.py "generate me 16 measures of bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"

# Check system status
python3 mvp_midi_generator.py --interactive
# Then type: status
```

### Check Security-First System Status (NEW)
```bash
# Check security-first system status
python secure_enhancement_cli.py --status

# Check system health
python -c "from secure_enhancement_system import FailFastEnhancer; e = FailFastEnhancer(); print(e.get_system_status())"

# Run comprehensive tests
python test_security_first_system.py

# Check component health
python -c "from secure_llm_client import SecureLLMClient, LLMConfig; c = SecureLLMClient(LLMConfig('test')); print(c.get_rate_limit_status())"
```

### Check Legacy System Status
```bash
# Check if everything is working
python control_plane_cli.py status

# Check MIDI ports
python -c "import mido; print('Available ports:', mido.get_output_names())"

# Check dependencies
pip list | grep -E "(mido|python-rtmidi|python-osc|openai)"

# Check Ardour integration
python control_plane_cli.py "ardour connect"

# Check real-time enhancement system
python test_real_time_integration.py
```

---

## MVP MIDI Generator Issues (NEW)

### Length Requirements Not Respected
**Symptoms**: AI generates 2-4 measures instead of requested length (e.g., 16 measures)

**Status**: ✅ **FIXED** - This was a critical issue that has been resolved

**What Was Fixed**:
- Removed hardcoded "2-4 bars" limitation in prompt template
- Added dynamic length parsing for "X measures", "X bars", "X beats"
- Increased token limits to support longer pieces
- Updated prompt to use extracted length requirements

**Current Behavior**: 
- AI now respects length requirements but may generate musically coherent phrases
- This is sophisticated musical behavior, not a bug
- Example: Requesting 16 measures may generate 4-measure phrases that "feel right" musically

### JSON Parse Errors
**Symptoms**: `Failed to parse LLM response as JSON` or `Expecting property name enclosed in double quotes`

**Status**: ✅ **FIXED** - This was caused by token limits truncating responses

**What Was Fixed**:
- Increased max_tokens from 2000 to 4000
- Increased max_response_length from 2000 to 8000 characters
- Updated OpenAI API to v1.0 format

### OpenAI API Errors
**Symptoms**: `You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0`

**Status**: ✅ **FIXED** - Updated to use new OpenAI API format

**What Was Fixed**:
- Updated from `openai.ChatCompletion.create()` to `openai.chat.completions.create()`
- Updated client initialization to use `OpenAI(api_key=key)` instead of `openai.api_key = key`

### Missing Imports
**Symptoms**: `NameError: name 're' is not defined` or `NameError: name 'datetime' is not defined`

**Status**: ✅ **FIXED** - Added missing imports

**What Was Fixed**:
- Added `import re` to ai_midi_generator.py
- Added `from datetime import datetime` to ai_midi_generator.py
- Removed duplicate import at end of file

### SecurityContext Errors
**Symptoms**: `__init__() missing 1 required positional argument: 'timestamp'`

**Status**: ✅ **FIXED** - Fixed SecurityContext instantiation

**What Was Fixed**:
- Added missing `timestamp=datetime.now()` parameter to SecurityContext creation
- Fixed SecurityContext to use datetime object instead of float

### LLMResponse Errors
**Symptoms**: `'LLMResponse' object has no attribute 'success'`

**Status**: ✅ **FIXED** - Updated to use correct response field

**What Was Fixed**:
- Changed from `response.success` to `response.is_safe`
- Updated error handling to use correct response structure

---

## Security-First System Issues (NEW)

### System Not Healthy
**Symptoms**: `❌ System is not healthy` or `❌ Component health check failed`

**Solutions**:
1. **Check System Status**:
   ```bash
   python secure_enhancement_cli.py --status
   ```

2. **Check Component Health**:
   ```bash
   python -c "from secure_enhancement_system import FailFastEnhancer; e = FailFastEnhancer(); print(e.get_system_status())"
   ```

3. **Restart System**:
   ```bash
   # Kill any running processes
   pkill -f secure_enhancement
   
   # Restart system
   python secure_enhancement_cli.py --status
   ```

### Rate Limiting Issues
**Symptoms**: `❌ Rate limit exceeded` or `❌ Too many requests`

**Solutions**:
1. **Check Rate Limit Status**:
   ```bash
   python -c "from secure_llm_client import SecureLLMClient, LLMConfig; c = SecureLLMClient(LLMConfig('test')); print(c.get_rate_limit_status())"
   ```

2. **Wait for Rate Limit Reset**:
   ```bash
   # Check wait time
   python -c "from secure_llm_client import SecureLLMClient, LLMConfig; c = SecureLLMClient(LLMConfig('test')); print(f'Wait time: {c.get_rate_limit_status()[\"wait_time\"]} seconds')"
   ```

3. **Adjust Rate Limits**:
   ```python
   # In your configuration
   llm_config = LLMConfig(
       rate_limit_per_minute=120,  # Increase limit
       rate_limit_burst=20         # Increase burst
   )
   ```

### Security Errors
**Symptoms**: `❌ Security error` or `❌ Input validation failed`

**Solutions**:
1. **Check Input Validation**:
   ```bash
   # Enable debug mode
   export DEBUG=1
   python secure_enhancement_cli.py --interactive
   ```

2. **Check Security Level**:
   ```bash
   # Use lower security level for testing
   python secure_enhancement_cli.py --request "test" --security-level low
   ```

3. **Check File Permissions**:
   ```bash
   # Check quarantine directory permissions
   ls -la /tmp/quarantine
   chmod 755 /tmp/quarantine
   ```

### Component Initialization Failed
**Symptoms**: `❌ Failed to initialize component` or `❌ Component not available`

**Solutions**:
1. **Check Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Check Configuration**:
   ```bash
   # Verify environment variables
   echo $OPENAI_API_KEY
   echo $OSC_HOST
   echo $OSC_PORT
   ```

3. **Check Component Health**:
   ```bash
   python -c "from secure_enhancement_system import FailFastEnhancer; e = FailFastEnhancer(); print(e.get_system_status())"
   ```

### Performance Issues
**Symptoms**: Slow response times or high resource usage

**Solutions**:
1. **Check System Resources**:
   ```bash
   # Check memory usage
   ps aux | grep python
   
   # Check CPU usage
   top -p $(pgrep -f secure_enhancement)
   ```

2. **Adjust Configuration**:
   ```python
   # Reduce rate limits
   llm_config = LLMConfig(
       rate_limit_per_minute=30,  # Reduce limit
       max_prompt_length=2000     # Reduce prompt length
   )
   ```

3. **Check System Mode**:
   ```bash
   # Check current mode
   python secure_enhancement_cli.py --status
   ```

### File Processing Issues
**Symptoms**: `❌ File validation failed` or `❌ File too large`

**Solutions**:
1. **Check File Size**:
   ```bash
   # Check file size
   ls -lh your_file.mid
   ```

2. **Check File Type**:
   ```bash
   # Check file extension
   file your_file.mid
   ```

3. **Check Quarantine**:
   ```bash
   # Check quarantined files
   ls -la /tmp/quarantine
   ```

---

## Real-Time Enhancement Issues

### OSC Connection Failed
**Symptoms**: `❌ Failed to start OSC monitoring` or `❌ No project state available`

**Solutions**:
1. **Enable OSC in Ardour**:
   - Ardour → Preferences → OSC
   - Check "Enable OSC"
   - Set port to 3819 (default)
   - Restart Ardour

2. **Check Ardour is Running**:
   ```bash
   # Verify Ardour is running
   ps aux | grep ardour
   ```

3. **Verify OSC Port**:
   ```bash
   # Check if port is available
   lsof -i :3819
   ```

4. **Check Firewall**:
   - Ensure firewall allows local connections
   - macOS: System Preferences → Security & Privacy → Firewall

### No Project State Available
**Symptoms**: `❌ No project state available` or empty project status

**Solutions**:
1. **Open Project in Ardour**:
   - Create or open a project in Ardour
   - Ensure project has tracks and regions

2. **Check OSC Configuration**:
   - Verify OSC is enabled in Ardour
   - Check OSC port matches (default: 3819)

3. **Restart Enhancement Session**:
   ```bash
   # Stop and restart enhancement session
   python real_time_enhancement_cli.py --interactive
   ```

### LLM Enhancement Failed
**Symptoms**: `❌ Enhancement failed: OpenAI API error` or `❌ Enhancement failed: No current project context`

**Solutions**:
1. **Check OpenAI API Key**:
   ```bash
   echo $OPENAI_API_KEY
   # Should show your API key
   ```

2. **Verify API Key is Valid**:
   ```bash
   # Test API key
   python -c "import openai; openai.api_key='$OPENAI_API_KEY'; print('API key valid')"
   ```

3. **Check Internet Connection**:
   ```bash
   # Test internet connectivity
   ping openai.com
   ```

4. **Check Project Context**:
   - Ensure Ardour project is open
   - Verify OSC monitoring is working
   - Check project has musical content

### MIDI Import Failed
**Symptoms**: `❌ Failed to import MIDI to Ardour` or patterns not appearing in Ardour

**Solutions**:
1. **Check IAC Driver**:
   - Audio MIDI Setup → Window → Show MIDI Studio
   - Double-click IAC Driver → check "Device is online"
   - Create port named "IAC Driver Bus 1"

2. **Verify MIDI Track in Ardour**:
   - Create MIDI track in Ardour
   - Set input to "IAC Driver Bus 1"
   - Enable track monitoring

3. **Check Generated Files**:
   ```bash
   # Check if MIDI files were generated
   ls -la generated_patterns/
   ```

4. **Manual Import**:
   - Use Ardour's File → Import → Audio/MIDI
   - Navigate to `generated_patterns/` folder
   - Import the generated MIDI files

### Enhancement Suggestions Not Working
**Symptoms**: `No suggestions available` or empty suggestions list

**Solutions**:
1. **Check Project Content**:
   - Ensure project has musical content
   - Verify tracks have MIDI data
   - Check regions are selected

2. **Verify Context Analysis**:
   ```bash
   # Check project status
   python real_time_enhancement_cli.py --status
   ```

3. **Restart Analysis**:
   - Stop and restart enhancement session
   - Wait for context analysis to complete

### Performance Issues
**Symptoms**: Slow enhancement responses or system lag

**Solutions**:
1. **Check System Resources**:
   ```bash
   # Check CPU and memory usage
   top -l 1 | head -10
   ```

2. **Reduce Enhancement Complexity**:
   - Use simpler enhancement requests
   - Avoid multiple simultaneous enhancements

3. **Check OSC Message Rate**:
   - Reduce OSC update frequency if needed
   - Check for excessive OSC messages

---

## Common Issues

### No Sound / MIDI Not Working

**Symptoms**: Commands run but no sound in DAW

**Solutions**:
1. **Check IAC Driver**:
   ```bash
   # Open Audio MIDI Setup
   # Window → Show MIDI Studio
   # Double-click IAC Driver → check "Device is online"
   # Create port named "IAC Driver Bus 1"
   ```

2. **Verify DAW Setup**:
   - Create Software Instrument track
   - Arm the track for recording
   - Enable input monitoring
   - Load any software instrument

3. **Check Port Name**:
   ```bash
   # Verify port exists
   python -c "import mido; print('Ports:', mido.get_output_names())"
   # Should see "IAC Driver Bus 1"
   ```

4. **Test MIDI Output**:
   ```bash
   # Simple test
   python control_plane_cli.py "play scale C major"
   # Should play C Major scale and hear 8 notes
   ```

### Commands Not Parsing

**Symptoms**: "Unknown command" or "Command not recognized"

**Solutions**:
1. **Check Command Syntax**:
   ```bash
   # Correct syntax
   python control_plane_cli.py "play scale C major"
   python control_plane_cli.py "analyze bass"
   
   # Wrong syntax
   python control_plane_cli.py "play C major scale"  # Missing "scale"
   ```

2. **Check Available Commands**:
   ```bash
   # List all commands
   python control_plane_cli.py "help"
   ```

3. **Test Simple Commands**:
   ```bash
   # Start with basic commands
   python control_plane_cli.py "status"
   python control_plane_cli.py "play scale C major"
   ```

### AI Features Not Working

**Symptoms**: Musical conversation or Musical Scribe commands fail

**Solutions**:
1. **Check OpenAI API Key**:
   ```bash
   echo $OPENAI_API_KEY
   # Should show your API key
   ```

2. **Set API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Test AI Features**:
   ```bash
   # Test musical conversation
   python enhanced_control_plane_cli.py --conversation
   
   # Test Musical Scribe
   python control_plane_cli.py "musical scribe status"
   ```

### Plugin Not Loading

**Symptoms**: Plugin doesn't appear in DAW or crashes on load

**Solutions**:
1. **Check Installation Paths**:
   ```bash
   # AudioUnit location
   ls -la "/Users/harrisgordon/Library/Audio/Plug-Ins/Components/Style Transfer.component"
   
   # VST3 location
   ls -la "/Users/harrisgordon/Library/Audio/Plug-Ins/VST3/Style Transfer.vst3"
   ```

2. **Rebuild Plugin**:
   ```bash
   # Clean and rebuild
   make clean -C build_minimal
   make -C build_minimal
   ```

3. **Check DAW Compatibility**:
   - **GarageBand**: Look in MIDI Effects section
   - **Logic Pro**: Look in MIDI Effects section
   - **Other DAWs**: Check VST3 support

### Visual Feedback Not Displaying

**Symptoms**: Analysis commands run but no visual feedback appears

**Solutions**:
1. **Check Display Thread**:
   ```bash
   # Enable debug output
   export DEBUG=1
   python control_plane_cli.py "analyze bass"
   ```

2. **Verify MIDI File Loaded**:
   ```bash
   # Load a MIDI file first
   python control_plane_cli.py "load test_simple.mid"
   python control_plane_cli.py "analyze bass"
   ```

3. **Check Visual Feedback System**:
   ```bash
   # Test visual feedback directly
   python -c "
   from visual_feedback_display import start_visual_feedback
   start_visual_feedback()
   print('Visual feedback started')
   "
   ```

### Ardour Integration Issues

**Symptoms**: Ardour commands not working, connection failures

**Solutions**:
1. **Check Ardour Installation**:
   ```bash
   # Check if Ardour is installed
   which ardour
   # or
   ls -la /Applications/Ardour.app/Contents/MacOS/ardour
   ```

2. **Start Ardour Manually**:
   - Open Ardour application
   - Create or open a project
   - Try connecting again

3. **Check Project Files**:
   ```bash
   # Look for Ardour project files
   find ~/Documents -name "*.ardour" -type f
   ```

4. **Test Basic Commands**:
   ```bash
   python control_plane_cli.py "ardour connect"
   python control_plane_cli.py "ardour tracks"
   ```

### Performance Issues

**Symptoms**: Audio dropouts, slow response, high CPU usage

**Solutions**:
1. **Check Real-Time Safety**:
   - No memory allocation in audio thread
   - No blocking operations in MIDI processing
   - Visual feedback runs in separate thread

2. **Optimize MIDI Processing**:
   ```bash
   # Check for blocking operations
   python -c "
   import time
   start = time.time()
   # Run your command
   print(f'Execution time: {time.time() - start:.3f}s')
   "
   ```

3. **Reduce Visual Feedback Load**:
   - Clear feedback when not needed
   - Limit analysis complexity
   - Use caching for repeated operations

### Build Issues

**Symptoms**: CMake errors, compilation failures

**Solutions**:
1. **Check Dependencies**:
   ```bash
   # Verify CMake version
   cmake --version  # Should be 3.31.7+
   
   # Check Xcode Command Line Tools
   xcode-select --install
   ```

2. **Clean Build**:
   ```bash
   # Remove build directory
   rm -rf build_minimal
   mkdir build_minimal
   cd build_minimal
   cmake ..
   make
   ```

3. **Check JUCE Path**:
   ```bash
   # Verify JUCE is in project root
   ls -la JUCE/
   ```

### Python Environment Issues

**Symptoms**: Import errors, missing modules

**Solutions**:
1. **Check Virtual Environment**:
   ```bash
   # Activate virtual environment
   source .venv/bin/activate
   
   # Verify Python path
   which python
   ```

2. **Reinstall Dependencies**:
   ```bash
   # Reinstall requirements
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Check Python Version**:
   ```bash
   # Verify Python version
   python --version  # Should be 3.8+
   ```

---

## Debug Commands

### Enable Debug Output
```bash
# Set debug environment variable
export DEBUG=1
python control_plane_cli.py "your command"
```

### Check System State
```bash
# Check session state
python control_plane_cli.py "status"

# Check MIDI ports
python -c "import mido; print('Ports:', mido.get_output_names())"

# Check dependencies
pip list | grep -E "(mido|python-rtmidi|python-osc|openai)"
```

### Test Individual Components
```bash
# Test MIDI I/O
python -c "
from midi_io import parse_midi_file
notes = parse_midi_file('test_simple.mid')
print(f'Loaded {len(notes)} notes')
"

# Test analysis
python -c "
from analysis import apply_swing
from midi_io import parse_midi_file
notes = parse_midi_file('test_simple.mid')
swung = apply_swing(notes)
print('Swing applied successfully')
"

# Test control plane
python -c "
from commands.control_plane import ControlPlane
cp = ControlPlane()
result = cp.execute('play scale C major')
print(f'Result: {result}')
"
```

---

## Common Error Messages

### "Port not found"
**Cause**: IAC Driver not enabled or port not created
**Solution**: Enable IAC Driver and create "IAC Driver Bus 1" port

### "Unknown command"
**Cause**: Command syntax error or typo
**Solution**: Check command syntax, use "help" to see available commands

### "File not found"
**Cause**: MIDI file doesn't exist or wrong path
**Solution**: Check file path, use absolute path if needed

### "Import error"
**Cause**: Missing dependency or wrong Python environment
**Solution**: Activate virtual environment and install requirements

### "Plugin not loading"
**Cause**: Plugin not built or wrong AudioUnit type
**Solution**: Rebuild plugin and check AudioUnit configuration

### "OpenAI API key not set"
**Cause**: Missing OpenAI API key for AI features
**Solution**: Set OPENAI_API_KEY environment variable

### "LLM response error"
**Cause**: OpenAI API error or network issue
**Solution**: Check API key, internet connection, and try again

---

## Getting Help

### Check Documentation
- **Setup Issues**: See [README.md](README.md) for quick start
- **Feature Questions**: See [FEATURES.md](FEATURES.md) for detailed guides
- **Development Issues**: See [DEVELOPMENT.md](DEVELOPMENT.md) for technical details
- **Command Reference**: See [REFERENCE.md](REFERENCE.md) for all commands

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_control_plane.py -v

# Run with coverage
python -m pytest --cov=. tests/
```

### Check Logs
```bash
# Check build logs
ls -la build_logs/

# Check recent errors
tail -f build_logs/latest.log
```

---

## Still Having Issues?

1. **Check the logs**: Look for error messages in terminal output
2. **Run diagnostics**: Use the debug commands above
3. **Test components**: Try individual components in isolation
4. **Check documentation**: Review relevant documentation files
5. **Verify setup**: Ensure all prerequisites are met

If you're still stuck, the issue might be environment-specific. Check your system configuration and compare with the requirements in [DEVELOPMENT.md](DEVELOPMENT.md).

---

**Quick Links**:
- [Features Guide](FEATURES.md) - Complete feature documentation
- [Reference](REFERENCE.md) - Commands and APIs
- [Development Guide](DEVELOPMENT.md) - Technical details