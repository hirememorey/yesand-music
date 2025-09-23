#!/usr/bin/env python3
"""
Demo script for Ardour file-based integration.

This script demonstrates the file-based Ardour integration workflow:
1. Connect to Ardour
2. List tracks
3. Export selected region
4. Analyze exported MIDI
5. Improve the exported MIDI
6. Import improved version back
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from commands.control_plane import ControlPlane


def demo_ardour_integration():
    """Demonstrate Ardour integration functionality."""
    print("🎵 YesAnd Music - Ardour Integration Demo")
    print("=" * 50)
    
    # Initialize control plane
    try:
        with ControlPlane() as cp:
            print("✅ Control plane initialized")
            
            # Test Ardour connection
            print("\n1. Testing Ardour connection...")
            result = cp.execute("ardour connect")
            print(f"   {result}")
            
            if "Failed" in result:
                print("   ⚠️  Ardour not running. Starting Ardour...")
                print("   Please start Ardour manually and try again.")
                return
            
            # List tracks
            print("\n2. Listing Ardour tracks...")
            result = cp.execute("ardour tracks")
            print(f"   {result}")
            
            # Export selected region
            print("\n3. Exporting selected region...")
            result = cp.execute("ardour export selected")
            print(f"   {result}")
            
            # Analyze exported region
            print("\n4. Analyzing exported region...")
            result = cp.execute("ardour analyze selected")
            print(f"   {result}")
            
            # Improve exported region
            print("\n5. Improving exported region...")
            result = cp.execute("ardour improve selected")
            print(f"   {result}")
            
            # Test import functionality
            print("\n6. Testing MIDI import...")
            # Create a simple test MIDI file
            test_midi = "test_ardour_import.mid"
            result = cp.execute(f"ardour import {test_midi}")
            print(f"   {result}")
            
            # Disconnect
            print("\n7. Disconnecting from Ardour...")
            result = cp.execute("ardour disconnect")
            print(f"   {result}")
            
            print("\n✅ Ardour integration demo completed!")
            
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        return False
    
    return True


def interactive_demo():
    """Interactive demo mode."""
    print("🎵 YesAnd Music - Interactive Ardour Demo")
    print("=" * 50)
    print("Available commands:")
    print("  ardour connect          - Connect to Ardour")
    print("  ardour tracks           - List tracks")
    print("  ardour export selected  - Export selected region")
    print("  ardour analyze selected - Analyze exported region")
    print("  ardour improve selected - Improve exported region")
    print("  ardour import [FILE]    - Import MIDI file")
    print("  ardour disconnect       - Disconnect from Ardour")
    print("  help                    - Show all commands")
    print("  quit                    - Exit demo")
    print()
    
    try:
        with ControlPlane() as cp:
            while True:
                try:
                    command = input("YesAnd> ").strip()
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if not command:
                        continue
                    
                    result = cp.execute(command)
                    print(f"   {result}")
                    print()
                    
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
    
    except Exception as e:
        print(f"Failed to initialize control plane: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        demo_ardour_integration()
