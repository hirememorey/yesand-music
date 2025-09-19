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
            
        # Commands with no parameters (STOP, STATUS, HELP) have empty params
        
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

System:
  stop                      - Stop current playback
  status                    - Show current state
  help                      - Show this help
"""
