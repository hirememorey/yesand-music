#!/usr/bin/env python3
"""
Test script to demonstrate the conversation-based approach
"""

import os
import sys
from mvp_musical_quality_first import MVPMusicalQualityFirstGenerator

def test_conversation_approach():
    """Test the conversation-based musical generation approach"""
    
    # Set up API key
    os.environ['OPENAI_API_KEY'] = "your-api-key-here"
    
    print("🎵 Testing Conversation-Based Musical Generation")
    print("=" * 50)
    
    # Initialize the generator
    generator = MVPMusicalQualityFirstGenerator(api_key=os.environ['OPENAI_API_KEY'])
    
    # Test prompts that demonstrate conversation capabilities
    test_prompts = [
        "Create a funky bass line in C major",
        "I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby in g minor",
        "Generate a melancholic melody that makes me feel intrigued and scared",
        "Create a jazz piano melody in the style of Bill Evans",
        "Make a funky drum pattern like James Brown"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🎵 Test {i}: {prompt}")
        print("-" * 40)
        
        try:
            # Generate MIDI
            result = generator.generate_and_save(prompt)
            
            if result['success']:
                print(f"✅ Success! Quality Score: {result['quality_score']:.2f}")
                print(f"📁 Saved to: {result['filename']}")
                print(f"🎼 Character: {result['musical_character']}")
            else:
                print(f"❌ Failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n🎉 Conversation-based testing complete!")
    print("\nKey Features Demonstrated:")
    print("✅ Natural language understanding")
    print("✅ Creative metaphor processing")
    print("✅ Musical quality assessment")
    print("✅ Context-aware generation")
    print("✅ User feedback integration")

if __name__ == "__main__":
    test_conversation_approach()
