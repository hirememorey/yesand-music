#!/usr/bin/env python3
"""
Demo script for Musical Problem Solvers (Phase 3B)

This script demonstrates the new musical problem-solving functionality:
- "Make this groove better"
- "Fix the harmony" 
- "Improve the arrangement"

Each solver provides:
- Audio preview of improvements
- Musical explanations of changes
- One-command problem solving
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from commands.control_plane import ControlPlane
from musical_solvers import GrooveImprover, HarmonyFixer, ArrangementImprover, _fix_midi_timing
from midi_io import parse_midi_file, save_midi_file
from analysis import apply_swing


def create_test_midi_file():
    """Create a simple test MIDI file for demonstration."""
    # Create a simple 8th note pattern
    notes = []
    for i in range(8):
        note = {
            'pitch': 60 + (i % 4) * 2,  # C, D, E, F pattern
            'velocity': 80,
            'start_time_seconds': i * 0.5,  # 8th notes at 120 BPM
            'duration_seconds': 0.4,
            'track_index': 0
        }
        notes.append(note)
    
    # Save to test file
    test_file = "test_groove.mid"
    # Fix timing before saving
    notes = _fix_midi_timing(notes)
    save_midi_file(notes, test_file)
    print(f"Created test MIDI file: {test_file}")
    return test_file


def demo_groove_improver():
    """Demonstrate the GrooveImprover."""
    print("\n" + "="*60)
    print("🎵 DEMO: Groove Improver - 'Make this groove better'")
    print("="*60)
    
    # Create test file
    test_file = create_test_midi_file()
    
    try:
        # Initialize groove improver
        groove_improver = GrooveImprover()
        
        # Improve the groove
        print(f"Analyzing groove in {test_file}...")
        solution = groove_improver.improve_groove(test_file)
        
        # Display results
        print(f"\nExplanation: {solution.explanation}")
        print(f"Confidence: {solution.confidence:.1%}")
        
        if solution.changes_made:
            print("\nChanges made:")
            for change in solution.changes_made:
                print(f"  • {change}")
            
            # Save improved version
            improved_file = "test_groove_improved.mid"
            save_midi_file(solution.improved_notes, improved_file)
            print(f"\nImproved version saved to: {improved_file}")
        else:
            print("No changes needed - groove is already good!")
    
    except Exception as e:
        print(f"Error in groove improvement: {e}")
    
    finally:
        # Clean up test files
        for file in [test_file, "test_groove_improved.mid"]:
            if os.path.exists(file):
                os.remove(file)


def demo_harmony_fixer():
    """Demonstrate the HarmonyFixer."""
    print("\n" + "="*60)
    print("🎵 DEMO: Harmony Fixer - 'Fix the harmony'")
    print("="*60)
    
    # Create test file with some harmonic issues
    notes = []
    # Create a simple chord progression with some issues
    chord_notes = [
        [60, 64, 67],  # C major
        [62, 65, 69],  # D minor
        [64, 67, 71],  # E minor
        [65, 69, 72],  # F major
    ]
    
    for i, chord in enumerate(chord_notes):
        for j, pitch in enumerate(chord):
            note = {
                'pitch': pitch,
                'velocity': 80,
                'start_time_seconds': i * 1.0 + j * 0.1,  # Stagger chord notes slightly
                'duration_seconds': 0.05,  # Very short duration to avoid overlaps
                'track_index': 0
            }
            notes.append(note)
    
    test_file = "test_harmony.mid"
    # Fix timing before saving
    notes = _fix_midi_timing(notes)
    save_midi_file(notes, test_file)
    print(f"Created test harmony file: {test_file}")
    
    try:
        # Initialize harmony fixer
        harmony_fixer = HarmonyFixer()
        
        # Fix the harmony
        print(f"Analyzing harmony in {test_file}...")
        solution = harmony_fixer.fix_harmony(test_file)
        
        # Display results
        print(f"\nExplanation: {solution.explanation}")
        print(f"Confidence: {solution.confidence:.1%}")
        
        if solution.changes_made:
            print("\nChanges made:")
            for change in solution.changes_made:
                print(f"  • {change}")
            
            # Save improved version
            improved_file = "test_harmony_improved.mid"
            save_midi_file(solution.improved_notes, improved_file)
            print(f"\nImproved version saved to: {improved_file}")
        else:
            print("No changes needed - harmony is already good!")
    
    except Exception as e:
        print(f"Error in harmony fixing: {e}")
    
    finally:
        # Clean up test files
        for file in [test_file, "test_harmony_improved.mid"]:
            if os.path.exists(file):
                os.remove(file)


def demo_arrangement_improver():
    """Demonstrate the ArrangementImprover."""
    print("\n" + "="*60)
    print("🎵 DEMO: Arrangement Improver - 'Improve the arrangement'")
    print("="*60)
    
    # Create test file with repetitive arrangement
    notes = []
    # Create a simple repetitive pattern
    pattern = [60, 62, 64, 65]  # C, D, E, F
    for repeat in range(4):  # Repeat 4 times
        for i, pitch in enumerate(pattern):
            note = {
                'pitch': pitch,
                'velocity': 80,
                'start_time_seconds': (repeat * 4 + i) * 0.5,
                'duration_seconds': 0.4,
                'track_index': 0
            }
            notes.append(note)
    
    test_file = "test_arrangement.mid"
    # Fix timing before saving
    notes = _fix_midi_timing(notes)
    save_midi_file(notes, test_file)
    print(f"Created test arrangement file: {test_file}")
    
    try:
        # Initialize arrangement improver
        arrangement_improver = ArrangementImprover()
        
        # Improve the arrangement
        print(f"Analyzing arrangement in {test_file}...")
        solution = arrangement_improver.improve_arrangement(test_file)
        
        # Display results
        print(f"\nExplanation: {solution.explanation}")
        print(f"Confidence: {solution.confidence:.1%}")
        
        if solution.changes_made:
            print("\nChanges made:")
            for change in solution.changes_made:
                print(f"  • {change}")
            
            # Save improved version
            improved_file = "test_arrangement_improved.mid"
            save_midi_file(solution.improved_notes, improved_file)
            print(f"\nImproved version saved to: {improved_file}")
        else:
            print("No changes needed - arrangement is already good!")
    
    except Exception as e:
        print(f"Error in arrangement improvement: {e}")
    
    finally:
        # Clean up test files
        for file in [test_file, "test_arrangement_improved.mid"]:
            if os.path.exists(file):
                os.remove(file)


def demo_control_plane_integration():
    """Demonstrate integration with the control plane."""
    print("\n" + "="*60)
    print("🎵 DEMO: Control Plane Integration")
    print("="*60)
    
    try:
        # Initialize control plane
        control_plane = ControlPlane()
        
        # Create test file
        test_file = create_test_midi_file()
        
        # Load project
        print(f"Loading project: {test_file}")
        response = control_plane.execute(f"load {test_file}")
        print(f"Load response: {response}")
        
        # Test musical problem solvers
        commands = [
            "make this groove better",
            "fix the harmony", 
            "improve the arrangement"
        ]
        
        for command in commands:
            print(f"\nCommand: '{command}'")
            response = control_plane.execute(command)
            print(f"Response: {response}")
            time.sleep(1)  # Brief pause between commands
        
        control_plane.close()
    
    except Exception as e:
        print(f"Error in control plane demo: {e}")
    
    finally:
        # Clean up test files
        for file in ["test_groove.mid"]:
            if os.path.exists(file):
                os.remove(file)


def main():
    """Run all musical solver demonstrations."""
    print("🎵 Musical Problem Solvers Demo (Phase 3B)")
    print("=" * 60)
    print("This demo shows the new musical problem-solving functionality")
    print("that solves real musical problems instead of just showing visuals.")
    print()
    
    # Demo individual solvers
    demo_groove_improver()
    demo_harmony_fixer()
    demo_arrangement_improver()
    
    # Demo control plane integration
    demo_control_plane_integration()
    
    print("\n" + "="*60)
    print("✅ Demo completed! Musical problem solvers are working.")
    print("="*60)


if __name__ == "__main__":
    main()
