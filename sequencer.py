"""
Sequencing and musical timing engine.

The Sequencer collects note events and schedules them in real time using a
provided MidiPlayer and BPM setting.
"""

from __future__ import annotations

import time
from typing import Dict, List

from midi_player import MidiPlayer


class Sequencer:
    """Simple beat-based sequencer.

    Stores note events with start time in beats and durations in beats, then
    plays them back in real time using the given MidiPlayer.
    """

    def __init__(self, midi_player: MidiPlayer, bpm: int) -> None:
        """Initialize with a MidiPlayer and tempo in BPM.

        Computes seconds per beat and prepares an internal note list.
        """
        self.midi_player: MidiPlayer = midi_player
        self.bpm: float = float(bpm)
        self.seconds_per_beat: float = 60.0 / self.bpm if self.bpm > 0 else 0.0
        self.notes: List[Dict[str, float]] = []

    def add_note(self, pitch: int, velocity: int, start_beat: float, duration_beats: float) -> None:
        """Add a note event to the sequence.

        Args:
            pitch: MIDI note number (0-127)
            velocity: MIDI velocity (0-127)
            start_beat: When the note starts, in beats from sequence start
            duration_beats: How long the note lasts, in beats
        """
        self.notes.append(
            {
                "pitch": int(pitch),
                "velocity": int(velocity),
                "start_beat": float(start_beat),
                "duration_beats": float(duration_beats),
            }
        )

    def play(self) -> None:
        """Play all scheduled notes in order based on their start beats.

        Notes are sorted by start_beat. The sequencer sleeps between events
        to align playback with the beat grid, then triggers notes via MidiPlayer.
        """
        if not self.notes:
            return

        # Sort notes by start position in beats
        sorted_notes = sorted(self.notes, key=lambda n: n["start_beat"])

        current_beat = 0.0
        for note in sorted_notes:
            target_start = float(note["start_beat"])
            sleep_beats = target_start - current_beat
            if sleep_beats > 0:
                time.sleep(sleep_beats * self.seconds_per_beat)

            duration_seconds = float(note["duration_beats"]) * self.seconds_per_beat
            self.midi_player.send_note(
                pitch=int(note["pitch"]),
                velocity=int(note["velocity"]),
                duration_in_seconds=duration_seconds,
            )

            # Move current time reference to this note's start beat
            current_beat = target_start


