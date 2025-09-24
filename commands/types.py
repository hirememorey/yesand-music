"""
Data types for the control plane command system.

This module defines the core data structures used throughout the control plane,
including commands, session state, and musical patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class CommandType(Enum):
    """Types of commands that can be parsed and executed."""
    PLAY_SCALE = "play_scale"
    PLAY_ARP = "play_arp"
    PLAY_RANDOM = "play_random"
    SET_KEY = "set_key"
    SET_DENSITY = "set_density"
    SET_TEMPO = "set_tempo"
    SET_RANDOMNESS = "set_randomness"
    SET_VELOCITY = "set_velocity"
    SET_REGISTER = "set_register"
    CC = "cc"
    MOD = "mod"
    TARGET = "target"
    STOP = "stop"
    STATUS = "status"
    HELP = "help"
    # OSC Style Control Commands
    SET_SWING = "set_swing"
    SET_ACCENT = "set_accent"
    SET_HUMANIZE_TIMING = "set_humanize_timing"
    SET_HUMANIZE_VELOCITY = "set_humanize_velocity"
    SET_OSC_ENABLED = "set_osc_enabled"
    SET_OSC_PORT = "set_osc_port"
    SET_STYLE_PRESET = "set_style_preset"
    OSC_RESET = "osc_reset"
    # Contextual Intelligence Commands
    LOAD_PROJECT = "load_project"
    ANALYZE_BASS = "analyze_bass"
    ANALYZE_MELODY = "analyze_melody"
    ANALYZE_HARMONY = "analyze_harmony"
    ANALYZE_RHYTHM = "analyze_rhythm"
    ANALYZE_ALL = "analyze_all"
    GET_SUGGESTIONS = "get_suggestions"
    APPLY_SUGGESTION = "apply_suggestion"
    SHOW_FEEDBACK = "show_feedback"
    CLEAR_FEEDBACK = "clear_feedback"
    # Musical Problem Solvers (Phase 3B)
    IMPROVE_GROOVE = "improve_groove"
    FIX_HARMONY = "fix_harmony"
    IMPROVE_ARRANGEMENT = "improve_arrangement"
    # Ardour Integration Commands
    ARDOUR_CONNECT = "ardour_connect"
    ARDOUR_DISCONNECT = "ardour_disconnect"
    ARDOUR_LIST_TRACKS = "ardour_list_tracks"
    ARDOUR_EXPORT_SELECTED = "ardour_export_selected"
    ARDOUR_IMPORT_MIDI = "ardour_import_midi"
    ARDOUR_ANALYZE_SELECTED = "ardour_analyze_selected"
    ARDOUR_IMPROVE_SELECTED = "ardour_improve_selected"
    # Musical Scribe Commands
    MUSICAL_SCRIBE_ENHANCE = "musical_scribe_enhance"
    MUSICAL_SCRIBE_ANALYZE = "musical_scribe_analyze"
    MUSICAL_SCRIBE_PROMPT = "musical_scribe_prompt"
    MUSICAL_SCRIBE_STATUS = "musical_scribe_status"


class Density(Enum):
    """Note density levels."""
    LOW = "low"
    MEDIUM = "med"
    HIGH = "high"


class Mode(Enum):
    """Musical modes."""
    MAJOR = "major"
    MINOR = "minor"
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    LOCRIAN = "locrian"


@dataclass
class Command:
    """Represents a parsed command with its parameters."""
    type: CommandType
    params: Dict[str, Any]
    raw_text: str


@dataclass
class SessionState:
    """Current session state for the control plane."""
    key: str = "C"
    mode: Mode = Mode.MAJOR
    tempo: int = 120
    density: Density = Density.MEDIUM
    randomness: float = 0.0
    velocity: int = 90
    register: int = 4  # MIDI octave (4 = C4)
    target_part: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session state to dictionary for serialization."""
        return {
            "key": self.key,
            "mode": self.mode.value,
            "tempo": self.tempo,
            "density": self.density.value,
            "randomness": self.randomness,
            "velocity": self.velocity,
            "register": self.register,
            "target_part": self.target_part,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SessionState:
        """Create session state from dictionary."""
        return cls(
            key=data.get("key", "C"),
            mode=Mode(data.get("mode", "major")),
            tempo=data.get("tempo", 120),
            density=Density(data.get("density", "med")),
            randomness=data.get("randomness", 0.0),
            velocity=data.get("velocity", 90),
            register=data.get("register", 4),
            target_part=data.get("target_part"),
        )


@dataclass
class Note:
    """Represents a musical note with timing and dynamics."""
    pitch: int
    velocity: int
    start_beat: float
    duration_beats: float
    
    def to_dict(self) -> Dict[str, Union[int, float]]:
        """Convert note to dictionary for serialization."""
        return {
            "pitch": self.pitch,
            "velocity": self.velocity,
            "start_beat": self.start_beat,
            "duration_beats": self.duration_beats,
        }
