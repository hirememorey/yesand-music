"""
Project module for managing musical data.

This module provides the Project class, which serves as a container for musical data
including notes and metadata. It provides a clean interface for loading from and
saving to MIDI files while maintaining separation of concerns.

The Project class is designed to be simple, testable, and free from the "Spaghetti Code"
problem by keeping data management separate from musical analysis or processing logic.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from pathlib import Path
from midi_io import parse_midi_file, save_midi_file, validate_notes_data


class Project:
    """
    A container for musical data including notes and metadata.
    
    This class provides a simple interface for managing musical projects without
    mixing concerns. It focuses purely on data storage and basic I/O operations.
    """
    
    def __init__(self, tempo: int = 120, ticks_per_beat: int = 480, name: str = "Untitled Project"):
        """
        Initialize an empty musical project.
        
        Args:
            tempo: Tempo in beats per minute (default: 120)
            ticks_per_beat: MIDI ticks per quarter note (default: 480)
            name: Project name (default: "Untitled Project")
        """
        self.notes: List[Dict[str, Any]] = []
        self.tempo = tempo
        self.ticks_per_beat = ticks_per_beat
        self.name = name
        self.filepath: Optional[str] = None
    
    def load_from_midi(self, filepath: str) -> None:
        """
        Load notes from a MIDI file into this project.
        
        Args:
            filepath: Path to the MIDI file to load
            
        Raises:
            FileNotFoundError: If the MIDI file doesn't exist
            ValueError: If the MIDI file is corrupted or invalid
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"MIDI file not found: {filepath}")
        
        # Parse the MIDI file
        notes_data = parse_midi_file(str(filepath))
        
        # Validate the data
        if not validate_notes_data(notes_data):
            raise ValueError(f"Invalid notes data loaded from {filepath}")
        
        # Store the notes and update metadata
        self.notes = notes_data
        self.filepath = str(filepath)
        
        # Update project name from filename if not explicitly set
        if self.name == "Untitled Project":
            self.name = filepath.stem
    
    def save_to_midi(self, filepath: str) -> None:
        """
        Save the project's notes to a MIDI file.
        
        Args:
            filepath: Path where to save the MIDI file
            
        Raises:
            ValueError: If the notes data is invalid or empty
            OSError: If the file cannot be written
        """
        if not self.notes:
            raise ValueError("Cannot save empty project - no notes to save")
        
        # Validate notes data before saving
        if not validate_notes_data(self.notes):
            raise ValueError("Project contains invalid notes data")
        
        # Save to MIDI file
        save_midi_file(filepath, self.notes, self.ticks_per_beat)
        
        # Update the project's filepath
        self.filepath = str(filepath)
    
    def get_all_notes(self) -> List[Dict[str, Any]]:
        """
        Get all notes in the project.
        
        Returns:
            List of note dictionaries. Each note has the structure:
            {
                'pitch': int,
                'velocity': int,
                'start_time_seconds': float,
                'duration_seconds': float,
                'track_index': int
            }
        """
        return self.notes.copy()  # Return a copy to prevent external modification
    
    def add_note(self, pitch: int, velocity: int, start_time_seconds: float, 
                 duration_seconds: float, track_index: int = 0) -> None:
        """
        Add a single note to the project.
        
        Args:
            pitch: MIDI note number (0-127)
            velocity: MIDI velocity (0-127)
            start_time_seconds: When the note starts (seconds from project start)
            duration_seconds: How long the note lasts (seconds)
            track_index: Which track the note belongs to (0-based, default: 0)
            
        Raises:
            ValueError: If any parameter is out of valid range
        """
        # Validate parameters
        if not (0 <= pitch <= 127):
            raise ValueError(f"Pitch {pitch} out of range (0-127)")
        if not (0 <= velocity <= 127):
            raise ValueError(f"Velocity {velocity} out of range (0-127)")
        if start_time_seconds < 0:
            raise ValueError(f"Start time {start_time_seconds} cannot be negative")
        if duration_seconds <= 0:
            raise ValueError(f"Duration {duration_seconds} must be positive")
        if not isinstance(track_index, int) or track_index < 0:
            raise ValueError(f"Track index {track_index} must be non-negative integer")
        
        # Create note dictionary
        note = {
            'pitch': pitch,
            'velocity': velocity,
            'start_time_seconds': start_time_seconds,
            'duration_seconds': duration_seconds,
            'track_index': track_index
        }
        
        # Add to notes list
        self.notes.append(note)
    
    def clear_notes(self) -> None:
        """Remove all notes from the project."""
        self.notes.clear()
    
    def get_notes_by_track(self, track_index: int) -> List[Dict[str, Any]]:
        """
        Get all notes from a specific track.
        
        Args:
            track_index: The track index to filter by
            
        Returns:
            List of note dictionaries from the specified track
        """
        return [note for note in self.notes if note['track_index'] == track_index]
    
    def get_notes_in_time_range(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """
        Get all notes that overlap with the specified time range.
        
        Args:
            start_time: Start of time range (seconds)
            end_time: End of time range (seconds)
            
        Returns:
            List of note dictionaries that overlap with the time range
        """
        overlapping_notes = []
        for note in self.notes:
            note_start = note['start_time_seconds']
            note_end = note_start + note['duration_seconds']
            
            # Check if note overlaps with the time range
            if note_start < end_time and note_end > start_time:
                overlapping_notes.append(note)
        
        return overlapping_notes
    
    def get_duration(self) -> float:
        """
        Get the total duration of the project in seconds.
        
        Returns:
            Duration in seconds, or 0.0 if no notes
        """
        if not self.notes:
            return 0.0
        
        max_end_time = 0.0
        for note in self.notes:
            end_time = note['start_time_seconds'] + note['duration_seconds']
            max_end_time = max(max_end_time, end_time)
        
        return max_end_time
    
    def get_track_count(self) -> int:
        """
        Get the number of tracks in the project.
        
        Returns:
            Number of tracks (0 if no notes)
        """
        if not self.notes:
            return 0
        
        max_track_index = max(note['track_index'] for note in self.notes)
        return max_track_index + 1
    
    def get_note_count(self) -> int:
        """
        Get the total number of notes in the project.
        
        Returns:
            Number of notes
        """
        return len(self.notes)
    
    def is_empty(self) -> bool:
        """
        Check if the project has any notes.
        
        Returns:
            True if no notes, False otherwise
        """
        return len(self.notes) == 0
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get project metadata.
        
        Returns:
            Dictionary containing project metadata
        """
        return {
            'name': self.name,
            'tempo': self.tempo,
            'ticks_per_beat': self.ticks_per_beat,
            'filepath': self.filepath,
            'note_count': self.get_note_count(),
            'track_count': self.get_track_count(),
            'duration_seconds': self.get_duration()
        }
    
    def __str__(self) -> str:
        """String representation of the project."""
        metadata = self.get_metadata()
        return (f"Project '{self.name}': {metadata['note_count']} notes, "
                f"{metadata['track_count']} tracks, {metadata['duration_seconds']:.2f}s")
    
    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return (f"Project(name='{self.name}', tempo={self.tempo}, "
                f"ticks_per_beat={self.ticks_per_beat}, notes={len(self.notes)})")
