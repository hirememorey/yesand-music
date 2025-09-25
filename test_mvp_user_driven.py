#!/usr/bin/env python3
"""
Comprehensive test suite for MVP User-Driven MIDI Generator

Tests musical quality gates, user feedback integration, and overall system functionality.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from mvp_user_driven_generator import (
    MusicalQualityGate,
    MusicalContextExtractor,
    MIDIGenerator,
    MVPUserDrivenGenerator
)


class TestMusicalQualityGate(unittest.TestCase):
    """Test musical quality assessment engine."""
    
    def setUp(self):
        self.quality_gate = MusicalQualityGate()
    
    def test_assess_quality_basic(self):
        """Test basic quality assessment."""
        midi_data = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        user_context = {'style': 'jazz', 'user_id': 'test_user'}
        
        quality_score, feedback = self.quality_gate.assess_quality(midi_data, user_context, 'test_id')
        
        self.assertIsInstance(quality_score, float)
        self.assertGreaterEqual(quality_score, 0.0)
        self.assertLessEqual(quality_score, 1.0)
        self.assertIsInstance(feedback, dict)
        self.assertIn('musical_coherence', feedback)
        self.assertIn('style_accuracy', feedback)
        self.assertIn('technical_quality', feedback)
        self.assertIn('user_preference', feedback)
    
    def test_assess_quality_empty_notes(self):
        """Test quality assessment with empty notes."""
        midi_data = {'notes': [], 'duration': 1.0}
        user_context = {'style': 'jazz'}
        
        quality_score, feedback = self.quality_gate.assess_quality(midi_data, user_context, 'test_id')
        
        # Empty notes should have low but not zero quality due to other factors
        self.assertLess(quality_score, 0.5)
        self.assertEqual(feedback['musical_coherence'], 0.0)
    
    def test_musical_coherence_assessment(self):
        """Test musical coherence assessment."""
        # Good coherence
        midi_data_good = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        
        score = self.quality_gate._assess_musical_coherence(midi_data_good)
        self.assertGreater(score, 0.5)
        
        # Poor coherence (too many notes)
        midi_data_bad = {
            'notes': [{'pitch': 60, 'velocity': 80, 'start_time': i*0.1, 'duration': 0.1} for i in range(50)],
            'duration': 1.0
        }
        
        score = self.quality_gate._assess_musical_coherence(midi_data_bad)
        self.assertLess(score, 0.8)
    
    def test_technical_quality_assessment(self):
        """Test technical quality assessment."""
        # Valid MIDI data
        midi_data_valid = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5}
            ]
        }
        
        score = self.quality_gate._assess_technical_quality(midi_data_valid)
        self.assertGreater(score, 0.8)
        
        # Invalid MIDI data
        midi_data_invalid = {
            'notes': [
                {'pitch': 200, 'velocity': 300, 'start_time': 0.0, 'duration': 0.5},  # Invalid pitch and velocity
            ]
        }
        
        score = self.quality_gate._assess_technical_quality(midi_data_invalid)
        self.assertLess(score, 0.8)
    
    def test_user_feedback_recording(self):
        """Test user feedback recording."""
        generation_id = 'test_gen_123'
        user_id = 'test_user'
        
        # Record feedback
        self.quality_gate.record_user_feedback(generation_id, 4.5, 'Great bass line!', user_id)
        
        # Check if feedback was recorded
        self.assertIn(user_id, self.quality_gate.user_feedback_db)
        self.assertEqual(len(self.quality_gate.user_feedback_db[user_id]), 1)
        
        feedback_entry = self.quality_gate.user_feedback_db[user_id][0]
        self.assertEqual(feedback_entry['generation_id'], generation_id)
        self.assertEqual(feedback_entry['rating'], 4.5)
        self.assertEqual(feedback_entry['comments'], 'Great bass line!')


class TestMusicalContextExtractor(unittest.TestCase):
    """Test musical context extraction from prompts."""
    
    def setUp(self):
        self.extractor = MusicalContextExtractor()
    
    def test_extract_key(self):
        """Test key extraction from prompts."""
        prompts = [
            "Create a bass line in C major",
            "Generate jazz in G minor",
            "Make a melody in F# major",
            "Bass line in B minor"
        ]
        
        expected_keys = ["C major", "G minor", "F# major", "B minor"]
        
        for prompt, expected_key in zip(prompts, expected_keys):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['key'], expected_key)
    
    def test_extract_tempo(self):
        """Test tempo extraction from prompts."""
        prompts = [
            "Create a bass line at 120 BPM",
            "Generate jazz at 140 beats per minute",
            "Make a slow melody",
            "Fast rock beat"
        ]
        
        expected_tempos = [120, 140, 80, 160]
        
        for prompt, expected_tempo in zip(prompts, expected_tempos):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['tempo'], expected_tempo)
    
    def test_extract_style(self):
        """Test style extraction from prompts."""
        prompts = [
            "Create a jazz bass line",
            "Generate rock music",
            "Make funky drums",
            "Blues piano part"
        ]
        
        expected_styles = ["jazz", "rock", "funk", "blues"]
        
        for prompt, expected_style in zip(prompts, expected_styles):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['style'], expected_style)
    
    def test_extract_instrument(self):
        """Test instrument extraction from prompts."""
        prompts = [
            "Create a bass line",
            "Generate drum pattern",
            "Make piano melody",
            "Guitar part"
        ]
        
        expected_instruments = ["bass", "drums", "piano", "guitar"]
        
        for prompt, expected_instrument in zip(prompts, expected_instruments):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['instrument'], expected_instrument)
    
    def test_extract_length(self):
        """Test length extraction from prompts."""
        prompts = [
            "Create 8 measures of bass",
            "Generate 16 bars of drums",
            "Make 4 beats of melody",
            "Piano for 10 seconds"
        ]
        
        expected_lengths = [
            {'value': 8, 'unit': 'measures'},
            {'value': 16, 'unit': 'measures'},
            {'value': 4, 'unit': 'beats'},
            {'value': 10, 'unit': 'seconds'}
        ]
        
        for prompt, expected_length in zip(prompts, expected_lengths):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['length'], expected_length)
    
    def test_extract_mood(self):
        """Test mood extraction from prompts."""
        prompts = [
            "Create a dark bass line",
            "Generate happy music",
            "Make melancholic melody",
            "Energetic rock beat"
        ]
        
        expected_moods = ["dark", "bright", "melancholic", "energetic"]
        
        for prompt, expected_mood in zip(prompts, expected_moods):
            context = self.extractor.extract_context(prompt)
            self.assertEqual(context['mood'], expected_mood)
    
    def test_complex_prompt_extraction(self):
        """Test extraction from complex prompts with multiple elements."""
        prompt = "Create a complex jazz bass line in G minor at 120 BPM for 8 measures with a dark mood"
        
        context = self.extractor.extract_context(prompt)
        
        self.assertEqual(context['key'], 'G minor')
        self.assertEqual(context['tempo'], 120)
        self.assertEqual(context['style'], 'jazz')
        self.assertEqual(context['instrument'], 'bass')
        self.assertEqual(context['length'], {'value': 8, 'unit': 'measures'})
        self.assertEqual(context['mood'], 'dark')
        self.assertEqual(context['complexity'], 'complex')


class TestMIDIGenerator(unittest.TestCase):
    """Test MIDI generation with quality validation."""
    
    def setUp(self):
        # Mock OpenAI client
        self.mock_client = Mock()
        self.generator = MIDIGenerator("fake_api_key")
        self.generator.client = self.mock_client
    
    def test_generate_midi_success(self):
        """Test successful MIDI generation."""
        # Mock quality gate
        mock_quality_gate = Mock()
        mock_quality_gate.assess_quality.return_value = (0.8, {'test': 0.8})
        self.generator.quality_gate = mock_quality_gate
        
        # Mock context extractor
        mock_context_extractor = Mock()
        mock_context_extractor.extract_context.return_value = {
            'key': 'C major',
            'tempo': 120,
            'style': 'jazz',
            'instrument': 'bass'
        }
        self.generator.context_extractor = mock_context_extractor
        
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''
        {
            "notes": [
                {"pitch": 60, "velocity": 80, "start_time": 0.0, "duration": 0.5},
                {"pitch": 64, "velocity": 75, "start_time": 0.5, "duration": 0.5}
            ],
            "tempo": 120,
            "key": "C major",
            "time_signature": "4/4",
            "duration": 2.0
        }
        '''
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test generation
        result = self.generator.generate_midi("Create a bass line", "test_user")
        
        self.assertTrue(result['success'])
        self.assertIn('midi_data', result)
        self.assertIn('quality_score', result)
        self.assertIn('generation_id', result)
        self.assertGreaterEqual(result['quality_score'], 0.0)
    
    def test_build_enhanced_prompt(self):
        """Test enhanced prompt building."""
        prompt = "Create a bass line"
        context = {
            'key': 'C major',
            'tempo': 120,
            'style': 'jazz',
            'instrument': 'bass',
            'length': {'value': 8, 'unit': 'measures'},
            'mood': 'dark',
            'complexity': 'complex'
        }
        
        enhanced_prompt = self.generator._build_enhanced_prompt(prompt, context)
        
        self.assertIn("Create a bass line", enhanced_prompt)
        self.assertIn("C major", enhanced_prompt)
        self.assertIn("120", enhanced_prompt)
        self.assertIn("jazz", enhanced_prompt)
        self.assertIn("bass", enhanced_prompt)
        self.assertIn("8 measures", enhanced_prompt)
        self.assertIn("dark", enhanced_prompt)
        self.assertIn("complex", enhanced_prompt)
        self.assertIn("JSON", enhanced_prompt)


class TestMVPUserDrivenGenerator(unittest.TestCase):
    """Test main MVP system."""
    
    def setUp(self):
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock the generator
        with patch('mvp_user_driven_generator.MIDIGenerator'):
            self.mvp_generator = MVPUserDrivenGenerator("fake_api_key")
            self.mvp_generator.output_dir = Path(self.temp_dir)
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_save_midi_file(self):
        """Test MIDI file saving."""
        midi_data = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5, 'channel': 0},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5, 'channel': 0}
            ],
            'tempo': 120
        }
        
        filepath = Path(self.temp_dir) / "test.mid"
        
        # Should not raise an exception
        self.mvp_generator._save_midi_file(midi_data, filepath)
        
        # Check if file was created
        self.assertTrue(filepath.exists())
        
        # Check if it's a valid MIDI file
        import mido
        mid = mido.MidiFile(str(filepath))
        self.assertGreater(len(mid.tracks), 0)
    
    def test_generate_and_save_mock(self):
        """Test generate and save with mocked generation."""
        # Mock the generator's generate_midi method
        mock_result = {
            'success': True,
            'midi_data': {
                'notes': [
                    {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5, 'channel': 0}
                ],
                'tempo': 120
            },
            'quality_score': 0.8,
            'feedback': {'test': 0.8},
            'generation_id': 'test_123',
            'context': {},
            'attempt': 1
        }
        
        with patch.object(self.mvp_generator.generator, 'generate_midi', return_value=mock_result):
            with patch.object(self.mvp_generator, '_prompt_user_feedback'):
                result = self.mvp_generator.generate_and_save("Create a bass line", "test_user")
                
                self.assertTrue(result['success'])
                self.assertIn('filepath', result)
                self.assertIn('filename', result)
    
    def test_show_help(self):
        """Test help display."""
        # Should not raise an exception
        self.mvp_generator._show_help()
    
    def test_show_status(self):
        """Test status display."""
        # Should not raise an exception
        self.mvp_generator._show_status()


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_quality_flow(self):
        """Test complete quality assessment flow."""
        quality_gate = MusicalQualityGate()
        context_extractor = MusicalContextExtractor()
        
        # Extract context
        prompt = "Create a jazz bass line in C major at 120 BPM"
        context = context_extractor.extract_context(prompt)
        
        # Create sample MIDI data
        midi_data = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}
            ],
            'tempo': 120,
            'key': 'C major',
            'duration': 2.0
        }
        
        # Assess quality
        quality_score, feedback = quality_gate.assess_quality(midi_data, context, 'test_id')
        
        # Verify results
        self.assertIsInstance(quality_score, float)
        self.assertGreaterEqual(quality_score, 0.0)
        self.assertLessEqual(quality_score, 1.0)
        self.assertIsInstance(feedback, dict)
        
        # Record user feedback
        quality_gate.record_user_feedback('test_id', 4.5, 'Great jazz bass!', 'test_user')
        
        # Verify feedback was recorded
        self.assertIn('test_user', quality_gate.user_feedback_db)
        self.assertEqual(len(quality_gate.user_feedback_db['test_user']), 1)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestMusicalQualityGate,
        TestMusicalContextExtractor,
        TestMIDIGenerator,
        TestMVPUserDrivenGenerator,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
