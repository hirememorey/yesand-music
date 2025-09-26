#!/usr/bin/env python3
"""
Enhanced Musical Conversation CLI

This is the main CLI interface for the Enhanced Musical Conversation System.
It integrates intent discovery, creative enhancement, and prompt generation
through natural musical conversation.

Key Features:
- Natural musical conversation flow
- Intent discovery through dialogue
- Creative enhancement suggestions
- Context-aware prompt generation
- Seamless workflow integration
"""

import argparse
import json
import os
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path

from enhanced_musical_conversation_engine import EnhancedMusicalConversationEngine, MusicalSuggestion


class EnhancedMusicalConversationCLI:
    """Main CLI interface for enhanced musical conversation system"""
    
    def __init__(self):
        self.conversation_engine = EnhancedMusicalConversationEngine()
        self.current_project_path = None
        self.current_suggestions = []
        self.current_prompt = None
    
    def safe_input(self, prompt: str) -> Optional[str]:
        """Safely get user input with EOF error handling"""
        try:
            return input(prompt).strip()
        except EOFError:
            print("\n❌ Error: EOF when reading input. This environment doesn't support interactive input.")
            print("💡 Try using the demo mode instead: python enhanced_musical_conversation_cli.py --demo")
            return None
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Happy music making!")
            return None

    def start_interactive_mode(self, project_path: Optional[str] = None, initial_input: str = None):
        """Start interactive conversation mode with EOF handling"""
        print("🎵 Enhanced Musical Conversation System")
        print("=" * 60)
        
        # Start conversation
        print(self.conversation_engine.start_conversation(project_path, initial_input))
        
        if project_path:
            self.current_project_path = project_path
            print(f"📁 Project loaded: {project_path}")
        
        print("\nType 'help' for available commands, 'quit' to exit.")
        print("-" * 60)
        
        while True:
            try:
                user_input = self.safe_input("\n🎵 You: ")
                
                if user_input is None:  # EOF or KeyboardInterrupt
                    break
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy music making!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.lower() == 'status':
                    self._show_status()
                elif user_input.lower() == 'suggestions':
                    self._show_suggestions()
                elif user_input.lower() == 'context':
                    self._show_context()
                elif user_input.lower() == 'discovery':
                    self._show_discovery_summary()
                elif user_input.lower() == 'enhancements':
                    self._show_enhancements()
                elif user_input.lower() == 'prompt':
                    self._show_prompt()
                elif user_input.lower().startswith('generate '):
                    self._handle_generate_command(user_input)
                elif user_input.lower().startswith('enhance '):
                    self._handle_enhance_command(user_input)
                else:
                    # Process as conversation input
                    response = self.conversation_engine.process_user_input(user_input)
                    print(f"🤖 AI: {response}")
                    
                    # Check if we should generate suggestions
                    if self._should_generate_suggestions(user_input):
                        self._generate_and_show_suggestions()
                
            except Exception as e:
                print(f"❌ Error: {e}")
                break
    
    def start_demo_mode(self, project_path: Optional[str] = None):
        """Start demo mode with simulated conversation"""
        print("🎵 Enhanced Musical Conversation System - Demo Mode")
        print("=" * 60)
        
        # Start conversation
        print(self.conversation_engine.start_conversation(project_path, "I'm working on a jazz piece"))
        
        if project_path:
            self.current_project_path = project_path
            print(f"📁 Project loaded: {project_path}")
        
        print("\n🎵 Running simulated conversation...")
        print("-" * 40)
        
        # Simulate a conversation
        demo_responses = [
            "It's in G minor at 120 BPM",
            "I want a mysterious, dark sound like Miles Davis",
            "Swung eighths for the rhythm",
            "Jazz sevenths for the harmony",
            "A sparse, ascending melody that builds tension"
        ]
        
        for response in demo_responses:
            print(f"\n🎵 You: {response}")
            result = self.conversation_engine.process_user_input(response)
            print(f"🤖 AI: {result}")
        
        print("\n🎵 Testing suggestion generation...")
        print("-" * 40)
        
        # Test suggestion generation
        suggestions = self.conversation_engine.get_musical_suggestions()
        if suggestions:
            print("💡 Generated musical suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion.title}")
                print(f"   {suggestion.description}")
                print(f"   Confidence: {suggestion.confidence_score:.1%}")
                print()
        
        print("\n🎵 Testing prompt generation...")
        print("-" * 40)
        
        # Test prompt generation
        prompt = self.conversation_engine.generate_midi_prompt("4-bar", "rhythm and harmony")
        print("🎼 Generated MIDI prompt:")
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
        
        print("\n🎉 Demo Complete!")
        print("The Enhanced Musical Conversation System is working correctly!")
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
🎵 Available Commands:

Conversation:
  - Just type your musical ideas and questions
  - "I'm working on a jazz piece"
  - "I want a mysterious sound"
  - "Swung eighths for the rhythm"

Discovery:
  discovery        - Show intent discovery summary
  context          - Show current musical context
  status           - Show system status

Suggestions:
  suggestions      - Show current musical suggestions
  enhancements     - Show creative enhancement suggestions
  generate <type>  - Generate specific type of suggestion

Generation:
  prompt           - Show generated MIDI prompt
  enhance <level>  - Apply creative enhancements (low/medium/high)

System:
  help             - Show this help
  quit             - Exit the system
        """
        print(help_text)
    
    def _show_status(self):
        """Show current system status"""
        print("\n📊 System Status:")
        print("-" * 30)
        
        # Discovery status
        if self.conversation_engine.conversation_context:
            if self.conversation_engine.conversation_context.discovery_complete:
                print("✅ Discovery Complete - Ready for generation")
            else:
                print("🔄 Discovery in Progress - Building musical vision")
            
            if self.current_project_path:
                print(f"📁 Project: {self.current_project_path}")
            else:
                print("📁 Project: None loaded")
        else:
            print("🎵 Discovery: Not started")
        
        # Suggestions status
        print(f"💡 Suggestions: {len(self.current_suggestions)} available")
        if self.current_prompt:
            print("🎼 Prompt: Generated and ready")
        else:
            print("🎼 Prompt: Not generated yet")
    
    def _show_context(self):
        """Show current musical context"""
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical vision.")
            return
        
        print("\n🎵 Current Musical Context:")
        print("-" * 40)
        print(self.conversation_engine.get_context_summary())
    
    def _show_discovery_summary(self):
        """Show intent discovery summary"""
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical vision.")
            return
        
        summary = self.conversation_engine.get_discovery_summary()
        
        print("\n🔍 Intent Discovery Summary:")
        print("-" * 40)
        
        if "error" in summary:
            print(f"❌ {summary['error']}")
            return
        
        print(f"Total Intents: {summary['discovery_metrics']['total_intents']}")
        print(f"Intent Types: {summary['discovery_metrics']['intent_types_discovered']}")
        print(f"Conversation Turns: {summary['discovery_metrics']['conversation_turns']}")
        print(f"Discovery Stage: {summary['discovery_metrics']['discovery_stage']}")
        print(f"Completeness: {summary['discovery_metrics']['completeness_score']:.1%}")
        
        if summary['musical_examples']:
            print(f"Musical Examples: {', '.join(summary['musical_examples'])}")
        
        if summary['musical_insights']:
            print(f"Insights: {', '.join(summary['musical_insights'])}")
    
    def _show_enhancements(self):
        """Show creative enhancement suggestions"""
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical vision.")
            return
        
        if not self.conversation_engine.conversation_context.creative_enhancements:
            print("❌ No creative enhancements available. Complete the discovery process first.")
            return
        
        print("\n🎨 Creative Enhancement Suggestions:")
        print("-" * 40)
        
        for i, enhancement in enumerate(self.conversation_engine.conversation_context.creative_enhancements, 1):
            print(f"{i}. {enhancement['enhancement']}")
            print(f"   Type: {enhancement['type']}, Category: {enhancement['category']}")
            print(f"   Reasoning: {enhancement['reasoning']}")
            print()
    
    def _show_prompt(self):
        """Show generated MIDI prompt"""
        if not self.conversation_engine.conversation_context:
            print("❌ No active conversation. Start by describing your musical vision.")
            return
        
        if not self.conversation_engine.conversation_context.discovery_complete:
            print("❌ Discovery not complete. Continue the conversation to build your musical vision.")
            return
        
        prompt = self.conversation_engine.generate_midi_prompt("4-bar", "all elements")
        self.current_prompt = prompt
        
        print("\n🎼 Generated MIDI Prompt:")
        print("-" * 40)
        print(prompt)
    
    def _show_suggestions(self):
        """Show current musical suggestions"""
        if not self.current_suggestions:
            print("❌ No suggestions available. Complete the discovery process first!")
            return
        
        print("\n💡 Current Musical Suggestions:")
        print("-" * 40)
        
        for i, suggestion in enumerate(self.current_suggestions, 1):
            print(f"{i}. {suggestion.title}")
            print(f"   {suggestion.description}")
            print(f"   Confidence: {suggestion.confidence_score:.1%}")
            print(f"   Type: {suggestion.suggestion_type}")
            
            if suggestion.enhancement_suggestions:
                print(f"   Enhancements: {len(suggestion.enhancement_suggestions)} available")
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
        suggestions = self.conversation_engine.get_musical_suggestions()
        self.current_suggestions = suggestions
        
        if suggestions:
            print("\n💡 I've generated some musical suggestions for you:")
            print("-" * 50)
            
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion.title}")
                print(f"   {suggestion.description}")
                print(f"   Confidence: {suggestion.confidence_score:.1%}")
                print()
        else:
            print("❌ I need more context to generate suggestions. Tell me more about your musical vision!")
    
    def _handle_generate_command(self, command: str):
        """Handle generate command"""
        parts = command.split()
        if len(parts) < 2:
            print("❌ Usage: generate <type>")
            print("Types: prompt, suggestions, enhancements")
            return
        
        generate_type = parts[1].lower()
        
        if generate_type == "prompt":
            self._show_prompt()
        elif generate_type == "suggestions":
            self._generate_and_show_suggestions()
        elif generate_type == "enhancements":
            self._show_enhancements()
        else:
            print(f"❌ Invalid type. Valid types: prompt, suggestions, enhancements")
    
    def _handle_enhance_command(self, command: str):
        """Handle enhance command"""
        parts = command.split()
        if len(parts) < 2:
            print("❌ Usage: enhance <level>")
            print("Levels: low, medium, high")
            return
        
        level = parts[1].lower()
        if level not in ["low", "medium", "high"]:
            print("❌ Invalid level. Valid levels: low, medium, high")
            return
        
        if not self.conversation_engine.conversation_context or not self.conversation_engine.conversation_context.intent_collection:
            print("❌ No musical intent discovered yet. Complete the discovery process first.")
            return
        
        # Generate enhancements with specified level
        from creative_enhancement import suggest_musical_enhancements
        enhancements = suggest_musical_enhancements(
            self.conversation_engine.conversation_context.intent_collection,
            level
        )
        
        self.conversation_engine.conversation_context.creative_enhancements = enhancements
        
        print(f"✅ Generated {len(enhancements)} creative enhancements at {level} level:")
        for i, enhancement in enumerate(enhancements, 1):
            print(f"{i}. {enhancement['enhancement']} - {enhancement['reasoning']}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Enhanced Musical Conversation System")
    parser.add_argument("--project", "-p", help="Path to DAW project file to analyze")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--demo", "-d", action="store_true", help="Run demo")
    parser.add_argument("--input", help="Initial musical input to start conversation")
    
    args = parser.parse_args()
    
    cli = EnhancedMusicalConversationCLI()
    
    if args.demo:
        # Run demo mode
        cli.start_demo_mode(args.project)
        
    elif args.interactive or not any([args.project, args.demo]):
        # Start interactive mode
        cli.start_interactive_mode(args.project, args.input)
    
    else:
        print("Use --interactive to start interactive mode or --demo to run demo")


if __name__ == "__main__":
    main()
