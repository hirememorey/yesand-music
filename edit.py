#!/usr/bin/env python3
"""
YesAnd Music - Semantic MIDI Editor (Phase 1: Manual Roundtrip MVP)

A command-line tool for applying musical transformations to MIDI files.
This is the "Brain" component of the YesAnd Music architecture.

Usage:
    python edit.py --input input.mid --output output.mid --command "apply swing"
    python edit.py --input song.mid --output swung.mid --command "make it jazzier"
"""

import argparse
import sys
from pathlib import Path
from midi_io import parse_midi_file, save_midi_file
from analysis import apply_swing


def resolve_overlaps(notes_data):
    """
    Resolve overlapping notes by truncating earlier notes when they overlap with later ones.
    
    This is a simple strategy that preserves the musical intent while ensuring MIDI format
    compatibility. More sophisticated strategies could be implemented later.
    
    Args:
        notes_data (list): List of note dictionaries sorted by start_time_seconds
        
    Returns:
        list: New list with overlaps resolved
    """
    if not notes_data:
        return notes_data
    
    resolved_notes = []
    
    for i, note in enumerate(notes_data):
        # Create a copy to avoid modifying the original
        new_note = note.copy()
        
        # Check if this note overlaps with the next note
        if i < len(notes_data) - 1:
            next_note = notes_data[i + 1]
            current_end = note['start_time_seconds'] + note['duration_seconds']
            next_start = next_note['start_time_seconds']
            
            # If there's an overlap, truncate this note
            if current_end > next_start:
                new_duration = next_start - note['start_time_seconds']
                if new_duration > 0:
                    new_note['duration_seconds'] = new_duration
                else:
                    # If the overlap is complete, skip this note
                    continue
        
        resolved_notes.append(new_note)
    
    return resolved_notes


def main():
    """Main entry point for the semantic MIDI editor."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="YesAnd Music - Semantic MIDI Editor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python edit.py --input song.mid --output swung.mid --command "apply swing"
  python edit.py --input track.mid --output jazz.mid --command "make it jazzier"
  python edit.py --input input.mid --output output.mid --command "add accent"
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to the input MIDI file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Path for the output MIDI file'
    )
    
    parser.add_argument(
        '--command', '-c',
        type=str,
        required=True,
        help='Transformation command (e.g., "apply swing", "make it jazzier")'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.mid':
        print(f"Error: Input file '{args.input}' is not a MIDI file (.mid extension required).")
        sys.exit(1)
    
    # Validate output directory exists
    output_path = Path(args.output)
    output_dir = output_path.parent
    if not output_dir.exists():
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
    
    # Print the arguments received
    print("YesAnd Music - Semantic MIDI Editor")
    print("=" * 40)
    print(f"Input file:  {args.input}")
    print(f"Output file: {args.output}")
    print(f"Command:     {args.command}")
    print("=" * 40)
    
    try:
        # Load the MIDI file
        print("Loading MIDI file...")
        notes_data = parse_midi_file(args.input)
        print(f"File loaded: {len(notes_data)} notes found")
        
        # Apply transformation based on command
        if args.command == "apply_swing":
            print("Applying transformation: Swing")
            notes_data = apply_swing(notes_data)
        else:
            print(f"Error: Unknown command '{args.command}'")
            print("Available commands: apply_swing")
            sys.exit(1)
        
        # Sort notes by start time to ensure chronological order for MIDI format
        print("Sorting notes by start time...")
        notes_data.sort(key=lambda note: note['start_time_seconds'])
        
        # Resolve overlaps that might have been created by transformations
        print("Resolving overlaps...")
        notes_data = resolve_overlaps(notes_data)
        
        # Save the MIDI file
        print("Saving MIDI file...")
        save_midi_file(args.output, notes_data)
        print("File saved successfully")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
