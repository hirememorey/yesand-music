# Ardour Integration Guide

This guide explains how to use YesAnd Music with Ardour DAW through file-based integration.

## Overview

YesAnd Music provides file-based integration with Ardour DAW, allowing you to:
- Export selected regions from Ardour for analysis
- Analyze exported MIDI data with musical intelligence
- Improve exported MIDI using problem solvers
- Import improved versions back into Ardour

## Prerequisites

- Ardour 8.9+ installed and running
- YesAnd Music project set up
- Python virtual environment activated

## Quick Start

### 1. Connect to Ardour

```bash
python control_plane_cli.py "ardour connect"
```

### 2. List Tracks

```bash
python control_plane_cli.py "ardour tracks"
```

### 3. Export Selected Region

```bash
python control_plane_cli.py "ardour export selected"
```

### 4. Analyze Exported Region

```bash
python control_plane_cli.py "ardour analyze selected"
```

### 5. Improve Exported Region

```bash
python control_plane_cli.py "ardour improve selected"
```

## Available Commands

### Connection Commands

- `ardour connect` - Connect to Ardour DAW
- `ardour disconnect` - Disconnect from Ardour
- `ardour tracks` - List Ardour tracks

### Export/Import Commands

- `ardour export selected` - Export selected region to MIDI file
- `ardour import [FILE]` - Import MIDI file to Ardour

### Analysis Commands

- `ardour analyze selected` - Analyze exported region
- `ardour improve selected` - Improve exported region

## Workflow

### Basic Analysis Workflow

1. **Start Ardour** and open your project
2. **Select a region** you want to analyze
3. **Connect YesAnd Music**:
   ```bash
   python control_plane_cli.py "ardour connect"
   ```
4. **Export the region**:
   ```bash
   python control_plane_cli.py "ardour export selected"
   ```
5. **Analyze the region**:
   ```bash
   python control_plane_cli.py "ardour analyze selected"
   ```

### Improvement Workflow

1. **Export a region** (as above)
2. **Improve the region**:
   ```bash
   python control_plane_cli.py "ardour improve selected"
   ```
3. **Import the improved version**:
   ```bash
   python control_plane_cli.py "ardour import improved_groove_region.mid"
   ```

## File-Based Integration Details

### How It Works

The integration uses a file-based workflow:

1. **Export**: Selected regions are exported from Ardour as MIDI files
2. **Analysis**: MIDI files are analyzed using YesAnd Music's intelligence
3. **Improvement**: Musical problem solvers create improved versions
4. **Import**: Improved MIDI files are imported back into Ardour

### File Locations

- **Exported files**: Stored in temporary directory
- **Improved files**: Saved with descriptive names
- **Lua scripts**: Generated for Ardour automation

### Project File Parsing

The integration automatically:
- Finds the most recent Ardour project
- Parses track information from `.ardour` files
- Extracts track names, types, and states

## Lua Scripts

YesAnd Music can generate Lua scripts for Ardour automation:

### Export Script

```lua
-- Export selected region to MIDI file
function export_selected_region()
    local session = Session:get()
    if not session then
        print("No active session")
        return false
    end
    
    local selection = session:get_selection()
    if not selection then
        print("No region selected")
        return false
    end
    
    -- Export logic would go here
    print("Exporting selected region...")
    return true
end

export_selected_region()
```

### Import Script

```lua
-- Import MIDI file to new track
function import_midi_file(file_path, track_name)
    local session = Session:get()
    if not session then
        print("No active session")
        return false
    end
    
    -- Import logic would go here
    print("Importing MIDI file: " .. file_path)
    return true
end
```

## Troubleshooting

### Ardour Not Found

**Problem**: "Ardour executable not found"

**Solutions**:
1. Install Ardour from [ardour.org](https://ardour.org)
2. Specify Ardour path:
   ```python
   ardour = ArdourIntegration(ardour_path="/path/to/ardour")
   ```

### Connection Failed

**Problem**: "Failed to connect to Ardour"

**Solutions**:
1. Make sure Ardour is running
2. Check if Ardour process is accessible
3. Try starting Ardour manually

### No Tracks Found

**Problem**: "No tracks found or not connected"

**Solutions**:
1. Make sure you have an open Ardour project
2. Check if project files are in expected locations
3. Verify project file permissions

### Export Failed

**Problem**: "Failed to export selected region"

**Solutions**:
1. Make sure a region is selected in Ardour
2. Check if the region contains MIDI data
3. Verify file system permissions

## Advanced Usage

### Custom Ardour Path

```python
from ardour_integration import ArdourIntegration

# Specify custom Ardour path
ardour = ArdourIntegration(ardour_path="/Applications/Ardour.app/Contents/MacOS/ardour")
```

### Custom OSC Port

```python
# Use custom OSC port
ardour = ArdourIntegration(osc_port=3820)
```

### Direct Integration Usage

```python
from ardour_integration import ArdourIntegration

with ArdourIntegration() as ardour:
    # Connect to Ardour
    if ardour.connect():
        # List tracks
        tracks = ardour.list_tracks()
        print(f"Found {len(tracks)} tracks")
        
        # Export selected region
        exported_file = ardour.export_selected_region()
        if exported_file:
            print(f"Exported to: {exported_file}")
            
            # Analyze the region
            analysis = ardour.analyze_selected_region()
            print(f"Analysis: {analysis}")
```

## Demo Scripts

### Interactive Demo

```bash
python demo_ardour_integration.py --interactive
```

### Automated Demo

```bash
python demo_ardour_integration.py
```

### Test Suite

```bash
python test_ardour_integration.py
```

## Limitations

### Current Limitations

1. **File-based only**: No real-time state access
2. **Manual workflow**: Requires manual export/import steps
3. **Project parsing**: Limited to basic track information
4. **OSC integration**: Basic connection only

### Future Improvements

1. **Real-time state access**: Direct Ardour state reading
2. **Automated workflow**: Seamless export/import
3. **Advanced parsing**: Full project state access
4. **OSC integration**: Complete parameter control

## Integration with Existing Features

### Contextual Intelligence

Ardour integration works with all contextual intelligence features:
- Musical analysis (bass, melody, harmony, rhythm)
- Visual feedback and highlighting
- Smart suggestions and improvements

### Musical Problem Solvers

All problem solvers work with Ardour:
- Groove improvement
- Harmony fixing
- Arrangement enhancement

### Control Plane

Ardour commands integrate seamlessly with the control plane:
- Natural language command parsing
- Session state management
- Error handling and recovery

## Best Practices

### Workflow Optimization

1. **Keep regions small**: Export only what you need to analyze
2. **Use descriptive names**: Name your tracks clearly
3. **Save frequently**: Save your Ardour project often
4. **Test improvements**: Always listen to improved versions

### File Management

1. **Clean up temp files**: The integration cleans up automatically
2. **Backup originals**: Keep copies of original MIDI files
3. **Organize exports**: Use descriptive filenames for exports

### Performance

1. **Close unused projects**: Close Ardour projects you're not using
2. **Limit analysis scope**: Analyze small regions for faster processing
3. **Use SSD storage**: Store projects on fast storage for better performance

## Support

### Getting Help

1. **Check logs**: Look for error messages in terminal output
2. **Run tests**: Use the test suite to verify functionality
3. **Check documentation**: Review this guide and other docs
4. **Verify setup**: Ensure Ardour and YesAnd Music are properly installed

### Common Issues

- **Ardour not starting**: Check installation and permissions
- **Export failures**: Verify region selection and MIDI content
- **Analysis errors**: Check MIDI file format and content
- **Import issues**: Verify file paths and Ardour project state

The Ardour integration provides a solid foundation for file-based DAW integration while maintaining the reliability and educational value of YesAnd Music's musical intelligence features.
