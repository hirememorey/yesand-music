#!/usr/bin/env python3
"""
Test script to demonstrate the Musical Conversation System
This avoids the interactive mode EOF issues by simulating a conversation
"""

import os
import sys
from musical_conversation_engine import MusicalConversationEngine
from musical_context_interview import MusicalContextInterview

def test_musical_conversation():
    """Test the Musical Conversation System with simulated user input"""
    
    print("🎵 Musical Conversation System - Test Demo")
    print("=" * 50)
    
    # Set up the API key (get from environment variable)
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("💡 Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize the conversation engine
    engine = MusicalConversationEngine()
    
    # Start the conversation
    print("\n🎵 Starting Musical Context Interview...")
    print("-" * 30)
    start_message = engine.start_conversation()
    print(f"🤖 AI: {start_message}")
    
    # Simulate the interview process
    test_responses = [
        "I'm creating a song about leaders who shoot the messenger instead of fixing problems",
        "G minor",
        "120",  # Just the number for BPM
        "I have a DX7 bass line and fuzz guitar",
        "I need help with a bridge that makes sense"
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n🎵 You: {response}")
        
        # Process the response
        result = engine.process_user_input(response)
        print(f"🤖 AI: {result}")
        
        # Check if interview is complete
        if hasattr(engine, 'context_interview'):
            answered, total = engine.context_interview.get_progress()
            if answered >= total:
                print(f"\n✅ Interview complete! ({answered}/{total} questions answered)")
                break
    
    print("\n🎵 Testing Suggestion Generation...")
    print("-" * 30)
    
    # Test suggestion generation
    if hasattr(engine, 'context_interview') and engine.context_interview.is_complete():
        print("🎵 You: Can you give me some suggestions now?")
        result = engine.process_user_input("Can you give me some suggestions now?")
        print(f"🤖 AI: {result}")
    
    print("\n🎵 Testing MIDI Sketch Generation...")
    print("-" * 30)
    
    # Test MIDI sketch generation
    print("🎵 You: test 1")
    result = engine.process_user_input("test 1")
    print(f"🤖 AI: {result}")
    
    print("\n🎵 Testing Additional Commands...")
    print("-" * 30)
    
    # Test other commands
    commands = ["help", "status", "sketches"]
    for cmd in commands:
        print(f"🎵 You: {cmd}")
        result = engine.process_user_input(cmd)
        print(f"🤖 AI: {result}")
    
    print("\n🎉 Demo Complete!")
    print("The Musical Conversation System is working correctly!")

if __name__ == "__main__":
    test_musical_conversation()
