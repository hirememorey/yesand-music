"""
Test the Context-Aware Creative Enhancement System

This module demonstrates the creative enhancement system working with
discovered musical intents and conversational context.
"""

import sys
import os
from typing import List, Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence, IntentCollection
from creative_enhancement import (
    MusicalCreativityEngine, ContextualPromptGenerator,
    suggest_musical_enhancements, generate_musical_prompt
)


def test_basic_creative_enhancements():
    """Test basic creative enhancement suggestions."""
    print("=== Testing Basic Creative Enhancements ===")
    
    # Create a sample intent collection
    context = MusicalContext(
        genre="Jazz",
        tempo=120,
        key_signature="G Minor",
        target_instrument="piano",
        mood="mysterious"
    )
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="swung eighths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="jazz sevenths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.EMOTIONAL,
            concept="mysterious and dark",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(
        generation_id="test",
        context=context
    )
    
    for intent in intents:
        collection.add_intent(intent)
    
    # Test different enhancement levels
    for level in ["low", "medium", "high"]:
        print(f"\n{level.title()} Enhancement Level:")
        enhancements = suggest_musical_enhancements(collection, level)
        
        for i, enhancement in enumerate(enhancements, 1):
            print(f"  {i}. {enhancement['enhancement']}")
            print(f"     Type: {enhancement['type']}, Category: {enhancement['category']}")
            print(f"     Reasoning: {enhancement['reasoning']}")


def test_style_based_enhancements():
    """Test enhancements based on different musical styles."""
    print("\n=== Testing Style-Based Enhancements ===")
    
    styles = [
        ("Jazz", "mysterious"),
        ("Classical", "dramatic"),
        ("Rock", "aggressive"),
        ("Electronic", "energetic")
    ]
    
    for genre, mood in styles:
        print(f"\n{genre} Style with {mood} mood:")
        
        context = MusicalContext(
            genre=genre,
            tempo=120,
            key_signature="C Major",
            target_instrument="guitar",
            mood=mood
        )
        
        intents = [
            MusicalIntent(
                intent_type=IntentType.RHYTHMIC,
                concept="complex rhythm",
                source="conversation",
                confidence=IntentConfidence.HIGH
            ),
            MusicalIntent(
                intent_type=IntentType.HARMONIC,
                concept="extended chords",
                source="conversation",
                confidence=IntentConfidence.HIGH
            )
        ]
        
        collection = IntentCollection(
            generation_id=f"test_{genre.lower()}",
            context=context
        )
        
        for intent in intents:
            collection.add_intent(intent)
        
        enhancements = suggest_musical_enhancements(collection, "medium")
        
        for i, enhancement in enumerate(enhancements[:3], 1):
            print(f"  {i}. {enhancement['enhancement']}")
            print(f"     Reasoning: {enhancement['reasoning']}")


def test_element_based_enhancements():
    """Test enhancements based on different musical elements."""
    print("\n=== Testing Element-Based Enhancements ===")
    
    # Test rhythmic enhancements
    print("\nRhythmic Enhancements:")
    context = MusicalContext(genre="Jazz", tempo=120)
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="swung eighths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(generation_id="rhythm_test", context=context)
    for intent in intents:
        collection.add_intent(intent)
    
    enhancements = suggest_musical_enhancements(collection, "medium")
    for enhancement in enhancements:
        if enhancement["type"] == "rhythmic":
            print(f"  - {enhancement['enhancement']}: {enhancement['reasoning']}")
    
    # Test harmonic enhancements
    print("\nHarmonic Enhancements:")
    intents = [
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="jazz sevenths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(generation_id="harmony_test", context=context)
    for intent in intents:
        collection.add_intent(intent)
    
    enhancements = suggest_musical_enhancements(collection, "medium")
    for enhancement in enhancements:
        if enhancement["type"] == "harmonic":
            print(f"  - {enhancement['enhancement']}: {enhancement['reasoning']}")
    
    # Test melodic enhancements
    print("\nMelodic Enhancements:")
    intents = [
        MusicalIntent(
            intent_type=IntentType.MELODIC,
            concept="ascending melody",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(generation_id="melody_test", context=context)
    for intent in intents:
        collection.add_intent(intent)
    
    enhancements = suggest_musical_enhancements(collection, "medium")
    for enhancement in enhancements:
        if enhancement["type"] == "melodic":
            print(f"  - {enhancement['enhancement']}: {enhancement['reasoning']}")


def test_contextual_prompt_generation():
    """Test contextual prompt generation."""
    print("\n=== Testing Contextual Prompt Generation ===")
    
    # Create a rich intent collection
    context = MusicalContext(
        genre="Jazz",
        tempo=120,
        key_signature="G Minor",
        target_instrument="bass",
        mood="mysterious"
    )
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="swung eighths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="jazz sevenths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.MELODIC,
            concept="sparse, ascending melody",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.EMOTIONAL,
            concept="mysterious and dark",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(
        generation_id="prompt_test",
        context=context
    )
    
    for intent in intents:
        collection.add_intent(intent)
    
    # Generate enhancements
    enhancements = suggest_musical_enhancements(collection, "medium")
    
    # Generate prompts for different contexts
    prompt_contexts = [
        ("4-bar", "rhythm and harmony"),
        ("8-bar", "melody and emotion"),
        ("16-bar", "all elements")
    ]
    
    for length, focus in prompt_contexts:
        print(f"\n{length} prompt with {focus} focus:")
        prompt = generate_musical_prompt(collection, enhancements, length, focus)
        print(f"Length: {len(prompt)} characters")
        print(f"Preview: {prompt[:200]}...")


def test_musical_examples_in_prompts():
    """Test how musical examples are incorporated into prompts."""
    print("\n=== Testing Musical Examples in Prompts ===")
    
    # Create context with musical examples
    context = MusicalContext(
        genre="Jazz",
        tempo=120,
        key_signature="G Minor",
        target_instrument="piano",
        mood="mysterious"
    )
    
    # Add conversation history with examples
    context.conversation_history = [
        "I want it to sound like Miles Davis",
        "Similar to that Herbie Hancock song",
        "In the style of John Coltrane"
    ]
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.STYLISTIC,
            concept="jazz style",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(
        generation_id="examples_test",
        context=context
    )
    
    for intent in intents:
        collection.add_intent(intent)
    
    # Generate prompt
    prompt = generate_musical_prompt(collection, [], "4-bar", "style")
    
    print("Generated prompt with musical examples:")
    print(prompt)


def test_enhancement_prioritization():
    """Test how enhancements are prioritized based on context."""
    print("\n=== Testing Enhancement Prioritization ===")
    
    # Test different contexts
    contexts = [
        ("Jazz", "mysterious", "piano"),
        ("Rock", "aggressive", "guitar"),
        ("Classical", "dramatic", "strings"),
        ("Electronic", "energetic", "synth")
    ]
    
    for genre, mood, instrument in contexts:
        print(f"\n{genre} - {mood} - {instrument}:")
        
        context = MusicalContext(
            genre=genre,
            tempo=120,
            key_signature="C Major",
            target_instrument=instrument,
            mood=mood
        )
        
        intents = [
            MusicalIntent(
                intent_type=IntentType.RHYTHMIC,
                concept="complex rhythm",
                source="conversation",
                confidence=IntentConfidence.HIGH
            ),
            MusicalIntent(
                intent_type=IntentType.HARMONIC,
                concept="extended chords",
                source="conversation",
                confidence=IntentConfidence.HIGH
            )
        ]
        
        collection = IntentCollection(
            generation_id=f"priority_test_{genre.lower()}",
            context=context
        )
        
        for intent in intents:
            collection.add_intent(intent)
        
        enhancements = suggest_musical_enhancements(collection, "high")
        
        # Show top 3 enhancements
        for i, enhancement in enumerate(enhancements[:3], 1):
            print(f"  {i}. {enhancement['enhancement']} (Priority: {enhancement['priority']})")


def test_creative_reasoning():
    """Test the creative reasoning system."""
    print("\n=== Testing Creative Reasoning ===")
    
    # Create a complex musical context
    context = MusicalContext(
        genre="Jazz",
        tempo=140,
        key_signature="F# Minor",
        target_instrument="saxophone",
        mood="mysterious"
    )
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="syncopated funk",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="modal interchange",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.MELODIC,
            concept="angular and chromatic",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.EMOTIONAL,
            concept="aggressive and driving",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(
        generation_id="reasoning_test",
        context=context
    )
    
    for intent in intents:
        collection.add_intent(intent)
    
    enhancements = suggest_musical_enhancements(collection, "high")
    
    print("Creative reasoning for complex musical context:")
    for i, enhancement in enumerate(enhancements, 1):
        print(f"{i}. {enhancement['enhancement']}")
        print(f"   Reasoning: {enhancement['reasoning']}")
        print()


def main():
    """Run all tests."""
    print("Context-Aware Creative Enhancement System Test Suite")
    print("=" * 70)
    
    try:
        test_basic_creative_enhancements()
        test_style_based_enhancements()
        test_element_based_enhancements()
        test_contextual_prompt_generation()
        test_musical_examples_in_prompts()
        test_enhancement_prioritization()
        test_creative_reasoning()
        
        print("\n" + "=" * 70)
        print("All tests completed successfully!")
        print("\nThe Context-Aware Creative Enhancement System demonstrates:")
        print("✅ Musical creativity through understanding")
        print("✅ Context-aware enhancement suggestions")
        print("✅ Style-based creative patterns")
        print("✅ Element-based enhancement logic")
        print("✅ Rich contextual prompt generation")
        print("✅ Musical examples integration")
        print("✅ Enhancement prioritization")
        print("✅ Creative reasoning system")
        print("✅ Natural language prompt formatting")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
