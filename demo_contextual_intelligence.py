#!/usr/bin/env python3
"""
Demo script for Contextual Intelligence with Visual Feedback

This script demonstrates the new contextual intelligence features that provide
on-demand visual feedback and analysis for musical content.

Usage:
    python demo_contextual_intelligence.py

Features demonstrated:
- Loading MIDI projects for analysis
- Visual feedback for musical elements
- Educational explanations
- Smart suggestions
- Non-intrusive visual display
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from commands.control_plane import ControlPlane
from contextual_intelligence import ContextualIntelligence
from visual_feedback_display import start_visual_feedback, add_visual_feedback_list


def create_sample_midi():
    """Create a sample MIDI file for demonstration."""
    from midi_io import save_midi_file
    
    # Create a simple 8th note pattern with bass and melody
    notes = [
        # Bass line (C2, E2, G2, C2)
        {'pitch': 36, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 0.5, 'track_index': 0},
        {'pitch': 40, 'velocity': 80, 'start_time_seconds': 0.5, 'duration_seconds': 0.5, 'track_index': 0},
        {'pitch': 43, 'velocity': 80, 'start_time_seconds': 1.0, 'duration_seconds': 0.5, 'track_index': 0},
        {'pitch': 36, 'velocity': 80, 'start_time_seconds': 1.5, 'duration_seconds': 0.5, 'track_index': 0},
        
        # Melody line (C4, D4, E4, F4)
        {'pitch': 60, 'velocity': 90, 'start_time_seconds': 0.0, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 62, 'velocity': 90, 'start_time_seconds': 0.25, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 64, 'velocity': 90, 'start_time_seconds': 0.5, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 65, 'velocity': 90, 'start_time_seconds': 0.75, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 67, 'velocity': 90, 'start_time_seconds': 1.0, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 69, 'velocity': 90, 'start_time_seconds': 1.25, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 71, 'velocity': 90, 'start_time_seconds': 1.5, 'duration_seconds': 0.25, 'track_index': 1},
        {'pitch': 72, 'velocity': 90, 'start_time_seconds': 1.75, 'duration_seconds': 0.25, 'track_index': 1},
    ]
    
    # Save the MIDI file
    midi_file = "demo_song.mid"
    save_midi_file(notes, midi_file)
    print(f"Created sample MIDI file: {midi_file}")
    return midi_file


def demonstrate_contextual_intelligence():
    """Demonstrate the contextual intelligence features."""
    print("YesAnd Music - Contextual Intelligence Demo")
    print("=" * 50)
    
    # Create sample MIDI file
    midi_file = create_sample_midi()
    
    # Start visual feedback display
    print("\nStarting visual feedback display...")
    start_visual_feedback()
    time.sleep(1)  # Give the display time to start
    
    # Initialize control plane
    print("\nInitializing control plane...")
    try:
        with ControlPlane() as control_plane:
            print("Control plane initialized successfully!")
            
            # Demonstrate contextual intelligence commands
            print("\n" + "=" * 50)
            print("CONTEXTUAL INTELLIGENCE DEMONSTRATION")
            print("=" * 50)
            
            # Load project
            print(f"\n1. Loading project: {midi_file}")
            response = control_plane.execute(f"load {midi_file}")
            print(f"Response: {response}")
            time.sleep(1)
            
            # Analyze bass
            print("\n2. Analyzing bass line...")
            response = control_plane.execute("analyze bass")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Analyze melody
            print("\n3. Analyzing melody...")
            response = control_plane.execute("analyze melody")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Analyze harmony
            print("\n4. Analyzing harmony...")
            response = control_plane.execute("analyze harmony")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Analyze rhythm
            print("\n5. Analyzing rhythm...")
            response = control_plane.execute("analyze rhythm")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Complete analysis
            print("\n6. Complete analysis...")
            response = control_plane.execute("analyze all")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Get suggestions
            print("\n7. Getting suggestions...")
            response = control_plane.execute("get suggestions")
            print(f"Response: {response}")
            time.sleep(2)
            
            # Show feedback summary
            print("\n8. Showing feedback summary...")
            response = control_plane.execute("show feedback")
            print(f"Response: {response}")
            time.sleep(2)
            
            print("\n" + "=" * 50)
            print("DEMONSTRATION COMPLETE")
            print("=" * 50)
            print("\nThe visual feedback display should show:")
            print("- Color-coded musical element analysis")
            print("- Educational explanations")
            print("- Smart suggestions for improvement")
            print("- Real-time updates as you interact")
            print("\nThis demonstrates the contextual intelligence approach:")
            print("- Background analysis without visual interference")
            print("- On-demand visual feedback for understanding")
            print("- Educational value through explanations")
            print("- Non-intrusive integration with DAW workflows")
            
            # Keep the display running for a bit
            print("\nVisual feedback display will remain open for 10 seconds...")
            time.sleep(10)
            
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(midi_file):
            os.remove(midi_file)
            print(f"\nCleaned up sample file: {midi_file}")


def interactive_demo():
    """Run an interactive demo where users can try commands."""
    print("\n" + "=" * 50)
    print("INTERACTIVE CONTEXTUAL INTELLIGENCE DEMO")
    print("=" * 50)
    print("Try these commands:")
    print("- load [filename] - Load a MIDI file for analysis")
    print("- analyze bass - Analyze the bass line")
    print("- analyze melody - Analyze the melody")
    print("- analyze harmony - Analyze the harmony")
    print("- analyze rhythm - Analyze the rhythm")
    print("- analyze all - Complete analysis")
    print("- get suggestions - Get improvement suggestions")
    print("- show feedback - Show feedback summary")
    print("- clear feedback - Clear visual feedback")
    print("- help - Show all available commands")
    print("- quit - Exit the demo")
    print("\nThe visual feedback display will show the results!")
    
    # Start visual feedback display
    start_visual_feedback()
    time.sleep(1)
    
    try:
        with ControlPlane() as control_plane:
            while True:
                try:
                    command = input("\nYesAnd Music> ").strip()
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if command:
                        response = control_plane.execute(command)
                        print(f"Response: {response}")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error: {e}")
    
    except Exception as e:
        print(f"Error initializing control plane: {e}")


def main():
    """Main demo function."""
    print("YesAnd Music - Contextual Intelligence Demo")
    print("Choose demo mode:")
    print("1. Automated demonstration")
    print("2. Interactive demo")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            demonstrate_contextual_intelligence()
        elif choice == "2":
            interactive_demo()
        else:
            print("Invalid choice. Running automated demonstration...")
            demonstrate_contextual_intelligence()
    
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
