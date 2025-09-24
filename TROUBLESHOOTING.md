# Troubleshooting

Common issues and solutions for YesAnd Music.

## Quick Diagnostics

### Check System Status
```bash
# Check if everything is working
python control_plane_cli.py status

# Check MIDI ports
python -c "import mido; print('Available ports:', mido.get_output_names())"

# Check dependencies
pip list | grep -E "(mido|python-rtmidi|python-osc|openai)"

# Check Ardour integration
python control_plane_cli.py "ardour connect"
```

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