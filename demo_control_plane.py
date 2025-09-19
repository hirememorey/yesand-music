#!/usr/bin/env python3
"""
Demo script for the control plane.

This script demonstrates the control plane functionality with example commands.
"""

from __future__ import annotations

import time
from commands.control_plane import ControlPlane


def main():
    """Run the control plane demo."""
    print("Control Plane Demo")
    print("=================")
    print()
    print("This demo will show various control plane commands.")
    print("Make sure you have:")
    print("1. IAC Driver enabled with 'IAC Driver Bus 1' port")
    print("2. GarageBand open with an armed Software Instrument track")
    print()
    
    input("Press Enter to continue...")
    print()
    
    try:
        with ControlPlane() as control_plane:
            # Demo commands
            demo_commands = [
                "status",
                "set key to D minor",
                "set tempo to 100",
                "set density to high",
                "set randomness to 0.2",
                "play scale D minor",
                "stop",
                "play arp D minor",
                "stop",
                "play random 6",
                "stop",
                "set key to C major",
                "set tempo to 120",
                "play scale C major",
                "stop",
                "status",
            ]
            
            for command in demo_commands:
                print(f"Command: {command}")
                result = control_plane.execute(command)
                print(f"Result: {result}")
                print()
                
                # Small delay between commands
                time.sleep(0.5)
            
            print("Demo completed!")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure MIDI port is available and GarageBand is set up correctly.")


if __name__ == "__main__":
    main()
