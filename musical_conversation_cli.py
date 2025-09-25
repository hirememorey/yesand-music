#!/usr/bin/env python3
"""
Musical Conversation CLI

This is the main CLI interface for the Musical Conversation & Problem-Solving System.
It combines the context interview, project analysis, conversation engine, and MIDI sketch generation.

Key Features:
- Interactive musical conversation
- Dual context sources (project state + user input)
- Rapid MIDI sketch generation for testing
- Contextual musical suggestions
- Seamless workflow integration
"""

import argparse
import json
import os
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path

from musical_context_interview import MusicalContextInterview
from project_state_analyzer import ProjectStateAnalyzer
from musical_conversation_engine import MusicalConversationEngine, MusicalSuggestion
from midi_sketch_generator import MIDISketchGenerator


class MusicalConversationCLI:
    """Main CLI interface for musical conversation system"""
    
    def __init__(self):
        self.conversation_engine = MusicalConversationEngine()
        self.sketch_generator = MIDISketchGenerator()
        self.project_analyzer = ProjectStateAnalyzer()
        self.context_interview = MusicalContextInterview()
        
        self.current_project_path = None
        self.current_suggestions = []
        self.current_sketches = []
    
    def start_interactive_mode(self, project_path: Optional[str] = None):
        """Start interactive conversation mode"""
        print("🎵 Musical Conversation & Problem-Solving System")
        print("=" * 60)
        
        # Start conversation
        print(self.conversation_engine.start_conversation(project_path))
        
        if project_path:
            self.current_project_path = project_path
            print(f"📁 Project loaded: {project_path}")
        
        print("\nType 'help' for available commands, 'quit' to exit.")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n🎵 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy music making!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.lower() == 'status':
                    self._show_status()
                elif user_input.lower() == 'suggestions':
                    self._show_suggestions()
                elif user_input.lower() == 'sketches':
                    self._show_sketches()
                elif user_input.lower() == 'context':
                    self._show_context()
                elif user_input.lower().startswith('generate '):
                    self._handle_generate_command(user_input)
                elif user_input.lower().startswith('test '):
                    self._handle_test_command(user_input)
                elif user_input.lower().startswith('load '):
                    self._handle_load_command(user_input)
                else:
                    # Process as conversation input
                    response = self.conversation_engine.process_user_input(user_input)
                    print(f"🤖 AI: {response}")
                    
                    # Check if we should generate suggestions
                    if self._should_generate_suggestions(user_input):
                        self._generate_and_show_suggestions()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Happy music making!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
🎵 Available Commands:

Conversation:
  - Just type your musical questions or problems
  - "I need help with a bridge"
  - "My song is about..."
  - "What key should I use?"

Project Management:
  load <path>     - Load a DAW project for analysis
  context         - Show current musical context
  status          - Show system status

Suggestions:
  suggestions     - Show current musical suggestions
  generate <type> - Generate specific type of suggestion
  test <id>       - Generate MIDI sketch for suggestion

Sketches:
  sketches        - Show generated MIDI sketches
  test all        - Generate sketches for all suggestions

System:
  help            - Show this help
  quit            - Exit the system
        """
        print(help_text)
    
    def _show_status(self):
        """Show current system status"""
        print("\n📊 System Status:")
        print("-" * 30)
        
        # Conversation status
        if self.conversation_engine.conversation_context:
            progress = self.context_interview.get_progress()
            print(f"🎵 Context Interview: {progress[0]}/{progress[1]} questions answered")
            
            if self.conversation_engine.conversation_context.project_state:
                print(f"📁 Project: {self.current_project_path}")
            else:
                print("📁 Project: None loaded")
        else:
            print("🎵 Context Interview: Not started")
        
        # Suggestions status
        print(f"💡 Suggestions: {len(self.current_suggestions)} available")
        print(f"🎼 Sketches: {len(self.current_sketches)} generated")
    
    def _show_context(self):
        """Show current musical context"""
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical problem.")
            return
        
        print("\n🎵 Current Musical Context:")
        print("-" * 40)
        print(self.conversation_engine.get_context_summary())
    
    def _show_suggestions(self):
        """Show current musical suggestions"""
        if not self.current_suggestions:
            print("❌ No suggestions available. Ask me about a musical problem first!")
            return
        
        print("\n💡 Current Musical Suggestions:")
        print("-" * 40)
        
        for i, suggestion in enumerate(self.current_suggestions, 1):
            print(f"{i}. {suggestion.title}")
            print(f"   {suggestion.description}")
            print(f"   Confidence: {suggestion.confidence_score:.1%}")
            print(f"   Type: {suggestion.suggestion_type}")
            print()
    
    def _show_sketches(self):
        """Show generated MIDI sketches"""
        if not self.current_sketches:
            print("❌ No sketches generated. Use 'test <suggestion_id>' to generate sketches.")
            return
        
        print("\n🎼 Generated MIDI Sketches:")
        print("-" * 40)
        
        for i, sketch in enumerate(self.current_sketches, 1):
            print(f"{i}. {sketch.title}")
            print(f"   {sketch.description}")
            print(f"   Duration: {sketch.duration_seconds:.1f}s")
            print(f"   Tracks: {sketch.track_count}")
            print(f"   File: {sketch.sketch_id}.mid")
            print()
    
    def _should_generate_suggestions(self, user_input: str) -> bool:
        """Check if we should generate suggestions based on user input"""
        suggestion_triggers = [
            'suggest', 'help with', 'what should', 'how can i',
            'i need help', 'i can\'t figure out', 'bridge', 'chorus',
            'verse', 'intro', 'outro', 'chord', 'melody', 'bass'
        ]
        
        user_input_lower = user_input.lower()
        return any(trigger in user_input_lower for trigger in suggestion_triggers)
    
    def _generate_and_show_suggestions(self):
        """Generate and show musical suggestions"""
        if not self.conversation_engine.conversation_context:
            return
        
        # Generate suggestions
        suggestions = self.conversation_engine._generate_musical_suggestions("")
        self.current_suggestions = suggestions
        
        if suggestions:
            print("\n💡 I've generated some musical suggestions for you:")
            print("-" * 50)
            
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion.title}")
                print(f"   {suggestion.description}")
                print(f"   Confidence: {suggestion.confidence_score:.1%}")
                print()
            
            print("Use 'test <number>' to generate a MIDI sketch for testing.")
        else:
            print("❌ I need more context to generate suggestions. Tell me more about your song!")
    
    def _handle_generate_command(self, command: str):
        """Handle generate command"""
        parts = command.split()
        if len(parts) < 2:
            print("❌ Usage: generate <type>")
            print("Types: chord_progression, melody, bass_line, bridge, intro, rhythm_pattern")
            return
        
        suggestion_type = parts[1].lower()
        valid_types = ['chord_progression', 'melody', 'bass_line', 'bridge', 'intro', 'rhythm_pattern']
        
        if suggestion_type not in valid_types:
            print(f"❌ Invalid type. Valid types: {', '.join(valid_types)}")
            return
        
        # Generate suggestion
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical problem.")
            return
        
        # Create a mock suggestion
        suggestion = MusicalSuggestion(
            suggestion_id="generated",
            title=f"{suggestion_type.replace('_', ' ').title()} Suggestion",
            description=f"Generated {suggestion_type} based on your context",
            musical_reasoning="Generated based on your musical context and preferences",
            implementation_notes="Use this as a starting point and modify as needed",
            confidence_score=0.8,
            suggestion_type=suggestion_type
        )
        
        self.current_suggestions = [suggestion]
        
        print(f"✅ Generated {suggestion_type} suggestion!")
        print(f"   {suggestion.description}")
        print("   Use 'test 1' to generate a MIDI sketch for testing.")
    
    def _handle_test_command(self, command: str):
        """Handle test command"""
        parts = command.split()
        if len(parts) < 2:
            print("❌ Usage: test <suggestion_number> or test all")
            return
        
        if parts[1].lower() == 'all':
            # Generate sketches for all suggestions
            if not self.current_suggestions:
                print("❌ No suggestions available. Generate some suggestions first.")
                return
            
            self.current_sketches = []
            for i, suggestion in enumerate(self.current_suggestions):
                sketch = self._generate_sketch_for_suggestion(suggestion, i + 1)
                if sketch:
                    self.current_sketches.append(sketch)
            
            print(f"✅ Generated {len(self.current_sketches)} MIDI sketches!")
            print("Use 'sketches' to see all generated sketches.")
        
        else:
            # Generate sketch for specific suggestion
            try:
                suggestion_num = int(parts[1])
                if suggestion_num < 1 or suggestion_num > len(self.current_suggestions):
                    print(f"❌ Invalid suggestion number. Available: 1-{len(self.current_suggestions)}")
                    return
                
                suggestion = self.current_suggestions[suggestion_num - 1]
                sketch = self._generate_sketch_for_suggestion(suggestion, suggestion_num)
                
                if sketch:
                    print(f"✅ Generated MIDI sketch for suggestion {suggestion_num}!")
                    print(f"   File: {sketch.sketch_id}.mid")
                    print("   Use 'sketches' to see all generated sketches.")
                
            except ValueError:
                print("❌ Invalid suggestion number. Use a number or 'all'.")
    
    def _generate_sketch_for_suggestion(self, suggestion: MusicalSuggestion, number: int) -> Optional[Any]:
        """Generate a MIDI sketch for a suggestion"""
        try:
            # Get context for sketch generation
            context = self.conversation_engine.conversation_context
            if not context:
                return None
            
            # Get parameters from context
            key = context.user_context.key_signature or "C major"
            tempo = context.user_context.tempo or 120
            
            # Generate sketch
            sketch = self.sketch_generator.generate_sketch(
                suggestion_type=suggestion.suggestion_type,
                key_signature=key,
                tempo=tempo,
                duration_bars=4
            )
            
            # Update title
            sketch.title = f"{suggestion.title} (Sketch {number})"
            
            # Save sketch
            filename = f"{suggestion.suggestion_type}_{number}_{sketch.sketch_id[:8]}.mid"
            filepath = self.sketch_generator.save_sketch(sketch, filename)
            
            print(f"   Saved to: {filepath}")
            
            return sketch
            
        except Exception as e:
            print(f"❌ Error generating sketch: {e}")
            return None
    
    def _handle_load_command(self, command: str):
        """Handle load command"""
        parts = command.split()
        if len(parts) < 2:
            print("❌ Usage: load <project_path>")
            return
        
        project_path = parts[1]
        
        try:
            # Analyze project
            project_state = self.project_analyzer.analyze_project(project_path)
            
            # Update conversation context
            if self.conversation_engine.conversation_context:
                self.conversation_engine.conversation_context.project_state = project_state
            
            self.current_project_path = project_path
            
            print(f"✅ Project loaded: {project_path}")
            print("\n📊 Project Analysis:")
            print(self.project_analyzer.get_context_summary(project_state))
            
        except Exception as e:
            print(f"❌ Error loading project: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Musical Conversation & Problem-Solving System")
    parser.add_argument("--project", "-p", help="Path to DAW project file to analyze")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--demo", "-d", action="store_true", help="Run demo")
    
    args = parser.parse_args()
    
    cli = MusicalConversationCLI()
    
    if args.demo:
        # Run demo
        print("🎵 Running Musical Conversation System Demo")
        print("=" * 50)
        
        # Demo context interview
        print("\n1. Context Interview Demo:")
        print("-" * 30)
        interview = MusicalContextInterview()
        print(interview.start_interview())
        
        # Demo project analyzer
        print("\n2. Project Analysis Demo:")
        print("-" * 30)
        analyzer = ProjectStateAnalyzer()
        try:
            # Look for MIDI files
            midi_files = list(Path(".").glob("*.mid")) + list(Path(".").glob("*.midi"))
            if midi_files:
                project_state = analyzer.analyze_project(str(midi_files[0]))
                print(analyzer.get_context_summary(project_state))
            else:
                print("No MIDI files found for demo")
        except Exception as e:
            print(f"Demo error: {e}")
        
        # Demo sketch generator
        print("\n3. MIDI Sketch Generation Demo:")
        print("-" * 30)
        generator = MIDISketchGenerator()
        sketch = generator.generate_sketch("chord_progression", "G minor", 120)
        print(f"Generated: {sketch.title}")
        print(f"Duration: {sketch.duration_seconds:.1f}s")
        print(f"Notes: {len(sketch.midi_data)}")
        
    elif args.interactive or not any([args.project, args.demo]):
        # Start interactive mode
        cli.start_interactive_mode(args.project)
    
    else:
        print("Use --interactive to start interactive mode or --demo to run demo")


if __name__ == "__main__":
    main()
