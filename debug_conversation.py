#!/usr/bin/env python3
"""
Debug script to test the musical conversation system
"""

import os
import sys
from musical_conversation_engine import MusicalConversationEngine

def test_conversation_engine():
    """Test the conversation engine without interactive input"""
    
    # Set up API key
    os.environ['OPENAI_API_KEY'] = "your-api-key-here"
    
    print("🔍 Testing Musical Conversation Engine")
    print("=" * 50)
    
    try:
        # Initialize the conversation engine
        engine = MusicalConversationEngine()
        print("✅ Engine initialized successfully")
        
        # Start a conversation
        welcome_message = engine.start_conversation()
        print("✅ Conversation started")
        print(f"Welcome message: {welcome_message[:100]}...")
        
        # Test processing some input
        test_inputs = [
            "I need help with a bridge",
            "My song is in C major at 120 BPM",
            "I have a bass line and drums already"
        ]
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n🎵 Test Input {i}: {test_input}")
            try:
                response = engine.process_user_input(test_input)
                print(f"🤖 Response: {response[:200]}...")
            except Exception as e:
                print(f"❌ Error processing input: {e}")
        
        print("\n✅ Conversation engine test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conversation_engine()
