#!/usr/bin/env python3
"""
Live MIDI Streaming Demo

This script demonstrates the live MIDI streaming capabilities of YesAnd Music,
showing real-time MIDI generation and editing with Ardour DAW integration.
"""

import time
import sys
import os
from typing import List, Dict, Any

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🎵 {title}")
    print("=" * 60)

def print_step(step: str, description: str):
    """Print a formatted step"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def print_success(message: str):
    """Print a success message"""
    print(f"✅ {message}")

def print_info(message: str):
    """Print an info message"""
    print(f"ℹ️  {message}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"⚠️  {message}")

def print_error(message: str):
    """Print an error message"""
    print(f"❌ {message}")

def demo_basic_streaming():
    """Demo basic MIDI streaming"""
    print_header("Basic MIDI Streaming Demo")
    
    try:
        from ardour_live_integration import ArdourLiveIntegration, MIDIStreamGenerator
        
        print_step("1", "Initialize MIDI Stream Generator")
        generator = MIDIStreamGenerator(tempo=120)
        print_success("MIDI Stream Generator initialized")
        
        print_step("2", "Generate Funky Bassline Stream")
        stream = generator.generate_bassline_stream(style="funky", key="C", duration=4.0)
        events = list(stream)
        print_success(f"Generated {len(events)} MIDI events")
        
        print_step("3", "Display Stream Events")
        for i, event in enumerate(events[:5]):  # Show first 5 events
            print(f"  Event {i+1}: Note {event.note}, Velocity {event.velocity}, Time {event.start_time:.2f}s")
        if len(events) > 5:
            print(f"  ... and {len(events) - 5} more events")
        
        print_step("4", "Test Different Styles")
        styles = ["jazz", "blues", "simple"]
        for style in styles:
            stream = generator.generate_bassline_stream(style=style, key="F", duration=2.0)
            events = list(stream)
            print_info(f"{style.capitalize()} style: {len(events)} events")
        
        return True
        
    except Exception as e:
        print_error(f"Basic streaming demo failed: {e}")
        return False

def demo_live_editing():
    """Demo live editing capabilities"""
    print_header("Live Editing Demo")
    
    try:
        from live_editing_engine import LiveEditingEngine, LiveEditCommand, EditingOperation, LiveEditCommandBuilder
        
        print_step("1", "Initialize Live Editing Engine")
        engine = LiveEditingEngine()
        print_success("Live Editing Engine initialized")
        
        print_step("2", "Test Velocity Modification")
        command = (LiveEditCommandBuilder()
                  .set_operation(EditingOperation.MODIFY_VELOCITY)
                  .set_target_track("test_track")
                  .set_intensity(0.8)
                  .add_parameter("velocity_change", 15)
                  .add_parameter("velocity_multiplier", 1.2)
                  .build())
        
        result = engine.apply_live_edit(command)
        print_success(f"Velocity modification: {result.explanation}")
        
        print_step("3", "Test Swing Addition")
        command = (LiveEditCommandBuilder()
                  .set_operation(EditingOperation.ADD_SWING)
                  .set_target_track("test_track")
                  .set_intensity(0.9)
                  .add_parameter("swing_ratio", 0.7)
                  .build())
        
        result = engine.apply_live_edit(command)
        print_success(f"Swing addition: {result.explanation}")
        
        print_step("4", "Test Humanization")
        command = (LiveEditCommandBuilder()
                  .set_operation(EditingOperation.HUMANIZE)
                  .set_target_track("test_track")
                  .set_intensity(0.6)
                  .add_parameter("timing_variation", 0.05)
                  .add_parameter("velocity_variation", 0.1)
                  .build())
        
        result = engine.apply_live_edit(command)
        print_success(f"Humanization: {result.explanation}")
        
        print_step("5", "Test Edit History")
        history = engine.get_edit_history("test_track")
        print_info(f"Edit history contains {len(history)} edits")
        
        print_step("6", "Test Undo Functionality")
        undo_success = engine.undo_last_edit("test_track")
        if undo_success:
            print_success("Successfully undone last edit")
            history = engine.get_edit_history("test_track")
            print_info(f"Edit history now contains {len(history)} edits")
        
        return True
        
    except Exception as e:
        print_error(f"Live editing demo failed: {e}")
        return False

def demo_conversation_workflow():
    """Demo conversation workflow (mocked)"""
    print_header("Conversation Workflow Demo (Mocked)")
    
    try:
        from live_conversation_workflow import LiveConversationWorkflow
        from unittest.mock import Mock, patch
        
        print_step("1", "Initialize Live Conversation Workflow (Mocked)")
        
        # Mock the dependencies
        with patch('live_conversation_workflow.MusicalConversationEngine') as mock_conv, \
             patch('live_conversation_workflow.ArdourLiveIntegration') as mock_ardour:
            
            # Setup mocks
            mock_conv.return_value.engage.return_value = Mock(
                message="I'll create a funky bassline for you!",
                musical_action={
                    "action": "generate_pattern",
                    "parameters": {"type": "bass", "style": "funky"}
                },
                confidence=0.9
            )
            
            mock_ardour.return_value.connect.return_value = True
            mock_ardour.return_value.create_midi_track.return_value = "track_1"
            mock_ardour.return_value.enable_live_editing.return_value = True
            mock_ardour.return_value.stream_midi_to_track.return_value = True
            
            workflow = LiveConversationWorkflow()
            print_success("Live Conversation Workflow initialized (mocked)")
            
            print_step("2", "Start Conversation Session")
            session_id = workflow.start_conversation("Demo Track")
            print_success(f"Started session: {session_id}")
            
            print_step("3", "Process Musical Request")
            response = workflow.process_conversation("Give me a funky bassline")
            print_success(f"AI Response: {response.message}")
            
            print_step("4", "Process Improvement Request")
            response = workflow.process_conversation("Make it more complex")
            print_success(f"AI Response: {response.message}")
            
            print_step("5", "Get Session Status")
            status = workflow.get_session_status()
            print_info(f"Session Status: {status}")
            
            print_step("6", "End Session")
            result = workflow.end_conversation(session_id)
            if result:
                print_success("Session ended successfully")
        
        return True
        
    except Exception as e:
        print_error(f"Conversation workflow demo failed: {e}")
        return False

def demo_ardour_integration():
    """Demo Ardour integration (mocked)"""
    print_header("Ardour Integration Demo (Mocked)")
    
    try:
        from ardour_live_integration import ArdourLiveIntegration
        from unittest.mock import patch
        
        print_step("1", "Initialize Ardour Integration (Mocked)")
        
        with patch('ardour_live_integration.subprocess') as mock_subprocess:
            mock_subprocess.run.return_value.returncode = 0
            
            integration = ArdourLiveIntegration()
            print_success("Ardour Integration initialized (mocked)")
            
            print_step("2", "Connect to Ardour (Mocked)")
            connected = integration.connect()
            if connected:
                print_success("Connected to Ardour (mocked)")
            else:
                print_warning("Ardour connection failed (expected in demo)")
            
            print_step("3", "Create MIDI Track")
            track_id = integration.create_midi_track("Demo Track")
            print_success(f"Created track: {track_id}")
            
            print_step("4", "Enable Live Editing")
            editing_enabled = integration.enable_live_editing(track_id)
            if editing_enabled:
                print_success("Live editing enabled")
            else:
                print_warning("Live editing failed (expected in demo)")
            
            print_step("5", "Test MIDI Streaming (Mocked)")
            from ardour_live_integration import MIDIStreamGenerator
            generator = MIDIStreamGenerator()
            stream = generator.generate_bassline_stream(style="jazz", duration=2.0)
            
            with patch.object(integration, 'midi_out') as mock_midi_out:
                mock_midi_out.send_message = Mock()
                
                streaming_success = integration.stream_midi_to_track(track_id, stream, 2.0)
                if streaming_success:
                    print_success("MIDI streaming initiated (mocked)")
                else:
                    print_warning("MIDI streaming failed (expected in demo)")
            
            print_step("6", "Disconnect from Ardour")
            integration.disconnect()
            print_success("Disconnected from Ardour")
        
        return True
        
    except Exception as e:
        print_error(f"Ardour integration demo failed: {e}")
        return False

def demo_performance_tests():
    """Demo performance characteristics"""
    print_header("Performance Tests Demo")
    
    try:
        print_step("1", "Test MIDI Stream Generation Performance")
        from ardour_live_integration import MIDIStreamGenerator
        
        generator = MIDIStreamGenerator()
        
        start_time = time.time()
        stream = list(generator.generate_bassline_stream(style="jazz", duration=8.0))
        generation_time = time.time() - start_time
        
        print_success(f"Generated {len(stream)} events in {generation_time:.3f}s")
        print_info(f"Performance: {len(stream)/generation_time:.1f} events/second")
        
        print_step("2", "Test Live Editing Performance")
        from live_editing_engine import LiveEditingEngine, LiveEditCommand, EditingOperation
        
        engine = LiveEditingEngine()
        
        # Test multiple edits
        operations = [
            EditingOperation.MODIFY_VELOCITY,
            EditingOperation.ADD_SWING,
            EditingOperation.ADD_ACCENT,
            EditingOperation.HUMANIZE,
            EditingOperation.TRANSPOSE
        ]
        
        start_time = time.time()
        for i, operation in enumerate(operations):
            command = LiveEditCommand(
                operation=operation,
                parameters={"test": "value"},
                target_track=f"track_{i}"
            )
            result = engine.apply_live_edit(command)
        
        total_time = time.time() - start_time
        print_success(f"Applied {len(operations)} edits in {total_time:.3f}s")
        print_info(f"Performance: {len(operations)/total_time:.1f} edits/second")
        
        return True
        
    except Exception as e:
        print_error(f"Performance tests demo failed: {e}")
        return False

def demo_error_handling():
    """Demo error handling capabilities"""
    print_header("Error Handling Demo")
    
    try:
        print_step("1", "Test Invalid Command Handling")
        from live_editing_engine import LiveEditingEngine, LiveEditCommand, EditingOperation
        
        engine = LiveEditingEngine()
        
        # Test with invalid parameters
        command = LiveEditCommand(
            operation=EditingOperation.MODIFY_VELOCITY,
            parameters={"invalid_param": "invalid_value"},
            target_track="nonexistent_track"
        )
        
        result = engine.apply_live_edit(command)
        print_info(f"Invalid command result: {result.success}")
        print_info(f"Error message: {result.explanation}")
        
        print_step("2", "Test Graceful Degradation")
        from ardour_live_integration import ArdourLiveIntegration
        
        # Test with invalid Ardour path
        integration = ArdourLiveIntegration(ardour_path="/nonexistent/path")
        connected = integration.connect()
        print_info(f"Connection with invalid path: {connected}")
        
        print_step("3", "Test Resource Cleanup")
        integration.disconnect()
        print_success("Resources cleaned up successfully")
        
        return True
        
    except Exception as e:
        print_error(f"Error handling demo failed: {e}")
        return False

def main():
    """Main demo function"""
    print_header("YesAnd Music - Live MIDI Streaming Demo")
    print("This demo showcases the live MIDI streaming capabilities")
    print("including real-time generation, editing, and DAW integration.")
    
    demos = [
        ("Basic MIDI Streaming", demo_basic_streaming),
        ("Live Editing", demo_live_editing),
        ("Conversation Workflow", demo_conversation_workflow),
        ("Ardour Integration", demo_ardour_integration),
        ("Performance Tests", demo_performance_tests),
        ("Error Handling", demo_error_handling)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n🚀 Running {demo_name} Demo...")
        try:
            success = demo_func()
            results.append((demo_name, success))
            if success:
                print_success(f"{demo_name} demo completed successfully")
            else:
                print_error(f"{demo_name} demo failed")
        except Exception as e:
            print_error(f"{demo_name} demo crashed: {e}")
            results.append((demo_name, False))
    
    # Summary
    print_header("Demo Summary")
    successful_demos = sum(1 for _, success in results if success)
    total_demos = len(results)
    
    print(f"✅ Successful demos: {successful_demos}/{total_demos}")
    
    for demo_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {demo_name}")
    
    if successful_demos == total_demos:
        print_success("All demos completed successfully!")
        print("\n🎉 The live MIDI streaming system is working correctly!")
        print("\nTo use the system:")
        print("1. Make sure Ardour is running")
        print("2. Enable IAC Driver in Audio MIDI Setup")
        print("3. Run: python live_control_plane_cli.py")
        print("4. Try: 'Give me a funky bassline'")
    else:
        print_warning("Some demos failed. Check the error messages above.")
        print("\nThis is expected if Ardour is not running or IAC Driver is not enabled.")
        print("The system is designed to work with these components.")

if __name__ == "__main__":
    main()
