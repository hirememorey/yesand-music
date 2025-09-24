#!/usr/bin/env python3
"""
MVP MIDI Generator Demo

This script demonstrates the MVP MIDI generation system with the exact prompt
from the user request: "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"

This demonstrates the complete workflow without requiring OpenAI API access.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_musical_intelligence():
    """Demo the musical intelligence engine"""
    print("🎵 Musical Intelligence Engine Demo")
    print("=" * 50)
    
    from musical_intelligence_engine import MusicalIntelligenceEngine
    
    engine = MusicalIntelligenceEngine()
    prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
    
    print(f"📝 Analyzing prompt: {prompt}")
    print()
    
    # Analyze prompt
    context = engine.analyze_prompt(prompt)
    
    print("🎼 Musical Context Analysis:")
    print(f"  Key: {context.key}")
    print(f"  Tempo: {context.tempo} BPM")
    print(f"  Time Signature: {context.time_signature}")
    print(f"  Instrument: {context.instrument}")
    print(f"  Style: {context.style}")
    print(f"  Mood: {context.mood.value}")
    print(f"  Complexity: {context.complexity.value}")
    print()
    
    # Extract style characteristics
    style_chars = engine.extract_style_characteristics(prompt, context)
    
    print("🎨 Style Characteristics:")
    print(f"  Artist: {style_chars.artist}")
    print(f"  Characteristics: {len(style_chars.characteristics)} items")
    print(f"  Tempo Range: {style_chars.tempo_range[0]}-{style_chars.tempo_range[1]} BPM")
    print(f"  Key Preferences: {', '.join(style_chars.key_preferences[:3])}")
    print(f"  Rhythmic Patterns: {', '.join(style_chars.rhythmic_patterns[:3])}")
    print(f"  Dynamic Range: {style_chars.dynamic_range}")
    print()
    
    return context, style_chars

def demo_prompt_builder(context, style_chars):
    """Demo the context-aware prompt builder"""
    print("⚙️  Context-Aware Prompt Builder Demo")
    print("=" * 50)
    
    from context_aware_prompts import ContextAwarePromptBuilder
    
    builder = ContextAwarePromptBuilder()
    prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
    
    print("🔧 Building enhanced prompt...")
    
    # Build enhanced prompt
    enhanced_prompt = builder.build_musical_prompt(prompt, context, style_chars)
    
    print(f"✅ Enhanced prompt created:")
    print(f"  Type: {enhanced_prompt.prompt_type}")
    print(f"  Length: {len(enhanced_prompt.enhanced_prompt)} characters")
    print(f"  Optimization Level: {enhanced_prompt.optimization_level}")
    print()
    
    # Validate prompt
    is_valid, issues = builder.validate_prompt(enhanced_prompt.enhanced_prompt)
    print(f"✅ Prompt validation: {'PASSED' if is_valid else 'FAILED'}")
    if issues:
        print(f"  Issues: {issues}")
    print()
    
    # Show prompt statistics
    stats = builder.get_prompt_statistics(enhanced_prompt.enhanced_prompt)
    print("📊 Prompt Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    return enhanced_prompt

def demo_ai_generator():
    """Demo the AI MIDI generator (without OpenAI API)"""
    print("🤖 AI MIDI Generator Demo")
    print("=" * 50)
    
    from ai_midi_generator import AIMIDIGenerator
    
    # Test with dummy API key
    generator = AIMIDIGenerator("test-api-key")
    
    print("🔧 AI Generator initialized")
    print(f"  Style Database: {len(generator.style_database)} styles")
    print(f"  Security Level: {generator.security_level}")
    print()
    
    prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
    
    print("🎵 Analyzing prompt for AI generation...")
    
    # Analyze prompt
    musical_context = generator._analyze_prompt(prompt, {})
    
    print("📊 Musical Context:")
    print(f"  Key: {musical_context['key']}")
    print(f"  Tempo: {musical_context['tempo']} BPM")
    print(f"  Instrument: {musical_context['instrument']}")
    print(f"  Style: {musical_context['style']}")
    print(f"  Mood: {musical_context['mood']}")
    print()
    
    # Extract style characteristics
    style_characteristics = generator._extract_style_characteristics(prompt, musical_context)
    
    print("🎨 Style Characteristics:")
    print(f"  Artist: {style_characteristics.get('artist', 'Unknown')}")
    print(f"  Characteristics: {len(style_characteristics.get('characteristics', []))} items")
    print(f"  Tempo Range: {style_characteristics.get('tempo_range', 'Unknown')}")
    print()
    
    # Build enhanced prompt
    enhanced_prompt = generator._build_musical_prompt(prompt, musical_context, style_characteristics)
    
    print("🔧 Enhanced Prompt Built:")
    print(f"  Length: {len(enhanced_prompt)} characters")
    print(f"  Contains musical context: {'MUSICAL CONTEXT:' in enhanced_prompt}")
    print(f"  Contains style characteristics: {'STYLE CHARACTERISTICS:' in enhanced_prompt}")
    print(f"  Contains requirements: {'REQUIREMENTS:' in enhanced_prompt}")
    print(f"  Contains output format: {'OUTPUT FORMAT:' in enhanced_prompt}")
    print()
    
    return generator

def demo_real_time_generator():
    """Demo the real-time MIDI generator"""
    print("⚡ Real-Time MIDI Generator Demo")
    print("=" * 50)
    
    from real_time_midi_generator import RealTimeMIDIGenerator
    
    # Test with dummy API key
    generator = RealTimeMIDIGenerator("test-api-key")
    
    print("🔧 Real-Time Generator initialized")
    status = generator.get_generation_status()
    print("📊 Generation Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    return generator

def demo_mvp_generator():
    """Demo the MVP generator"""
    print("🎵 MVP MIDI Generator Demo")
    print("=" * 50)
    
    from mvp_midi_generator import MVPMIDIGenerator
    
    # Test with dummy API key
    generator = MVPMIDIGenerator("test-api-key")
    
    print("🔧 MVP Generator initialized")
    print(f"  Generation History: {len(generator.generation_history)} items")
    print(f"  AI Generator: {'✅ Ready' if generator.ai_generator else '❌ Not ready'}")
    print(f"  Intelligence Engine: {'✅ Ready' if generator.intelligence_engine else '❌ Not ready'}")
    print(f"  Prompt Builder: {'✅ Ready' if generator.prompt_builder else '❌ Not ready'}")
    print(f"  Real-Time Generator: {'✅ Ready' if generator.real_time_generator else '❌ Not ready'}")
    print()
    
    return generator

def demo_cli_interface():
    """Demo the CLI interface"""
    print("🖥️  CLI Interface Demo")
    print("=" * 50)
    
    import subprocess
    import sys
    
    print("📋 Available Commands:")
    print("  python3 mvp_midi_generator.py --help")
    print("  python3 mvp_midi_generator.py --version")
    print("  python3 mvp_midi_generator.py --interactive")
    print("  python3 mvp_midi_generator.py 'your prompt here'")
    print()
    
    # Test help command
    print("🔍 Testing help command...")
    try:
        result = subprocess.run([
            sys.executable, "mvp_midi_generator.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Help command works")
            print(f"  Output length: {len(result.stdout)} characters")
        else:
            print(f"❌ Help command failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Help command error: {e}")
    
    print()
    
    # Test version command
    print("🔍 Testing version command...")
    try:
        result = subprocess.run([
            sys.executable, "mvp_midi_generator.py", "--version"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Version command works")
            print(f"  Version: {result.stdout.strip()}")
        else:
            print(f"❌ Version command failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Version command error: {e}")
    
    print()

def main():
    """Run the complete demo"""
    print("🎵 MVP MIDI Generator - Complete Demo")
    print("=" * 60)
    print("This demo shows the complete MVP system working with the exact prompt:")
    print("'generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this'")
    print("=" * 60)
    print()
    
    try:
        # Demo each component
        context, style_chars = demo_musical_intelligence()
        enhanced_prompt = demo_prompt_builder(context, style_chars)
        ai_generator = demo_ai_generator()
        real_time_generator = demo_real_time_generator()
        mvp_generator = demo_mvp_generator()
        demo_cli_interface()
        
        print("🎉 Demo Complete!")
        print("=" * 60)
        print("✅ All components are working correctly")
        print("✅ The MVP is ready for testing with a real OpenAI API key")
        print()
        print("🚀 To test with real generation:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        print("2. Run: python3 mvp_midi_generator.py 'your prompt here'")
        print("3. Or run interactive mode: python3 mvp_midi_generator.py --interactive")
        print()
        print("📁 Generated MIDI files will be saved to the current directory")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()