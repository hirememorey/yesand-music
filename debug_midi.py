#!/usr/bin/env python3
"""
Debug MIDI connection to Ardour
"""

import rtmidi
import time
import sys

def test_midi_connection():
    """Test MIDI connection and send test notes"""
    print("🎵 MIDI Debug Tool for Ardour")
    print("=" * 40)
    
    try:
        # Initialize MIDI output
        midi_out = rtmidi.MidiOut()
        
        # List available ports
        ports = midi_out.get_ports()
        print(f"Available MIDI ports: {ports}")
        
        if not ports:
            print("❌ No MIDI ports found!")
            return False
        
        # Find IAC Driver
        iac_port = None
        for i, port in enumerate(ports):
            if 'IAC Driver' in port:
                iac_port = i
                print(f"✅ Found IAC Driver at port {i}: {port}")
                break
        
        if iac_port is None:
            print("❌ IAC Driver not found!")
            return False
        
        # Open the port
        midi_out.open_port(iac_port)
        print("✅ Connected to IAC Driver")
        
        print("\n🎼 Sending test MIDI sequence...")
        print("Make sure Ardour is:")
        print("1. Has a project open")
        print("2. Has a MIDI track created")
        print("3. Track is armed for recording (red R button)")
        print("4. Recording is active (red record button)")
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        # Send a simple scale
        scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
        note_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
        
        for i, (note, name) in enumerate(zip(scale_notes, note_names)):
            print(f"  Playing {name}4 (note {note})")
            
            # Note on
            midi_out.send_message([0x90, note, 100])
            time.sleep(0.5)
            
            # Note off
            midi_out.send_message([0x80, note, 0])
            time.sleep(0.1)
        
        print("\n✅ Test sequence sent!")
        print("Check Ardour for recorded MIDI events.")
        
        # Close the port
        midi_out.close_port()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_midi_connection()
    if success:
        print("\n🎉 MIDI test completed successfully!")
    else:
        print("\n💥 MIDI test failed!")
        sys.exit(1)
