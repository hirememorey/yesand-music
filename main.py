"""
Entry point for the MIDI sequencing demo.

Generates a C Major scale and schedules it for playback using the Sequencer
and MidiPlayer components.
"""

from __future__ import annotations

from typing import Optional

import config
from midi_player import MidiPlayer
from sequencer import Sequencer
from theory import create_major_scale


def main() -> None:
    """Set up MIDI, create a sequence, and play a C Major scale."""
    midi_player = MidiPlayer(config.MIDI_PORT_NAME)
    if midi_player.port is None:
        # Could not open port; abort gracefully after informing the user.
        return

    seq = Sequencer(midi_player=midi_player, bpm=config.BPM)

    # Build a C Major scale starting from MIDI note 60 (C4)
    scale_notes = create_major_scale(60)

    # Quarter-note sequence: notes start on beats 0, 1, 2, ...
    for index, note in enumerate(scale_notes):
        seq.add_note(pitch=note, velocity=90, start_beat=float(index), duration_beats=1.0)

    print("Playing C Major Scale...")
    try:
        seq.play()
    finally:
        midi_player.close()


if __name__ == "__main__":
    main()


