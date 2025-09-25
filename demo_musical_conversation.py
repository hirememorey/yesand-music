#!/usr/bin/env python3
"""
Comprehensive Demo Script for Musical Conversation & Problem-Solving System

This demo showcases the complete workflow from context gathering to MIDI sketch generation.
It demonstrates how the system transforms musical problem-solving from technical manipulation
to intelligent conversation.

Key Features Demonstrated:
- Musical Context Interview
- Project State Analysis
- Contextual Suggestion Generation
- MIDI Sketch Generation
- Complete Workflow Integration
"""

import os
import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from musical_context_interview import MusicalContextInterview
from project_state_analyzer import ProjectStateAnalyzer
from musical_conversation_engine import MusicalConversationEngine
from midi_sketch_generator import MIDISketchGenerator
from musical_conversation_cli import MusicalConversationCLI


def print_section(title, description=""):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"🎵 {title}")
    print("="*60)
    if description:
        print(description)
    print()


def print_step(step_num, title, description=""):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {title}")
    print("-" * 40)
    if description:
        print(description)
    print()


def demo_context_interview():
    """Demo the Musical Context Interview system"""
    print_section("Musical Context Interview Demo", 
                 "This demonstrates how the system guides users through describing their musical context step-by-step.")
    
    interview = MusicalContextInterview()
    
    print("Starting the musical context interview...")
    print(interview.start_interview())
    
    # Simulate user answers
    answers = [
        ("song_concept", "A song about leaders who shoot the messenger instead of fixing problems"),
        ("key_signature", "G minor"),
        ("tempo", "120"),
        ("time_signature", "4/4"),
        ("existing_parts", "DX7 bass line, Dexed whistle effect, fuzz guitar"),
        ("musical_problem", "I need help with a bridge that makes sense"),
        ("style_preferences", "Grunge, Alice in Chains, Soundgarden"),
        ("emotional_intent", "Dark, aggressive, confrontational")
    ]
    
    print_step(1, "Answering Interview Questions")
    
    for question_id, answer in answers:
        question = interview.get_next_question()
        if question:
            print(f"❓ {question.question_text}")
            if question.examples:
                print(f"   Examples: {', '.join(question.examples)}")
            print(f"💬 User: {answer}")
            
            success, message = interview.answer_question(question_id, answer)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
            print()
    
    print_step(2, "Context Summary")
    print(interview.get_context_summary())
    
    print_step(3, "AI Context Format")
    context_data = interview.get_context_for_ai()
    print("Context data for AI processing:")
    for key, value in context_data.items():
        print(f"  {key}: {value}")
    
    return interview.current_context


def demo_project_analysis():
    """Demo the Project State Analyzer"""
    print_section("Project State Analysis Demo",
                 "This demonstrates how the system analyzes existing DAW projects to extract musical context.")
    
    analyzer = ProjectStateAnalyzer()
    
    print_step(1, "Looking for MIDI Files")
    
    # Look for MIDI files in current directory
    current_dir = Path(".")
    midi_files = list(current_dir.glob("*.mid")) + list(current_dir.glob("*.midi"))
    
    if not midi_files:
        print("No MIDI files found in current directory.")
        print("Creating a sample MIDI file for demonstration...")
        
        # Create a simple sample MIDI file
        import mido
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)
        
        # Add tempo
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
        
        # Add time signature
        track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
        
        # Add some notes (C major chord)
        track.append(mido.Message('note_on', channel=0, note=60, velocity=80, time=0))
        track.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
        track.append(mido.Message('note_on', channel=0, note=67, velocity=80, time=0))
        
        track.append(mido.Message('note_off', channel=0, note=60, velocity=0, time=480))
        track.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=0))
        track.append(mido.Message('note_off', channel=0, note=67, velocity=0, time=0))
        
        # Save sample file
        sample_file = "sample_demo.mid"
        midi_file.save(sample_file)
        midi_files = [Path(sample_file)]
        print(f"Created sample file: {sample_file}")
    
    # Analyze the first MIDI file
    midi_file = midi_files[0]
    print(f"Analyzing: {midi_file}")
    
    try:
        project_state = analyzer.analyze_project(str(midi_file))
        
        print_step(2, "Project Analysis Results")
        print(analyzer.get_context_summary(project_state))
        
        print_step(3, "AI Context Format")
        context_data = analyzer.get_context_for_ai(project_state)
        print("Project context data for AI processing:")
        for key, value in context_data.items():
            if key != "tracks":  # Skip tracks for brevity
                print(f"  {key}: {value}")
        
        return project_state
        
    except Exception as e:
        print(f"❌ Error analyzing project: {e}")
        return None


def demo_conversation_engine():
    """Demo the Musical Conversation Engine"""
    print_section("Musical Conversation Engine Demo",
                 "This demonstrates how the system combines project state and user input for contextual suggestions.")
    
    engine = MusicalConversationEngine()
    
    print_step(1, "Starting Conversation")
    print(engine.start_conversation())
    
    print_step(2, "Simulating User Input")
    
    # Simulate conversation
    user_inputs = [
        "My song is about leaders who shoot the messenger instead of fixing problems",
        "I need help with a bridge that makes sense",
        "The key is G minor and tempo is 120 BPM",
        "I have a DX7 bass line and fuzz guitar",
        "I'm going for a grungy, aggressive sound"
    ]
    
    for user_input in user_inputs:
        print(f"💬 User: {user_input}")
        response = engine.process_user_input(user_input)
        print(f"🤖 AI: {response}")
        print()
    
    print_step(3, "Context Summary")
    print(engine.get_context_summary())
    
    print_step(4, "Generating Musical Suggestions")
    suggestions = engine._generate_musical_suggestions("")
    
    if suggestions:
        print("Generated suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion.title}")
            print(f"     {suggestion.description}")
            print(f"     Confidence: {suggestion.confidence_score:.1%}")
            print()
    else:
        print("No suggestions generated (need more context)")
    
    return engine, suggestions


def demo_midi_sketch_generation(suggestions):
    """Demo the MIDI Sketch Generator"""
    print_section("MIDI Sketch Generation Demo",
                 "This demonstrates how the system generates quick MIDI sketches for testing suggestions.")
    
    generator = MIDISketchGenerator()
    
    print_step(1, "Generating Sketches for Suggestions")
    
    if not suggestions:
        print("No suggestions available. Creating sample suggestions...")
        suggestions = [
            type('MockSuggestion', (), {
                'suggestion_type': 'chord_progression',
                'title': 'Sample Chord Progression',
                'description': 'A sample chord progression for testing'
            }),
            type('MockSuggestion', (), {
                'suggestion_type': 'melody',
                'title': 'Sample Melody',
                'description': 'A sample melody for testing'
            }),
            type('MockSuggestion', (), {
                'suggestion_type': 'bass_line',
                'title': 'Sample Bass Line',
                'description': 'A sample bass line for testing'
            })
        ]
    
    sketches = []
    
    for i, suggestion in enumerate(suggestions[:3], 1):  # Limit to 3 for demo
        print(f"Generating sketch for: {suggestion.title}")
        
        sketch = generator.generate_sketch(
            suggestion_type=suggestion.suggestion_type,
            key_signature="G minor",
            tempo=120,
            duration_bars=4
        )
        
        print(f"  ✅ Generated: {sketch.title}")
        print(f"     Duration: {sketch.duration_seconds:.1f}s")
        print(f"     Tracks: {sketch.track_count}")
        print(f"     Notes: {len(sketch.midi_data)}")
        
        # Save the sketch
        filename = f"demo_sketch_{i}_{suggestion.suggestion_type}.mid"
        filepath = generator.save_sketch(sketch, filename)
        print(f"     Saved to: {filepath}")
        
        sketches.append(sketch)
        print()
    
    print_step(2, "Generating Multiple Variations")
    
    # Generate multiple variations of the same suggestion
    variations = generator.generate_multiple_sketches(
        suggestion_type="chord_progression",
        key_signature="G minor",
        tempo=120,
        count=3
    )
    
    print(f"Generated {len(variations)} variations:")
    for i, sketch in enumerate(variations, 1):
        print(f"  {i}. {sketch.title}")
        print(f"     Duration: {sketch.duration_seconds:.1f}s")
        print(f"     Notes: {len(sketch.midi_data)}")
    
    return sketches


def demo_complete_workflow():
    """Demo the complete workflow integration"""
    print_section("Complete Workflow Demo",
                 "This demonstrates the complete workflow from context gathering to MIDI sketch generation.")
    
    cli = MusicalConversationCLI()
    
    print_step(1, "Starting Complete Workflow")
    
    # Start conversation
    print(cli.conversation_engine.start_conversation())
    
    print_step(2, "Simulating Complete Conversation")
    
    # Simulate a complete conversation
    conversation_steps = [
        "My song is about leaders who shoot the messenger instead of fixing problems",
        "I need help with a bridge that makes sense",
        "The key is G minor and tempo is 120 BPM",
        "I have a DX7 bass line and fuzz guitar",
        "I'm going for a grungy, aggressive sound"
    ]
    
    for step in conversation_steps:
        print(f"💬 User: {step}")
        response = cli.conversation_engine.process_user_input(step)
        print(f"🤖 AI: {response}")
        print()
    
    print_step(3, "Generating Suggestions")
    cli._generate_and_show_suggestions()
    
    print_step(4, "Generating MIDI Sketches")
    if cli.current_suggestions:
        print("Generating sketches for all suggestions...")
        cli._handle_test_command("test all")
    
    print_step(5, "Final Status")
    cli._show_status()
    
    print_step(6, "Generated Files")
    print("MIDI sketches generated:")
    for sketch in cli.current_sketches:
        print(f"  - {sketch.title}")
        print(f"    Duration: {sketch.duration_seconds:.1f}s")
        print(f"    Tracks: {sketch.track_count}")


def demo_cli_commands():
    """Demo the CLI command system"""
    print_section("CLI Commands Demo",
                 "This demonstrates the available CLI commands and their usage.")
    
    cli = MusicalConversationCLI()
    
    print_step(1, "Available Commands")
    cli._show_help()
    
    print_step(2, "Command Examples")
    
    # Demo status command
    print("Status command:")
    cli._show_status()
    
    # Demo context command
    print("\nContext command:")
    cli._show_context()
    
    # Demo suggestions command
    print("\nSuggestions command:")
    cli._show_suggestions()
    
    # Demo sketches command
    print("\nSketches command:")
    cli._show_sketches()


def main():
    """Main demo function"""
    print("🎵 Musical Conversation & Problem-Solving System")
    print("=" * 60)
    print("Comprehensive Demo Script")
    print("=" * 60)
    
    print("\nThis demo showcases the complete workflow from context gathering to MIDI sketch generation.")
    print("It demonstrates how the system transforms musical problem-solving from technical manipulation")
    print("to intelligent conversation.")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set. Some features may not work properly.")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    try:
        # Run all demos
        print("Starting demos...")
        
        # Demo 1: Context Interview
        user_context = demo_context_interview()
        
        # Demo 2: Project Analysis
        project_state = demo_project_analysis()
        
        # Demo 3: Conversation Engine
        engine, suggestions = demo_conversation_engine()
        
        # Demo 4: MIDI Sketch Generation
        sketches = demo_midi_sketch_generation(suggestions)
        
        # Demo 5: Complete Workflow
        demo_complete_workflow()
        
        # Demo 6: CLI Commands
        demo_cli_commands()
        
        print_section("Demo Complete!",
                     "All demos completed successfully. The system is ready for use.")
        
        print("🎉 Key Features Demonstrated:")
        print("  ✅ Musical Context Interview - Guided context gathering")
        print("  ✅ Project State Analysis - Automatic DAW project analysis")
        print("  ✅ Contextual Suggestions - AI suggestions based on complete context")
        print("  ✅ MIDI Sketch Generation - Quick testing of musical ideas")
        print("  ✅ Complete Workflow - End-to-end musical problem solving")
        print("  ✅ CLI Interface - Easy-to-use command-line interface")
        
        print("\n🚀 Ready to Start Musical Conversations!")
        print("Run: python musical_conversation_cli.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
