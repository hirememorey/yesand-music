"""
Pattern engine for generating musical patterns.

This module provides the PatternEngine class that generates musical patterns
based on commands and session state.
"""

from __future__ import annotations

from typing import List

from .types import Command, CommandType, Note, SessionState
from theory import (
    apply_randomness,
    create_arpeggio,
    create_random_notes,
    create_rhythmic_pattern,
    create_scale,
    get_scale_notes_for_mode,
)


class PatternEngine:
    """Generates musical patterns based on commands and session state."""
    
    def __init__(self) -> None:
        """Initialize the pattern engine."""
        pass
    
    def generate_pattern(self, command: Command, state: SessionState) -> List[Note]:
        """Generate a musical pattern based on a command and session state.
        
        Args:
            command: The command to execute
            state: Current session state
            
        Returns:
            List of Note objects representing the pattern
        """
        if command.type == CommandType.PLAY_SCALE:
            return self._generate_scale_pattern(command, state)
        elif command.type == CommandType.PLAY_ARP:
            return self._generate_arpeggio_pattern(command, state)
        elif command.type == CommandType.PLAY_RANDOM:
            return self._generate_random_pattern(command, state)
        else:
            return []
    
    def _generate_scale_pattern(self, command: Command, state: SessionState) -> List[Note]:
        """Generate a scale pattern.
        
        Args:
            command: The play scale command
            state: Current session state
            
        Returns:
            List of Note objects for the scale
        """
        # Get key and mode from command or use session defaults
        key = command.params.get("key", state.key)
        mode_str = command.params.get("mode", state.mode.value)
        
        # Convert key to MIDI note
        root_note = self._key_to_midi_note(key, state.register)
        
        # Convert mode string to Mode enum
        try:
            from .types import Mode
            mode = Mode(mode_str.lower())
        except ValueError:
            mode = state.mode
        
        # Generate scale notes
        scale_notes = create_scale(root_note, mode)
        
        # Create rhythmic pattern
        notes = create_rhythmic_pattern(scale_notes, state.density)
        
        # Apply session state
        notes = self._apply_session_state(notes, state)
        
        return notes
    
    def _generate_arpeggio_pattern(self, command: Command, state: SessionState) -> List[Note]:
        """Generate an arpeggio pattern.
        
        Args:
            command: The play arp command
            state: Current session state
            
        Returns:
            List of Note objects for the arpeggio
        """
        # Get key and chord type from command
        key = command.params.get("key", state.key)
        chord_type = command.params.get("chord_type", "major")
        
        # Convert key to MIDI note
        root_note = self._key_to_midi_note(key, state.register)
        
        # Generate arpeggio notes
        arp_notes = create_arpeggio(root_note, chord_type, "up")
        
        # Create rhythmic pattern
        notes = create_rhythmic_pattern(arp_notes, state.density)
        
        # Apply session state
        notes = self._apply_session_state(notes, state)
        
        return notes
    
    def _generate_random_pattern(self, command: Command, state: SessionState) -> List[Note]:
        """Generate a random pattern.
        
        Args:
            command: The play random command
            state: Current session state
            
        Returns:
            List of Note objects for the random pattern
        """
        # Get count from command
        count = command.params.get("count", 8)
        
        # Get root note from session state
        root_note = self._key_to_midi_note(state.key, state.register)
        
        # Generate scale notes for the current mode
        scale_notes = create_scale(root_note, state.mode)
        
        # Generate random notes from the scale
        random_notes = create_random_notes(root_note, count, scale_notes)
        
        # Create rhythmic pattern
        notes = create_rhythmic_pattern(random_notes, state.density)
        
        # Apply session state
        notes = self._apply_session_state(notes, state)
        
        return notes
    
    def _apply_session_state(self, notes: List[Note], state: SessionState) -> List[Note]:
        """Apply session state to a list of notes.
        
        Args:
            notes: List of Note objects
            state: Current session state
            
        Returns:
            List of Note objects with session state applied
        """
        # Apply velocity
        for note in notes:
            note.velocity = state.velocity
        
        # Apply randomness
        if state.randomness > 0.0:
            notes = apply_randomness(notes, state.randomness)
        
        return notes
    
    def _key_to_midi_note(self, key: str, register: int) -> int:
        """Convert a key name and register to a MIDI note number.
        
        Args:
            key: Key name (e.g., "C", "F#", "Bb")
            register: MIDI octave (0-9)
            
        Returns:
            MIDI note number (0-127)
        """
        # Note name to semitone offset from C
        note_offsets = {
            'C': 0, 'C#': 1, 'DB': 1,
            'D': 2, 'D#': 3, 'EB': 3,
            'E': 4,
            'F': 5, 'F#': 6, 'GB': 6,
            'G': 7, 'G#': 8, 'AB': 8,
            'A': 9, 'A#': 10, 'BB': 10,
            'B': 11
        }
        
        # Get the base note offset
        note_name = key.upper()
        if note_name in note_offsets:
            offset = note_offsets[note_name]
        else:
            # Fallback to C if invalid key
            offset = 0
        
        # Calculate MIDI note: C4 = 60, so C{register} = 60 + (register - 4) * 12
        midi_note = 60 + (register - 4) * 12 + offset
        
        # Clamp to valid MIDI range
        return max(0, min(127, midi_note))
    
    def generate_cc_message(self, command: Command) -> tuple:
        """Generate a control change message.
        
        Args:
            command: The CC command
            
        Returns:
            Tuple of (cc_number, cc_value) or None if invalid
        """
        if command.type == CommandType.CC:
            cc_number = command.params.get("cc_number")
            cc_value = command.params.get("cc_value")
            if cc_number is not None and cc_value is not None:
                return (cc_number, cc_value)
        elif command.type == CommandType.MOD:
            mod_value = command.params.get("mod_value")
            if mod_value is not None:
                return (1, mod_value)  # CC1 is modulation wheel
        
        return None
