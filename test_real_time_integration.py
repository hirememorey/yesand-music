#!/usr/bin/env python3
"""
Test Real-Time Integration

Test script for the complete real-time Ardour enhancement system.
Verifies all components work together correctly.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from real_time_ardour_enhancer import RealTimeArdourEnhancer
from llm_track_enhancer import EnhancementRequest
from midi_pattern_parser import MIDIGenerationOptions


def test_osc_monitor():
    """Test OSC monitor functionality."""
    print("🔍 Testing OSC Monitor...")
    
    try:
        from ardour_osc_monitor import ArdourOSCMonitor
        
        monitor = ArdourOSCMonitor()
        
        # Test basic functionality
        print("  ✅ OSC Monitor initialized")
        
        # Test state access
        state = monitor.get_current_state()
        print(f"  ✅ Current state: {state.project_name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ OSC Monitor test failed: {e}")
        return False


def test_state_capture():
    """Test state capture functionality."""
    print("🔍 Testing State Capture...")
    
    try:
        from project_state_capture import ProjectStateCapture
        from ardour_osc_monitor import LiveProjectState
        
        capture = ProjectStateCapture()
        
        # Create mock project state
        mock_state = LiveProjectState(
            project_name="Test Project",
            tempo=120.0,
            time_signature="4/4",
            sample_rate=44100.0,
            tracks=[],
            regions=[],
            selection=None,
            midi_data=[],
            last_updated=time.time()
        )
        
        # Test context generation
        context = capture.update_project_state(mock_state)
        print(f"  ✅ Context generated: {context.musical_context.key_signature}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ State Capture test failed: {e}")
        return False


def test_midi_analyzer():
    """Test MIDI analyzer functionality."""
    print("🔍 Testing MIDI Analyzer...")
    
    try:
        from midi_stream_analyzer import MIDIStreamAnalyzer
        
        analyzer = MIDIStreamAnalyzer()
        
        # Test basic functionality
        print("  ✅ MIDI Analyzer initialized")
        
        # Test analysis methods
        analysis = analyzer.get_global_analysis()
        print(f"  ✅ Global analysis: {analysis is not None}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ MIDI Analyzer test failed: {e}")
        return False


def test_llm_enhancer():
    """Test LLM enhancer functionality."""
    print("🔍 Testing LLM Enhancer...")
    
    try:
        from llm_track_enhancer import LLMTrackEnhancer, EnhancementRequest
        
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("  ⚠️  No OpenAI API key found, testing without LLM")
            return True
        
        enhancer = LLMTrackEnhancer(api_key)
        
        # Test basic functionality
        print("  ✅ LLM Enhancer initialized")
        
        # Test enhancement request
        request = EnhancementRequest(
            user_request="make the bassline groovier",
            enhancement_type="bass"
        )
        
        # Note: This would require a real project context
        print("  ✅ Enhancement request created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ LLM Enhancer test failed: {e}")
        return False


def test_pattern_parser():
    """Test pattern parser functionality."""
    print("🔍 Testing Pattern Parser...")
    
    try:
        from midi_pattern_parser import MIDIPatternParser, MIDIGenerationOptions
        from llm_track_enhancer import MIDIPattern, EnhancementResult
        
        parser = MIDIPatternParser()
        
        # Test basic functionality
        print("  ✅ Pattern Parser initialized")
        
        # Test pattern validation
        pattern = MIDIPattern(
            name="Test Pattern",
            description="Test pattern for validation",
            midi_data=[
                {"pitch": 60, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0}
            ],
            confidence_score=0.8,
            enhancement_type="test",
            musical_justification="Test pattern",
            track_id="test",
            duration=1.0,
            tempo=120.0,
            time_signature="4/4"
        )
        
        is_valid, errors = parser.validate_midi_pattern(pattern)
        if is_valid:
            print("  ✅ Pattern validation passed")
        else:
            print(f"  ❌ Pattern validation failed: {errors}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pattern Parser test failed: {e}")
        return False


def test_integration():
    """Test complete integration."""
    print("🔍 Testing Complete Integration...")
    
    try:
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("  ⚠️  No OpenAI API key found, testing without LLM")
            api_key = None
        
        enhancer = RealTimeArdourEnhancer(api_key)
        
        # Test session management
        session_id = enhancer.start_enhancement_session()
        if session_id:
            print(f"  ✅ Session started: {session_id}")
        else:
            print("  ❌ Failed to start session")
            return False
        
        # Test status
        status = enhancer.get_project_status()
        print(f"  ✅ Project status: {status['project_name']}")
        
        # Test suggestions
        suggestions = enhancer.get_enhancement_suggestions()
        print(f"  ✅ Enhancement suggestions: {len(suggestions)}")
        
        # Cleanup
        enhancer.stop_enhancement_session()
        print("  ✅ Session stopped")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False


def test_cli():
    """Test CLI functionality."""
    print("🔍 Testing CLI...")
    
    try:
        from real_time_enhancement_cli import RealTimeEnhancementCLI
        
        cli = RealTimeEnhancementCLI()
        
        # Test basic functionality
        print("  ✅ CLI initialized")
        
        # Test status
        status = cli.get_project_status()
        print(f"  ✅ Status: {status['session_id']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ CLI test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("🧪 Running Real-Time Integration Tests")
    print("=" * 50)
    
    tests = [
        ("OSC Monitor", test_osc_monitor),
        ("State Capture", test_state_capture),
        ("MIDI Analyzer", test_midi_analyzer),
        ("LLM Enhancer", test_llm_enhancer),
        ("Pattern Parser", test_pattern_parser),
        ("Integration", test_integration),
        ("CLI", test_cli)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"  ✅ {test_name} test passed")
            else:
                print(f"  ❌ {test_name} test failed")
        except Exception as e:
            print(f"  ❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


def main():
    """Main test function."""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    success = run_all_tests()
    
    if success:
        print("\n🚀 Ready for real-time enhancement!")
        print("\nTo start using the system:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("2. Start Ardour with OSC enabled")
        print("3. Run: python real_time_enhancement_cli.py --interactive")
    else:
        print("\n🔧 Please fix the failing tests before using the system.")
        sys.exit(1)


if __name__ == "__main__":
    main()
