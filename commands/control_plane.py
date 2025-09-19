"""
Main control plane for chat-driven MIDI control.

This module provides the ControlPlane class that orchestrates all components
to provide a unified interface for natural language MIDI control.
"""

from __future__ import annotations

import threading
import time
from typing import Optional

from .parser import CommandParser
from .pattern_engine import PatternEngine
from .session import SessionManager
from .types import Command, CommandType, Note
from midi_player import MidiPlayer
from sequencer import Sequencer
import config


class ControlPlane:
    """Main control plane that orchestrates all components."""
    
    def __init__(self, midi_port_name: str = None, session_file: str = "session.json") -> None:
        """Initialize the control plane.
        
        Args:
            midi_port_name: Name of the MIDI output port (uses config default if None)
            session_file: Path to the session state file
        """
        self.midi_port_name = midi_port_name or config.MIDI_PORT_NAME
        self.session_file = session_file
        
        # Initialize components
        self.parser = CommandParser()
        self.session = SessionManager(session_file)
        self.pattern_engine = PatternEngine()
        
        # Initialize MIDI components
        self.midi_player = MidiPlayer(self.midi_port_name)
        if self.midi_player.port is None:
            raise RuntimeError(f"Could not open MIDI port '{self.midi_port_name}'")
        
        self.sequencer = Sequencer(midi_player=self.midi_player, bpm=self.session.get_state().tempo)
        
        # Playback state (now handled by sequencer)
    
    def execute(self, command_text: str) -> str:
        """Execute a command and return a response message.
        
        Args:
            command_text: The command text to execute
            
        Returns:
            Response message indicating success or failure
        """
        # Parse the command
        command = self.parser.parse(command_text)
        if command is None:
            return f"Unknown command: '{command_text}'. Type 'help' for available commands."
        
        try:
            # Update session state if needed
            if command.type in [
                CommandType.SET_KEY, CommandType.SET_DENSITY, CommandType.SET_TEMPO,
                CommandType.SET_RANDOMNESS, CommandType.SET_VELOCITY, CommandType.SET_REGISTER,
                CommandType.TARGET
            ]:
                self.session.update_from_command(command)
                return f"Updated: {self._format_command_result(command)}"
            
            # Handle playback commands
            elif command.type in [CommandType.PLAY_SCALE, CommandType.PLAY_ARP, CommandType.PLAY_RANDOM]:
                return self._handle_playback_command(command)
            
            # Handle control commands
            elif command.type in [CommandType.CC, CommandType.MOD]:
                return self._handle_control_command(command)
            
            # Handle system commands
            elif command.type == CommandType.STOP:
                return self._handle_stop_command()
            
            elif command.type == CommandType.STATUS:
                return self.session.get_status_text()
            
            elif command.type == CommandType.HELP:
                return self.parser.get_help_text()
            
            else:
                return f"Command '{command.type.value}' not yet implemented."
        
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def _handle_playback_command(self, command: Command) -> str:
        """Handle a playback command (play scale, arp, random).
        
        Args:
            command: The playback command
            
        Returns:
            Response message
        """
        # Stop any current playback
        self.sequencer.stop()
        
        # Generate pattern
        state = self.session.get_state()
        notes = self.pattern_engine.generate_pattern(command, state)
        
        if not notes:
            return "No pattern generated."
        
        # Update sequencer tempo if needed
        if self.sequencer.bpm != state.tempo:
            self.sequencer = Sequencer(midi_player=self.midi_player, bpm=state.tempo)
        
        # Clear sequencer and add notes
        self.sequencer.clear()
        for note in notes:
            self.sequencer.add_note(
                pitch=note.pitch,
                velocity=note.velocity,
                start_beat=note.start_beat,
                duration_beats=note.duration_beats
            )
        
        # Start playback in background thread
        self.sequencer.play_async()
        
        pattern_type = command.type.value.replace("play_", "")
        return f"Playing {pattern_type} pattern with {len(notes)} notes..."
    
    def _handle_control_command(self, command: Command) -> str:
        """Handle a control command (CC, mod wheel).
        
        Args:
            command: The control command
            
        Returns:
            Response message
        """
        cc_message = self.pattern_engine.generate_cc_message(command)
        if cc_message is None:
            return "Invalid control command."
        
        cc_number, cc_value = cc_message
        import mido
        self.midi_player.port.send(
            mido.Message(
                "control_change", 
                channel=0, 
                control=cc_number, 
                value=cc_value
            )
        )
        
        if command.type == CommandType.MOD:
            return f"Modulation wheel set to {cc_value}"
        else:
            return f"CC{cc_number} set to {cc_value}"
    
    def _handle_stop_command(self) -> str:
        """Handle the stop command.
        
        Returns:
            Response message
        """
        self.sequencer.stop()
        return "Playback stopped."
    
    def _format_command_result(self, command: Command) -> str:
        """Format the result of a command for display.
        
        Args:
            command: The command that was executed
            
        Returns:
            Formatted result string
        """
        if command.type == CommandType.SET_KEY:
            key = command.params.get("key", "C")
            mode = command.params.get("mode", "major")
            return f"Key set to {key} {mode.title()}"
        
        elif command.type == CommandType.SET_DENSITY:
            density = command.params.get("density", "med")
            return f"Density set to {density.title()}"
        
        elif command.type == CommandType.SET_TEMPO:
            tempo = command.params.get("tempo", 120)
            return f"Tempo set to {tempo} BPM"
        
        elif command.type == CommandType.SET_RANDOMNESS:
            randomness = command.params.get("randomness", 0.0)
            return f"Randomness set to {randomness:.2f}"
        
        elif command.type == CommandType.SET_VELOCITY:
            velocity = command.params.get("velocity", 90)
            return f"Velocity set to {velocity}"
        
        elif command.type == CommandType.SET_REGISTER:
            register = command.params.get("register", 4)
            return f"Register set to {register} (C{register})"
        
        elif command.type == CommandType.TARGET:
            part = command.params.get("part", "None")
            return f"Target part set to {part}"
        
        else:
            return f"Command '{command.type.value}' executed"
    
    def close(self) -> None:
        """Close the control plane and clean up resources."""
        self.sequencer.stop()
        if self.midi_player:
            self.midi_player.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
