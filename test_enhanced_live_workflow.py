#!/usr/bin/env python3
"""
Test Enhanced Live MIDI Streaming Workflow

This script demonstrates the enhanced live MIDI streaming capabilities
with improved pattern generation and real-time editing.
"""

import os
import sys
import time
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from live_conversation_workflow import LiveConversationWorkflow
from ardour_live_integration import ArdourLiveIntegration, MIDIStreamGenerator
from live_editing_engine import LiveEditingEngine, EditingOperation, LiveEditCommandBuilder

def test_midi_generation():
    """Test the enhanced MIDI generation capabilities"""
    print("🎵 Testing Enhanced MIDI Generation")
    print("=" * 50)
    
    generator = MIDIStreamGenerator()
    
    # Test different pattern types and styles
    test_cases = [
        ("bass", "funky", "C", 4.0),
        ("bass", "jazz", "F", 4.0),
        ("bass", "rock", "G", 4.0),
        ("melody", "jazz", "C", 4.0),
        ("melody", "classical", "D", 4.0),
        ("melody", "blues", "A", 4.0),
        ("drums", "rock", None, 4.0),
        ("drums", "jazz", None, 4.0),
        ("drums", "funk", None, 4.0),
    ]
    
    for pattern_type, style, key, duration in test_cases:
        print(f"\n🎼 Testing {style} {pattern_type} in {key or 'N/A'}")
        
        try:
            if pattern_type == "bass":
                stream = generator.generate_bassline_stream(style, key, duration)
            elif pattern_type == "melody":
                stream = generator.generate_melody_stream(style, key, duration)
            elif pattern_type == "drums":
                stream = generator.generate_drum_stream(style, duration)
            else:
                continue
            
            # Count events
            event_count = 0
            for event in stream:
                event_count += 1
                if event_count > 20:  # Limit for testing
                    break
            
            print(f"  ✅ Generated {event_count} MIDI events")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ MIDI Generation Test Complete")

def test_live_editing():
    """Test the enhanced live editing capabilities"""
    print("\n🔧 Testing Enhanced Live Editing")
    print("=" * 50)
    
    engine = LiveEditingEngine()
    
    # Test different editing operations
    test_operations = [
        (EditingOperation.ADD_SWING, {"swing_ratio": 0.7}),
        (EditingOperation.ADD_ACCENT, {"accent_amount": 20}),
        (EditingOperation.HUMANIZE, {"timing_variation": 0.05, "velocity_variation": 0.1}),
        (EditingOperation.BRIGHTEN, {"semitones": 2, "velocity_boost": 10}),
        (EditingOperation.DARKEN, {"semitones": 2, "velocity_reduction": 10}),
        (EditingOperation.ADD_GROOVE, {"groove_level": 0.7}),
        (EditingOperation.CHANGE_STYLE, {"new_style": "jazz"}),
        (EditingOperation.ADD_HARMONY, {"harmony_type": "chords"}),
        (EditingOperation.REMOVE_NOTES, {"removal_percentage": 0.3}),
        (EditingOperation.ADD_NOTES, {"addition_percentage": 0.3}),
        (EditingOperation.CHANGE_TEMPO, {"tempo_change": 10}),
        (EditingOperation.ADD_REVERB, {"reverb_amount": 0.5}),
        (EditingOperation.ADD_DELAY, {"delay_amount": 0.3, "delay_time": 0.25}),
    ]
    
    for operation, parameters in test_operations:
        print(f"\n🎛️ Testing {operation.value}")
        
        try:
            # Create command
            command = (LiveEditCommandBuilder()
                     .set_operation(operation)
                     .set_target_track("test_track")
                     .set_intensity(0.8)
                     .build())
            
            # Add parameters
            for key, value in parameters.items():
                command.parameters[key] = value
            
            # Apply edit
            result = engine.apply_live_edit(command)
            
            if result.success:
                print(f"  ✅ {result.explanation}")
                print(f"  📊 Changes applied: {result.changes_applied}")
                print(f"  🎯 Confidence: {result.confidence:.2f}")
            else:
                print(f"  ❌ Failed: {result.explanation}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Live Editing Test Complete")

def test_conversation_workflow():
    """Test the enhanced conversation workflow"""
    print("\n💬 Testing Enhanced Conversation Workflow")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI API key not found. Skipping conversation workflow test.")
        print("   Set OPENAI_API_KEY environment variable to test conversation features.")
        return
    
    try:
        workflow = LiveConversationWorkflow(api_key)
        
        # Test conversation inputs
        test_inputs = [
            "Give me a funky bassline",
            "Make it more complex",
            "Add some swing to it",
            "Make it brighter",
            "Change to jazz style",
            "Add harmony",
            "Make it groove better",
            "Add reverb",
            "Create a jazz melody",
            "Make it darker",
        ]
        
        print("🎵 Testing conversation inputs...")
        
        for user_input in test_inputs:
            print(f"\n👤 User: {user_input}")
            
            try:
                response = workflow.process_conversation(user_input)
                print(f"🤖 AI: {response.message}")
                
                if response.musical_action:
                    print(f"🎼 Action: {response.musical_action.get('action', 'unknown')}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n✅ Conversation Workflow Test Complete")
        
    except Exception as e:
        print(f"❌ Error initializing conversation workflow: {e}")

def test_ardour_integration():
    """Test Ardour integration (without actually connecting)"""
    print("\n🎛️ Testing Ardour Integration")
    print("=" * 50)
    
    try:
        # Test Ardour integration initialization
        ardour = ArdourLiveIntegration()
        
        print(f"📁 Ardour path: {ardour.ardour_path}")
        print(f"🎵 MIDI port: {ardour.midi_port}")
        
        # Test track creation
        track_id = ardour.create_midi_track("Test Track")
        if track_id:
            print(f"✅ Created track: {track_id}")
        else:
            print("❌ Failed to create track")
        
        # Test live editing session
        if track_id:
            success = ardour.enable_live_editing(track_id)
            if success:
                print("✅ Enabled live editing")
            else:
                print("❌ Failed to enable live editing")
        
        # Test track listing
        tracks = ardour.get_live_tracks()
        print(f"📋 Found {len(tracks)} tracks")
        
        print("\n✅ Ardour Integration Test Complete")
        
    except Exception as e:
        print(f"❌ Error testing Ardour integration: {e}")

def demonstrate_workflow():
    """Demonstrate the complete musician workflow"""
    print("\n🎵 Complete Musician Workflow Demonstration")
    print("=" * 60)
    
    print("""
    This demonstrates how a musician would use the enhanced live MIDI streaming:
    
    1. 🎵 Generate Musical Content
       "Give me a funky bassline" → MIDI appears in Ardour in real-time
    
    2. 🔧 Real-Time Editing
       "Make it more complex" → Existing MIDI gets modified live
       "Add some swing" → Timing changes applied immediately
       "Make it brighter" → Transpose up and boost velocity
    
    3. 🎨 Style Changes
       "Change to jazz style" → Musical style transformation
       "Add harmony" → Harmonic elements added
    
    4. 🎛️ Effects and Processing
       "Add reverb" → Audio effects applied
       "Make it groove better" → Groove enhancement
    
    5. 📝 Manual Editing in Ardour
       Musician can now edit the generated MIDI manually in Ardour
       - Move notes around
       - Change velocities
       - Copy and paste sections
       - Apply Ardour's built-in effects
    
    6. 🔄 Further AI Enhancement
       "Make it darker" → AI modifies the manually edited content
       "Add delay" → More effects applied
    
    The result is a seamless workflow where AI generates the foundation,
    musician refines it manually, and AI continues to enhance the work.
    """)

def main():
    """Run all tests"""
    print("🚀 Enhanced Live MIDI Streaming - Test Suite")
    print("=" * 60)
    
    # Run tests
    test_midi_generation()
    test_live_editing()
    test_conversation_workflow()
    test_ardour_integration()
    demonstrate_workflow()
    
    print("\n🎉 All Tests Complete!")
    print("\nTo use the enhanced live MIDI streaming:")
    print("1. Start Ardour and create a MIDI track")
    print("2. Run: python live_control_plane_cli.py")
    print("3. Try: 'Give me a funky bassline'")
    print("4. Then: 'Make it more complex'")
    print("5. Edit manually in Ardour as needed")

if __name__ == "__main__":
    main()
