"""
Musical Notation Converter

Converts the existing universal MIDI format to simple JSON for LLM context.
Leverages the existing midi_io.py universal format without adding complexity.
"""

from typing import List, Dict, Any, Optional
import json
from pathlib import Path

# Import existing MIDI I/O functions
from midi_io import parse_midi_file


def midi_to_note_name(midi_number: int) -> str:
    """Convert MIDI number to musical note name."""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_number // 12) - 1
    note_name = note_names[midi_number % 12]
    return f"{note_name}{octave}"


def convert_midi_to_json(midi_data: List[Dict[str, Any]], 
                        tempo: int = 120, 
                        key: str = "C major") -> Dict[str, Any]:
    """
    Convert universal MIDI format to simple JSON for LLM context.
    
    Args:
        midi_data: List of note dictionaries from midi_io.py
        tempo: Project tempo (default: 120)
        key: Project key (default: "C major")
    
    Returns:
        Simple JSON structure for LLM consumption
    """
    # Group notes by track
    tracks = {}
    for note in midi_data:
        track_index = note.get('track_index', 0)
        if track_index not in tracks:
            tracks[track_index] = []
        
        # Convert to simple format
        json_note = {
            'pitch': midi_to_note_name(note['pitch']),
            'startTime': note['start_time_seconds'],
            'duration': note['duration_seconds'],
            'velocity': note['velocity']
        }
        tracks[track_index].append(json_note)
    
    # Create simple JSON structure
    result = {
        'tempo': tempo,
        'key': key,
        'tracks': []
    }
    
    # Add tracks
    for track_index, notes in tracks.items():
        track_name = f"Track {track_index + 1}"
        result['tracks'].append({
            'name': track_name,
            'notes': sorted(notes, key=lambda n: n['startTime'])
        })
    
    return result


def extract_project_context_from_midi_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Extract project context from a MIDI file.
    
    Args:
        filepath: Path to MIDI file
    
    Returns:
        JSON context or None if extraction fails
    """
    try:
        # Parse MIDI file using existing system
        midi_data = parse_midi_file(filepath)
        
        # Convert to JSON
        context = convert_midi_to_json(midi_data)
        
        return context
    except Exception as e:
        print(f"Warning: Could not extract context from {filepath}: {e}")
        return None


def save_context_to_file(context: Dict[str, Any], filepath: str) -> bool:
    """Save context JSON to file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(context, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving context to {filepath}: {e}")
        return False


def load_context_from_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Load context JSON from file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading context from {filepath}: {e}")
        return None
