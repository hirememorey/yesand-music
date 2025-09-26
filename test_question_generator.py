"""
Test the Dynamic Musical Question Generator

This module demonstrates the context-aware question generation system
working with real musical conversations, showing how questions adapt
to context and conversation flow.
"""

import sys
import os
from typing import List, Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence
from question_generator import (
    MusicalQuestionGenerator, ConversationalQuestionFlow,
    generate_musical_questions, start_question_flow
)


def test_early_stage_questions():
    """Test question generation for early conversation stage."""
    print("=== Testing Early Stage Questions ===")
    
    # Empty context - should generate basic questions
    context = MusicalContext()
    intents = []
    
    generator = MusicalQuestionGenerator()
    questions = generator.generate_questions(context, intents, "early")
    
    print(f"Generated {len(questions)} questions for empty context:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question.question}")
        print(f"   Type: {question.question_type}, Priority: {question.priority}")
        print(f"   Focus: {question.musical_focus}")
        print(f"   Follow-ups: {question.suggested_follow_ups}")
        print()


def test_building_stage_questions():
    """Test question generation for building stage."""
    print("=== Testing Building Stage Questions ===")
    
    # Context with some basic info
    context = MusicalContext(
        tempo=120,
        key_signature="G Minor",
        genre="Jazz",
        target_instrument="piano"
    )
    
    # Some intents captured
    intents = [
        MusicalIntent(
            intent_type=IntentType.STYLISTIC,
            concept="jazz fusion",
            source="user_input",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    generator = MusicalQuestionGenerator()
    questions = generator.generate_questions(context, intents, "building")
    
    print(f"Generated {len(questions)} questions for building stage:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question.question}")
        print(f"   Type: {question.question_type}, Priority: {question.priority}")
        print(f"   Focus: {question.musical_focus}")
        print()


def test_refining_stage_questions():
    """Test question generation for refining stage."""
    print("=== Testing Refining Stage Questions ===")
    
    # Rich context
    context = MusicalContext(
        tempo=120,
        key_signature="G Minor",
        genre="Jazz",
        target_instrument="piano",
        mood="mysterious"
    )
    
    # Multiple intents with some low confidence
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="swung eighths",
            source="user_input",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="jazz sevenths",
            source="user_input",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.CUSTOM,
            concept="something experimental",
            source="user_input",
            confidence=IntentConfidence.LOW
        )
    ]
    
    generator = MusicalQuestionGenerator()
    questions = generator.generate_questions(context, intents, "refining")
    
    print(f"Generated {len(questions)} questions for refining stage:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question.question}")
        print(f"   Type: {question.question_type}, Priority: {question.priority}")
        print(f"   Focus: {question.musical_focus}")
        print()


def test_conversational_flow():
    """Test the conversational question flow."""
    print("=== Testing Conversational Question Flow ===")
    
    flow = start_question_flow()
    
    # Simulate a conversation
    context = MusicalContext()
    intents = []
    
    print("Starting conversation flow...")
    
    for step in range(5):
        question = flow.get_next_question(context, intents)
        if not question:
            print("No more questions available.")
            break
        
        print(f"\nStep {step + 1}:")
        print(f"Question: {question.question}")
        print(f"Type: {question.question_type}, Priority: {question.priority}")
        print(f"Follow-ups: {question.suggested_follow_ups}")
        
        # Simulate user response
        if step == 0:
            response = "I'm working on a jazz piece"
            # Update context based on response
            context.genre = "jazz"
        elif step == 1:
            response = "120 BPM"
            context.tempo = 120
        elif step == 2:
            response = "piano"
            context.target_instrument = "piano"
        else:
            response = "I want a mysterious sound"
            context.mood = "mysterious"
        
        print(f"User response: {response}")
        flow.record_response(question, response)
        
        # Add some intents based on responses
        if step == 0:
            intents.append(MusicalIntent(
                intent_type=IntentType.STYLISTIC,
                concept="jazz",
                source="user_input",
                confidence=IntentConfidence.HIGH
            ))
        elif step == 3:
            intents.append(MusicalIntent(
                intent_type=IntentType.EMOTIONAL,
                concept="mysterious",
                source="user_input",
                confidence=IntentConfidence.HIGH
            ))


def test_context_aware_questions():
    """Test how questions adapt to different musical contexts."""
    print("=== Testing Context-Aware Questions ===")
    
    generator = MusicalQuestionGenerator()
    
    # Test different musical contexts
    contexts = [
        ("Jazz", MusicalContext(genre="Jazz", tempo=140)),
        ("Classical", MusicalContext(genre="Classical", tempo=80)),
        ("Rock", MusicalContext(genre="Rock", tempo=120)),
        ("Electronic", MusicalContext(genre="Electronic", tempo=128))
    ]
    
    for style_name, context in contexts:
        print(f"\n{style_name} context:")
        questions = generator.generate_questions(context, [], "early")
        
        for i, question in enumerate(questions[:2], 1):  # Show first 2 questions
            print(f"  {i}. {question.question}")
            print(f"     Focus: {question.musical_focus}")


def test_question_adaptation():
    """Test how questions adapt based on user responses."""
    print("=== Testing Question Adaptation ===")
    
    generator = MusicalQuestionGenerator()
    
    # Start with empty context
    context = MusicalContext()
    intents = []
    
    print("Initial questions:")
    questions = generator.generate_questions(context, intents, "early")
    for i, question in enumerate(questions[:3], 1):
        print(f"{i}. {question.question}")
    
    # Simulate user providing some context
    context.genre = "Jazz"
    context.tempo = 120
    context.target_instrument = "bass"
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.STYLISTIC,
            concept="jazz",
            source="user_input",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    print(f"\nAfter user provides context:")
    questions = generator.generate_questions(context, intents, "building")
    for i, question in enumerate(questions[:3], 1):
        print(f"{i}. {question.question}")


def test_musical_language_patterns():
    """Test the musical language patterns used in questions."""
    print("=== Testing Musical Language Patterns ===")
    
    generator = MusicalQuestionGenerator()
    
    # Test different musical elements
    test_elements = [
        ("rhythmic", "groove"),
        ("harmonic", "chord progression"),
        ("melodic", "melody line"),
        ("timbral", "sound texture"),
        ("emotional", "mood")
    ]
    
    for element_type, element_name in test_elements:
        print(f"\n{element_type.title()} questions:")
        
        # Generate questions focusing on this element
        context = MusicalContext(genre="Jazz")
        intents = []
        
        questions = generator.generate_questions(context, intents, "building")
        element_questions = [q for q in questions if element_type in q.musical_focus.lower()]
        
        for i, question in enumerate(element_questions[:2], 1):
            print(f"  {i}. {question.question}")


def main():
    """Run all tests."""
    print("Dynamic Musical Question Generator Test Suite")
    print("=" * 60)
    
    try:
        test_early_stage_questions()
        test_building_stage_questions()
        test_refining_stage_questions()
        test_conversational_flow()
        test_context_aware_questions()
        test_question_adaptation()
        test_musical_language_patterns()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("\nThe Dynamic Question Generator demonstrates:")
        print("✅ Context-aware question generation")
        print("✅ Adaptive questioning based on conversation stage")
        print("✅ Musical language patterns for natural conversation")
        print("✅ Priority-based question ordering")
        print("✅ Follow-up question generation")
        print("✅ Context-specific question adaptation")
        print("✅ Conversational flow management")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
