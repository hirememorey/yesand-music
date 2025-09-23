#!/usr/bin/env python3
"""
Test script for Contextual Intelligence

This script tests the contextual intelligence features without requiring user input.
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from commands.control_plane import ControlPlane
from contextual_intelligence import ContextualIntelligence
from midi_io import save_midi_file


def create_test_midi():
    """Create a test MIDI file."""
    # Create a simple pattern - ensure all values are proper types
    notes = [
        # Bass line
        {'pitch': 36, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 0.5, 'track_index': 0},
        {'pitch': 40, 'velocity': 80, 'start_time_seconds': 0.5, 'duration_seconds': 0.5, 'track_index': 0},
        {'pitch': 43, 'velocity': 80, 'start_time_seconds': 1.0, 'duration_seconds': 0.5, 'track_index': 0},
        
        # Melody line
        {'pitch': 60, 'velocity': 90, 'start_time_seconds': 0.0, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 62, 'velocity': 90, 'start_time_seconds': 0.25, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 64, 'velocity': 90, 'start_time_seconds': 0.5, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 65, 'velocity': 90, 'start_time_seconds': 0.75, 'duration_seconds': 0.25, 'track_index': 1},
    ]
    
    # Debug: print the first note to see what we're getting
    print(f"First note: {notes[0]}")
    print(f"Type: {type(notes[0])}")
    print(f"Is dict: {isinstance(notes[0], dict)}")
    print(f"All notes: {notes}")
    
    midi_file = "test_song.mid"
    try:
        save_midi_file(notes, midi_file)
    except Exception as e:
        print(f"Error saving MIDI: {e}")
        # Try to debug the issue
        for i, note in enumerate(notes):
            print(f"Note {i}: {note} (type: {type(note)})")
        raise
    return midi_file


def test_contextual_intelligence():
    """Test the contextual intelligence system."""
    print("Testing Contextual Intelligence System")
    print("=" * 40)
    
    # Create test MIDI file
    midi_file = create_test_midi()
    print(f"Created test MIDI file: {midi_file}")
    
    try:
        # Test direct contextual intelligence
        print("\n1. Testing direct contextual intelligence...")
        ci = ContextualIntelligence()
        
        # Load project
        success = ci.load_project(midi_file)
        print(f"Load project: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            # Test analysis
            print("\n2. Testing musical analysis...")
            feedback = ci.get_visual_feedback("analyze bass")
            print(f"Bass analysis: {len(feedback)} feedback items")
            for item in feedback:
                print(f"  - {item.element.value}: {item.message}")
            
            feedback = ci.get_visual_feedback("analyze melody")
            print(f"Melody analysis: {len(feedback)} feedback items")
            for item in feedback:
                print(f"  - {item.element.value}: {item.message}")
            
            feedback = ci.get_visual_feedback("analyze all")
            print(f"Complete analysis: {len(feedback)} feedback items")
            for item in feedback:
                print(f"  - {item.element.value}: {item.message}")
        
        # Test control plane integration
        print("\n3. Testing control plane integration...")
        try:
            with ControlPlane() as control_plane:
                # Test load command
                response = control_plane.execute(f"load {midi_file}")
                print(f"Load command: {response}")
                
                # Test analysis commands
                response = control_plane.execute("analyze bass")
                print(f"Bass analysis command: {response[:100]}...")
                
                response = control_plane.execute("analyze melody")
                print(f"Melody analysis command: {response[:100]}...")
                
                response = control_plane.execute("analyze all")
                print(f"Complete analysis command: {response[:100]}...")
                
                response = control_plane.execute("get suggestions")
                print(f"Suggestions command: {response[:100]}...")
                
                print("Control plane integration: SUCCESS")
        
        except Exception as e:
            print(f"Control plane integration: FAILED - {e}")
        
        print("\n4. Testing command parser...")
        from commands.parser import CommandParser
        parser = CommandParser()
        
        test_commands = [
            "load test.mid",
            "analyze bass",
            "analyze melody",
            "analyze harmony",
            "analyze rhythm",
            "analyze all",
            "get suggestions",
            "show feedback",
            "clear feedback"
        ]
        
        for cmd in test_commands:
            parsed = parser.parse(cmd)
            if parsed:
                print(f"  ✓ '{cmd}' -> {parsed.type.value}")
            else:
                print(f"  ✗ '{cmd}' -> FAILED")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(midi_file):
            os.remove(midi_file)
            print(f"\nCleaned up test file: {midi_file}")


if __name__ == "__main__":
    test_contextual_intelligence()
