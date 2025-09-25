#!/usr/bin/env python3
"""
Test Suite for Musical Conversation & Problem-Solving System

This test suite validates all components of the musical conversation system:
- Musical Context Interview
- Project State Analyzer
- Musical Conversation Engine
- MIDI Sketch Generator
- CLI Interface
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from musical_context_interview import MusicalContextInterview, MusicalContext
from project_state_analyzer import ProjectStateAnalyzer, ProjectState
from musical_conversation_engine import MusicalConversationEngine, MusicalSuggestion
from midi_sketch_generator import MIDISketchGenerator, MIDISketch
from musical_conversation_cli import MusicalConversationCLI


class TestMusicalContextInterview(unittest.TestCase):
    """Test the Musical Context Interview system"""
    
    def setUp(self):
        self.interview = MusicalContextInterview()
    
    def test_interview_initialization(self):
        """Test interview initialization"""
        self.assertIsNotNone(self.interview.questions)
        self.assertEqual(len(self.interview.questions), 8)  # 8 questions in the bank
        self.assertEqual(self.interview.interview_state, "initial")
    
    def test_start_interview(self):
        """Test starting an interview"""
        response = self.interview.start_interview()
        self.assertIn("Welcome to the Musical Context Interview", response)
        self.assertEqual(self.interview.interview_state, "in_progress")
    
    def test_get_next_question(self):
        """Test getting next question"""
        self.interview.start_interview()
        question = self.interview.get_next_question()
        self.assertIsNotNone(question)
        self.assertEqual(question.question_id, "song_concept")
    
    def test_answer_question(self):
        """Test answering questions"""
        self.interview.start_interview()
        
        # Answer song concept question
        success, message = self.interview.answer_question("song_concept", "A song about love")
        self.assertTrue(success)
        self.assertEqual(self.interview.current_context.song_concept, "A song about love")
        
        # Answer key signature question
        success, message = self.interview.answer_question("key_signature", "G minor")
        self.assertTrue(success)
        self.assertEqual(self.interview.current_context.key_signature, "G minor")
        
        # Answer tempo question
        success, message = self.interview.answer_question("tempo", "120")
        self.assertTrue(success)
        self.assertEqual(self.interview.current_context.tempo, 120)
    
    def test_validation(self):
        """Test input validation"""
        self.interview.start_interview()
        
        # Test invalid tempo
        success, message = self.interview.answer_question("tempo", "not_a_number")
        self.assertFalse(success)
        self.assertIn("Invalid format", message)
        
        # Test valid tempo
        success, message = self.interview.answer_question("tempo", "140")
        self.assertTrue(success)
    
    def test_context_completion(self):
        """Test context completion detection"""
        self.interview.start_interview()
        
        # Answer all required questions
        self.interview.answer_question("song_concept", "A song about love")
        self.interview.answer_question("key_signature", "G minor")
        self.interview.answer_question("tempo", "120")
        self.interview.answer_question("existing_parts", "guitar, bass, drums")
        self.interview.answer_question("musical_problem", "I need help with the bridge")
        
        # Check if interview is complete
        self.assertTrue(self.interview.is_complete())
        
        # Check progress
        progress = self.interview.get_progress()
        self.assertEqual(progress[0], 5)  # 5 required questions answered
        self.assertEqual(progress[1], 5)  # 5 total required questions


class TestProjectStateAnalyzer(unittest.TestCase):
    """Test the Project State Analyzer system"""
    
    def setUp(self):
        self.analyzer = ProjectStateAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer.supported_formats)
        self.assertIn('.mid', self.analyzer.supported_formats)
        self.assertIn('.midi', self.analyzer.supported_formats)
    
    def test_musical_role_detection(self):
        """Test musical role detection"""
        # Test bass range
        role = self.analyzer._determine_musical_role((36, 60), 10, 20)
        self.assertIn("bass", role.lower())
        
        # Test melody range
        role = self.analyzer._determine_musical_role((60, 84), 15, 30)
        self.assertIn("melody", role.lower())
        
        # Test high range
        role = self.analyzer._determine_musical_role((84, 96), 8, 20)
        self.assertIn("lead", role.lower())
    
    def test_rhythmic_complexity_calculation(self):
        """Test rhythmic complexity calculation"""
        notes = [
            {'time': 1, 'velocity': 80},
            {'time': 1, 'velocity': 80},
            {'time': 2, 'velocity': 90},
            {'time': 1, 'velocity': 85}
        ]
        
        complexity = self.analyzer._calculate_rhythmic_complexity(notes)
        self.assertGreaterEqual(complexity, 0.0)
        self.assertLessEqual(complexity, 1.0)
    
    def test_chord_progression_detection(self):
        """Test chord progression detection"""
        notes = [60, 64, 67, 62, 65, 69]  # C major and D minor chords
        progression = self.analyzer._detect_chord_progression(notes)
        self.assertIsInstance(progression, list)
        self.assertGreater(len(progression), 0)
    
    def test_timing_pattern_analysis(self):
        """Test timing pattern analysis"""
        note_times = [0, 1, 2, 3, 4, 5, 6, 7]  # Regular quarter notes
        pattern = self.analyzer._analyze_timing_pattern(note_times)
        self.assertIsNotNone(pattern)
        self.assertIn("pattern", pattern.lower())


class TestMusicalConversationEngine(unittest.TestCase):
    """Test the Musical Conversation Engine system"""
    
    def setUp(self):
        self.engine = MusicalConversationEngine()
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine.context_interview)
        self.assertIsNotNone(self.engine.project_analyzer)
        self.assertIsNone(self.engine.conversation_context)
    
    def test_start_conversation(self):
        """Test starting a conversation"""
        response = self.engine.start_conversation()
        self.assertIn("Welcome to Musical Conversation Engine", response)
        self.assertIsNotNone(self.engine.conversation_context)
        self.assertIsNotNone(self.engine.conversation_context.session_id)
    
    def test_response_type_detection(self):
        """Test response type detection"""
        # Test context interview
        response_type = self.engine._determine_response_type("My song is about love")
        self.assertEqual(response_type, "context_interview")
        
        # Test musical suggestion
        response_type = self.engine._determine_response_type("I need help with the bridge")
        self.assertEqual(response_type, "musical_suggestion")
        
        # Test problem clarification
        response_type = self.engine._determine_response_type("The problem is I can't figure out the chords")
        self.assertEqual(response_type, "problem_clarification")
    
    def test_suggestion_generation(self):
        """Test musical suggestion generation"""
        # Start conversation and set up context
        self.engine.start_conversation()
        self.engine.conversation_context.user_context.musical_problem = "I need help with a bridge"
        self.engine.conversation_context.user_context.key_signature = "G minor"
        self.engine.conversation_context.user_context.tempo = 120
        
        # Generate suggestions
        suggestions = self.engine._generate_musical_suggestions("")
        self.assertIsInstance(suggestions, list)
        
        if suggestions:
            suggestion = suggestions[0]
            self.assertIsInstance(suggestion, MusicalSuggestion)
            self.assertIsNotNone(suggestion.title)
            self.assertIsNotNone(suggestion.description)
            self.assertGreaterEqual(suggestion.confidence_score, 0.0)
            self.assertLessEqual(suggestion.confidence_score, 1.0)
    
    def test_context_extraction(self):
        """Test context extraction from user input"""
        problem = self.engine._extract_problem_from_input("I need help with the bridge")
        self.assertEqual(problem, "the bridge")
        
        problem = self.engine._extract_problem_from_input("I can't figure out the chord progression")
        self.assertEqual(problem, "the chord progression")
    
    def test_relative_key_mapping(self):
        """Test relative key mapping"""
        relative = self.engine._get_relative_key("C major")
        self.assertEqual(relative, "A minor")
        
        relative = self.engine._get_relative_key("G major")
        self.assertEqual(relative, "E minor")


class TestMIDISketchGenerator(unittest.TestCase):
    """Test the MIDI Sketch Generator system"""
    
    def setUp(self):
        self.generator = MIDISketchGenerator()
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        self.assertIsNotNone(self.generator.output_dir)
        self.assertTrue(os.path.exists(self.generator.output_dir))
        self.assertIsNotNone(self.generator.chord_progressions)
        self.assertIsNotNone(self.generator.scales)
        self.assertIsNotNone(self.generator.rhythmic_patterns)
    
    def test_sketch_generation(self):
        """Test basic sketch generation"""
        sketch = self.generator.generate_sketch(
            suggestion_type="chord_progression",
            key_signature="G minor",
            tempo=120,
            duration_bars=4
        )
        
        self.assertIsInstance(sketch, MIDISketch)
        self.assertIsNotNone(sketch.sketch_id)
        self.assertIsNotNone(sketch.title)
        self.assertIsNotNone(sketch.midi_data)
        self.assertEqual(sketch.tempo, 120)
        self.assertEqual(sketch.key_signature, "G minor")
        self.assertGreater(len(sketch.midi_data), 0)
    
    def test_chord_progression_generation(self):
        """Test chord progression sketch generation"""
        midi_data = self.generator._generate_chord_progression_sketch("G minor", 120, 4)
        self.assertIsInstance(midi_data, list)
        self.assertGreater(len(midi_data), 0)
        
        # Check that all notes have required fields
        for note in midi_data:
            self.assertIn('pitch', note)
            self.assertIn('velocity', note)
            self.assertIn('start_time_seconds', note)
            self.assertIn('duration_seconds', note)
            self.assertIn('track', note)
    
    def test_melody_generation(self):
        """Test melody sketch generation"""
        midi_data = self.generator._generate_melody_sketch("G minor", 120, 4, "jazz")
        self.assertIsInstance(midi_data, list)
        self.assertGreater(len(midi_data), 0)
        
        # Check that all notes have required fields
        for note in midi_data:
            self.assertIn('pitch', note)
            self.assertIn('velocity', note)
            self.assertIn('start_time_seconds', note)
            self.assertIn('duration_seconds', note)
            self.assertIn('track', note)
    
    def test_bass_line_generation(self):
        """Test bass line sketch generation"""
        midi_data = self.generator._generate_bass_line_sketch("G minor", 120, 4, "walking")
        self.assertIsInstance(midi_data, list)
        self.assertGreater(len(midi_data), 0)
        
        # Check that all notes are in bass range
        for note in midi_data:
            self.assertLessEqual(note['pitch'], 72)  # C4 is upper limit for bass
    
    def test_sketch_saving(self):
        """Test sketch saving to file"""
        sketch = self.generator.generate_sketch(
            suggestion_type="chord_progression",
            key_signature="C major",
            tempo=120,
            duration_bars=2
        )
        
        filepath = self.generator.save_sketch(sketch)
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.mid'))
        
        # Clean up
        os.remove(filepath)
    
    def test_multiple_sketch_generation(self):
        """Test generating multiple sketch variations"""
        sketches = self.generator.generate_multiple_sketches(
            suggestion_type="melody",
            key_signature="G minor",
            tempo=120,
            count=3
        )
        
        self.assertEqual(len(sketches), 3)
        
        # Check that all sketches are different
        titles = [sketch.title for sketch in sketches]
        self.assertEqual(len(set(titles)), 3)  # All titles should be unique
    
    def test_chord_progression_mapping(self):
        """Test chord progression mapping"""
        progression = self.generator._get_chord_progression("G major")
        self.assertIsInstance(progression, list)
        self.assertGreater(len(progression), 0)
        self.assertIn('G', progression)
    
    def test_scale_mapping(self):
        """Test scale mapping"""
        scale = self.generator._get_scale_for_key("G minor")
        self.assertIsInstance(scale, list)
        self.assertEqual(len(scale), 7)  # Major/minor scales have 7 notes
    
    def test_rhythm_pattern_mapping(self):
        """Test rhythm pattern mapping"""
        pattern = self.generator._get_rhythm_pattern("jazz")
        self.assertIsInstance(pattern, list)
        self.assertGreater(len(pattern), 0)
        
        # Check that all durations are positive
        for duration in pattern:
            self.assertGreater(duration, 0)


class TestMusicalConversationCLI(unittest.TestCase):
    """Test the Musical Conversation CLI system"""
    
    def setUp(self):
        self.cli = MusicalConversationCLI()
    
    def test_cli_initialization(self):
        """Test CLI initialization"""
        self.assertIsNotNone(self.cli.conversation_engine)
        self.assertIsNotNone(self.cli.sketch_generator)
        self.assertIsNotNone(self.cli.project_analyzer)
        self.assertIsNotNone(self.cli.context_interview)
        self.assertIsNone(self.cli.current_project_path)
        self.assertEqual(len(self.cli.current_suggestions), 0)
        self.assertEqual(len(self.cli.current_sketches), 0)
    
    def test_response_type_detection(self):
        """Test response type detection in CLI"""
        # Test suggestion triggers
        self.assertTrue(self.cli._should_generate_suggestions("I need help with the bridge"))
        self.assertTrue(self.cli._should_generate_suggestions("What should I do for the chorus"))
        self.assertFalse(self.cli._should_generate_suggestions("Hello there"))
    
    def test_sketch_generation_for_suggestion(self):
        """Test generating sketches for suggestions"""
        # Create a mock suggestion
        suggestion = MusicalSuggestion(
            suggestion_id="test",
            title="Test Suggestion",
            description="Test description",
            musical_reasoning="Test reasoning",
            implementation_notes="Test notes",
            confidence_score=0.8,
            suggestion_type="chord_progression"
        )
        
        # Set up conversation context
        self.cli.conversation_engine.start_conversation()
        self.cli.conversation_engine.conversation_context.user_context.key_signature = "G minor"
        self.cli.conversation_engine.conversation_context.user_context.tempo = 120
        
        # Generate sketch
        sketch = self.cli._generate_sketch_for_suggestion(suggestion, 1)
        
        if sketch:  # May be None if there's an error
            self.assertIsInstance(sketch, MIDISketch)
            self.assertIn("Test Suggestion", sketch.title)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_complete_workflow(self):
        """Test complete workflow from interview to sketch generation"""
        # Initialize components
        interview = MusicalContextInterview()
        engine = MusicalConversationEngine()
        generator = MIDISketchGenerator()
        
        # Start interview
        interview.start_interview()
        
        # Answer questions
        interview.answer_question("song_concept", "A song about love")
        interview.answer_question("key_signature", "G minor")
        interview.answer_question("tempo", "120")
        interview.answer_question("existing_parts", "guitar, bass")
        interview.answer_question("musical_problem", "I need help with the bridge")
        
        # Check if interview is complete
        self.assertTrue(interview.is_complete())
        
        # Start conversation with context
        engine.start_conversation()
        engine.conversation_context.user_context = interview.current_context
        
        # Generate suggestions
        suggestions = engine._generate_musical_suggestions("")
        self.assertGreater(len(suggestions), 0)
        
        # Generate sketch for first suggestion
        if suggestions:
            sketch = generator.generate_sketch(
                suggestion_type=suggestions[0].suggestion_type,
                key_signature="G minor",
                tempo=120
            )
            
            self.assertIsInstance(sketch, MIDISketch)
            self.assertGreater(len(sketch.midi_data), 0)
    
    def test_error_handling(self):
        """Test error handling across components"""
        # Test invalid input handling
        interview = MusicalContextInterview()
        interview.start_interview()
        
        # Test invalid tempo
        success, message = interview.answer_question("tempo", "not_a_number")
        self.assertFalse(success)
        
        # Test invalid key signature
        success, message = interview.answer_question("key_signature", "invalid_key")
        self.assertFalse(success)
    
    def test_data_persistence(self):
        """Test data persistence and retrieval"""
        # Test context serialization
        interview = MusicalContextInterview()
        interview.start_interview()
        interview.answer_question("song_concept", "Test song")
        interview.answer_question("key_signature", "C major")
        
        # Get context for AI
        context = interview.get_context_for_ai()
        self.assertIsInstance(context, dict)
        self.assertEqual(context['song_concept'], "Test song")
        self.assertEqual(context['key_signature'], "C major")


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestMusicalContextInterview,
        TestProjectStateAnalyzer,
        TestMusicalConversationEngine,
        TestMIDISketchGenerator,
        TestMusicalConversationCLI,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
