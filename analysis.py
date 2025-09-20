"""
Musical Analysis Module

This module contains pure functions for analyzing musical data using the universal
note dictionary format. All functions are designed to be:
- Pure (no side effects)
- Testable in isolation
- Free from external dependencies
- Compatible with the universal note format

Universal note format:
{'pitch': int, 'velocity': int, 'start_time_seconds': float, 'duration_seconds': float, 'track_index': int}
"""


def filter_notes_by_pitch(notes_data, max_pitch=60):
    """
    Filter notes by pitch, returning only notes with pitch <= max_pitch.
    
    This is a pure function that creates a new list without modifying the original.
    It's designed to be the foundation for bass line analysis and other pitch-based filtering.
    
    Args:
        notes_data (list): List of note dictionaries in universal format
        max_pitch (int): Maximum pitch value to include (default: 60 = C4)
        
    Returns:
        list: New list containing only notes with pitch <= max_pitch
        
    Example:
        >>> notes = [
        ...     {'pitch': 48, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 1.0, 'track_index': 0},
        ...     {'pitch': 72, 'velocity': 90, 'start_time_seconds': 1.0, 'duration_seconds': 1.0, 'track_index': 0}
        ... ]
        >>> bass_notes = filter_notes_by_pitch(notes, max_pitch=60)
        >>> len(bass_notes)
        1
        >>> bass_notes[0]['pitch']
        48
    """
    if not isinstance(notes_data, list):
        raise TypeError("notes_data must be a list")
    
    if not isinstance(max_pitch, int):
        raise TypeError("max_pitch must be an integer")
    
    # Pure function: create new list, don't modify original
    filtered_notes = []
    
    for note in notes_data:
        # Validate note structure
        if not isinstance(note, dict):
            continue  # Skip invalid entries silently
            
        if 'pitch' not in note:
            continue  # Skip notes without pitch
            
        if not isinstance(note['pitch'], int):
            continue  # Skip notes with invalid pitch type
            
        # Apply pitch filter
        if note['pitch'] <= max_pitch:
            filtered_notes.append(note)
    
    return filtered_notes


def apply_swing(notes_data, swing_ratio=0.6, beat_duration=0.5):
    """
    Apply swing feel to notes by delaying off-beat notes.
    
    This is a pure function that creates a new list with modified timing for off-beat notes.
    It implements the swing transformation that's critical for the JUCE plugin's real-time
    MIDI processing, but in a pure Python form for analysis and testing.
    
    Args:
        notes_data (list): List of note dictionaries in universal format
        swing_ratio (float): Swing intensity (0.5 = straight, >0.5 = swing, default: 0.6)
        beat_duration (float): Duration of one beat in seconds (default: 0.5 = 120 BPM)
        
    Returns:
        list: New list with modified timing for off-beat notes
        
    Example:
        >>> notes = [
        ...     {'pitch': 60, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 0.25, 'track_index': 0},  # On-beat
        ...     {'pitch': 62, 'velocity': 80, 'start_time_seconds': 0.25, 'duration_seconds': 0.25, 'track_index': 0}, # Off-beat
        ...     {'pitch': 64, 'velocity': 80, 'start_time_seconds': 0.5, 'duration_seconds': 0.25, 'track_index': 0}   # On-beat
        ... ]
        >>> swung_notes = apply_swing(notes, swing_ratio=0.6, beat_duration=0.5)
        >>> # Off-beat note at 0.25s should be delayed
        >>> swung_notes[1]['start_time_seconds'] > 0.25
        True
    """
    if not isinstance(notes_data, list):
        raise TypeError("notes_data must be a list")
    
    if not isinstance(swing_ratio, (int, float)):
        raise TypeError("swing_ratio must be a number")
    
    if not isinstance(beat_duration, (int, float)):
        raise TypeError("beat_duration must be a number")
    
    if beat_duration <= 0:
        raise ValueError("beat_duration must be positive")
    
    # Pure function: create new list, don't modify original
    swung_notes = []
    
    for note in notes_data:
        # Validate note structure
        if not isinstance(note, dict):
            continue  # Skip invalid entries silently
            
        if 'start_time_seconds' not in note:
            continue  # Skip notes without timing
            
        if not isinstance(note['start_time_seconds'], (int, float)):
            continue  # Skip notes with invalid timing type
        
        # Create a copy of the note to avoid modifying the original
        new_note = note.copy()
        
        # Calculate position within the beat
        start_time = note['start_time_seconds']
        beat_position = start_time % beat_duration
        beat_fraction = beat_position / beat_duration
        
        # Identify off-beat notes (8th note positions: 0.4 to 0.6 of beat)
        is_off_beat = 0.4 <= beat_fraction <= 0.6
        
        if is_off_beat:
            # Calculate swing delay
            # swing_ratio 0.5 = no delay, 0.6 = slight delay, 0.7 = more delay
            swing_delay = (swing_ratio - 0.5) * beat_duration * 0.25  # Max delay is 25% of beat
            
            # Apply the delay
            new_note['start_time_seconds'] = start_time + swing_delay
        
        swung_notes.append(new_note)
    
    return swung_notes
