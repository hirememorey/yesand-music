"""
Track Manager for Automatic Track Creation and Management

This module provides intelligent track management for Ardour, automatically
creating appropriate tracks based on enhancement types and musical context.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TrackType(Enum):
    """Types of tracks in Ardour."""
    MIDI = "midi"
    AUDIO = "audio"
    BUS = "bus"
    MASTER = "master"


class EnhancementType(Enum):
    """Types of musical enhancements."""
    BASS = "bass"
    DRUMS = "drums"
    MELODY = "melody"
    HARMONY = "harmony"
    GENERAL = "general"


@dataclass
class TrackTemplate:
    """Template for track creation."""
    name: str
    type: TrackType
    channel_count: int
    default_volume: float
    default_pan: float
    color: str
    description: str


@dataclass
class TrackInfo:
    """Information about an existing track."""
    id: str
    name: str
    type: TrackType
    channel_count: int
    volume: float
    pan: float
    muted: bool
    solo: bool
    armed: bool


class TrackManager:
    """
    Intelligent track manager for Ardour.
    
    Automatically creates and manages tracks based on enhancement types
    and musical context, ensuring proper track organization.
    """
    
    def __init__(self):
        """Initialize track manager."""
        self.logger = logging.getLogger(__name__)
        self.track_templates = self._initialize_track_templates()
        self.existing_tracks: List[TrackInfo] = []
    
    def _initialize_track_templates(self) -> Dict[EnhancementType, TrackTemplate]:
        """Initialize track templates for different enhancement types."""
        return {
            EnhancementType.BASS: TrackTemplate(
                name="Bass",
                type=TrackType.MIDI,
                channel_count=1,
                default_volume=0.8,
                default_pan=0.0,
                color="blue",
                description="Bass line track"
            ),
            EnhancementType.DRUMS: TrackTemplate(
                name="Drums",
                type=TrackType.MIDI,
                channel_count=1,
                default_volume=0.9,
                default_pan=0.0,
                color="red",
                description="Drum pattern track"
            ),
            EnhancementType.MELODY: TrackTemplate(
                name="Melody",
                type=TrackType.MIDI,
                channel_count=1,
                default_volume=0.7,
                default_pan=0.0,
                color="green",
                description="Melody track"
            ),
            EnhancementType.HARMONY: TrackTemplate(
                name="Harmony",
                type=TrackType.MIDI,
                channel_count=1,
                default_volume=0.6,
                default_pan=0.0,
                color="purple",
                description="Harmony track"
            ),
            EnhancementType.GENERAL: TrackTemplate(
                name="Generated",
                type=TrackType.MIDI,
                channel_count=1,
                default_volume=0.7,
                default_pan=0.0,
                color="orange",
                description="Generated content track"
            )
        }
    
    def get_track_for_enhancement(self, enhancement_type: EnhancementType, 
                                 track_name: str = None) -> Tuple[str, bool]:
        """
        Get appropriate track for enhancement type.
        
        Args:
            enhancement_type: Type of enhancement
            track_name: Optional specific track name
            
        Returns:
            Tuple of (track_name, was_created)
        """
        template = self.track_templates.get(enhancement_type)
        if not template:
            template = self.track_templates[EnhancementType.GENERAL]
        
        # Use provided name or template name
        target_name = track_name or template.name
        
        # Check if track already exists
        existing_track = self._find_track_by_name(target_name)
        if existing_track:
            self.logger.info(f"Using existing track: {target_name}")
            return target_name, False
        
        # Check for similar tracks
        similar_track = self._find_similar_track(enhancement_type)
        if similar_track:
            self.logger.info(f"Using similar track: {similar_track.name}")
            return similar_track.name, False
        
        # Create new track
        self.logger.info(f"Creating new track: {target_name}")
        return target_name, True
    
    def create_track_config(self, enhancement_type: EnhancementType, 
                          track_name: str = None, position: float = 0.0) -> Dict[str, Any]:
        """
        Create track configuration for enhancement.
        
        Args:
            enhancement_type: Type of enhancement
            track_name: Optional specific track name
            position: Position in timeline
            
        Returns:
            Track configuration dictionary
        """
        template = self.track_templates.get(enhancement_type)
        if not template:
            template = self.track_templates[EnhancementType.GENERAL]
        
        target_name = track_name or template.name
        
        # Ensure unique name
        unique_name = self._ensure_unique_track_name(target_name)
        
        return {
            "name": unique_name,
            "type": template.type.value,
            "channel_count": template.channel_count,
            "default_volume": template.default_volume,
            "default_pan": template.default_pan,
            "color": template.color,
            "description": template.description,
            "position": position,
            "enhancement_type": enhancement_type.value
        }
    
    def get_track_placement_strategy(self, enhancement_type: EnhancementType, 
                                   existing_tracks: List[TrackInfo]) -> Dict[str, Any]:
        """
        Get track placement strategy based on enhancement type and existing tracks.
        
        Args:
            enhancement_type: Type of enhancement
            existing_tracks: List of existing tracks
            
        Returns:
            Placement strategy dictionary
        """
        strategy = {
            "position": 0.0,
            "track_order": "append",
            "group_with": None,
            "color_scheme": "enhancement_type"
        }
        
        # Determine position based on enhancement type
        if enhancement_type == EnhancementType.BASS:
            strategy["position"] = 0.0  # Bass typically goes first
            strategy["track_order"] = "prepend"
        elif enhancement_type == EnhancementType.DRUMS:
            strategy["position"] = 0.0  # Drums also go early
            strategy["track_order"] = "prepend"
        elif enhancement_type == EnhancementType.MELODY:
            # Melody goes after rhythm section
            rhythm_tracks = [t for t in existing_tracks 
                           if t.name.lower() in ["bass", "drums", "percussion"]]
            strategy["position"] = len(rhythm_tracks) * 1.0
        elif enhancement_type == EnhancementType.HARMONY:
            # Harmony goes after melody
            melody_tracks = [t for t in existing_tracks 
                           if t.name.lower() in ["melody", "lead", "vocal"]]
            strategy["position"] = len(melody_tracks) * 1.0
        else:
            # General tracks go at the end
            strategy["position"] = len(existing_tracks) * 1.0
            strategy["track_order"] = "append"
        
        return strategy
    
    def suggest_track_improvements(self, track_info: TrackInfo, 
                                 enhancement_type: EnhancementType) -> List[str]:
        """
        Suggest improvements for existing track based on enhancement type.
        
        Args:
            track_info: Information about existing track
            enhancement_type: Type of enhancement
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check track type compatibility
        if enhancement_type == EnhancementType.BASS and track_info.type != TrackType.MIDI:
            suggestions.append(f"Consider using MIDI track for bass enhancement")
        
        if enhancement_type == EnhancementType.DRUMS and track_info.type != TrackType.MIDI:
            suggestions.append(f"Consider using MIDI track for drum enhancement")
        
        # Check volume levels
        template = self.track_templates.get(enhancement_type)
        if template and abs(track_info.volume - template.default_volume) > 0.2:
            suggestions.append(f"Consider adjusting volume to {template.default_volume} for {enhancement_type.value}")
        
        # Check track naming
        if not self._is_track_name_appropriate(track_info.name, enhancement_type):
            suggestions.append(f"Consider renaming track to better reflect {enhancement_type.value} content")
        
        return suggestions
    
    def update_existing_tracks(self, tracks: List[TrackInfo]):
        """Update list of existing tracks."""
        self.existing_tracks = tracks.copy()
        self.logger.debug(f"Updated existing tracks: {len(tracks)} tracks")
    
    def _find_track_by_name(self, name: str) -> Optional[TrackInfo]:
        """Find track by name."""
        for track in self.existing_tracks:
            if track.name.lower() == name.lower():
                return track
        return None
    
    def _find_similar_track(self, enhancement_type: EnhancementType) -> Optional[TrackInfo]:
        """Find similar track for enhancement type."""
        template = self.track_templates.get(enhancement_type)
        if not template:
            return None
        
        # Look for tracks with similar names
        similar_names = self._get_similar_names(enhancement_type)
        
        for track in self.existing_tracks:
            if any(name in track.name.lower() for name in similar_names):
                return track
        
        return None
    
    def _get_similar_names(self, enhancement_type: EnhancementType) -> List[str]:
        """Get similar names for enhancement type."""
        name_mappings = {
            EnhancementType.BASS: ["bass", "bassline", "low", "bottom"],
            EnhancementType.DRUMS: ["drum", "percussion", "beat", "rhythm"],
            EnhancementType.MELODY: ["melody", "lead", "vocal", "voice", "sing"],
            EnhancementType.HARMONY: ["harmony", "chord", "pad", "accompaniment"],
            EnhancementType.GENERAL: ["generated", "ai", "enhanced", "new"]
        }
        
        return name_mappings.get(enhancement_type, [])
    
    def _ensure_unique_track_name(self, base_name: str) -> str:
        """Ensure track name is unique."""
        if not self._find_track_by_name(base_name):
            return base_name
        
        counter = 1
        while True:
            unique_name = f"{base_name}_{counter}"
            if not self._find_track_by_name(unique_name):
                return unique_name
            counter += 1
    
    def _is_track_name_appropriate(self, track_name: str, enhancement_type: EnhancementType) -> bool:
        """Check if track name is appropriate for enhancement type."""
        similar_names = self._get_similar_names(enhancement_type)
        return any(name in track_name.lower() for name in similar_names)
    
    def get_track_summary(self) -> Dict[str, Any]:
        """Get summary of track management state."""
        return {
            "total_tracks": len(self.existing_tracks),
            "track_types": {
                track_type.value: len([t for t in self.existing_tracks if t.type == track_type])
                for track_type in TrackType
            },
            "enhancement_tracks": {
                enhancement_type.value: len([
                    t for t in self.existing_tracks 
                    if self._is_track_name_appropriate(t.name, enhancement_type)
                ])
                for enhancement_type in EnhancementType
            },
            "templates_available": len(self.track_templates)
        }
