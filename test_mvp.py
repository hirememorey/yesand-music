#!/usr/bin/env python3
"""
Test script for MVP MIDI Generator

This script tests the MVP MIDI generation system to ensure all components
are working correctly before user testing.
"""

import os
import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from ai_midi_generator import AIMIDIGenerator
        print("  ✅ ai_midi_generator imported")
    except ImportError as e:
        print(f"  ❌ ai_midi_generator import failed: {e}")
        return False
    
    try:
        from musical_intelligence_engine import MusicalIntelligenceEngine
        print("  ✅ musical_intelligence_engine imported")
    except ImportError as e:
        print(f"  ❌ musical_intelligence_engine import failed: {e}")
        return False
    
    try:
        from context_aware_prompts import ContextAwarePromptBuilder
        print("  ✅ context_aware_prompts imported")
    except ImportError as e:
        print(f"  ❌ context_aware_prompts import failed: {e}")
        return False
    
    try:
        from real_time_midi_generator import RealTimeMIDIGenerator
        print("  ✅ real_time_midi_generator imported")
    except ImportError as e:
        print(f"  ❌ real_time_midi_generator import failed: {e}")
        return False
    
    try:
        from mvp_midi_generator import MVPMIDIGenerator
        print("  ✅ mvp_midi_generator imported")
    except ImportError as e:
        print(f"  ❌ mvp_midi_generator import failed: {e}")
        return False
    
    return True

def test_musical_intelligence():
    """Test musical intelligence engine"""
    print("\n🎵 Testing Musical Intelligence Engine...")
    
    try:
        from musical_intelligence_engine import MusicalIntelligenceEngine
        
        engine = MusicalIntelligenceEngine()
        
        # Test prompt analysis
        prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
        context = engine.analyze_prompt(prompt)
        
        print(f"  ✅ Key: {context.key}")
        print(f"  ✅ Tempo: {context.tempo}")
        print(f"  ✅ Instrument: {context.instrument}")
        print(f"  ✅ Style: {context.style}")
        print(f"  ✅ Mood: {context.mood.value}")
        print(f"  ✅ Complexity: {context.complexity.value}")
        
        # Test style characteristics
        style_chars = engine.extract_style_characteristics(prompt, context)
        print(f"  ✅ Style Artist: {style_chars.artist}")
        print(f"  ✅ Characteristics: {len(style_chars.characteristics)} items")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Musical Intelligence Engine test failed: {e}")
        return False

def test_prompt_builder():
    """Test context-aware prompt builder"""
    print("\n⚙️  Testing Context-Aware Prompt Builder...")
    
    try:
        from musical_intelligence_engine import MusicalIntelligenceEngine
        from context_aware_prompts import ContextAwarePromptBuilder
        
        engine = MusicalIntelligenceEngine()
        builder = ContextAwarePromptBuilder()
        
        # Test prompt analysis
        prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
        context = engine.analyze_prompt(prompt)
        style_chars = engine.extract_style_characteristics(prompt, context)
        
        # Test prompt building
        enhanced_prompt = builder.build_musical_prompt(prompt, context, style_chars)
        
        print(f"  ✅ Enhanced prompt length: {len(enhanced_prompt.enhanced_prompt)} characters")
        print(f"  ✅ Prompt type: {enhanced_prompt.prompt_type}")
        print(f"  ✅ Optimization level: {enhanced_prompt.optimization_level}")
        
        # Test prompt validation
        is_valid, issues = builder.validate_prompt(enhanced_prompt.enhanced_prompt)
        if is_valid:
            print("  ✅ Prompt validation passed")
        else:
            print(f"  ⚠️  Prompt validation issues: {issues}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Context-Aware Prompt Builder test failed: {e}")
        return False

def test_ai_generator():
    """Test AI MIDI generator (without OpenAI API)"""
    print("\n🤖 Testing AI MIDI Generator...")
    
    try:
        from ai_midi_generator import AIMIDIGenerator
        
        # Test with dummy API key
        generator = AIMIDIGenerator("test-api-key")
        
        print("  ✅ AI Generator initialized")
        print(f"  ✅ Style database: {len(generator.style_database)} styles")
        
        # Test prompt analysis
        prompt = "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
        musical_context = generator._analyze_prompt(prompt, {})
        
        print(f"  ✅ Musical context: {musical_context['key']}, {musical_context['tempo']} BPM")
        print(f"  ✅ Style: {musical_context['style']}")
        print(f"  ✅ Mood: {musical_context['mood']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ AI MIDI Generator test failed: {e}")
        return False

def test_real_time_generator():
    """Test real-time MIDI generator"""
    print("\n⚡ Testing Real-Time MIDI Generator...")
    
    try:
        from real_time_midi_generator import RealTimeMIDIGenerator
        
        # Test with dummy API key
        generator = RealTimeMIDIGenerator("test-api-key")
        
        print("  ✅ Real-Time Generator initialized")
        print(f"  ✅ Generation status: {generator.get_generation_status()}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Real-Time MIDI Generator test failed: {e}")
        return False

def test_mvp_generator():
    """Test MVP generator (without OpenAI API)"""
    print("\n🎵 Testing MVP MIDI Generator...")
    
    try:
        from mvp_midi_generator import MVPMIDIGenerator
        
        # Test with dummy API key
        generator = MVPMIDIGenerator("test-api-key")
        
        print("  ✅ MVP Generator initialized")
        print(f"  ✅ Generation history: {len(generator.generation_history)} items")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MVP MIDI Generator test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface"""
    print("\n🖥️  Testing CLI Interface...")
    
    try:
        import subprocess
        import sys
        
        # Test help command
        result = subprocess.run([
            sys.executable, "mvp_midi_generator.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ CLI help command works")
        else:
            print(f"  ❌ CLI help command failed: {result.stderr}")
            return False
        
        # Test version command
        result = subprocess.run([
            sys.executable, "mvp_midi_generator.py", "--version"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ CLI version command works")
        else:
            print(f"  ❌ CLI version command failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ CLI Interface test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MVP MIDI Generator Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_musical_intelligence,
        test_prompt_builder,
        test_ai_generator,
        test_real_time_generator,
        test_mvp_generator,
        test_cli_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MVP is ready for testing.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before testing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)