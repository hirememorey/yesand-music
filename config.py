"""
Global configuration settings for the MIDI framework.

Edit these values to change the default MIDI output port, tempo, and OSC settings.
"""

# Name of the virtual MIDI output port (e.g., IAC Driver on macOS)
MIDI_PORT_NAME: str = "IAC Driver Bus 1"

# Global tempo in beats per minute
BPM: int = 120

# OSC communication settings for JUCE plugin control
OSC_IP_ADDRESS: str = "127.0.0.1"  # IP address of the JUCE plugin
OSC_PORT: int = 3819  # OSC port number (matches JUCE plugin default)

# OSC message addresses for style parameters
OSC_ADDRESSES = {
    'swing': '/style/swing',
    'accent': '/style/accent', 
    'humanize_timing': '/style/humanizeTiming',
    'humanize_velocity': '/style/humanizeVelocity',
    'osc_enabled': '/style/enable',
    'osc_port': '/style/port'
}


