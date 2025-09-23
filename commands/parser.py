"""
Command parser for the control plane.

This module handles parsing natural language commands into structured
Command objects that can be executed by the control plane.
"""

from __future__ import annotations

import re
from typing import Optional

from .types import Command, CommandType, Density, Mode


class CommandParser:
    """Parses natural language commands into structured Command objects."""
    
    def __init__(self) -> None:
        """Initialize the parser with compiled regex patterns."""
        self.patterns = {
            CommandType.PLAY_SCALE: [
                r"play\s+scale\s+([A-G][#b]?)\s+(\w+)",
                r"play\s+([A-G][#b]?)\s+(\w+)\s+scale",
                r"scale\s+([A-G][#b]?)\s+(\w+)",
            ],
            CommandType.PLAY_ARP: [
                r"play\s+arp\s+([A-G][#b]?)\s+(\w+)",
                r"play\s+arpeggio\s+([A-G][#b]?)\s+(\w+)",
                r"arp\s+([A-G][#b]?)\s+(\w+)",
            ],
            CommandType.PLAY_RANDOM: [
                r"play\s+random\s+(\d+)",
                r"play\s+(\d+)\s+random\s+notes",
                r"random\s+(\d+)",
            ],
            CommandType.SET_KEY: [
                r"set\s+key\s+to\s+([A-G][#b]?)\s+(\w+)",
                r"key\s+([A-G][#b]?)\s+(\w+)",
                r"set\s+([A-G][#b]?)\s+(\w+)",
            ],
            CommandType.SET_DENSITY: [
                r"set\s+density\s+to\s+(low|med|high)",
                r"density\s+(low|med|high)",
                r"set\s+density\s+(low|med|high)",
            ],
            CommandType.SET_TEMPO: [
                r"set\s+tempo\s+to\s+(\d+)",
                r"tempo\s+(\d+)",
                r"set\s+tempo\s+(\d+)",
                r"bpm\s+(\d+)",
            ],
            CommandType.SET_RANDOMNESS: [
                r"set\s+randomness\s+to\s+([0-9]*\.?[0-9]+)",
                r"randomness\s+([0-9]*\.?[0-9]+)",
                r"set\s+randomness\s+([0-9]*\.?[0-9]+)",
            ],
            CommandType.SET_VELOCITY: [
                r"set\s+velocity\s+to\s+(\d+)",
                r"velocity\s+(\d+)",
                r"set\s+velocity\s+(\d+)",
            ],
            CommandType.SET_REGISTER: [
                r"set\s+register\s+to\s+(\d+)",
                r"register\s+(\d+)",
                r"set\s+register\s+(\d+)",
                r"octave\s+(\d+)",
            ],
            CommandType.CC: [
                r"cc\s+(\d+)\s+to\s+(\d+)",
                r"cc\s+(\d+)\s+(\d+)",
                r"control\s+change\s+(\d+)\s+(\d+)",
            ],
            CommandType.MOD: [
                r"mod\s+wheel\s+(\d+)",
                r"mod\s+(\d+)",
                r"modulation\s+(\d+)",
            ],
            CommandType.TARGET: [
                r"target\s+(\w+)",
                r"set\s+target\s+to\s+(\w+)",
                r"play\s+on\s+(\w+)",
            ],
            CommandType.STOP: [
                r"stop",
                r"silence",
                r"quiet",
                r"halt",
            ],
            CommandType.STATUS: [
                r"status",
                r"state",
                r"current",
                r"show\s+state",
            ],
            CommandType.HELP: [
                r"help",
                r"\?",
                r"commands",
            ],
            # OSC Style Control Commands
            CommandType.SET_SWING: [
                r"set\s+swing\s+to\s+([0-9]*\.?[0-9]+)",
                r"swing\s+([0-9]*\.?[0-9]+)",
                r"set\s+swing\s+([0-9]*\.?[0-9]+)",
            ],
            CommandType.SET_ACCENT: [
                r"set\s+accent\s+to\s+([0-9]*\.?[0-9]+)",
                r"accent\s+([0-9]*\.?[0-9]+)",
                r"set\s+accent\s+([0-9]*\.?[0-9]+)",
            ],
            CommandType.SET_HUMANIZE_TIMING: [
                r"set\s+humanize\s+timing\s+to\s+([0-9]*\.?[0-9]+)",
                r"humanize\s+timing\s+([0-9]*\.?[0-9]+)",
                r"set\s+humanize\s+timing\s+([0-9]*\.?[0-9]+)",
            ],
            CommandType.SET_HUMANIZE_VELOCITY: [
                r"set\s+humanize\s+velocity\s+to\s+([0-9]*\.?[0-9]+)",
                r"humanize\s+velocity\s+([0-9]*\.?[0-9]+)",
                r"set\s+humanize\s+velocity\s+([0-9]*\.?[0-9]+)",
            ],
            CommandType.SET_OSC_ENABLED: [
                r"set\s+osc\s+enabled\s+to\s+(true|false|on|off)",
                r"osc\s+enabled\s+(true|false|on|off)",
                r"set\s+osc\s+(true|false|on|off)",
                r"enable\s+osc",
                r"disable\s+osc",
            ],
            CommandType.SET_OSC_PORT: [
                r"set\s+osc\s+port\s+to\s+(\d+)",
                r"osc\s+port\s+(\d+)",
                r"set\s+osc\s+port\s+(\d+)",
            ],
            CommandType.SET_STYLE_PRESET: [
                r"set\s+style\s+to\s+(\w+)",
                r"style\s+(\w+)",
                r"set\s+style\s+(\w+)",
                r"make\s+it\s+(\w+)",
                r"apply\s+(\w+)\s+style",
            ],
            CommandType.OSC_RESET: [
                r"reset\s+osc",
                r"osc\s+reset",
                r"reset\s+style",
                r"style\s+reset",
            ],
            # Contextual Intelligence Commands
            CommandType.LOAD_PROJECT: [
                r"load\s+project\s+(.+)",
                r"load\s+(.+)",
                r"open\s+(.+)",
            ],
            CommandType.ANALYZE_BASS: [
                r"analyze\s+bass",
                r"show\s+bass",
                r"what\s+is\s+the\s+bass\s+doing",
                r"bass\s+analysis",
                r"highlight\s+bass",
            ],
            CommandType.ANALYZE_MELODY: [
                r"analyze\s+melody",
                r"show\s+melody",
                r"what\s+is\s+the\s+melody\s+doing",
                r"melody\s+analysis",
                r"highlight\s+melody",
            ],
            CommandType.ANALYZE_HARMONY: [
                r"analyze\s+harmony",
                r"show\s+harmony",
                r"what\s+is\s+the\s+harmony\s+doing",
                r"harmony\s+analysis",
                r"highlight\s+harmony",
            ],
            CommandType.ANALYZE_RHYTHM: [
                r"analyze\s+rhythm",
                r"show\s+rhythm",
                r"what\s+is\s+the\s+rhythm\s+doing",
                r"rhythm\s+analysis",
                r"highlight\s+rhythm",
            ],
            CommandType.ANALYZE_ALL: [
                r"analyze\s+all",
                r"analyze\s+everything",
                r"show\s+analysis",
                r"complete\s+analysis",
                r"full\s+analysis",
            ],
            CommandType.GET_SUGGESTIONS: [
                r"get\s+suggestions",
                r"show\s+suggestions",
                r"what\s+can\s+I\s+improve",
                r"how\s+can\s+I\s+make\s+this\s+better",
                r"suggest\s+improvements",
            ],
            CommandType.APPLY_SUGGESTION: [
                r"apply\s+suggestion\s+(.+)",
                r"use\s+suggestion\s+(.+)",
                r"try\s+suggestion\s+(.+)",
                r"implement\s+(.+)",
            ],
            CommandType.SHOW_FEEDBACK: [
                r"show\s+feedback",
                r"feedback\s+summary",
                r"what\s+did\s+you\s+find",
                r"show\s+results",
            ],
            CommandType.CLEAR_FEEDBACK: [
                r"clear\s+feedback",
                r"clear\s+visuals",
                r"hide\s+feedback",
                r"reset\s+feedback",
            ],
        }
        
        # Compile all patterns for efficiency
        self.compiled_patterns = {}
        for cmd_type, patterns in self.patterns.items():
            self.compiled_patterns[cmd_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def parse(self, text: str) -> Optional[Command]:
        """Parse a command string into a Command object.
        
        Args:
            text: The command text to parse
            
        Returns:
            Command object if parsing succeeds, None otherwise
        """
        text = text.strip()
        if not text:
            return None
        
        for cmd_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                match = pattern.match(text)
                if match:
                    params = self._extract_params(cmd_type, match.groups())
                    return Command(
                        type=cmd_type,
                        params=params,
                        raw_text=text
                    )
        
        return None
    
    def _extract_params(self, cmd_type: CommandType, groups: tuple) -> dict:
        """Extract and validate parameters from regex match groups.
        
        Args:
            cmd_type: The type of command
            groups: The matched groups from the regex
            
        Returns:
            Dictionary of validated parameters
        """
        params = {}
        
        if cmd_type == CommandType.PLAY_SCALE:
            params["key"] = groups[0].upper()
            params["mode"] = groups[1].lower()
            
        elif cmd_type == CommandType.PLAY_ARP:
            params["key"] = groups[0].upper()
            params["chord_type"] = groups[1].lower()
            
        elif cmd_type == CommandType.PLAY_RANDOM:
            params["count"] = int(groups[0])
            
        elif cmd_type == CommandType.SET_KEY:
            params["key"] = groups[0].upper()
            params["mode"] = groups[1].lower()
            
        elif cmd_type == CommandType.SET_DENSITY:
            density_map = {"low": "low", "med": "med", "medium": "med", "high": "high"}
            params["density"] = density_map.get(groups[0].lower(), "med")
            
        elif cmd_type == CommandType.SET_TEMPO:
            params["tempo"] = max(60, min(200, int(groups[0])))  # Clamp to reasonable range
            
        elif cmd_type == CommandType.SET_RANDOMNESS:
            params["randomness"] = max(0.0, min(1.0, float(groups[0])))
            
        elif cmd_type == CommandType.SET_VELOCITY:
            params["velocity"] = max(1, min(127, int(groups[0])))
            
        elif cmd_type == CommandType.SET_REGISTER:
            params["register"] = max(0, min(9, int(groups[0])))
            
        elif cmd_type == CommandType.CC:
            params["cc_number"] = max(1, min(119, int(groups[0])))
            params["cc_value"] = max(0, min(127, int(groups[1])))
            
        elif cmd_type == CommandType.MOD:
            params["mod_value"] = max(0, min(127, int(groups[0])))
            
        elif cmd_type == CommandType.TARGET:
            params["part"] = groups[0].lower()
            
        # OSC Style Control Commands
        elif cmd_type == CommandType.SET_SWING:
            params["swing"] = max(0.0, min(1.0, float(groups[0])))
            
        elif cmd_type == CommandType.SET_ACCENT:
            params["accent"] = max(0.0, min(50.0, float(groups[0])))
            
        elif cmd_type == CommandType.SET_HUMANIZE_TIMING:
            params["humanize_timing"] = max(0.0, min(1.0, float(groups[0])))
            
        elif cmd_type == CommandType.SET_HUMANIZE_VELOCITY:
            params["humanize_velocity"] = max(0.0, min(1.0, float(groups[0])))
            
        elif cmd_type == CommandType.SET_OSC_ENABLED:
            # Handle various boolean representations
            value = groups[0].lower()
            if value in ["true", "on", "enable"]:
                params["enabled"] = True
            elif value in ["false", "off", "disable"]:
                params["enabled"] = False
            else:
                params["enabled"] = bool(value)
                
        elif cmd_type == CommandType.SET_OSC_PORT:
            params["port"] = max(1000, min(65535, int(groups[0])))
            
        elif cmd_type == CommandType.SET_STYLE_PRESET:
            params["preset"] = groups[0].lower()
            
        # Contextual Intelligence Commands
        elif cmd_type == CommandType.LOAD_PROJECT:
            params["file_path"] = groups[0].strip()
            
        elif cmd_type == CommandType.APPLY_SUGGESTION:
            params["suggestion"] = groups[0].strip()
            
        # Commands with no parameters (STOP, STATUS, HELP, OSC_RESET, analysis commands) have empty params
        
        return params
    
    def get_help_text(self) -> str:
        """Get help text showing available commands."""
        return """
Available Commands:

Play Commands:
  play scale [KEY] [MODE]     - Play a scale (e.g., "play scale C major")
  play arp [KEY] [CHORD]     - Play an arpeggio (e.g., "play arp C major")
  play random [COUNT]        - Play random notes (e.g., "play random 8")

Settings:
  set key to [KEY] [MODE]    - Set session key (e.g., "set key to D minor")
  set density to [LEVEL]     - Set note density (low/med/high)
  set tempo to [BPM]         - Set tempo (e.g., "set tempo to 140")
  set randomness to [0-1]    - Set randomness level (e.g., "set randomness to 0.3")
  set velocity to [1-127]    - Set note velocity (e.g., "set velocity to 100")
  set register to [0-9]      - Set octave (e.g., "set register to 5")

Control:
  cc [NUMBER] to [VALUE]     - Send control change (e.g., "cc 74 to 64")
  mod wheel [VALUE]          - Send modulation wheel (e.g., "mod wheel 32")
  target [PART]              - Set target part (e.g., "target piano")

OSC Style Control (JUCE Plugin):
  set swing to [0-1]         - Set swing ratio (e.g., "set swing to 0.7")
  set accent to [0-50]       - Set accent amount (e.g., "set accent to 25")
  set humanize timing to [0-1] - Set timing humanization (e.g., "set humanize timing to 0.3")
  set humanize velocity to [0-1] - Set velocity humanization (e.g., "set humanize velocity to 0.4")
  set osc enabled to [on/off] - Enable/disable OSC control (e.g., "set osc enabled to on")
  set osc port to [PORT]     - Set OSC port (e.g., "set osc port to 3819")
  set style to [PRESET]      - Apply style preset (e.g., "set style to jazz")
  make it [STYLE]            - Apply style (e.g., "make it jazzier")
  reset osc                  - Reset all OSC parameters to defaults

Contextual Intelligence (Visual Analysis):
  load [FILE]                - Load MIDI project for analysis (e.g., "load song.mid")
  analyze bass               - Show bass line analysis and highlighting
  analyze melody             - Show melody analysis and highlighting
  analyze harmony            - Show harmony analysis and highlighting
  analyze rhythm             - Show rhythm analysis and highlighting
  analyze all                - Complete musical analysis
  get suggestions            - Get improvement suggestions
  apply suggestion [ID]      - Apply a specific suggestion
  show feedback              - Show visual feedback summary
  clear feedback             - Clear all visual feedback

System:
  stop                      - Stop current playback
  status                    - Show current state
  help                      - Show this help
"""
