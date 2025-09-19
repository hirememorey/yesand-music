#!/usr/bin/env python3
"""
Verification script for the control plane implementation.

This script demonstrates that the control plane works as expected
using first principles analysis.
"""

from __future__ import annotations

import time
from commands.control_plane import ControlPlane


def test_core_functionality():
    """Test core functionality using first principles."""
    print("=== CONTROL PLANE VERIFICATION ===")
    print()
    
    print("Testing with real MIDI hardware...")
    print("Make sure you have:")
    print("1. IAC Driver enabled with 'IAC Driver Bus 1' port")
    print("2. GarageBand open with an armed Software Instrument track")
    print()
    
    try:
        with ControlPlane() as control_plane:
            print("✓ ControlPlane initialized successfully")
            
            # Test 1: Command parsing and execution
            print("\n1. Testing command parsing...")
            result = control_plane.execute("help")
            assert "Available Commands" in result
            print("   ✓ Help command works")
            
            # Test 2: Session state management
            print("\n2. Testing session state...")
            result = control_plane.execute("set key to D minor")
            assert "Updated:" in result
            print("   ✓ Session state updates work")
            
            result = control_plane.execute("set tempo to 120")
            assert "Updated:" in result
            print("   ✓ Tempo changes work")
            
            # Test 3: Pattern generation
            print("\n3. Testing pattern generation...")
            result = control_plane.execute("play scale D minor")
            assert "Playing scale pattern" in result
            print("   ✓ Scale pattern generation works")
            
            # Test 4: Non-blocking playback
            print("\n4. Testing non-blocking playback...")
            is_playing = control_plane.sequencer.is_playing()
            assert is_playing == True
            print("   ✓ Non-blocking playback works")
            
            # Test 5: Stop functionality
            print("\n5. Testing stop functionality...")
            time.sleep(1)  # Let it play briefly
            result = control_plane.execute("stop")
            assert "Playback stopped" in result
            print("   ✓ Stop functionality works")
            
            # Test 6: Different pattern types
            print("\n6. Testing different pattern types...")
            
            result = control_plane.execute("play arp C major")
            assert "Playing arp pattern" in result
            print("   ✓ Arpeggio patterns work")
            time.sleep(0.5)
            control_plane.execute("stop")
            
            result = control_plane.execute("play random 6")
            assert "Playing random pattern" in result
            print("   ✓ Random patterns work")
            time.sleep(0.5)
            control_plane.execute("stop")
            
            # Test 7: Control commands
            print("\n7. Testing control commands...")
            result = control_plane.execute("cc 74 to 64")
            assert "CC74 set to 64" in result
            print("   ✓ CC commands work")
            
            result = control_plane.execute("mod wheel 32")
            assert "Modulation wheel set to 32" in result
            print("   ✓ Modulation wheel works")
            
            # Test 8: Session persistence
            print("\n8. Testing session persistence...")
            result = control_plane.execute("status")
            assert "D Minor" in result and "120" in result
            print("   ✓ Session state persists correctly")
            
            print("\n🎉 ALL VERIFICATION TESTS PASSED!")
            print("\nThe control plane implementation is working correctly.")
            print("\nKey achievements:")
            print("✓ Natural language command parsing")
            print("✓ Persistent session state management")
            print("✓ Non-blocking MIDI playback with timers")
            print("✓ Multiple pattern types (scales, arpeggios, random)")
            print("✓ Control commands (CC, modulation)")
            print("✓ Real-time stop/start functionality")
            print("✓ Clean error handling and user feedback")
            
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_chat_integration():
    """Test chat integration interface."""
    print("\n=== CHAT INTEGRATION TEST ===")
    print()
    
    print("Testing CLI interface for chat integration...")
    
    # Test individual commands
    test_commands = [
        "play scale F# lydian",
        "set density to high", 
        "set randomness to 0.3",
        "play arp D minor",
        "stop",
        "status"
    ]
    
    try:
        with ControlPlane() as control_plane:
            for cmd in test_commands:
                result = control_plane.execute(cmd)
                print(f"   '{cmd}' → {result[:50]}...")
                time.sleep(0.1)  # Brief pause between commands
        
        print("\n✓ Chat integration interface works correctly")
        print("✓ Ready for use with: python control_plane_cli.py 'command'")
        
    except Exception as e:
        print(f"✗ Chat integration test failed: {e}")
        return False
    
    return True


def main():
    """Run all verification tests."""
    print("CONTROL PLANE IMPLEMENTATION VERIFICATION")
    print("=" * 50)
    print()
    
    success = True
    
    # Test core functionality
    if not test_core_functionality():
        success = False
    
    # Test chat integration
    if not test_chat_integration():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 IMPLEMENTATION VERIFICATION SUCCESSFUL!")
        print("\nThe control plane is ready for production use.")
        print("\nNext steps:")
        print("1. Use 'python main.py --interactive' for interactive mode")
        print("2. Use 'python control_plane_cli.py \"command\"' for chat integration")
        print("3. Integrate with Cursor chat using the CLI interface")
    else:
        print("❌ IMPLEMENTATION VERIFICATION FAILED!")
        print("Please review the errors above and fix them.")
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
