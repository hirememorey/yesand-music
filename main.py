"""
Entry point for the MIDI sequencing demo.

This script demonstrates both the original simple demo and the new control plane.
"""

from __future__ import annotations

import sys
from typing import Optional

import config
from midi_player import MidiPlayer
from sequencer import Sequencer
from theory import create_major_scale


def original_demo() -> None:
    """Original demo: Set up MIDI, create a sequence, and play a C Major scale."""
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


def control_plane_demo() -> None:
    """Demo using the new control plane."""
    print("Control Plane Demo")
    print("=================")
    print()
    print("Available commands:")
    print("  python main.py --demo                    - Run original demo")
    print("  python main.py --control-plane           - Run control plane demo")
    print("  python main.py --interactive             - Start interactive control plane")
    print("  python main.py --help                    - Show help")
    print()
    print("Control plane commands:")
    print("  play scale [KEY] [MODE]                  - Play a scale")
    print("  play arp [KEY] [CHORD]                   - Play an arpeggio")
    print("  play random [COUNT]                      - Play random notes")
    print("  set key to [KEY] [MODE]                  - Set session key")
    print("  set tempo to [BPM]                       - Set tempo")
    print("  set density to [low|med|high]            - Set note density")
    print("  set randomness to [0-1]                  - Set randomness level")
    print("  status                                   - Show current state")
    print("  stop                                     - Stop playback")
    print("  help                                     - Show all commands")
    print()
    print("Examples:")
    print("  python main.py --interactive")
    print("  Then type: 'play scale D minor'")
    print("  Then type: 'set tempo to 140'")
    print("  Then type: 'play arp C major'")


def interactive_mode() -> None:
    """Start interactive control plane mode."""
    try:
        from commands.control_plane import ControlPlane
        
        print("Starting Interactive Control Plane...")
        print("Type 'help' for available commands, 'quit' to exit.")
        print()
        
        with ControlPlane() as control_plane:
            while True:
                try:
                    command = input("> ").strip()
                    if not command:
                        continue
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    result = control_plane.execute(command)
                    print(result)
                    print()
                
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except EOFError:
                    print("\nExiting...")
                    break
    
    except ImportError as e:
        print(f"Error: Could not import control plane: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            original_demo()
        elif sys.argv[1] == "--control-plane":
            control_plane_demo()
        elif sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--help":
            control_plane_demo()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            control_plane_demo()
    else:
        # Default: run original demo
        original_demo()


if __name__ == "__main__":
    main()


