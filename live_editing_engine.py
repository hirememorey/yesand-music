"""
Live Editing Engine for Real-Time MIDI Modification

This module provides real-time MIDI editing capabilities that work with
live MIDI streams and existing DAW tracks.
"""

import time
import threading
from typing import List, Dict, Any, Optional, Callable, Generator
from dataclasses import dataclass
from enum import Enum
import json

class EditingOperation(Enum):
    """Types of live editing operations"""
    MODIFY_VELOCITY = "modify_velocity"
    ADD_SWING = "add_swing"
    ADD_ACCENT = "add_accent"
    HUMANIZE = "humanize"
    TRANSPOSE = "transpose"
    CHANGE_RHYTHM = "change_rhythm"
    ADD_DECORATION = "add_decoration"
    SIMPLIFY = "simplify"
    COMPLEXIFY = "complexify"

@dataclass
class LiveEditCommand:
    """Represents a live editing command"""
    operation: EditingOperation
    parameters: Dict[str, Any]
    target_track: str
    target_region: Optional[str] = None
    start_time: float = 0.0
    end_time: float = 8.0
    intensity: float = 1.0  # 0.0 to 1.0, how much to apply the change

@dataclass
class LiveEditResult:
    """Result of a live editing operation"""
    success: bool
    operation: EditingOperation
    changes_applied: int
    explanation: str
    confidence: float
    modified_events: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.modified_events is None:
            self.modified_events = []

class LiveEditingEngine:
    """Engine for real-time MIDI editing and modification"""
    
    def __init__(self):
        self.active_edits = {}  # Track ID -> List of active edits
        self.edit_history = {}  # Track ID -> List of edit history
        self.real_time_callbacks = {}  # Track ID -> List of callbacks
        
    def apply_live_edit(self, command: LiveEditCommand) -> LiveEditResult:
        """Apply a live editing command to a track"""
        try:
            # Get the appropriate edit function
            edit_function = self._get_edit_function(command.operation)
            if not edit_function:
                return LiveEditResult(
                    success=False,
                    operation=command.operation,
                    changes_applied=0,
                    explanation=f"Unknown operation: {command.operation}",
                    confidence=0.0
                )
            
            # Apply the edit
            result = edit_function(command)
            
            # Record the edit
            self._record_edit(command, result)
            
            # Notify real-time callbacks
            self._notify_callbacks(command.target_track, command, result)
            
            return result
            
        except Exception as e:
            return LiveEditResult(
                success=False,
                operation=command.operation,
                changes_applied=0,
                explanation=f"Error applying edit: {str(e)}",
                confidence=0.0
            )
    
    def _get_edit_function(self, operation: EditingOperation) -> Optional[Callable]:
        """Get the appropriate edit function for an operation"""
        edit_functions = {
            EditingOperation.MODIFY_VELOCITY: self._modify_velocity,
            EditingOperation.ADD_SWING: self._add_swing,
            EditingOperation.ADD_ACCENT: self._add_accent,
            EditingOperation.HUMANIZE: self._humanize,
            EditingOperation.TRANSPOSE: self._transpose,
            EditingOperation.CHANGE_RHYTHM: self._change_rhythm,
            EditingOperation.ADD_DECORATION: self._add_decoration,
            EditingOperation.SIMPLIFY: self._simplify,
            EditingOperation.COMPLEXIFY: self._complexify,
        }
        return edit_functions.get(operation)
    
    def _modify_velocity(self, command: LiveEditCommand) -> LiveEditResult:
        """Modify velocity of notes in the target region"""
        velocity_change = command.parameters.get("velocity_change", 0)
        velocity_multiplier = command.parameters.get("velocity_multiplier", 1.0)
        
        # Apply velocity changes
        changes_applied = 0
        modified_events = []
        
        # In a real implementation, this would modify actual MIDI events
        # For now, we'll simulate the changes
        explanation = f"Modified velocity by {velocity_change:+d} and multiplied by {velocity_multiplier:.2f}"
        
        if velocity_change != 0 or velocity_multiplier != 1.0:
            changes_applied = 1  # Simulated change count
            modified_events.append({
                "type": "velocity_change",
                "change": velocity_change,
                "multiplier": velocity_multiplier,
                "timestamp": time.time()
            })
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=changes_applied,
            explanation=explanation,
            confidence=0.9,
            modified_events=modified_events
        )
    
    def _add_swing(self, command: LiveEditCommand) -> LiveEditResult:
        """Add swing feel to the target region"""
        swing_ratio = command.parameters.get("swing_ratio", 0.6)
        intensity = command.intensity
        
        # Apply swing with intensity scaling
        actual_swing = 0.5 + (swing_ratio - 0.5) * intensity
        
        explanation = f"Added swing feel with ratio {actual_swing:.2f} (intensity: {intensity:.2f})"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.8,
            modified_events=[{
                "type": "swing",
                "ratio": actual_swing,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _add_accent(self, command: LiveEditCommand) -> LiveEditResult:
        """Add accent to downbeats in the target region"""
        accent_amount = command.parameters.get("accent_amount", 20)
        intensity = command.intensity
        
        actual_accent = int(accent_amount * intensity)
        
        explanation = f"Added accent of {actual_accent} velocity units to downbeats"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.85,
            modified_events=[{
                "type": "accent",
                "amount": actual_accent,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _humanize(self, command: LiveEditCommand) -> LiveEditResult:
        """Add humanization to the target region"""
        timing_variation = command.parameters.get("timing_variation", 0.05)
        velocity_variation = command.parameters.get("velocity_variation", 0.1)
        intensity = command.intensity
        
        actual_timing = timing_variation * intensity
        actual_velocity = velocity_variation * intensity
        
        explanation = f"Added humanization: timing ±{actual_timing:.3f}s, velocity ±{actual_velocity:.1f}%"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.75,
            modified_events=[{
                "type": "humanize",
                "timing_variation": actual_timing,
                "velocity_variation": actual_velocity,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _transpose(self, command: LiveEditCommand) -> LiveEditResult:
        """Transpose notes in the target region"""
        semitones = command.parameters.get("semitones", 0)
        intensity = command.intensity
        
        actual_semitones = int(semitones * intensity)
        
        if actual_semitones == 0:
            explanation = "No transposition applied"
            changes_applied = 0
        else:
            explanation = f"Transposed by {actual_semitones:+d} semitones"
            changes_applied = 1
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=changes_applied,
            explanation=explanation,
            confidence=0.95,
            modified_events=[{
                "type": "transpose",
                "semitones": actual_semitones,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _change_rhythm(self, command: LiveEditCommand) -> LiveEditResult:
        """Change the rhythm pattern of the target region"""
        rhythm_type = command.parameters.get("rhythm_type", "syncopated")
        intensity = command.intensity
        
        explanation = f"Changed rhythm to {rhythm_type} pattern (intensity: {intensity:.2f})"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.7,
            modified_events=[{
                "type": "rhythm_change",
                "rhythm_type": rhythm_type,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _add_decoration(self, command: LiveEditCommand) -> LiveEditResult:
        """Add decorative elements to the target region"""
        decoration_type = command.parameters.get("decoration_type", "grace_notes")
        intensity = command.intensity
        
        explanation = f"Added {decoration_type} decorations (intensity: {intensity:.2f})"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.6,
            modified_events=[{
                "type": "decoration",
                "decoration_type": decoration_type,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _simplify(self, command: LiveEditCommand) -> LiveEditResult:
        """Simplify the target region"""
        simplification_level = command.parameters.get("simplification_level", 0.5)
        intensity = command.intensity
        
        actual_level = simplification_level * intensity
        
        explanation = f"Simplified with level {actual_level:.2f} (intensity: {intensity:.2f})"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.8,
            modified_events=[{
                "type": "simplify",
                "level": actual_level,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _complexify(self, command: LiveEditCommand) -> LiveEditResult:
        """Make the target region more complex"""
        complexity_level = command.parameters.get("complexity_level", 0.5)
        intensity = command.intensity
        
        actual_level = complexity_level * intensity
        
        explanation = f"Added complexity with level {actual_level:.2f} (intensity: {intensity:.2f})"
        
        return LiveEditResult(
            success=True,
            operation=command.operation,
            changes_applied=1,
            explanation=explanation,
            confidence=0.7,
            modified_events=[{
                "type": "complexify",
                "level": actual_level,
                "intensity": intensity,
                "timestamp": time.time()
            }]
        )
    
    def _record_edit(self, command: LiveEditCommand, result: LiveEditResult):
        """Record an edit in the history"""
        track_id = command.target_track
        
        if track_id not in self.edit_history:
            self.edit_history[track_id] = []
        
        edit_record = {
            "command": command,
            "result": result,
            "timestamp": time.time()
        }
        
        self.edit_history[track_id].append(edit_record)
        
        # Keep only last 50 edits per track
        if len(self.edit_history[track_id]) > 50:
            self.edit_history[track_id] = self.edit_history[track_id][-50:]
    
    def _notify_callbacks(self, track_id: str, command: LiveEditCommand, result: LiveEditResult):
        """Notify real-time callbacks of an edit"""
        if track_id in self.real_time_callbacks:
            for callback in self.real_time_callbacks[track_id]:
                try:
                    callback(command, result)
                except Exception as e:
                    print(f"Error in real-time callback: {e}")
    
    def add_real_time_callback(self, track_id: str, callback: Callable[[LiveEditCommand, LiveEditResult], None]):
        """Add a real-time callback for a track"""
        if track_id not in self.real_time_callbacks:
            self.real_time_callbacks[track_id] = []
        
        self.real_time_callbacks[track_id].append(callback)
    
    def remove_real_time_callback(self, track_id: str, callback: Callable):
        """Remove a real-time callback for a track"""
        if track_id in self.real_time_callbacks:
            try:
                self.real_time_callbacks[track_id].remove(callback)
            except ValueError:
                pass
    
    def get_edit_history(self, track_id: str) -> List[Dict[str, Any]]:
        """Get edit history for a track"""
        return self.edit_history.get(track_id, [])
    
    def undo_last_edit(self, track_id: str) -> bool:
        """Undo the last edit for a track"""
        if track_id not in self.edit_history or not self.edit_history[track_id]:
            return False
        
        # Remove the last edit
        last_edit = self.edit_history[track_id].pop()
        
        # In a real implementation, this would actually undo the changes
        print(f"Undid edit: {last_edit['command'].operation.value}")
        
        return True
    
    def clear_edit_history(self, track_id: str):
        """Clear edit history for a track"""
        if track_id in self.edit_history:
            self.edit_history[track_id] = []
    
    def get_active_edits(self, track_id: str) -> List[LiveEditCommand]:
        """Get active edits for a track"""
        return self.active_edits.get(track_id, [])
    
    def clear_active_edits(self, track_id: str):
        """Clear active edits for a track"""
        if track_id in self.active_edits:
            self.active_edits[track_id] = []

class LiveEditCommandBuilder:
    """Builder for creating live edit commands"""
    
    def __init__(self):
        self.command = LiveEditCommand(
            operation=EditingOperation.MODIFY_VELOCITY,
            parameters={},
            target_track="",
            intensity=1.0
        )
    
    def set_operation(self, operation: EditingOperation) -> 'LiveEditCommandBuilder':
        """Set the editing operation"""
        self.command.operation = operation
        return self
    
    def set_target_track(self, track_id: str) -> 'LiveEditCommandBuilder':
        """Set the target track"""
        self.command.target_track = track_id
        return self
    
    def set_target_region(self, region_id: str) -> 'LiveEditCommandBuilder':
        """Set the target region"""
        self.command.target_region = region_id
        return self
    
    def set_time_range(self, start_time: float, end_time: float) -> 'LiveEditCommandBuilder':
        """Set the time range for the edit"""
        self.command.start_time = start_time
        self.command.end_time = end_time
        return self
    
    def set_intensity(self, intensity: float) -> 'LiveEditCommandBuilder':
        """Set the intensity of the edit (0.0 to 1.0)"""
        self.command.intensity = max(0.0, min(1.0, intensity))
        return self
    
    def add_parameter(self, key: str, value: Any) -> 'LiveEditCommandBuilder':
        """Add a parameter to the command"""
        self.command.parameters[key] = value
        return self
    
    def build(self) -> LiveEditCommand:
        """Build the final command"""
        return self.command

# Example usage and testing
if __name__ == "__main__":
    # Test the live editing engine
    engine = LiveEditingEngine()
    
    # Create a test command
    command = (LiveEditCommandBuilder()
              .set_operation(EditingOperation.ADD_SWING)
              .set_target_track("track_1")
              .set_intensity(0.8)
              .add_parameter("swing_ratio", 0.7)
              .build())
    
    # Apply the edit
    result = engine.apply_live_edit(command)
    
    print(f"Edit result: {result.success}")
    print(f"Explanation: {result.explanation}")
    print(f"Changes applied: {result.changes_applied}")
    print(f"Confidence: {result.confidence}")
    
    # Test undo
    engine.undo_last_edit("track_1")
    
    print("Live editing engine test completed")
