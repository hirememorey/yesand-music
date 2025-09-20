"""
MIDI I/O module for reading and writing MIDI files.

This module provides pure Python functions for parsing MIDI files into a simple,
universal data structure and saving that data back to MIDI files. Uses mido
for low-level MIDI parsing while maintaining full control over the data format.

No heavy music theory libraries are used - everything is built from first principles
to avoid the "Black Box Dependency Problem" and maintain velocity.
"""

from __future__ import annotations

import mido
from typing import List, Dict, Any, Optional
from pathlib import Path


def parse_midi_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Parse a MIDI file into a simple, universal list of dictionaries.
    
    Each note is represented as:
    {
        'pitch': int,           # MIDI note number (0-127)
        'velocity': int,        # MIDI velocity (0-127)
        'start_time_seconds': float,  # When the note starts (seconds from file start)
        'duration_seconds': float,    # How long the note lasts (seconds)
        'track_index': int      # Which track the note belongs to (0-based)
    }
    
    Args:
        filepath: Path to the MIDI file to parse
        
    Returns:
        List of note dictionaries in chronological order
        
    Raises:
        FileNotFoundError: If the MIDI file doesn't exist
        ValueError: If the MIDI file is corrupted or invalid
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"MIDI file not found: {filepath}")
    
    try:
        midi_file = mido.MidiFile(str(filepath))
    except Exception as e:
        raise ValueError(f"Failed to parse MIDI file {filepath}: {e}")
    
    # Convert ticks to seconds using the file's tempo
    ticks_per_beat = midi_file.ticks_per_beat
    tempo = 500000  # Default tempo (120 BPM) in microseconds per beat
    
    notes_data = []
    track_times = [0.0] * len(midi_file.tracks)  # Current time for each track
    
    # Process each track
    for track_index, track in enumerate(midi_file.tracks):
        current_time_ticks = 0
        active_notes = {}  # Track note-on events waiting for note-off
        
        for message in track:
            # Update current time in ticks
            current_time_ticks += message.time
            
            # Convert ticks to seconds
            current_time_seconds = mido.tick2second(
                current_time_ticks, 
                ticks_per_beat, 
                tempo
            )
            
            # Handle tempo changes
            if message.type == 'set_tempo':
                tempo = message.tempo
            
            # Handle note-on events
            elif message.type == 'note_on' and message.velocity > 0:
                note_key = (message.channel, message.note)
                active_notes[note_key] = {
                    'pitch': message.note,
                    'velocity': message.velocity,
                    'start_time_seconds': current_time_seconds,
                    'track_index': track_index
                }
            
            # Handle note-off events
            elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
                note_key = (message.channel, message.note)
                if note_key in active_notes:
                    note_data = active_notes.pop(note_key)
                    duration_seconds = current_time_seconds - note_data['start_time_seconds']
                    
                    # Only include notes with positive duration
                    if duration_seconds > 0:
                        notes_data.append({
                            'pitch': note_data['pitch'],
                            'velocity': note_data['velocity'],
                            'start_time_seconds': note_data['start_time_seconds'],
                            'duration_seconds': duration_seconds,
                            'track_index': note_data['track_index']
                        })
    
    # Sort notes by start time for chronological order
    notes_data.sort(key=lambda note: note['start_time_seconds'])
    
    return notes_data


def save_midi_file(filepath: str, notes_data: List[Dict[str, Any]], ticks_per_beat: int = 480) -> None:
    """
    Save a list of note dictionaries to a MIDI file.
    
    Args:
        filepath: Path where to save the MIDI file
        notes_data: List of note dictionaries with the structure:
                   {
                       'pitch': int,
                       'velocity': int, 
                       'start_time_seconds': float,
                       'duration_seconds': float,
                       'track_index': int
                   }
        ticks_per_beat: MIDI ticks per quarter note (default: 480)
        
    Raises:
        ValueError: If notes_data is invalid or empty
        OSError: If the file cannot be written
    """
    if not notes_data:
        raise ValueError("Cannot save empty notes data")
    
    # Validate notes data structure
    required_keys = {'pitch', 'velocity', 'start_time_seconds', 'duration_seconds', 'track_index'}
    for i, note in enumerate(notes_data):
        if not isinstance(note, dict):
            raise ValueError(f"Note {i} is not a dictionary")
        if not required_keys.issubset(note.keys()):
            missing = required_keys - set(note.keys())
            raise ValueError(f"Note {i} missing required keys: {missing}")
        
        # Validate data types and ranges
        if not (0 <= note['pitch'] <= 127):
            raise ValueError(f"Note {i} pitch {note['pitch']} out of range (0-127)")
        if not (0 <= note['velocity'] <= 127):
            raise ValueError(f"Note {i} velocity {note['velocity']} out of range (0-127)")
        if note['start_time_seconds'] < 0:
            raise ValueError(f"Note {i} start_time_seconds {note['start_time_seconds']} cannot be negative")
        if note['duration_seconds'] <= 0:
            raise ValueError(f"Note {i} duration_seconds {note['duration_seconds']} must be positive")
        if not isinstance(note['track_index'], int) or note['track_index'] < 0:
            raise ValueError(f"Note {i} track_index {note['track_index']} must be non-negative integer")
    
    # Group notes by track
    tracks_data = {}
    for note in notes_data:
        track_index = note['track_index']
        if track_index not in tracks_data:
            tracks_data[track_index] = []
        tracks_data[track_index].append(note)
    
    # Create MIDI file
    midi_file = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    
    # Add tracks (create at least one track even if empty)
    max_track_index = max(tracks_data.keys()) if tracks_data else 0
    for track_index in range(max_track_index + 1):
        track = mido.MidiTrack()
        
        # Add tempo message to first track
        if track_index == 0:
            track.append(mido.MetaMessage('set_tempo', tempo=500000))  # 120 BPM
        
        # Add notes for this track
        if track_index in tracks_data:
            track_notes = sorted(tracks_data[track_index], key=lambda n: n['start_time_seconds'])
            
            # Convert notes to MIDI messages
            current_time_ticks = 0
            for note in track_notes:
                # Convert seconds to ticks
                start_ticks = int(mido.second2tick(note['start_time_seconds'], ticks_per_beat, 500000))
                end_ticks = int(mido.second2tick(
                    note['start_time_seconds'] + note['duration_seconds'], 
                    ticks_per_beat, 
                    500000
                ))
                
                # Add note-on message
                note_on_delta = start_ticks - current_time_ticks
                track.append(mido.Message('note_on', 
                                        channel=0,  # Use channel 0 for all notes
                                        note=note['pitch'], 
                                        velocity=note['velocity'], 
                                        time=note_on_delta))
                
                # Add note-off message
                note_off_delta = end_ticks - start_ticks
                track.append(mido.Message('note_off', 
                                        channel=0,  # Use channel 0 for all notes
                                        note=note['pitch'], 
                                        velocity=0, 
                                        time=note_off_delta))
                
                current_time_ticks = end_ticks
        
        midi_file.tracks.append(track)
    
    # Save the file
    try:
        midi_file.save(str(filepath))
    except Exception as e:
        raise OSError(f"Failed to save MIDI file {filepath}: {e}")


def validate_notes_data(notes_data: List[Dict[str, Any]]) -> bool:
    """
    Validate that notes_data has the correct structure.
    
    Args:
        notes_data: List of note dictionaries to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(notes_data, list):
        return False
    
    required_keys = {'pitch', 'velocity', 'start_time_seconds', 'duration_seconds', 'track_index'}
    
    for note in notes_data:
        if not isinstance(note, dict):
            return False
        if not required_keys.issubset(note.keys()):
            return False
        if not (0 <= note['pitch'] <= 127):
            return False
        if not (0 <= note['velocity'] <= 127):
            return False
        if note['start_time_seconds'] < 0:
            return False
        if note['duration_seconds'] <= 0:
            return False
        if not isinstance(note['track_index'], int) or note['track_index'] < 0:
            return False
    
    return True


def get_file_info(filepath: str) -> Dict[str, Any]:
    """
    Get basic information about a MIDI file without parsing all notes.
    
    Args:
        filepath: Path to the MIDI file
        
    Returns:
        Dictionary with file information:
        {
            'ticks_per_beat': int,
            'num_tracks': int,
            'duration_seconds': float,
            'num_notes': int
        }
    """
    try:
        midi_file = mido.MidiFile(str(filepath))
        
        # Count notes and find duration
        num_notes = 0
        max_time_ticks = 0
        tempo = 500000  # Default tempo
        
        for track in midi_file.tracks:
            current_time_ticks = 0
            for message in track:
                current_time_ticks += message.time
                if message.type == 'set_tempo':
                    tempo = message.tempo
                if message.type in ['note_on', 'note_off']:
                    num_notes += 1
                max_time_ticks = max(max_time_ticks, current_time_ticks)
        
        duration_seconds = mido.tick2second(max_time_ticks, midi_file.ticks_per_beat, tempo)
        
        return {
            'ticks_per_beat': midi_file.ticks_per_beat,
            'num_tracks': len(midi_file.tracks),
            'duration_seconds': duration_seconds,
            'num_notes': num_notes
        }
        
    except Exception as e:
        raise ValueError(f"Failed to get file info for {filepath}: {e}")
