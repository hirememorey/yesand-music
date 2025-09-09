#!/bin/bash
# Launch Ardour with correct environment variables for backend detection
# This script resolves the "No audio/MIDI backends detected" error

set -e

# Default Ardour build path
ARDOUR_BUILD="${ARDOUR_BUILD:-$HOME/Documents/Development/Audio/ardour/build}"

# Check if Ardour build exists
if [ ! -d "$ARDOUR_BUILD" ]; then
    echo "Error: Ardour build directory not found at $ARDOUR_BUILD"
    echo "Please set ARDOUR_BUILD environment variable or ensure Ardour is built at the default location"
    exit 1
fi

# Check if Ardour binary exists
if [ ! -f "$ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0" ]; then
    echo "Error: Ardour binary not found at $ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0"
    echo "Please ensure Ardour is built successfully"
    exit 1
fi

# Set environment variables for proper backend detection
# --- SYSTEM B: GTK ---
# GTK needs a path to find its theme engines (e.g., libclearlooks.dylib)
export GTK_PATH="$ARDOUR_BUILD/libs/clearlooks-newer"

# --- SYSTEM A: Ardour ---
# ARDOUR_DATA_PATH must be a composite path. It needs to find build artifacts
# (like menus) in the build output, and source assets (like fonts and color
# definitions) in the source tree. The build path must come first.
export ARDOUR_DATA_PATH="$ARDOUR_BUILD/gtk2_ardour:$HOME/Documents/Development/Audio/ardour/gtk2_ardour"
export ARDOUR_CONFIG_PATH="$HOME/Library/Preferences/Ardour8"
# ARDOUR_DLL_PATH must point to the main gtk2_ardour directory AND an
# explicit, colon-separated list of every panner plugin subdirectory.
PANNER_PATHS=$(ls -d "$ARDOUR_BUILD/libs/panners"/*/ | tr '\n' ':' | sed 's/:$//')
export ARDOUR_DLL_PATH="$ARDOUR_BUILD/gtk2_ardour:$PANNER_PATHS"
export ARDOUR_BACKEND_PATH="$ARDOUR_BUILD/libs/backends/coreaudio:$ARDOUR_BUILD/libs/backends/dummy"

# --- PRE-FLIGHT CONFIGURATION ---
# Ardour expects some essential files (menus, keybindings) to be present in its
# config directory on first launch. We copy them from the build output to
# satisfy this dependency before the application starts.
echo "Pre-populating config directory..."
mkdir -p "$ARDOUR_CONFIG_PATH"
cp "$ARDOUR_BUILD/gtk2_ardour/ardour.keys" "$ARDOUR_CONFIG_PATH/ardour.keys"
cp "$ARDOUR_BUILD/gtk2_ardour/ardour.menus" "$ARDOUR_CONFIG_PATH/ardour.menus"

echo "Launching Ardour..."
echo "Backend path: $ARDOUR_BACKEND_PATH"
echo "Data path: $ARDOUR_DATA_PATH"

# Launch Ardour with the provided arguments or default to creating a new session
if [ $# -eq 0 ]; then
    # Default: launch to the session dialog without creating a new session
    exec "$ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0" -n --no-announcements --no-splash
else
    # Pass through all arguments
    exec "$ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0" "$@"
fi
