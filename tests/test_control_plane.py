#!/usr/bin/env python3
"""
Test script for the control plane.

This script tests the control plane functionality without requiring MIDI hardware.
"""

from __future__ import annotations

import sys
import time
from unittest.mock import Mock, patch

# Mock the MIDI components for testing
sys.modules['mido'] = Mock()
sys.modules['python_rtmidi'] = Mock()

from commands.control_plane import ControlPlane
from commands.parser import CommandParser
from commands.session import SessionManager
from commands.types import CommandType


def test_command_parser():
    """Test the command parser."""
    print("Testing Command Parser...")
    
    parser = CommandParser()
    
    # Test valid commands
    test_cases = [
        ("play scale C major", CommandType.PLAY_SCALE),
        ("play arp D minor", CommandType.PLAY_ARP),
        ("play random 8", CommandType.PLAY_RANDOM),
        ("set key to F# lydian", CommandType.SET_KEY),
        ("set density to high", CommandType.SET_DENSITY),
        ("set tempo to 140", CommandType.SET_TEMPO),
        ("set randomness to 0.3", CommandType.SET_RANDOMNESS),
        ("set velocity to 100", CommandType.SET_VELOCITY),
        ("set register to 5", CommandType.SET_REGISTER),
        ("cc 74 to 64", CommandType.CC),
        ("mod wheel 32", CommandType.MOD),
        ("target piano", CommandType.TARGET),
        ("stop", CommandType.STOP),
        ("status", CommandType.STATUS),
        ("help", CommandType.HELP),
    ]
    
    for command_text, expected_type in test_cases:
        command = parser.parse(command_text)
        assert command is not None, f"Failed to parse: {command_text}"
        assert command.type == expected_type, f"Wrong type for '{command_text}': {command.type} != {expected_type}"
        print(f"  ✓ {command_text}")
    
    # Test invalid commands
    invalid_commands = ["invalid command", "play", "set", ""]
    for command_text in invalid_commands:
        command = parser.parse(command_text)
        assert command is None, f"Should not parse: {command_text}"
        print(f"  ✓ (correctly rejected) {command_text}")
    
    print("Command Parser tests passed!\n")


def test_session_manager():
    """Test the session manager."""
    print("Testing Session Manager...")
    
    import tempfile
    import os
    
    # Create a temporary session file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        session = SessionManager(temp_file)
        
        # Test initial state
        state = session.get_state()
        assert state.key == "C"
        assert state.mode.value == "major"
        assert state.tempo == 120
        print("  ✓ Initial state correct")
        
        # Test state updates
        from commands.types import Command, CommandType
        command = Command(CommandType.SET_KEY, {"key": "D", "mode": "minor"}, "test")
        session.update_from_command(command)
        
        state = session.get_state()
        assert state.key == "D"
        assert state.mode.value == "minor"
        print("  ✓ State update works")
        
        # Test MIDI note conversion
        midi_note = session.get_midi_root_note()
        assert midi_note == 62  # D4
        print("  ✓ MIDI note conversion works")
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    print("Session Manager tests passed!\n")


def test_pattern_engine():
    """Test the pattern engine."""
    print("Testing Pattern Engine...")
    
    from commands.pattern_engine import PatternEngine
    from commands.types import Command, CommandType, SessionState, Mode, Density
    
    engine = PatternEngine()
    state = SessionState(key="C", mode=Mode.MAJOR, density=Density.MEDIUM)
    
    # Test scale pattern generation
    command = Command(CommandType.PLAY_SCALE, {"key": "C", "mode": "major"}, "test")
    notes = engine.generate_pattern(command, state)
    assert len(notes) > 0, "Should generate notes for scale"
    print(f"  ✓ Generated {len(notes)} notes for scale")
    
    # Test arpeggio pattern generation
    command = Command(CommandType.PLAY_ARP, {"key": "C", "chord_type": "major"}, "test")
    notes = engine.generate_pattern(command, state)
    assert len(notes) > 0, "Should generate notes for arpeggio"
    print(f"  ✓ Generated {len(notes)} notes for arpeggio")
    
    # Test random pattern generation
    command = Command(CommandType.PLAY_RANDOM, {"count": 5}, "test")
    notes = engine.generate_pattern(command, state)
    assert len(notes) == 5, "Should generate exactly 5 random notes"
    print(f"  ✓ Generated {len(notes)} random notes")
    
    print("Pattern Engine tests passed!\n")


def test_control_plane_mock():
    """Test the control plane with mocked MIDI."""
    print("Testing Control Plane (mocked)...")
    
    # Mock the MIDI player
    mock_midi_player = Mock()
    mock_midi_player.port = Mock()
    mock_midi_player.port.send = Mock()
    
    with patch('commands.control_plane.MidiPlayer', return_value=mock_midi_player):
        with patch('commands.control_plane.Sequencer') as mock_sequencer_class:
            # Create a mock sequencer
            mock_sequencer = Mock()
            mock_sequencer_class.return_value = mock_sequencer
            
            # Test control plane creation
            control_plane = ControlPlane()
            
            # Test command execution
            result = control_plane.execute("set key to D minor")
            assert "Updated:" in result and "Key set to D Minor" in result
            print("  ✓ Set key command works")
            
            result = control_plane.execute("set tempo to 140")
            assert "Updated:" in result and "Tempo set to 140" in result
            print("  ✓ Set tempo command works")
            
            result = control_plane.execute("status")
            assert "Current Session State" in result
            print("  ✓ Status command works")
            
            result = control_plane.execute("help")
            assert "Available Commands" in result
            print("  ✓ Help command works")
            
            # Test invalid command
            result = control_plane.execute("invalid command")
            assert "Unknown command" in result
            print("  ✓ Invalid command handling works")
            
            control_plane.close()
    
    print("Control Plane tests passed!\n")


def main():
    """Run all tests."""
    print("Running Control Plane Tests")
    print("=" * 40)
    
    try:
        test_command_parser()
        test_session_manager()
        test_pattern_engine()
        test_control_plane_mock()
        
        print("All tests passed! 🎉")
        return 0
    
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
