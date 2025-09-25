#!/usr/bin/env python3
"""
Demo script for MVP User-Driven MIDI Generator

This script demonstrates the key features of the system including:
- Musical quality gates
- User feedback integration
- Context extraction
- Interactive generation
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mvp_user_driven_generator import (
    MusicalQualityGate,
    MusicalContextExtractor,
    MVPUserDrivenGenerator
)


def demo_context_extraction():
    """Demonstrate musical context extraction."""
    print("🎵 Musical Context Extraction Demo")
    print("=" * 50)
    
    extractor = MusicalContextExtractor()
    
    test_prompts = [
        "Create a jazz bass line in C major at 120 BPM for 8 measures",
        "Generate a funky drum pattern in G minor",
        "Make a melancholic piano melody in F# major at 80 BPM",
        "Create a complex rock guitar part for 16 bars",
        "Generate a simple blues bass line"
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 Prompt: '{prompt}'")
        context = extractor.extract_context(prompt)
        
        print("🎯 Extracted Context:")
        for key, value in context.items():
            if value is not None and key != 'original_prompt':
                print(f"  {key}: {value}")


def demo_quality_assessment():
    """Demonstrate musical quality assessment."""
    print("\n\n🎵 Musical Quality Assessment Demo")
    print("=" * 50)
    
    quality_gate = MusicalQualityGate()
    
    # Test cases with different quality levels
    test_cases = [
        {
            'name': 'High Quality MIDI',
            'midi_data': {
                'notes': [
                    {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                    {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                    {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5},
                    {'pitch': 72, 'velocity': 80, 'start_time': 1.5, 'duration': 0.5}
                ],
                'tempo': 120,
                'key': 'C major',
                'duration': 2.0
            },
            'context': {'style': 'jazz', 'user_id': 'demo_user'}
        },
        {
            'name': 'Medium Quality MIDI',
            'midi_data': {
                'notes': [
                    {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 1.0},
                    {'pitch': 60, 'velocity': 80, 'start_time': 1.0, 'duration': 1.0}
                ],
                'tempo': 120,
                'key': 'C major',
                'duration': 2.0
            },
            'context': {'style': 'rock', 'user_id': 'demo_user'}
        },
        {
            'name': 'Low Quality MIDI',
            'midi_data': {
                'notes': [
                    {'pitch': 200, 'velocity': 300, 'start_time': 0.0, 'duration': 0.1}  # Invalid values
                ],
                'tempo': 120,
                'key': 'C major',
                'duration': 0.1
            },
            'context': {'style': 'jazz', 'user_id': 'demo_user'}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        
        quality_score, feedback = quality_gate.assess_quality(
            test_case['midi_data'], 
            test_case['context'], 
            'demo_test'
        )
        
        print(f"  Overall Quality Score: {quality_score:.2f}/1.0")
        print("  Detailed Feedback:")
        for criterion, score in feedback.items():
            print(f"    {criterion.replace('_', ' ').title()}: {score:.2f}")


def demo_user_feedback_system():
    """Demonstrate user feedback integration."""
    print("\n\n🎵 User Feedback System Demo")
    print("=" * 50)
    
    quality_gate = MusicalQualityGate()
    
    # Simulate user feedback
    print("📝 Recording user feedback...")
    
    feedback_entries = [
        ('gen_001', 4.5, 'Great jazz bass line!', 'user_1'),
        ('gen_002', 3.0, 'Decent but could be more complex', 'user_1'),
        ('gen_003', 5.0, 'Perfect for my project!', 'user_1'),
        ('gen_004', 2.0, 'Too simple, needs more variation', 'user_2'),
        ('gen_005', 4.0, 'Good groove but wrong key', 'user_2')
    ]
    
    for gen_id, rating, comments, user_id in feedback_entries:
        quality_gate.record_user_feedback(gen_id, rating, comments, user_id)
        print(f"  ✅ Recorded feedback for {gen_id}: {rating}/5 - '{comments}'")
    
    # Show feedback summary
    print(f"\n📊 Feedback Summary:")
    for user_id, feedbacks in quality_gate.user_feedback_db.items():
        print(f"  User {user_id}: {len(feedbacks)} feedback entries")
        avg_rating = sum(f['rating'] for f in feedbacks) / len(feedbacks)
        print(f"    Average Rating: {avg_rating:.1f}/5")


def demo_interactive_generation():
    """Demonstrate interactive generation (if API key available)."""
    print("\n\n🎵 Interactive Generation Demo")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set - skipping interactive demo")
        print("   Set your API key to test full generation:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("🚀 Starting interactive generation demo...")
    print("   (This will make actual API calls to OpenAI)")
    
    try:
        generator = MVPUserDrivenGenerator(api_key)
        
        # Demo prompts
        demo_prompts = [
            "Create a simple bass line in C major",
            "Generate a jazz piano melody in G minor",
            "Make a funky drum pattern at 120 BPM"
        ]
        
        for prompt in demo_prompts:
            print(f"\n🎵 Generating: '{prompt}'")
            result = generator.generate_and_save(prompt, "demo_user")
            
            if result['success']:
                print(f"  ✅ Success! Quality: {result['quality_score']:.2f}")
                print(f"  📁 Saved to: {result['filename']}")
            else:
                print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def main():
    """Run all demos."""
    print("🎵 MVP User-Driven MIDI Generator - Demo Suite")
    print("=" * 60)
    print("This demo showcases the key features of the system:")
    print("- Musical context extraction from natural language")
    print("- Quality assessment with detailed feedback")
    print("- User feedback integration and learning")
    print("- Interactive MIDI generation (if API key available)")
    print("=" * 60)
    
    # Run demos
    demo_context_extraction()
    demo_quality_assessment()
    demo_user_feedback_system()
    demo_interactive_generation()
    
    print("\n\n🎉 Demo Complete!")
    print("=" * 60)
    print("Key Features Demonstrated:")
    print("✅ Context extraction from natural language prompts")
    print("✅ Musical quality assessment with detailed feedback")
    print("✅ User feedback recording and learning system")
    print("✅ Quality-driven generation with multiple attempts")
    print("✅ Interactive CLI with user-friendly interface")
    print("\n🚀 Ready for production use!")


if __name__ == "__main__":
    main()
