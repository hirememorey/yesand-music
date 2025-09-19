#!/bin/bash
#
# run_in_ardour_env.sh: Executes a given command inside the full Ardour runtime env.
#
# This script ensures that any diagnostic tool (dtruss, lldb, etc.) is run
# with the exact same environment variables that a normal launch of Ardour would have.
#
# Usage: ./run_in_ardour_env.sh <command_to_run> [args...]
# Example: ./run_in_ardour_env.sh lldb ./build/gtk2_ardour/ardour-8.9.0

set -e

# --- Source the Environment Specification ---
# We slightly modify the logic of the original launch script. Instead of exec-ing
# Ardour at the end, this script will set up the environment and then exec
# whatever command was passed to it.

# Default Ardour build path
ARDOUR_BUILD="${ARDOUR_BUILD:-$HOME/Documents/Development/Audio/ardour/build}"

# Basic validation
if [ ! -d "$ARDOUR_BUILD" ]; then
    echo "Error: Ardour build directory not found at $ARDOUR_BUILD"
    exit 1
fi

# --- SYSTEM B: GTK ---
export GTK_PATH="$ARDOUR_BUILD/libs/clearlooks-newer"

# --- SYSTEM A: Ardour ---
export ARDOUR_DATA_PATH="$ARDOUR_BUILD/gtk2_ardour:$HOME/Documents/Development/Audio/ardour/gtk2_ardour"
export ARDOUR_CONFIG_PATH="$HOME/Library/Preferences/Ardour8"
PANNER_PATHS=$(ls -d "$ARDOUR_BUILD/libs/panners"/*/ | tr '\n' ':' | sed 's/:$//')
export ARDOUR_DLL_PATH="$ARDOUR_BUILD/gtk2_ardour:$PANNER_PATHS"
export ARDOUR_BACKEND_PATH="$ARDOUR_BUILD/libs/backends/coreaudio:$ARDOUR_BUILD/libs/backends/dummy"

# --- PRE-FLIGHT CONFIGURATION ---
# This can be run safely multiple times.
mkdir -p "$ARDOUR_CONFIG_PATH"
if [ ! -f "$ARDOUR_CONFIG_PATH/ardour.keys" ]; then
    echo "Pre-populating .keys file..."
    cp "$ARDOUR_BUILD/gtk2_ardour/ardour.keys" "$ARDOUR_CONFIG_PATH/ardour.keys"
fi
if [ ! -f "$ARDOUR_CONFIG_PATH/ardour.menus" ]; then
    echo "Pre-populating .menus file..."
    cp "$ARDOUR_BUILD/gtk2_ardour/ardour.menus" "$ARDOUR_CONFIG_PATH/ardour.menus"
fi

echo "Ardour environment configured. Executing command: $@"
echo "----------------------------------------------------"

# Execute the command you passed in ($1, $2, etc.)
exec "$@"


