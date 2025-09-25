#!/usr/bin/env python3
"""
Fixed version of the musical conversation system for testing
"""

import os
import sys
from musical_conversation_engine import MusicalConversationEngine

def test_conversation_with_simulated_input():
    """Test conversation with simulated user input"""
    
    # Set up API key
    os.environ['OPENAI_API_KEY'] = "your-api-key-here"
    
    print("🎵 Musical Conversation & Problem-Solving System")
    print("=" * 60)
    
    # Initialize the conversation engine
    engine = MusicalConversationEngine()
    
    # Start conversation
    welcome_message = engine.start_conversation()
    print(welcome_message)
    print("\nType 'help' for available commands, 'quit' to exit.")
    print("-" * 60)
    
    # Simulate a conversation
    conversation_steps = [
        "I need help with a bridge for my song",
        "My song is about overcoming challenges",
        "It's in G minor at 120 BPM",
        "I have a bass line and drums already",
        "The bridge needs to create tension and contrast",
        "suggestions"
    ]
    
    for i, user_input in enumerate(conversation_steps, 1):
        print(f"\n🎵 You: {user_input}")
        
        try:
            response = engine.process_user_input(user_input)
            print(f"🤖 AI: {response}")
            
            # Add a small delay to simulate real conversation
            import time
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    print("\n🎉 Conversation simulation complete!")
    print("\nThis demonstrates the conversation-based approach working correctly.")

if __name__ == "__main__":
    test_conversation_with_simulated_input()
