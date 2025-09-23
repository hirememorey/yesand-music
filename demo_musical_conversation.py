#!/usr/bin/env python3
"""
Demo: Musical Conversation System

This script demonstrates the musical conversation capabilities of the enhanced control plane.
"""

import os
import sys
import time
import logging
from typing import List, Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_control_plane import EnhancedControlPlane

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicalConversationDemo:
    """Demo class for musical conversation system"""
    
    def __init__(self):
        """Initialize the demo"""
        self.enhanced_cp = None
        self.demo_scenarios = [
            {
                "name": "Generate Funky Bass Line",
                "input": "I need a funky bass line for my song",
                "expected": "Should generate a funky bass pattern"
            },
            {
                "name": "Brighten Up Chorus",
                "input": "This chorus is landing flat, can you brighten it up?",
                "expected": "Should suggest harmonic improvements"
            },
            {
                "name": "Musical Reference",
                "input": "Make it groove like that Stevie Wonder track",
                "expected": "Should use Stevie Wonder as reference"
            },
            {
                "name": "Style Request",
                "input": "I want something jazzy but not too complex",
                "expected": "Should generate jazz-style content"
            },
            {
                "name": "Feedback Loop",
                "input": "Make it more complex",
                "expected": "Should refine based on feedback"
            }
        ]
    
    def setup(self) -> bool:
        """Setup the enhanced control plane"""
        try:
            print("🎵 Setting up Enhanced Control Plane...")
            
            # Check for OpenAI API key
            if not os.getenv("OPENAI_API_KEY"):
                print("❌ Error: OPENAI_API_KEY environment variable not set")
                print("Please set your OpenAI API key:")
                print("export OPENAI_API_KEY='your-api-key-here'")
                return False
            
            # Initialize enhanced control plane
            self.enhanced_cp = EnhancedControlPlane()
            print("✅ Enhanced Control Plane initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Enhanced Control Plane: {e}")
            return False
    
    def run_demo_scenarios(self):
        """Run the demo scenarios"""
        print("\n🎵 Running Demo Scenarios")
        print("=" * 50)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ---")
            print(f"Input: {scenario['input']}")
            print(f"Expected: {scenario['expected']}")
            print("-" * 30)
            
            try:
                # Execute the scenario
                response = self.enhanced_cp.execute(scenario['input'])
                print(f"Response: {response}")
                
                # Wait a moment between scenarios
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
            
            print()
    
    def run_interactive_demo(self):
        """Run an interactive demo"""
        print("\n🎵 Interactive Demo")
        print("=" * 50)
        print("Try these example conversations:")
        print()
        
        example_inputs = [
            "start conversation",
            "I need a funky bass line",
            "Make it more complex",
            "This sounds too busy, simplify it",
            "Make it groove like Bootsy Collins",
            "What key would work better?",
            "project status",
            "stop conversation"
        ]
        
        for user_input in example_inputs:
            print(f"🎵 User: {user_input}")
            try:
                response = self.enhanced_cp.execute(user_input)
                print(f"🤖 AI: {response}")
                print()
                time.sleep(2)  # Pause between interactions
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
    
    def test_feedback_loop(self):
        """Test the feedback loop functionality"""
        print("\n🎵 Testing Feedback Loop")
        print("=" * 50)
        
        # Start conversation
        print("Starting conversation...")
        response = self.enhanced_cp.execute("start conversation")
        print(f"AI: {response}")
        print()
        
        # Generate initial content
        print("Generating initial content...")
        response = self.enhanced_cp.execute("I need a jazz bass line")
        print(f"AI: {response}")
        print()
        
        # Provide feedback
        feedback_examples = [
            "Make it more complex",
            "This is too busy, simplify it",
            "Make it swing more",
            "I want it in a different key",
            "Make it brighter"
        ]
        
        for feedback in feedback_examples:
            print(f"🎵 User feedback: {feedback}")
            try:
                response = self.enhanced_cp.process_feedback(feedback)
                print(f"🤖 AI: {response}")
                print()
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error processing feedback: {e}")
                print()
    
    def test_musical_references(self):
        """Test musical reference system"""
        print("\n🎵 Testing Musical References")
        print("=" * 50)
        
        reference_tests = [
            "Make it funky like Bootsy Collins",
            "I want that Stevie Wonder groove",
            "Make it bright like a major 7th chord",
            "Give it that jazz swing feel",
            "Make it dark and moody"
        ]
        
        for test_input in reference_tests:
            print(f"🎵 User: {test_input}")
            try:
                response = self.enhanced_cp.execute(test_input)
                print(f"🤖 AI: {response}")
                print()
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
    
    def show_project_summary(self):
        """Show project summary"""
        print("\n🎵 Project Summary")
        print("=" * 50)
        
        try:
            summary = self.enhanced_cp.execute("project status")
            print(summary)
        except Exception as e:
            print(f"❌ Error getting project summary: {e}")
    
    def run_full_demo(self):
        """Run the full demo"""
        print("🎵 Musical Conversation System Demo")
        print("=" * 60)
        print("This demo showcases the conversational AI capabilities")
        print("for musical collaboration and creation.")
        print()
        
        # Setup
        if not self.setup():
            return
        
        # Run demo scenarios
        self.run_demo_scenarios()
        
        # Test feedback loop
        self.test_feedback_loop()
        
        # Test musical references
        self.test_musical_references()
        
        # Show project summary
        self.show_project_summary()
        
        print("\n🎵 Demo Complete!")
        print("The musical conversation system is working and ready for use.")
        print("Try running: python enhanced_control_plane_cli.py --conversation")

def main():
    """Main demo entry point"""
    demo = MusicalConversationDemo()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            demo.setup()
            demo.run_interactive_demo()
        elif sys.argv[1] == "feedback":
            demo.setup()
            demo.test_feedback_loop()
        elif sys.argv[1] == "references":
            demo.setup()
            demo.test_musical_references()
        else:
            print("Usage: python demo_musical_conversation.py [interactive|feedback|references]")
    else:
        demo.run_full_demo()

if __name__ == "__main__":
    main()
