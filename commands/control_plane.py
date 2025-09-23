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
from osc_sender import OSCSender
from contextual_intelligence import ContextualIntelligence
from musical_solvers import GrooveImprover, HarmonyFixer, ArrangementImprover
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
        
        # Initialize OSC sender for JUCE plugin control
        self.osc_sender = OSCSender(config.OSC_IP_ADDRESS, config.OSC_PORT)
        
        # Initialize contextual intelligence system
        self.contextual_intelligence = ContextualIntelligence(session_file)
        
        # Initialize musical problem solvers
        self.groove_improver = GrooveImprover()
        self.harmony_fixer = HarmonyFixer()
        self.arrangement_improver = ArrangementImprover()
        
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
            
            # Handle OSC style control commands
            elif command.type in [
                CommandType.SET_SWING, CommandType.SET_ACCENT, 
                CommandType.SET_HUMANIZE_TIMING, CommandType.SET_HUMANIZE_VELOCITY,
                CommandType.SET_OSC_ENABLED, CommandType.SET_OSC_PORT,
                CommandType.SET_STYLE_PRESET, CommandType.OSC_RESET
            ]:
                return self._handle_osc_command(command)
            
            # Handle contextual intelligence commands
            elif command.type in [
                CommandType.LOAD_PROJECT, CommandType.ANALYZE_BASS, CommandType.ANALYZE_MELODY,
                CommandType.ANALYZE_HARMONY, CommandType.ANALYZE_RHYTHM, CommandType.ANALYZE_ALL,
                CommandType.GET_SUGGESTIONS, CommandType.APPLY_SUGGESTION, CommandType.SHOW_FEEDBACK,
                CommandType.CLEAR_FEEDBACK
            ]:
                return self._handle_contextual_intelligence_command(command)
            
            # Handle musical problem solver commands
            elif command.type in [
                CommandType.IMPROVE_GROOVE, CommandType.FIX_HARMONY, CommandType.IMPROVE_ARRANGEMENT
            ]:
                return self._handle_musical_solver_command(command)
            
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
    
    def _handle_osc_command(self, command: Command) -> str:
        """Handle OSC style control commands.
        
        Args:
            command: The OSC command to execute
            
        Returns:
            Response message indicating success or failure
        """
        try:
            if command.type == CommandType.SET_SWING:
                swing = command.params.get("swing", 0.5)
                if self.osc_sender.set_swing_ratio(swing):
                    return f"OSC: Swing ratio set to {swing:.2f}"
                else:
                    return f"OSC: Failed to set swing ratio to {swing:.2f}"
            
            elif command.type == CommandType.SET_ACCENT:
                accent = command.params.get("accent", 20.0)
                if self.osc_sender.set_accent_amount(accent):
                    return f"OSC: Accent amount set to {accent:.1f}"
                else:
                    return f"OSC: Failed to set accent amount to {accent:.1f}"
            
            elif command.type == CommandType.SET_HUMANIZE_TIMING:
                timing = command.params.get("humanize_timing", 0.0)
                if self.osc_sender.set_humanize_timing(timing):
                    return f"OSC: Humanize timing set to {timing:.2f}"
                else:
                    return f"OSC: Failed to set humanize timing to {timing:.2f}"
            
            elif command.type == CommandType.SET_HUMANIZE_VELOCITY:
                velocity = command.params.get("humanize_velocity", 0.0)
                if self.osc_sender.set_humanize_velocity(velocity):
                    return f"OSC: Humanize velocity set to {velocity:.2f}"
                else:
                    return f"OSC: Failed to set humanize velocity to {velocity:.2f}"
            
            elif command.type == CommandType.SET_OSC_ENABLED:
                enabled = command.params.get("enabled", False)
                if self.osc_sender.set_osc_enabled(enabled):
                    status = "enabled" if enabled else "disabled"
                    return f"OSC: Control {status}"
                else:
                    return f"OSC: Failed to {'enable' if enabled else 'disable'} control"
            
            elif command.type == CommandType.SET_OSC_PORT:
                port = command.params.get("port", 3819)
                if self.osc_sender.set_osc_port(port):
                    return f"OSC: Port set to {port}"
                else:
                    return f"OSC: Failed to set port to {port}"
            
            elif command.type == CommandType.SET_STYLE_PRESET:
                preset = command.params.get("preset", "straight")
                if self.osc_sender.set_style_preset(preset):
                    return f"OSC: Style preset '{preset}' applied"
                else:
                    return f"OSC: Failed to apply style preset '{preset}'"
            
            elif command.type == CommandType.OSC_RESET:
                if self.osc_sender.reset_to_defaults():
                    return "OSC: All parameters reset to defaults"
                else:
                    return "OSC: Failed to reset parameters to defaults"
            
            else:
                return f"OSC: Unknown command '{command.type.value}'"
                
        except Exception as e:
            return f"OSC: Error executing command: {str(e)}"
    
    def _handle_contextual_intelligence_command(self, command: Command) -> str:
        """Handle contextual intelligence commands.
        
        Args:
            command: The contextual intelligence command to execute
            
        Returns:
            Response message indicating success or failure
        """
        try:
            if command.type == CommandType.LOAD_PROJECT:
                file_path = command.params.get("file_path", "")
                if self.contextual_intelligence.load_project(file_path):
                    return f"Project loaded: {file_path}"
                else:
                    return f"Failed to load project: {file_path}"
            
            elif command.type == CommandType.ANALYZE_BASS:
                feedback = self.contextual_intelligence.get_visual_feedback("analyze bass")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.ANALYZE_MELODY:
                feedback = self.contextual_intelligence.get_visual_feedback("analyze melody")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.ANALYZE_HARMONY:
                feedback = self.contextual_intelligence.get_visual_feedback("analyze harmony")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.ANALYZE_RHYTHM:
                feedback = self.contextual_intelligence.get_visual_feedback("analyze rhythm")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.ANALYZE_ALL:
                feedback = self.contextual_intelligence.get_visual_feedback("analyze all")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.GET_SUGGESTIONS:
                feedback = self.contextual_intelligence.get_visual_feedback("get suggestions")
                return self._format_visual_feedback(feedback)
            
            elif command.type == CommandType.APPLY_SUGGESTION:
                suggestion = command.params.get("suggestion", "")
                if self.contextual_intelligence.apply_suggestion({"suggestion": suggestion}):
                    return f"Suggestion applied: {suggestion}"
                else:
                    return f"Failed to apply suggestion: {suggestion}"
            
            elif command.type == CommandType.SHOW_FEEDBACK:
                return self.contextual_intelligence.get_feedback_summary()
            
            elif command.type == CommandType.CLEAR_FEEDBACK:
                self.contextual_intelligence.clear_feedback()
                return "Visual feedback cleared"
            
            else:
                return f"Unknown contextual intelligence command: {command.type.value}"
                
        except Exception as e:
            return f"Contextual Intelligence: Error executing command: {str(e)}"
    
    def _format_visual_feedback(self, feedback_list) -> str:
        """Format visual feedback for display.
        
        Args:
            feedback_list: List of VisualFeedback objects
            
        Returns:
            Formatted string representation
        """
        if not feedback_list:
            return "No visual feedback available."
        
        formatted = "Visual Feedback:\n"
        for feedback in feedback_list:
            formatted += f"- {feedback.element.value.title()}: {feedback.message}\n"
        
        return formatted
    
    def _handle_musical_solver_command(self, command: Command) -> str:
        """Handle a musical problem solver command.
        
        Args:
            command: The musical solver command
            
        Returns:
            Response message with solution and explanation
        """
        # Check if a project is loaded
        if not self.contextual_intelligence.current_project:
            return "Please load a MIDI project first using 'load [filename]' before using musical problem solvers."
        
        # Get the current project file path (we'll need to store this)
        # For now, we'll use a placeholder - in a real implementation, we'd store the file path
        project_path = "current_project.mid"  # This should be stored when loading
        
        try:
            if command.type == CommandType.IMPROVE_GROOVE:
                solution = self.groove_improver.improve_groove(project_path)
                return self._format_musical_solution("Groove", solution)
            
            elif command.type == CommandType.FIX_HARMONY:
                solution = self.harmony_fixer.fix_harmony(project_path)
                return self._format_musical_solution("Harmony", solution)
            
            elif command.type == CommandType.IMPROVE_ARRANGEMENT:
                solution = self.arrangement_improver.improve_arrangement(project_path)
                return self._format_musical_solution("Arrangement", solution)
            
            else:
                return f"Unknown musical solver command: {command.type.value}"
                
        except Exception as e:
            return f"Error processing musical solution: {str(e)}"
    
    def _format_musical_solution(self, problem_type: str, solution) -> str:
        """Format a musical solution for display.
        
        Args:
            problem_type: Type of problem solved (e.g., "Groove", "Harmony")
            solution: MusicalSolution object
            
        Returns:
            Formatted response message
        """
        if not solution.changes_made:
            return f"{problem_type} Analysis: {solution.explanation}"
        
        response = f"🎵 {problem_type} Improvements Made:\n\n"
        response += f"{solution.explanation}\n\n"
        
        if solution.changes_made:
            response += "Changes Applied:\n"
            for change in solution.changes_made:
                response += f"• {change}\n"
        
        response += f"\nConfidence: {solution.confidence:.1%}"
        
        if solution.audio_preview_path:
            response += f"\n\nAudio preview saved to: {solution.audio_preview_path}"
        
        return response
    
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
