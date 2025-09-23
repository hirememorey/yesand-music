#!/usr/bin/env python3
"""
Comprehensive Tests for Live MIDI Streaming System

This module provides comprehensive testing for the live MIDI streaming
and real-time editing capabilities.
"""

import unittest
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from ardour_live_integration import (
    ArdourLiveIntegration, MIDIStreamGenerator, MIDIStreamEvent, 
    LiveMIDITrack, LiveEditingSession
)
from live_editing_engine import (
    LiveEditingEngine, LiveEditCommand, EditingOperation, 
    LiveEditCommandBuilder, LiveEditResult
)
from live_conversation_workflow import (
    LiveConversationWorkflow, LiveWorkflowSession, LiveWorkflowState
)

class TestMIDIStreamGenerator(unittest.TestCase):
    """Test MIDI stream generation"""
    
    def setUp(self):
        self.generator = MIDIStreamGenerator(tempo=120)
    
    def test_funky_bassline_generation(self):
        """Test funky bassline generation"""
        stream = list(self.generator.generate_bassline_stream(
            style="funky", key="C", duration=4.0
        ))
        
        self.assertGreater(len(stream), 0, "Should generate at least one event")
        
        # Check that events have required properties
        for event in stream:
            self.assertIsInstance(event, MIDIStreamEvent)
            self.assertIsInstance(event.note, int)
            self.assertIsInstance(event.velocity, int)
            self.assertIsInstance(event.start_time, float)
            self.assertIsInstance(event.duration, float)
            self.assertGreaterEqual(event.note, 0)
            self.assertLessEqual(event.note, 127)
            self.assertGreaterEqual(event.velocity, 0)
            self.assertLessEqual(event.velocity, 127)
    
    def test_jazz_bassline_generation(self):
        """Test jazz bassline generation"""
        stream = list(self.generator.generate_bassline_stream(
            style="jazz", key="F", duration=2.0
        ))
        
        self.assertGreater(len(stream), 0, "Should generate at least one event")
        
        # Jazz should have more events (16th notes)
        self.assertGreater(len(stream), 4, "Jazz should have more events than simple patterns")
    
    def test_blues_bassline_generation(self):
        """Test blues bassline generation"""
        stream = list(self.generator.generate_bassline_stream(
            style="blues", key="G", duration=1.0
        ))
        
        self.assertGreater(len(stream), 0, "Should generate at least one event")
    
    def test_simple_bassline_generation(self):
        """Test simple bassline generation"""
        stream = list(self.generator.generate_bassline_stream(
            style="simple", key="D", duration=2.0
        ))
        
        self.assertGreater(len(stream), 0, "Should generate at least one event")
        
        # Simple pattern should have fewer events (quarter notes)
        self.assertLessEqual(len(stream), 4, "Simple pattern should have fewer events")

class TestLiveEditingEngine(unittest.TestCase):
    """Test live editing engine"""
    
    def setUp(self):
        self.engine = LiveEditingEngine()
    
    def test_velocity_modification(self):
        """Test velocity modification"""
        command = LiveEditCommand(
            operation=EditingOperation.MODIFY_VELOCITY,
            parameters={"velocity_change": 10, "velocity_multiplier": 1.1},
            target_track="test_track",
            intensity=0.8
        )
        
        result = self.engine.apply_live_edit(command)
        
        self.assertTrue(result.success)
        self.assertEqual(result.operation, EditingOperation.MODIFY_VELOCITY)
        self.assertGreater(result.changes_applied, 0)
        self.assertIn("velocity", result.explanation.lower())
    
    def test_swing_addition(self):
        """Test swing addition"""
        command = LiveEditCommand(
            operation=EditingOperation.ADD_SWING,
            parameters={"swing_ratio": 0.7},
            target_track="test_track",
            intensity=0.9
        )
        
        result = self.engine.apply_live_edit(command)
        
        self.assertTrue(result.success)
        self.assertEqual(result.operation, EditingOperation.ADD_SWING)
        self.assertIn("swing", result.explanation.lower())
    
    def test_accent_addition(self):
        """Test accent addition"""
        command = LiveEditCommand(
            operation=EditingOperation.ADD_ACCENT,
            parameters={"accent_amount": 20},
            target_track="test_track",
            intensity=0.7
        )
        
        result = self.engine.apply_live_edit(command)
        
        self.assertTrue(result.success)
        self.assertEqual(result.operation, EditingOperation.ADD_ACCENT)
        self.assertIn("accent", result.explanation.lower())
    
    def test_humanization(self):
        """Test humanization"""
        command = LiveEditCommand(
            operation=EditingOperation.HUMANIZE,
            parameters={"timing_variation": 0.05, "velocity_variation": 0.1},
            target_track="test_track",
            intensity=0.6
        )
        
        result = self.engine.apply_live_edit(command)
        
        self.assertTrue(result.success)
        self.assertEqual(result.operation, EditingOperation.HUMANIZE)
        self.assertIn("human", result.explanation.lower())
    
    def test_transpose(self):
        """Test transposition"""
        command = LiveEditCommand(
            operation=EditingOperation.TRANSPOSE,
            parameters={"semitones": 5},
            target_track="test_track",
            intensity=1.0
        )
        
        result = self.engine.apply_live_edit(command)
        
        self.assertTrue(result.success)
        self.assertEqual(result.operation, EditingOperation.TRANSPOSE)
        self.assertIn("transpose", result.explanation.lower())
    
    def test_edit_history(self):
        """Test edit history tracking"""
        command = LiveEditCommand(
            operation=EditingOperation.MODIFY_VELOCITY,
            parameters={"velocity_change": 5},
            target_track="test_track"
        )
        
        result = self.engine.apply_live_edit(command)
        
        # Check that edit was recorded
        history = self.engine.get_edit_history("test_track")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["command"], command)
        self.assertEqual(history[0]["result"], result)
    
    def test_undo_functionality(self):
        """Test undo functionality"""
        command = LiveEditCommand(
            operation=EditingOperation.ADD_SWING,
            parameters={"swing_ratio": 0.6},
            target_track="test_track"
        )
        
        # Apply edit
        result = self.engine.apply_live_edit(command)
        self.assertTrue(result.success)
        
        # Check history
        history = self.engine.get_edit_history("test_track")
        self.assertEqual(len(history), 1)
        
        # Undo
        undo_success = self.engine.undo_last_edit("test_track")
        self.assertTrue(undo_success)
        
        # Check history is empty
        history = self.engine.get_edit_history("test_track")
        self.assertEqual(len(history), 0)
    
    def test_command_builder(self):
        """Test command builder"""
        command = (LiveEditCommandBuilder()
                  .set_operation(EditingOperation.ADD_ACCENT)
                  .set_target_track("track_1")
                  .set_intensity(0.8)
                  .add_parameter("accent_amount", 25)
                  .build())
        
        self.assertEqual(command.operation, EditingOperation.ADD_ACCENT)
        self.assertEqual(command.target_track, "track_1")
        self.assertEqual(command.intensity, 0.8)
        self.assertEqual(command.parameters["accent_amount"], 25)

class TestArdourLiveIntegration(unittest.TestCase):
    """Test Ardour live integration (mocked)"""
    
    def setUp(self):
        # Mock the Ardour integration to avoid requiring actual Ardour
        with patch('ardour_live_integration.subprocess') as mock_subprocess:
            mock_subprocess.run.return_value.returncode = 0
            self.integration = ArdourLiveIntegration()
    
    def test_connection_mock(self):
        """Test connection (mocked)"""
        with patch('ardour_live_integration.subprocess') as mock_subprocess:
            mock_subprocess.run.return_value.returncode = 0
            result = self.integration.connect()
            # Should succeed in mock environment
            self.assertTrue(result)
    
    def test_track_creation(self):
        """Test track creation"""
        track_id = self.integration.create_midi_track("Test Track")
        self.assertIsNotNone(track_id)
        self.assertIn(track_id, self.integration.live_tracks)
    
    def test_live_editing_enable(self):
        """Test enabling live editing"""
        track_id = self.integration.create_midi_track("Test Track")
        result = self.integration.enable_live_editing(track_id)
        self.assertTrue(result)
        self.assertIn(track_id, self.integration.active_sessions)
    
    def test_midi_streaming_mock(self):
        """Test MIDI streaming (mocked)"""
        track_id = self.integration.create_midi_track("Test Track")
        
        # Create a simple MIDI stream
        generator = MIDIStreamGenerator()
        stream = generator.generate_bassline_stream(style="simple", duration=1.0)
        
        # Mock the MIDI output
        with patch.object(self.integration, 'midi_out') as mock_midi_out:
            mock_midi_out.send_message = Mock()
            
            result = self.integration.stream_midi_to_track(track_id, stream, 1.0)
            self.assertTrue(result)
    
    def test_disconnect(self):
        """Test disconnection"""
        self.integration.disconnect()
        self.assertFalse(self.integration.connected)
        self.assertEqual(len(self.integration.live_tracks), 0)
        self.assertEqual(len(self.integration.active_sessions), 0)

class TestLiveConversationWorkflow(unittest.TestCase):
    """Test live conversation workflow (mocked)"""
    
    def setUp(self):
        # Mock the conversation engine and Ardour integration
        with patch('live_conversation_workflow.MusicalConversationEngine') as mock_conv, \
             patch('live_conversation_workflow.ArdourLiveIntegration') as mock_ardour:
            
            # Setup mocks
            mock_conv.return_value.engage.return_value = Mock(
                message="Test response",
                musical_action=None,
                confidence=0.8
            )
            mock_ardour.return_value.connect.return_value = True
            mock_ardour.return_value.create_midi_track.return_value = "track_1"
            mock_ardour.return_value.enable_live_editing.return_value = True
            
            self.workflow = LiveConversationWorkflow()
    
    def test_session_creation(self):
        """Test session creation"""
        session_id = self.workflow.start_conversation("Test Track")
        self.assertIsNotNone(session_id)
        self.assertIn(session_id, self.workflow.active_sessions)
        self.assertEqual(self.workflow.current_session.session_id, session_id)
    
    def test_conversation_processing(self):
        """Test conversation processing"""
        session_id = self.workflow.start_conversation("Test Track")
        
        response = self.workflow.process_conversation("Give me a funky bassline")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response.message, str)
    
    def test_session_status(self):
        """Test session status"""
        session_id = self.workflow.start_conversation("Test Track")
        
        status = self.workflow.get_session_status()
        
        self.assertIn("session_id", status)
        self.assertIn("track_id", status)
        self.assertIn("state", status)
        self.assertEqual(status["session_id"], session_id)
    
    def test_session_ending(self):
        """Test session ending"""
        session_id = self.workflow.start_conversation("Test Track")
        
        result = self.workflow.end_conversation(session_id)
        self.assertTrue(result)
        self.assertNotIn(session_id, self.workflow.active_sessions)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_workflow_mock(self):
        """Test end-to-end workflow (mocked)"""
        with patch('live_conversation_workflow.MusicalConversationEngine') as mock_conv, \
             patch('live_conversation_workflow.ArdourLiveIntegration') as mock_ardour, \
             patch('live_conversation_workflow.LiveEditingEngine') as mock_edit:
            
            # Setup comprehensive mocks
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
            
            mock_edit.return_value.apply_live_edit.return_value = Mock(
                success=True,
                explanation="Added swing feel",
                confidence=0.8,
                changes_applied=1
            )
            
            # Test the workflow
            workflow = LiveConversationWorkflow()
            
            # Start session
            session_id = workflow.start_conversation("Integration Test Track")
            self.assertIsNotNone(session_id)
            
            # Process conversation
            response = workflow.process_conversation("Give me a funky bassline")
            self.assertIsNotNone(response)
            self.assertIn("funky bassline", response.message.lower())
            
            # Test improvement
            response = workflow.process_conversation("Make it more complex")
            self.assertIsNotNone(response)
            
            # End session
            result = workflow.end_conversation(session_id)
            self.assertTrue(result)

class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def test_stream_generation_performance(self):
        """Test MIDI stream generation performance"""
        generator = MIDIStreamGenerator()
        
        start_time = time.time()
        stream = list(generator.generate_bassline_stream(style="jazz", duration=8.0))
        generation_time = time.time() - start_time
        
        # Should generate quickly (less than 1 second)
        self.assertLess(generation_time, 1.0, "Stream generation should be fast")
        self.assertGreater(len(stream), 0, "Should generate events")
    
    def test_edit_application_performance(self):
        """Test edit application performance"""
        engine = LiveEditingEngine()
        
        command = LiveEditCommand(
            operation=EditingOperation.ADD_SWING,
            parameters={"swing_ratio": 0.7},
            target_track="test_track"
        )
        
        start_time = time.time()
        result = engine.apply_live_edit(command)
        edit_time = time.time() - start_time
        
        # Should apply edits quickly (less than 0.1 seconds)
        self.assertLess(edit_time, 0.1, "Edit application should be fast")
        self.assertTrue(result.success)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMIDIStreamGenerator,
        TestLiveEditingEngine,
        TestArdourLiveIntegration,
        TestLiveConversationWorkflow,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("🧪 Running Live MIDI Streaming Tests")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        exit(1)
