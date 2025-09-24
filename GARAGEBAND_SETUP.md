# GarageBand Setup Guide

## Overview

This guide provides step-by-step instructions for setting up and using the YesAnd Music Style Transfer plugin in GarageBand.

## Prerequisites

- macOS with GarageBand 10.4.12 or later
- YesAnd Music project installed and built
- Python virtual environment activated

## Plugin Installation

The Style Transfer plugin is automatically installed during the build process:

```bash
cd /Users/harrisgordon/Documents/Development/Python/not_sports/music_cursor
source .venv/bin/activate
# Plugin is already built and installed
```

**Plugin Location:**
- AudioUnit: `~/Library/Audio/Plug-Ins/Components/Style Transfer.component`
- VST3: `~/Library/Audio/Plug-Ins/VST3/Style Transfer.vst3`

## Loading the Plugin in GarageBand

### Method 1: Smart Controls Panel (Recommended)

1. **Open GarageBand** and create a new project
2. **Create a Software Instrument track**:
   - Click the "+" button to add a new track
   - Select "Software Instrument"
   - Choose any instrument (piano, synth, etc.)
3. **Load the Style Transfer plugin**:
   - Click on the track to select it
   - Look for the "Smart Controls" panel on the right side
   - In the Smart Controls, look for "MIDI Effects" section
   - Click on the MIDI Effects slot (it might show "None" or be empty)
   - Look for "Style Transfer" in the list and select it

### Method 2: Track Inspector

1. **Select your MIDI track**
2. **Go to Track > Show Track Inspector** (or press Cmd+I)
3. **Look for the "MIDI Effects" section**
4. **Click the dropdown** and select "Style Transfer"

## Plugin Parameters

Once loaded, you'll see these parameters:

- **Swing Ratio** (0.0 to 1.0): Controls swing feel
  - 0.5 = straight timing
  - > 0.5 = swing feel (off-beat notes delayed)
- **Accent Amount** (0 to 50): Velocity boost for down-beat notes
- **OSC Enabled**: Toggle for remote control via Python
- **OSC Port**: Port number for OSC communication (default: 3819)

## Testing the Plugin

### Basic Testing

1. **Load the plugin** using the instructions above
2. **Play some MIDI notes** (either from keyboard or control plane)
3. **Adjust the Swing Ratio** to hear timing changes
4. **Adjust the Accent Amount** to hear velocity changes

### Control Plane Testing

```bash
# Test basic MIDI playback
python control_plane_cli.py "play scale C major"

# Test OSC control
python control_plane_cli.py "set swing to 0.7"
python control_plane_cli.py "set accent to 25"
python control_plane_cli.py "make it jazz"

# Test style presets
python control_plane_cli.py "set style to classical"
python control_plane_cli.py "make it blues"
```

### Interactive Mode Testing

```bash
# Start interactive mode
python control_plane_cli.py --interactive

# Try these commands:
play scale D minor
set tempo to 140
set swing to 0.8
play arp C major
stop
```

## Troubleshooting

### Plugin Not Appearing in List

**Problem**: Style Transfer doesn't appear in the MIDI Effects list

**Solutions**:
1. **Restart GarageBand** - Sometimes needed for new plugins
2. **Check plugin installation**:
   ```bash
   ls -la ~/Library/Audio/Plug-Ins/Components/ | grep -i style
   ```
3. **Verify plugin validation**:
   ```bash
   auval -v aumf StTr Mcrs
   ```

### Plugin Loads But No Effect

**Problem**: Plugin loads but doesn't affect MIDI

**Solutions**:
1. **Check MIDI routing** - Ensure MIDI is going through the plugin
2. **Verify parameters** - Make sure Swing Ratio > 0.5 or Accent Amount > 0
3. **Test with control plane** - Use Python commands to send MIDI

### OSC Control Not Working

**Problem**: Python OSC commands don't affect the plugin

**Solutions**:
1. **Enable OSC** - Set "OSC Enabled" to "On" in the plugin
2. **Check port** - Ensure OSC Port matches Python settings (default: 3819)
3. **Test connection**:
   ```bash
   python control_plane_cli.py "set osc enabled to on"
   python control_plane_cli.py "set swing to 0.7"
   ```

## Advanced Usage

### Style Presets

The plugin supports 5 built-in style presets:

- **Jazz**: swing=0.7, accent=25, humanize_timing=0.3, humanize_velocity=0.4
- **Classical**: swing=0.5, accent=15, humanize_timing=0.2, humanize_velocity=0.3
- **Electronic**: swing=0.5, accent=5, humanize_timing=0.0, humanize_velocity=0.0
- **Blues**: swing=0.6, accent=30, humanize_timing=0.4, humanize_velocity=0.5
- **Straight**: swing=0.5, accent=0, humanize_timing=0.0, humanize_velocity=0.0

### Real-Time Control

You can control the plugin in real-time while playing:

```bash
# Start with straight timing
python control_plane_cli.py "set swing to 0.5"

# Gradually increase swing
python control_plane_cli.py "set swing to 0.6"
python control_plane_cli.py "set swing to 0.7"
python control_plane_cli.py "set swing to 0.8"

# Add accent
python control_plane_cli.py "set accent to 20"
python control_plane_cli.py "set accent to 30"
```

## Performance Notes

- **Real-time Safe**: The plugin is designed for real-time audio processing
- **Low Latency**: Minimal processing delay for live performance
- **CPU Efficient**: Optimized for minimal CPU usage
- **Thread Safe**: OSC control doesn't interfere with audio processing

## Next Steps

Once you have the plugin working in GarageBand:

1. **Experiment with different styles** using the presets
2. **Try real-time control** with the Python commands
3. **Create your own MIDI patterns** and apply transformations
4. **Explore the semantic MIDI editor** for offline editing

## Support

If you encounter issues:

1. **Check the main README.md** for general troubleshooting
2. **Review the test results** by running `python test_plugin.py`
3. **Verify plugin validation** with `auval -v aumf StTr Mcrs`
4. **Check the logs** in the terminal when running commands

The plugin has been thoroughly tested and validated for GarageBand compatibility. It should work seamlessly once properly loaded.
