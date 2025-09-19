"""
MIDI I/O module.

This module provides the MidiPlayer class, which wraps mido's output port
to send MIDI note messages to a virtual MIDI device (e.g., GarageBand via IAC on macOS).
"""

from __future__ import annotations

import time
from typing import Optional

import mido


class MidiPlayer:
    """High-level MIDI output helper using mido.

    Responsible for opening a MIDI output port and sending note on/off messages.
    """

    def __init__(self, port_name: str) -> None:
        """Attempt to open the given MIDI output port.

        If the port cannot be opened, an error is printed along with a list of
        available output ports. The opened port is stored on the instance.
        """

        self.port_name: str = port_name
        self.port: Optional[mido.ports.BaseOutput] = None
        try:
            self.port = mido.open_output(self.port_name)
        except Exception as exc:  # Broad to capture platform-specific errors
            available = mido.get_output_names()
            print(
                "Failed to open MIDI port '" + self.port_name + "'.\n"
                + "Available output ports: " + ", ".join(available)
            )
            print("Underlying error:", exc)

    def send_note(self, pitch: int, velocity: int, duration_in_seconds: float) -> None:
        """Send a note-on, wait duration, then send note-off.

        Args:
            pitch: MIDI note number (0-127)
            velocity: MIDI velocity (0-127)
            duration_in_seconds: Time to hold the note before sending note-off
        """
        if self.port is None:
            return

        self.port.send(mido.Message("note_on", note=int(pitch), velocity=int(velocity)))
        time.sleep(max(0.0, float(duration_in_seconds)))
        self.port.send(mido.Message("note_off", note=int(pitch), velocity=0))
    
    def send_note_on(self, pitch: int, velocity: int) -> None:
        """Send a note-on message immediately.
        
        Args:
            pitch: MIDI note number (0-127)
            velocity: MIDI velocity (0-127)
        """
        if self.port is None:
            return
        self.port.send(mido.Message("note_on", note=int(pitch), velocity=int(velocity)))
    
    def send_note_off(self, pitch: int) -> None:
        """Send a note-off message immediately.
        
        Args:
            pitch: MIDI note number (0-127)
        """
        if self.port is None:
            return
        self.port.send(mido.Message("note_off", note=int(pitch), velocity=0))

    def close(self) -> None:
        """Close the MIDI output port if open."""
        if self.port is not None:
            try:
                self.port.close()
            finally:
                self.port = None


