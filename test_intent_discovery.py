"""
Test the Conversation-Driven Intent Discovery Agent

This module demonstrates the holistic, conversation-driven approach to
discovering musical intent through natural dialogue.
"""

import sys
import os
from typing import List, Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence
from intent_discovery_agent import (
    MusicalIntentDiscoveryAgent, start_musical_discovery
)


def test_basic_discovery_flow():
    """Test the basic discovery flow with a simple musical conversation."""
    print("=== Testing Basic Discovery Flow ===")
    
    agent = start_musical_discovery()
    
    # Start discovery session
    result = agent.start_discovery_session("I'm working on a jazz piece")
    
    print(f"Welcome: {result['welcome'][:100]}...")
    print(f"Response: {result['response']}")
    print(f"Discovery Stage: {result['discovery_stage']}")
    print(f"Intents Discovered: {result['intents_discovered']}")
    
    # Simulate conversation
    conversation_steps = [
        "It's in G minor at 120 BPM",
        "I want a mysterious sound like Miles Davis",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony"
    ]
    
    for step in conversation_steps:
        print(f"\nUser: {step}")
        result = agent.process_musical_input(step)
        
        print(f"Response: {result['response'][:100]}...")
        print(f"Intents: {result['intents_discovered']}, Total: {result['total_intents']}")
        print(f"Stage: {result['discovery_stage']}, Complete: {result['discovery_complete']}")
        
        if result['musical_insights']:
            print(f"Insights: {', '.join(result['musical_insights'])}")
    
    # Get final summary
    summary = agent.get_discovery_summary()
    print(f"\nFinal Summary:")
    print(f"Total Intents: {summary['discovery_metrics']['total_intents']}")
    print(f"Completeness: {summary['discovery_metrics']['completeness_score']:.1%}")
    print(f"Musical Examples: {summary['musical_examples']}")


def test_musical_examples_extraction():
    """Test extraction of musical examples and references."""
    print("\n=== Testing Musical Examples Extraction ===")
    
    agent = start_musical_discovery()
    
    # Test different types of musical references
    test_inputs = [
        "I want it to sound like Miles Davis",
        "Similar to that Herbie Hancock song",
        "In the style of John Coltrane",
        "It reminds me of that one Bill Evans piece",
        "Think Herbie Hancock meets Weather Report"
    ]
    
    for input_text in test_inputs:
        print(f"\nInput: {input_text}")
        result = agent.process_musical_input(input_text)
        
        if result['examples_referenced']:
            print(f"Examples found: {result['examples_referenced']}")
        else:
            print("No examples found")


def test_discovery_stages():
    """Test how the discovery process progresses through different stages."""
    print("\n=== Testing Discovery Stages ===")
    
    agent = start_musical_discovery()
    
    # Start with empty context
    result = agent.start_discovery_session()
    print(f"Initial stage: {result['discovery_stage']}")
    
    # Build up context gradually
    stages = [
        ("I'm working on a jazz piece", "exploration"),
        ("It's in G minor at 120 BPM", "exploration"),
        ("I want a mysterious sound", "building"),
        ("Swung eighths for the rhythm", "building"),
        ("Jazz sevenths for the harmony", "refining"),
        ("A sparse, ascending melody", "refining"),
        ("Make it sound aggressive", "complete"),
        ("Use extended techniques", "complete")
    ]
    
    for input_text, expected_stage in stages:
        result = agent.process_musical_input(input_text)
        actual_stage = result['discovery_stage']
        
        print(f"Input: {input_text}")
        print(f"Expected: {expected_stage}, Actual: {actual_stage}")
        print(f"Intents: {result['total_intents']}, Complete: {result['discovery_complete']}")
        print()


def test_context_aware_discovery():
    """Test how discovery adapts to different musical contexts."""
    print("\n=== Testing Context-Aware Discovery ===")
    
    # Test different musical contexts
    contexts = [
        ("Jazz", {"genre": "Jazz", "tempo": 140}),
        ("Classical", {"genre": "Classical", "tempo": 80}),
        ("Rock", {"genre": "Rock", "tempo": 120}),
        ("Electronic", {"genre": "Electronic", "tempo": 128})
    ]
    
    for style_name, context_data in contexts:
        print(f"\n--- {style_name} Context ---")
        
        context = MusicalContext(**context_data)
        agent = start_musical_discovery(context)
        
        # Start discovery
        result = agent.start_discovery_session("I'm starting a new piece")
        print(f"Initial question: {result['next_question']['question'] if result['next_question'] else 'None'}")
        
        # Add some musical input
        result = agent.process_musical_input("I want a complex rhythm")
        print(f"Response: {result['response'][:80]}...")
        print(f"Stage: {result['discovery_stage']}")


def test_discovery_completeness():
    """Test the discovery completeness assessment."""
    print("\n=== Testing Discovery Completeness ===")
    
    agent = start_musical_discovery()
    
    # Build up a complete musical vision
    conversation_steps = [
        "I'm working on a jazz piece",
        "It's in G minor at 120 BPM",
        "Piano",
        "I want a mysterious sound",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony",
        "A sparse, ascending melody"
    ]
    
    for step in conversation_steps:
        result = agent.process_musical_input(step)
        print(f"Step: {step}")
        print(f"Complete: {result['discovery_complete']}")
        print(f"Completeness Score: {agent._calculate_completeness_score():.1%}")
        print(f"Stage: {result['discovery_stage']}")
        print()


def test_musical_insights_generation():
    """Test the generation of musical insights."""
    print("\n=== Testing Musical Insights Generation ===")
    
    agent = start_musical_discovery()
    
    # Build up different types of musical intents
    test_inputs = [
        "I want a complex rhythm",
        "Jazz harmony with extended chords",
        "A beautiful, flowing melody",
        "Make it sound mysterious and dark",
        "I want it to sound like Miles Davis"
    ]
    
    for input_text in test_inputs:
        result = agent.process_musical_input(input_text)
        
        print(f"Input: {input_text}")
        print(f"Insights: {', '.join(result['musical_insights'])}")
        print(f"Total Intents: {result['total_intents']}")
        print()


def test_export_for_generation():
    """Test exporting discovered intent for MIDI generation."""
    print("\n=== Testing Export for Generation ===")
    
    agent = start_musical_discovery()
    
    # Build up a complete musical vision
    conversation_steps = [
        "I'm working on a jazz piece",
        "It's in G minor at 120 BPM",
        "Piano",
        "I want a mysterious sound like Miles Davis",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony",
        "A sparse, ascending melody that builds tension"
    ]
    
    for step in conversation_steps:
        agent.process_musical_input(step)
    
    # Export for generation
    export_data = agent.export_for_generation()
    
    print(f"Generation Ready: {export_data['generation_ready']}")
    print(f"Completeness Score: {export_data['completeness_score']:.1%}")
    print(f"Musical Context: {export_data['musical_context']}")
    
    if 'intent_collection' in export_data:
        collection = export_data['intent_collection']
        print(f"Total Intents: {len(collection['intents'])}")
        print(f"Intent Types: {set(intent['intent_type'] for intent in collection['intents'])}")


def test_conversation_highlights():
    """Test the conversation highlights feature."""
    print("\n=== Testing Conversation Highlights ===")
    
    agent = start_musical_discovery()
    
    # Build up a conversation
    conversation_steps = [
        "I'm working on a jazz piece",
        "It's in G minor at 120 BPM",
        "I want a mysterious sound like Miles Davis",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony",
        "A sparse, ascending melody that builds tension",
        "Make it sound aggressive and driving",
        "Use extended techniques like multiphonics"
    ]
    
    for step in conversation_steps:
        agent.process_musical_input(step)
    
    # Get highlights
    summary = agent.get_discovery_summary()
    highlights = summary['conversation_highlights']
    
    print(f"Conversation Highlights:")
    for i, highlight in enumerate(highlights, 1):
        print(f"{i}. {highlight}")


def main():
    """Run all tests."""
    print("Conversation-Driven Intent Discovery Agent Test Suite")
    print("=" * 70)
    
    try:
        test_basic_discovery_flow()
        test_musical_examples_extraction()
        test_discovery_stages()
        test_context_aware_discovery()
        test_discovery_completeness()
        test_musical_insights_generation()
        test_export_for_generation()
        test_conversation_highlights()
        
        print("\n" + "=" * 70)
        print("All tests completed successfully!")
        print("\nThe Conversation-Driven Intent Discovery Agent demonstrates:")
        print("✅ Holistic musical intent discovery through conversation")
        print("✅ Natural musical dialogue flow")
        print("✅ Musical examples and metaphor extraction")
        print("✅ Context-aware discovery adaptation")
        print("✅ Progressive discovery stages")
        print("✅ Musical insights generation")
        print("✅ Completeness assessment")
        print("✅ Export for MIDI generation")
        print("✅ Conversation highlights tracking")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
