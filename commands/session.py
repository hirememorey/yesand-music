"""
Session management for the control plane.

This module handles persistent storage and management of session state
across command executions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .types import Command, CommandType, Density, Mode, SessionState


class SessionManager:
    """Manages persistent session state for the control plane."""
    
    def __init__(self, session_file: str = "session.json") -> None:
        """Initialize the session manager.
        
        Args:
            session_file: Path to the session state file
        """
        self.session_file = Path(session_file)
        self.state = self._load_state()
    
    def _load_state(self) -> SessionState:
        """Load session state from file or create default state.
        
        Returns:
            Current session state
        """
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                return SessionState.from_dict(data)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Could not load session state: {e}")
                print("Using default session state.")
        
        return SessionState()
    
    def _save_state(self) -> None:
        """Save current session state to file atomically.
        
        Uses a temporary file and atomic rename to prevent corruption.
        """
        temp_file = self.session_file.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                json.dump(self.state.to_dict(), f, indent=2)
            temp_file.replace(self.session_file)
        except Exception as e:
            print(f"Warning: Could not save session state: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                temp_file.unlink()
    
    def get_state(self) -> SessionState:
        """Get current session state.
        
        Returns:
            Current session state (read-only)
        """
        return self.state
    
    def update_from_command(self, command: Command) -> bool:
        """Update session state based on a command.
        
        Args:
            command: The command to process
            
        Returns:
            True if state was updated, False otherwise
        """
        updated = False
        
        if command.type == CommandType.SET_KEY:
            key = command.params.get("key", self.state.key)
            mode_str = command.params.get("mode", self.state.mode.value)
            try:
                mode = Mode(mode_str)
                if key != self.state.key or mode != self.state.mode:
                    self.state.key = key
                    self.state.mode = mode
                    updated = True
            except ValueError:
                print(f"Warning: Invalid mode '{mode_str}', keeping current mode")
                
        elif command.type == CommandType.SET_DENSITY:
            density_str = command.params.get("density", self.state.density.value)
            try:
                density = Density(density_str)
                if density != self.state.density:
                    self.state.density = density
                    updated = True
            except ValueError:
                print(f"Warning: Invalid density '{density_str}', keeping current density")
                
        elif command.type == CommandType.SET_TEMPO:
            tempo = command.params.get("tempo", self.state.tempo)
            if tempo != self.state.tempo:
                self.state.tempo = tempo
                updated = True
                
        elif command.type == CommandType.SET_RANDOMNESS:
            randomness = command.params.get("randomness", self.state.randomness)
            if randomness != self.state.randomness:
                self.state.randomness = randomness
                updated = True
                
        elif command.type == CommandType.SET_VELOCITY:
            velocity = command.params.get("velocity", self.state.velocity)
            if velocity != self.state.velocity:
                self.state.velocity = velocity
                updated = True
                
        elif command.type == CommandType.SET_REGISTER:
            register = command.params.get("register", self.state.register)
            if register != self.state.register:
                self.state.register = register
                updated = True
                
        elif command.type == CommandType.TARGET:
            part = command.params.get("part", self.state.target_part)
            if part != self.state.target_part:
                self.state.target_part = part
                updated = True
        
        if updated:
            self._save_state()
        
        return updated
    
    def get_status_text(self) -> str:
        """Get human-readable status of current session state.
        
        Returns:
            Formatted status string
        """
        return f"""Current Session State:
  Key: {self.state.key} {self.state.mode.value.title()}
  Tempo: {self.state.tempo} BPM
  Density: {self.state.density.value.title()}
  Randomness: {self.state.randomness:.2f}
  Velocity: {self.state.velocity}
  Register: {self.state.register} (C{self.state.register})
  Target Part: {self.state.target_part or 'None'}"""
    
    def reset_to_defaults(self) -> None:
        """Reset session state to defaults and save."""
        self.state = SessionState()
        self._save_state()
        print("Session state reset to defaults.")
    
    def get_midi_root_note(self) -> int:
        """Get the MIDI note number for the current key and register.
        
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
        note_name = self.state.key.upper()
        if note_name in note_offsets:
            offset = note_offsets[note_name]
        else:
            # Fallback to C if invalid key
            offset = 0
            print(f"Warning: Invalid key '{self.state.key}', using C")
        
        # Calculate MIDI note: C4 = 60, so C{register} = 60 + (register - 4) * 12
        midi_note = 60 + (self.state.register - 4) * 12 + offset
        
        # Clamp to valid MIDI range
        return max(0, min(127, midi_note))
