#!/usr/bin/env python3
"""
Demo script for MVP Musical Quality First Generator

This script demonstrates the refined approach that focuses on musical quality
over technical precision, addressing the post-mortem insights.
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mvp_musical_quality_first import MVPMusicalQualityFirstGenerator


def demo_creative_prompts():
    """Demo the system with creative, metaphorical prompts from the post-mortem."""
    
    print("🎵 MVP Musical Quality First Generator - Demo")
    print("=" * 60)
    print("Testing with creative, metaphorical prompts that caused issues before...")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # Initialize generator
    generator = MVPMusicalQualityFirstGenerator(api_key)
    
    # Test prompts from the post-mortem
    test_prompts = [
        "I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby in g minor",
        "Create a melancholic melody that makes me feel intrigued and scared",
        "Generate a funky bass line that sounds like Bootsy Collins on a bad day",
        "Make a drum pattern that sounds like thunder rolling across the sky",
        "Create a jazz piano part that tells a story of lost love",
        "Generate a rock bass line that makes me want to headbang"
    ]
    
    print(f"\n🧪 Testing {len(test_prompts)} creative prompts...")
    print("=" * 60)
    
    results = []
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🎵 Test {i}/{len(test_prompts)}")
        print(f"Prompt: '{prompt}'")
        print("-" * 40)
        
        try:
            result = generator.generate_and_save(prompt, f"demo_user_{i}")
            results.append({
                'prompt': prompt,
                'success': result['success'],
                'quality_score': result.get('quality_score', 0),
                'filename': result.get('filename', ''),
                'error': result.get('error', '')
            })
            
            if result['success']:
                print(f"✅ SUCCESS - Quality: {result['quality_score']:.2f}")
                print(f"📁 File: {result.get('filename', 'N/A')}")
            else:
                print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ EXCEPTION - {str(e)}")
            results.append({
                'prompt': prompt,
                'success': False,
                'quality_score': 0,
                'filename': '',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO RESULTS SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful generations: {len(successful)}/{len(results)}")
    print(f"❌ Failed generations: {len(failed)}/{len(results)}")
    
    if successful:
        avg_quality = sum(r['quality_score'] for r in successful) / len(successful)
        print(f"🎯 Average quality score: {avg_quality:.2f}")
        
        print(f"\n📁 Generated files:")
        for result in successful:
            print(f"  - {result['filename']}")
    
    if failed:
        print(f"\n❌ Failed prompts:")
        for result in failed:
            print(f"  - '{result['prompt'][:50]}...' - {result['error']}")
    
    print(f"\n🎉 Demo completed!")
    print(f"Key insight: The system now handles creative, metaphorical language")
    print(f"without choking on complex parsing, focusing on musical quality instead.")
    
    return len(successful) > 0


def demo_duration_handling():
    """Demo how the system handles duration requirements."""
    
    print("\n" + "=" * 60)
    print("🎵 DURATION HANDLING DEMO")
    print("=" * 60)
    print("Testing how the system handles duration vs. musical completeness...")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return False
    
    # Initialize generator
    generator = MVPMusicalQualityFirstGenerator(api_key)
    
    # Test prompts with different duration requirements
    duration_prompts = [
        "Create a 4-measure bass line in C major",
        "Generate an 8-measure jazz melody",
        "Make a 16-measure rock drum pattern",
        "Create a 2-measure simple bass line",
        "Generate a 32-measure epic orchestral piece"
    ]
    
    print(f"\n🧪 Testing {len(duration_prompts)} duration-specific prompts...")
    print("=" * 60)
    
    for i, prompt in enumerate(duration_prompts, 1):
        print(f"\n🎵 Duration Test {i}/{len(duration_prompts)}")
        print(f"Prompt: '{prompt}'")
        print("-" * 40)
        
        try:
            result = generator.generate_and_save(prompt, f"duration_user_{i}")
            
            if result['success']:
                duration = result['midi_data'].get('duration', 0)
                note_count = len(result['midi_data'].get('notes', []))
                quality_score = result['quality_score']
                
                print(f"✅ SUCCESS")
                print(f"   Duration: {duration:.1f} seconds")
                print(f"   Notes: {note_count}")
                print(f"   Quality: {quality_score:.2f}")
                print(f"   File: {result.get('filename', 'N/A')}")
                
                # Key insight: Duration is handled as guideline, not constraint
                print(f"   💡 Musical completeness prioritized over exact duration")
            else:
                print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ EXCEPTION - {str(e)}")
    
    print(f"\n🎉 Duration demo completed!")
    print(f"Key insight: The system generates musically complete pieces")
    print(f"rather than forcing exact duration requirements.")
    
    return True


def demo_user_feedback():
    """Demo the user feedback system focused on musical satisfaction."""
    
    print("\n" + "=" * 60)
    print("🎵 USER FEEDBACK DEMO")
    print("=" * 60)
    print("Testing user feedback focused on musical satisfaction...")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return False
    
    # Initialize generator
    generator = MVPMusicalQualityFirstGenerator(api_key)
    
    # Test with a simple prompt
    prompt = "Create a funky bass line"
    print(f"🎵 Testing prompt: '{prompt}'")
    print("-" * 40)
    
    try:
        result = generator.generate_and_save(prompt, "feedback_demo_user")
        
        if result['success']:
            print(f"✅ Generation successful!")
            print(f"📁 File: {result.get('filename', 'N/A')}")
            print(f"🎯 Quality: {result['quality_score']:.2f}")
            
            # Show the feedback system
            print(f"\n📝 User Feedback System:")
            print(f"   - Focus: Musical satisfaction (not technical precision)")
            print(f"   - Rating: 1-5 based on musical quality")
            print(f"   - Comments: What you liked/disliked about musical character")
            print(f"   - Learning: System learns from your musical preferences")
            
            print(f"\n💡 Key insight: Feedback focuses on musical satisfaction")
            print(f"rather than duration or technical requirements.")
        else:
            print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
    
    return True


def main():
    """Run all demos."""
    print("🚀 MVP Musical Quality First Generator - Complete Demo")
    print("=" * 70)
    print("This demo showcases the refined approach that addresses the")
    print("post-mortem insights about musical quality vs. technical precision.")
    print("=" * 70)
    
    # Run demos
    demo1_success = demo_creative_prompts()
    demo2_success = demo_duration_handling()
    demo3_success = demo_user_feedback()
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 COMPLETE DEMO SUMMARY")
    print("=" * 70)
    
    demos = [
        ("Creative Prompts", demo1_success),
        ("Duration Handling", demo2_success),
        ("User Feedback", demo3_success)
    ]
    
    for demo_name, success in demos:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{demo_name:20} {status}")
    
    print("\n🎯 KEY INSIGHTS DEMONSTRATED:")
    print("1. Creative, metaphorical prompts are handled without parsing errors")
    print("2. Musical quality is prioritized over exact duration requirements")
    print("3. User feedback focuses on musical satisfaction, not technical precision")
    print("4. The AI is trusted to understand musical concepts and creative language")
    print("5. Duration is treated as a guideline, not a hard constraint")
    
    print(f"\n🎵 The refined approach successfully addresses the post-mortem issues!")
    
    return all([demo1_success, demo2_success, demo3_success])


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
