#!/usr/bin/env python3
"""
Demo script for OSC integration with JUCE plugin.

This script demonstrates the complete OSC integration between the Python
control plane and the JUCE StyleTransfer plugin.
"""

import time
import logging
from commands.control_plane import ControlPlane

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demo_osc_commands():
    """Demonstrate OSC command functionality."""
    print("🎵 YesAnd Music OSC Integration Demo")
    print("=" * 50)
    print("This demo shows how the Python control plane can remotely")
    print("control the JUCE StyleTransfer plugin via OSC messages.")
    print()
    print("Prerequisites:")
    print("1. JUCE plugin loaded in your DAW with OSC enabled")
    print("2. Plugin listening on port 3819 (default)")
    print("3. python-osc library installed: pip install python-osc")
    print()
    
    try:
        # Initialize control plane
        print("Initializing control plane...")
        control_plane = ControlPlane()
        print("✅ Control plane initialized")
        print()
        
        # Test OSC connection
        print("Testing OSC connection...")
        if control_plane.osc_sender.test_connection():
            print("✅ OSC connection successful")
        else:
            print("❌ OSC connection failed - make sure plugin is running with OSC enabled")
            return
        print()
        
        # Demo 1: Basic parameter control
        print("=== Demo 1: Basic Parameter Control ===")
        demos = [
            ("set swing to 0.7", "Set swing ratio to 70%"),
            ("set accent to 25", "Set accent amount to 25"),
            ("set humanize timing to 0.3", "Set timing humanization to 30%"),
            ("set humanize velocity to 0.4", "Set velocity humanization to 40%"),
        ]
        
        for command, description in demos:
            print(f"Command: {command}")
            print(f"Description: {description}")
            response = control_plane.execute(command)
            print(f"Response: {response}")
            time.sleep(1.0)  # Wait between commands
            print()
        
        # Demo 2: Style presets
        print("=== Demo 2: Style Presets ===")
        presets = [
            ("set style to jazz", "Apply jazz style preset"),
            ("set style to classical", "Apply classical style preset"),
            ("set style to electronic", "Apply electronic style preset"),
            ("set style to blues", "Apply blues style preset"),
            ("set style to straight", "Apply straight (no effects) preset"),
        ]
        
        for command, description in presets:
            print(f"Command: {command}")
            print(f"Description: {description}")
            response = control_plane.execute(command)
            print(f"Response: {response}")
            time.sleep(2.0)  # Wait longer to hear the effect
            print()
        
        # Demo 3: OSC control commands
        print("=== Demo 3: OSC Control Commands ===")
        osc_commands = [
            ("set osc enabled to on", "Enable OSC control"),
            ("set osc port to 3819", "Set OSC port to 3819"),
            ("reset osc", "Reset all parameters to defaults"),
        ]
        
        for command, description in osc_commands:
            print(f"Command: {command}")
            print(f"Description: {description}")
            response = control_plane.execute(command)
            print(f"Response: {response}")
            time.sleep(1.0)
            print()
        
        # Demo 4: Combined MIDI and OSC
        print("=== Demo 4: Combined MIDI and OSC Control ===")
        print("This demonstrates how MIDI playback and OSC style control work together:")
        print()
        
        # Set a style first
        print("Setting jazz style...")
        response = control_plane.execute("set style to jazz")
        print(f"Response: {response}")
        time.sleep(1.0)
        
        # Play some MIDI with the style applied
        print("Playing C major scale with jazz style...")
        response = control_plane.execute("play scale C major")
        print(f"Response: {response}")
        time.sleep(3.0)  # Let it play
        
        # Change style while playing
        print("Changing to classical style...")
        response = control_plane.execute("set style to classical")
        print(f"Response: {response}")
        time.sleep(1.0)
        
        # Play another scale
        print("Playing D minor scale with classical style...")
        response = control_plane.execute("play scale D minor")
        print(f"Response: {response}")
        time.sleep(3.0)
        
        # Stop playback
        print("Stopping playback...")
        response = control_plane.execute("stop")
        print(f"Response: {response}")
        print()
        
        # Demo 5: Error handling
        print("=== Demo 5: Error Handling ===")
        error_commands = [
            ("set swing to 1.5", "Invalid swing value (should be clamped to 1.0)"),
            ("set accent to -10", "Invalid accent value (should be clamped to 0.0)"),
            ("set style to invalid", "Invalid style preset (should be rejected)"),
        ]
        
        for command, description in error_commands:
            print(f"Command: {command}")
            print(f"Description: {description}")
            response = control_plane.execute(command)
            print(f"Response: {response}")
            print()
        
        print("=== Demo Complete ===")
        print("The OSC integration allows you to:")
        print("• Control style parameters in real-time")
        print("• Apply style presets with single commands")
        print("• Combine MIDI playback with style effects")
        print("• Use natural language for all operations")
        print()
        print("Try these commands in your control plane:")
        print("  python control_plane_cli.py 'set swing to 0.8'")
        print("  python control_plane_cli.py 'make it jazzier'")
        print("  python control_plane_cli.py 'set humanize timing to 0.5'")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.exception("Demo error")
    
    finally:
        # Cleanup
        try:
            control_plane.close()
            print("✅ Control plane closed")
        except:
            pass


def demo_help_commands():
    """Show all available OSC commands."""
    print("\n=== Available OSC Commands ===")
    
    try:
        control_plane = ControlPlane()
        help_text = control_plane.execute("help")
        print(help_text)
    except Exception as e:
        print(f"❌ Failed to get help: {e}")
    finally:
        try:
            control_plane.close()
        except:
            pass


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        demo_help_commands()
    else:
        demo_osc_commands()
