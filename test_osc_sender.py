#!/usr/bin/env python3
"""
Test script for OSC Sender functionality.

This script tests the OSC communication with the JUCE plugin.
Run this after starting the JUCE plugin with OSC enabled.
"""

import time
import logging
from osc_sender import OSCSender, create_osc_sender, send_style_command
from config import OSC_IP_ADDRESS, OSC_PORT

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_basic_connection():
    """Test basic OSC connection."""
    print("=== Testing Basic OSC Connection ===")
    
    try:
        sender = create_osc_sender(OSC_IP_ADDRESS, OSC_PORT)
        print(f"Created OSC sender: {sender}")
        
        # Test connection
        if sender.test_connection():
            print("✅ OSC connection test passed")
        else:
            print("❌ OSC connection test failed")
            
        return sender
    except Exception as e:
        print(f"❌ Failed to create OSC sender: {e}")
        return None


def test_parameter_control(sender: OSCSender):
    """Test parameter control methods."""
    print("\n=== Testing Parameter Control ===")
    
    if not sender:
        print("❌ No sender available for testing")
        return
    
    # Test swing ratio
    print("Testing swing ratio...")
    if sender.set_swing_ratio(0.7):
        print("✅ Swing ratio set to 0.7")
    else:
        print("❌ Failed to set swing ratio")
    
    time.sleep(0.5)
    
    # Test accent amount
    print("Testing accent amount...")
    if sender.set_accent_amount(25.0):
        print("✅ Accent amount set to 25.0")
    else:
        print("❌ Failed to set accent amount")
    
    time.sleep(0.5)
    
    # Test humanize timing
    print("Testing humanize timing...")
    if sender.set_humanize_timing(0.3):
        print("✅ Humanize timing set to 0.3")
    else:
        print("❌ Failed to set humanize timing")
    
    time.sleep(0.5)
    
    # Test humanize velocity
    print("Testing humanize velocity...")
    if sender.set_humanize_velocity(0.4):
        print("✅ Humanize velocity set to 0.4")
    else:
        print("❌ Failed to set humanize velocity")
    
    time.sleep(0.5)
    
    # Test OSC enabled
    print("Testing OSC enabled...")
    if sender.set_osc_enabled(True):
        print("✅ OSC enabled set to True")
    else:
        print("❌ Failed to set OSC enabled")


def test_style_presets(sender: OSCSender):
    """Test style preset functionality."""
    print("\n=== Testing Style Presets ===")
    
    if not sender:
        print("❌ No sender available for testing")
        return
    
    presets = ['jazz', 'classical', 'electronic', 'blues', 'straight']
    
    for preset in presets:
        print(f"Testing {preset} preset...")
        if sender.set_style_preset(preset):
            print(f"✅ {preset} preset applied successfully")
        else:
            print(f"❌ Failed to apply {preset} preset")
        time.sleep(1.0)  # Wait between presets


def test_convenience_functions():
    """Test convenience functions."""
    print("\n=== Testing Convenience Functions ===")
    
    # Test single command function
    print("Testing single command function...")
    if send_style_command('/style/swing', 0.8, OSC_IP_ADDRESS, OSC_PORT):
        print("✅ Single command sent successfully")
    else:
        print("❌ Failed to send single command")
    
    time.sleep(0.5)
    
    # Test with different values
    test_values = [
        ('/style/accent', 30.0),
        ('/style/humanizeTiming', 0.5),
        ('/style/humanizeVelocity', 0.6)
    ]
    
    for address, value in test_values:
        print(f"Testing {address} = {value}...")
        if send_style_command(address, value, OSC_IP_ADDRESS, OSC_PORT):
            print(f"✅ {address} = {value} sent successfully")
        else:
            print(f"❌ Failed to send {address} = {value}")
        time.sleep(0.5)


def test_error_handling(sender: OSCSender):
    """Test error handling and edge cases."""
    print("\n=== Testing Error Handling ===")
    
    if not sender:
        print("❌ No sender available for testing")
        return
    
    # Test invalid values (should be clamped)
    print("Testing value clamping...")
    
    # Test swing ratio clamping
    sender.set_swing_ratio(-0.5)  # Should be clamped to 0.0
    sender.set_swing_ratio(1.5)   # Should be clamped to 1.0
    print("✅ Value clamping tested")
    
    # Test accent amount clamping
    sender.set_accent_amount(-10.0)  # Should be clamped to 0.0
    sender.set_accent_amount(100.0)  # Should be clamped to 50.0
    print("✅ Accent amount clamping tested")
    
    # Test invalid preset
    print("Testing invalid preset...")
    if not sender.set_style_preset('invalid_preset'):
        print("✅ Invalid preset correctly rejected")
    else:
        print("❌ Invalid preset should have been rejected")


def main():
    """Main test function."""
    print("🎵 YesAnd Music OSC Sender Test")
    print("=" * 50)
    print(f"Target: {OSC_IP_ADDRESS}:{OSC_PORT}")
    print("Make sure the JUCE plugin is running with OSC enabled!")
    print()
    
    # Test basic connection
    sender = test_basic_connection()
    
    if sender:
        # Test parameter control
        test_parameter_control(sender)
        
        # Test style presets
        test_style_presets(sender)
        
        # Test convenience functions
        test_convenience_functions()
        
        # Test error handling
        test_error_handling(sender)
        
        # Reset to defaults
        print("\n=== Resetting to Defaults ===")
        if sender.reset_to_defaults():
            print("✅ Reset to defaults successful")
        else:
            print("❌ Failed to reset to defaults")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nTo use OSC in your control plane:")
    print("  from osc_sender import OSCSender")
    print("  sender = OSCSender()")
    print("  sender.set_swing_ratio(0.7)")


if __name__ == "__main__":
    main()
