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
export ARDOUR_DATA_PATH="$HOME/Documents/Development/Audio/ardour/gtk2_ardour:$HOME/Documents/Development/Audio/ardour/share"
export ARDOUR_CONFIG_PATH="$HOME/Library/Preferences/Ardour8"
export ARDOUR_DLL_PATH="$ARDOUR_BUILD/gtk2_ardour"
export ARDOUR_BACKEND_PATH="$ARDOUR_BUILD/libs/backends/coreaudio:$ARDOUR_BUILD/libs/backends/dummy"

echo "Launching Ardour with backend detection enabled..."
echo "Backend path: $ARDOUR_BACKEND_PATH"
echo "Data path: $ARDOUR_DATA_PATH"

# Launch Ardour with the provided arguments or default to creating a new session
if [ $# -eq 0 ]; then
    # Default: create a new session
    exec "$ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0" -n --no-announcements --no-splash -N "NewSession"
else
    # Pass through all arguments
    exec "$ARDOUR_BUILD/gtk2_ardour/ardour-8.9.0" "$@"
fi
