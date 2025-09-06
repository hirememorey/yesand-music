"""
Music theory utilities.

This module provides helper functions to generate common musical structures
such as scales and chords.
"""

from __future__ import annotations

from typing import List


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


