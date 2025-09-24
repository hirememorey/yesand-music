"""
Music theory utilities.

This module provides helper functions to generate common musical structures
such as scales, chords, and arpeggios.
"""

from __future__ import annotations

import random
from typing import List, Tuple

from commands.types import Density, Mode, Note


def create_major_scale(root_note_midi: int) -> List[int]:
    """Create a major scale (Ionian) starting at the given MIDI root note.

    Returns 8 MIDI notes including the octave.
    Example: C4 (60) -> [60, 62, 64, 65, 67, 69, 71, 72]
    """
    # Whole-step pattern for major scale: W W H W W W H
    # In semitones: 2, 2, 1, 2, 2, 2, 1
    steps = [2, 2, 1, 2, 2, 2, 1]
    notes = [int(root_note_midi)]
    current = int(root_note_midi)
    for step in steps:
        current += step
        notes.append(current)
    return notes


def create_scale(root_note_midi: int, mode: Mode) -> List[int]:
    """Create a scale starting at the given MIDI root note in the specified mode.

    Args:
        root_note_midi: MIDI note number for the root
        mode: The musical mode (major, minor, etc.)

    Returns:
        List of MIDI note numbers for the scale
    """
    # Mode patterns (semitones from root)
    mode_patterns = {
        Mode.MAJOR: [2, 2, 1, 2, 2, 2, 1],  # Ionian
        Mode.MINOR: [2, 1, 2, 2, 1, 2, 2],  # Aeolian
        Mode.DORIAN: [2, 1, 2, 2, 2, 1, 2],
        Mode.PHRYGIAN: [1, 2, 2, 2, 1, 2, 2],
        Mode.LYDIAN: [2, 2, 2, 1, 2, 2, 1],
        Mode.MIXOLYDIAN: [2, 2, 1, 2, 2, 1, 2],
        Mode.LOCRIAN: [1, 2, 2, 1, 2, 2, 2],
    }
    
    steps = mode_patterns.get(mode, mode_patterns[Mode.MAJOR])
    notes = [int(root_note_midi)]
    current = int(root_note_midi)
    for step in steps:
        current += step
        notes.append(current)
    return notes


def create_chord(root_note_midi: int, chord_type: str) -> List[int]:
    """Create a chord starting at the given MIDI root note.

    Args:
        root_note_midi: MIDI note number for the root
        chord_type: Type of chord (major, minor, diminished, augmented, etc.)

    Returns:
        List of MIDI note numbers for the chord
    """
    # Chord patterns (semitones from root)
    chord_patterns = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 3, 6],
        "augmented": [0, 4, 8],
        "major7": [0, 4, 7, 11],
        "minor7": [0, 3, 7, 10],
        "dominant7": [0, 4, 7, 10],
        "diminished7": [0, 3, 6, 9],
        "half_diminished7": [0, 3, 6, 10],
        "major6": [0, 4, 7, 9],
        "minor6": [0, 3, 7, 9],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
        "add9": [0, 4, 7, 14],
        "minor_add9": [0, 3, 7, 14],
    }
    
    pattern = chord_patterns.get(chord_type.lower(), chord_patterns["major"])
    return [int(root_note_midi) + offset for offset in pattern]


def create_arpeggio(root_note_midi: int, chord_type: str, pattern: str = "up") -> List[int]:
    """Create an arpeggio from a chord.

    Args:
        root_note_midi: MIDI note number for the root
        chord_type: Type of chord
        pattern: Arpeggio pattern ("up", "down", "updown", "downup", "random")

    Returns:
        List of MIDI note numbers for the arpeggio
    """
    chord_notes = create_chord(root_note_midi, chord_type)
    
    if pattern == "up":
        return chord_notes
    elif pattern == "down":
        return chord_notes[::-1]
    elif pattern == "updown":
        return chord_notes + chord_notes[-2:0:-1]
    elif pattern == "downup":
        return chord_notes[::-1] + chord_notes[1:-1]
    elif pattern == "random":
        notes = chord_notes.copy()
        random.shuffle(notes)
        return notes
    else:
        return chord_notes


def create_random_notes(root_note_midi: int, count: int, scale_notes: List[int] = None) -> List[int]:
    """Create random notes from a scale or chromatic range.

    Args:
        root_note_midi: Base MIDI note number
        count: Number of notes to generate
        scale_notes: Optional list of scale notes to choose from

    Returns:
        List of random MIDI note numbers
    """
    if scale_notes:
        return random.choices(scale_notes, k=count)
    else:
        # Use chromatic range around the root note
        min_note = max(0, root_note_midi - 12)
        max_note = min(127, root_note_midi + 12)
        return [random.randint(min_note, max_note) for _ in range(count)]


def create_rhythmic_pattern(notes: List[int], density: Density, duration_beats: float = 1.0) -> List[Note]:
    """Create a rhythmic pattern from a list of notes.

    Args:
        notes: List of MIDI note numbers
        density: Note density level
        duration_beats: Duration of each note in beats

    Returns:
        List of Note objects with timing
    """
    # Density patterns (note durations in beats)
    density_patterns = {
        Density.LOW: [2.0, 1.5, 1.0, 0.5],
        Density.MEDIUM: [1.0, 0.75, 0.5, 0.25],
        Density.HIGH: [0.5, 0.375, 0.25, 0.125],
    }
    
    durations = density_patterns.get(density, density_patterns[Density.MEDIUM])
    
    note_objects = []
    current_beat = 0.0
    
    for i, pitch in enumerate(notes):
        # Choose duration based on density
        duration = random.choice(durations)
        
        note_objects.append(Note(
            pitch=pitch,
            velocity=90,  # Default velocity, will be overridden by session state
            start_beat=current_beat,
            duration_beats=duration
        ))
        
        current_beat += duration
    
    return note_objects


def apply_randomness(notes: List[Note], randomness: float) -> List[Note]:
    """Apply randomness to note timing and velocity.

    Args:
        notes: List of Note objects
        randomness: Randomness level (0.0 to 1.0)

    Returns:
        List of Note objects with applied randomness
    """
    if randomness <= 0.0:
        return notes
    
    randomized_notes = []
    for note in notes:
        # Randomize timing
        time_variation = (random.random() - 0.5) * randomness * 0.5
        new_start = max(0.0, note.start_beat + time_variation)
        
        # Randomize velocity
        vel_variation = (random.random() - 0.5) * randomness * 20
        new_velocity = max(1, min(127, int(note.velocity + vel_variation)))
        
        # Randomize duration slightly
        dur_variation = (random.random() - 0.5) * randomness * 0.2
        new_duration = max(0.1, note.duration_beats + dur_variation)
        
        randomized_notes.append(Note(
            pitch=note.pitch,
            velocity=new_velocity,
            start_beat=new_start,
            duration_beats=new_duration
        ))
    
    return randomized_notes


def get_scale_notes_for_mode(mode: Mode) -> List[int]:
    """Get the scale pattern for a given mode.

    Args:
        mode: The musical mode

    Returns:
        List of semitone offsets from root for the mode
    """
    mode_patterns = {
        Mode.MAJOR: [0, 2, 4, 5, 7, 9, 11],
        Mode.MINOR: [0, 2, 3, 5, 7, 8, 10],
        Mode.DORIAN: [0, 2, 3, 5, 7, 9, 10],
        Mode.PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],
        Mode.LYDIAN: [0, 2, 4, 6, 7, 9, 11],
        Mode.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
        Mode.LOCRIAN: [0, 1, 3, 5, 6, 8, 10],
    }
    
    return mode_patterns.get(mode, mode_patterns[Mode.MAJOR])


def generate_scale(key: str, mode: str, octave_start: int, octave_end: int) -> List[int]:
    """Generate a scale for the given key and mode across multiple octaves.
    
    Args:
        key: The key (e.g., "C", "F#", "Bb")
        mode: The mode (e.g., "major", "minor", "dorian")
        octave_start: Starting octave (e.g., 2 for C2)
        octave_end: Ending octave (e.g., 6 for C6)
        
    Returns:
        List of MIDI note numbers for the scale across octaves
    """
    # Convert key to MIDI note number
    key_to_midi = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
        "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
    }
    
    # Convert mode to Mode enum
    mode_map = {
        "major": Mode.MAJOR,
        "minor": Mode.MINOR,
        "dorian": Mode.DORIAN,
        "phrygian": Mode.PHRYGIAN,
        "lydian": Mode.LYDIAN,
        "mixolydian": Mode.MIXOLYDIAN,
        "locrian": Mode.LOCRIAN
    }
    
    if key not in key_to_midi:
        key = "C"  # Default to C if key not found
    
    if mode not in mode_map:
        mode = "major"  # Default to major if mode not found
    
    # Get the base scale pattern
    base_pattern = get_scale_notes_for_mode(mode_map[mode])
    
    # Generate scale across multiple octaves
    scale_notes = []
    for octave in range(octave_start, octave_end + 1):
        for semitone_offset in base_pattern:
            # Calculate MIDI note number
            midi_note = key_to_midi[key] + (octave * 12) + semitone_offset
            scale_notes.append(midi_note)
    
    return scale_notes


