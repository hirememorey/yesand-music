"""
Sequencing and musical timing engine.

The Sequencer collects note events and schedules them in real time using a
provided MidiPlayer and BPM setting.
"""

from __future__ import annotations

import threading
import time
from typing import Dict, List, Optional
from collections import defaultdict

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
        
        # Playback control
        self._stop_event = threading.Event()
        self._playback_thread: Optional[threading.Thread] = None
        self._note_off_timers: Dict[int, threading.Timer] = {}

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
            # Check for stop signal
            if self._stop_event.is_set():
                break
                
            target_start = float(note["start_beat"])
            sleep_beats = target_start - current_beat
            if sleep_beats > 0:
                # Sleep in small increments to allow for stop signal
                sleep_seconds = sleep_beats * self.seconds_per_beat
                sleep_increment = 0.01  # 10ms increments
                while sleep_seconds > 0 and not self._stop_event.is_set():
                    sleep_time = min(sleep_increment, sleep_seconds)
                    time.sleep(sleep_time)
                    sleep_seconds -= sleep_time

            if self._stop_event.is_set():
                break

            duration_seconds = float(note["duration_beats"]) * self.seconds_per_beat
            self.midi_player.send_note(
                pitch=int(note["pitch"]),
                velocity=int(note["velocity"]),
                duration_in_seconds=duration_seconds,
            )

            # Move current time reference to this note's start beat
            current_beat = target_start

    def play_async(self) -> None:
        """Start playback in a background thread.
        
        This allows the sequencer to be stopped while playing.
        """
        if self._playback_thread and self._playback_thread.is_alive():
            self.stop()
        
        self._stop_event.clear()
        self._playback_thread = threading.Thread(target=self._play_non_blocking)
        self._playback_thread.daemon = True
        self._playback_thread.start()
    
    def _play_non_blocking(self) -> None:
        """Non-blocking playback that uses timers for note-off events.
        
        This method triggers notes immediately and schedules note-off events
        using timers, allowing for truly non-blocking playback.
        """
        if not self.notes:
            return

        # Sort notes by start position in beats
        sorted_notes = sorted(self.notes, key=lambda n: n["start_beat"])

        current_beat = 0.0
        for note in sorted_notes:
            # Check for stop signal
            if self._stop_event.is_set():
                break
                
            target_start = float(note["start_beat"])
            sleep_beats = target_start - current_beat
            if sleep_beats > 0:
                # Sleep in small increments to allow for stop signal
                sleep_seconds = sleep_beats * self.seconds_per_beat
                sleep_increment = 0.01  # 10ms increments
                while sleep_seconds > 0 and not self._stop_event.is_set():
                    sleep_time = min(sleep_increment, sleep_seconds)
                    time.sleep(sleep_time)
                    sleep_seconds -= sleep_time

            if self._stop_event.is_set():
                break

            # Send note-on immediately
            pitch = int(note["pitch"])
            velocity = int(note["velocity"])
            self.midi_player.send_note_on(pitch, velocity)
            
            # Schedule note-off with a timer
            duration_seconds = float(note["duration_beats"]) * self.seconds_per_beat
            timer = threading.Timer(duration_seconds, self._note_off_callback, args=[pitch])
            timer.start()
            self._note_off_timers[pitch] = timer

            # Move current time reference to this note's start beat
            current_beat = target_start
    
    def _note_off_callback(self, pitch: int) -> None:
        """Callback for note-off timer.
        
        Args:
            pitch: MIDI note number to turn off
        """
        if not self._stop_event.is_set():
            self.midi_player.send_note_off(pitch)
        # Clean up timer reference
        self._note_off_timers.pop(pitch, None)

    def stop(self) -> None:
        """Stop current playback."""
        self._stop_event.set()
        
        # Cancel all pending note-off timers
        for timer in self._note_off_timers.values():
            timer.cancel()
        self._note_off_timers.clear()
        
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)

    def is_playing(self) -> bool:
        """Check if the sequencer is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        return (self._playback_thread is not None and 
                self._playback_thread.is_alive() and 
                not self._stop_event.is_set())

    def clear(self) -> None:
        """Clear all notes from the sequence."""
        self.notes.clear()
        self.stop()


