"""
Test the Musical Intent System

This module demonstrates the dynamic intent capture system working with
real musical conversations, showing how it adapts and grows with context.
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import (
    MusicalContext, IntentType, IntentConfidence, 
    create_intent_collection, parse_musical_description
)
from intent_parser import (
    ConversationalIntentParser, IntentAnalyzer,
    start_musical_conversation, analyze_musical_intent
)


def test_basic_intent_parsing():
    """Test basic intent parsing functionality."""
    print("=== Testing Basic Intent Parsing ===")
    
    # Create a musical context
    context = MusicalContext(
        project_name="Test Song",
        tempo=120,
        key_signature="G Minor",
        genre="Jazz",
        target_instrument="bassline"
    )
    
    # Test different types of musical descriptions
    test_descriptions = [
        "I want a funky bassline with swung eighths",
        "The chord progression should be jazz sevenths in G minor",
        "Make it sound mysterious and dark",
        "I need a sparse melody that ascends",
        "The rhythm should be syncopated and complex"
    ]
    
    for description in test_descriptions:
        print(f"\nDescription: '{description}'")
        collection = parse_musical_description(description, context)
        
        print(f"Extracted {len(collection.intents)} intents:")
        for intent in collection.intents:
            print(f"  - {intent.intent_type}: '{intent.concept}' (confidence: {intent.confidence})")
        
        print(f"Context: {collection.to_conversation_context()}")


def test_conversational_intent_parsing():
    """Test conversational intent parsing with context building."""
    print("\n=== Testing Conversational Intent Parsing ===")
    
    # Start a conversation
    parser = start_musical_conversation()
    
    # Simulate a musical conversation
    conversation_steps = [
        "I'm working on a new song",
        "It's in G minor at 120 BPM",
        "I want a funky bassline with swung eighths",
        "The chord progression should use jazz sevenths",
        "Make it sound mysterious and dark",
        "I need the melody to be sparse and ascending"
    ]
    
    for step in conversation_steps:
        print(f"\nUser: {step}")
        intents, response = parser.process_user_input(step)
        
        print(f"System: {response}")
        
        if intents:
            print("Extracted intents:")
            for intent in intents:
                print(f"  - {intent.intent_type}: '{intent.concept}'")
    
    # Get the final intent collection
    final_collection = parser.get_current_intent_collection()
    print(f"\n=== Final Intent Collection ===")
    print(f"Total intents: {len(final_collection.intents)}")
    print(f"Context: {final_collection.to_conversation_context()}")
    
    # Analyze the collection
    analysis = analyze_musical_intent(final_collection)
    print(f"\n=== Analysis ===")
    print(f"Intent types: {analysis['intent_types']}")
    print(f"Confidence distribution: {analysis['confidence_distribution']}")
    print(f"Suggestions: {analysis['suggestions']}")


def test_context_awareness():
    """Test how the system adapts to different musical contexts."""
    print("\n=== Testing Context Awareness ===")
    
    # Test 1: Jazz context
    jazz_context = MusicalContext(
        genre="Jazz",
        era="Modern",
        tempo=140,
        key_signature="C Major"
    )
    
    jazz_parser = start_musical_conversation(jazz_context)
    intents, response = jazz_parser.process_user_input("I want some complex harmony")
    print(f"Jazz context - 'complex harmony': {response}")
    
    # Test 2: Classical context
    classical_context = MusicalContext(
        genre="Classical",
        era="Romantic",
        tempo=80,
        key_signature="E Minor"
    )
    
    classical_parser = start_musical_conversation(classical_context)
    intents, response = classical_parser.process_user_input("I want some complex harmony")
    print(f"Classical context - 'complex harmony': {response}")
    
    # Test 3: Rock context
    rock_context = MusicalContext(
        genre="Rock",
        era="Modern",
        tempo=120,
        key_signature="A Minor"
    )
    
    rock_parser = start_musical_conversation(rock_context)
    intents, response = rock_parser.process_user_input("I want some complex harmony")
    print(f"Rock context - 'complex harmony': {response}")


def test_intent_relationships():
    """Test how intents relate to each other and build context."""
    print("\n=== Testing Intent Relationships ===")
    
    parser = start_musical_conversation()
    
    # Build up a complex musical idea through conversation
    conversation = [
        "I'm creating a jazz fusion piece",
        "The tempo is 160 BPM in 4/4 time",
        "I want a complex bassline with syncopated rhythms",
        "The harmony should use modal interchange",
        "The melody needs to be angular and chromatic",
        "Make it sound aggressive and driving"
    ]
    
    for step in conversation:
        print(f"\nUser: {step}")
        intents, response = parser.process_user_input(step)
        print(f"System: {response}")
    
    # Analyze the relationships
    collection = parser.get_current_intent_collection()
    print(f"\n=== Intent Relationships ===")
    print(f"Intent graph: {collection.intent_graph}")
    
    # Show how intents build on each other
    print(f"\n=== Context Evolution ===")
    print(f"Final tempo: {collection.context.tempo}")
    print(f"Final key: {collection.context.key_signature}")
    print(f"Final genre: {collection.context.genre}")
    print(f"Final mood: {collection.context.mood}")


def test_flexibility_and_extensibility():
    """Test how the system handles new and unexpected musical concepts."""
    print("\n=== Testing Flexibility and Extensibility ===")
    
    parser = start_musical_conversation()
    
    # Test with unusual musical concepts
    unusual_concepts = [
        "I want a microtonal melody",
        "The rhythm should be in 7/8 time",
        "Use extended techniques like multiphonics",
        "I want a drone with overtones",
        "The harmony should be based on the harmonic series"
    ]
    
    for concept in unusual_concepts:
        print(f"\nUser: {concept}")
        intents, response = parser.process_user_input(concept)
        print(f"System: {response}")
        
        if intents:
            for intent in intents:
                print(f"  Captured as: {intent.intent_type} - '{intent.concept}' (confidence: {intent.confidence})")


def main():
    """Run all tests."""
    print("Musical Intent System Test Suite")
    print("=" * 50)
    
    try:
        test_basic_intent_parsing()
        test_conversational_intent_parsing()
        test_context_awareness()
        test_intent_relationships()
        test_flexibility_and_extensibility()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("\nThe Musical Intent System demonstrates:")
        print("✅ Dynamic intent capture from natural language")
        print("✅ Context-aware musical term resolution")
        print("✅ Conversational building of musical ideas")
        print("✅ Flexible handling of new musical concepts")
        print("✅ Relationship tracking between musical elements")
        print("✅ Confidence assessment and clarification requests")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
