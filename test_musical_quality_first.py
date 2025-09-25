#!/usr/bin/env python3
"""
Test suite for MVP Musical Quality First Generator

Tests the refined approach that focuses on musical quality over technical precision.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from mvp_musical_quality_first import (
    MusicalQualityFirstGate,
    SimplePromptProcessor,
    MusicalQualityFirstGenerator,
    MVPMusicalQualityFirstGenerator
)


class TestMusicalQualityFirstGate(unittest.TestCase):
    """Test musical quality assessment focused on musical satisfaction."""
    
    def setUp(self):
        self.quality_gate = MusicalQualityFirstGate()
    
    def test_assess_quality_musical_focus(self):
        """Test quality assessment with musical focus."""
        midi_data = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5},
                {'pitch': 60, 'velocity': 70, 'start_time': 1.5, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        user_context = {'style': 'jazz', 'user_id': 'test_user'}
        
        quality_score, feedback = self.quality_gate.assess_quality(midi_data, user_context, 'test_id')
        
        self.assertIsInstance(quality_score, float)
        self.assertGreaterEqual(quality_score, 0.0)
        self.assertLessEqual(quality_score, 1.0)
        self.assertIsInstance(feedback, dict)
        self.assertIn('musical_completeness', feedback)
        self.assertIn('musical_interest', feedback)
        self.assertIn('style_authenticity', feedback)
        self.assertIn('technical_quality', feedback)
    
    def test_musical_completeness_assessment(self):
        """Test musical completeness assessment."""
        # Good completeness - variety and development
        midi_data_good = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5},
                {'pitch': 60, 'velocity': 70, 'start_time': 1.5, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        
        score = self.quality_gate._assess_musical_completeness(midi_data_good)
        self.assertGreater(score, 0.7)
        
        # Poor completeness - too few notes
        midi_data_bad = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        
        score = self.quality_gate._assess_musical_completeness(midi_data_bad)
        self.assertLess(score, 0.6)
    
    def test_musical_interest_assessment(self):
        """Test musical interest assessment."""
        # Interesting - variety in rhythm, pitch, and dynamics
        midi_data_interesting = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 72, 'velocity': 60, 'start_time': 0.25, 'duration': 0.25},
                {'pitch': 64, 'velocity': 90, 'start_time': 0.75, 'duration': 0.5},
                {'pitch': 67, 'velocity': 70, 'start_time': 1.5, 'duration': 0.25}
            ],
            'duration': 2.0
        }
        
        score = self.quality_gate._assess_musical_interest(midi_data_interesting)
        self.assertGreater(score, 0.7)
        
        # Boring - all same pitch and velocity
        midi_data_boring = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 60, 'velocity': 80, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 60, 'velocity': 80, 'start_time': 1.0, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        
        score = self.quality_gate._assess_musical_interest(midi_data_boring)
        self.assertLessEqual(score, 0.7)
    
    def test_user_feedback_focus(self):
        """Test user feedback focuses on musical satisfaction."""
        generation_id = "test_gen_123"
        user_id = "test_user"
        
        # Record feedback
        self.quality_gate.record_user_feedback(
            generation_id, 4.5, "Really liked the musical character!", user_id
        )
        
        # Check feedback was recorded
        self.assertIn(user_id, self.quality_gate.user_feedback_db)
        user_feedback = self.quality_gate.user_feedback_db[user_id]
        self.assertEqual(len(user_feedback), 1)
        
        feedback_entry = user_feedback[0]
        self.assertEqual(feedback_entry['generation_id'], generation_id)
        self.assertEqual(feedback_entry['rating'], 4.5)
        self.assertEqual(feedback_entry['comments'], "Really liked the musical character!")
        self.assertEqual(feedback_entry['focus'], 'musical_satisfaction')


class TestSimplePromptProcessor(unittest.TestCase):
    """Test simple prompt processor that trusts the AI."""
    
    def setUp(self):
        self.processor = SimplePromptProcessor()
    
    def test_extract_basic_context(self):
        """Test basic context extraction."""
        prompt = "Create a funky bass line in G minor at 120 BPM"
        context = self.processor.extract_basic_context(prompt)
        
        self.assertEqual(context['original_prompt'], prompt)
        self.assertEqual(context['key'], 'g minor')
        self.assertEqual(context['tempo'], 120)
        self.assertEqual(context['instrument'], 'bass')
    
    def test_extract_context_creative_prompt(self):
        """Test context extraction with creative, metaphorical prompts."""
        # This is the key test - can it handle creative language?
        prompt = "I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby in g minor"
        context = self.processor.extract_basic_context(prompt)
        
        # Should extract basic info without choking on creative language
        self.assertEqual(context['original_prompt'], prompt)
        self.assertEqual(context['key'], 'g minor')
        self.assertEqual(context['tempo'], 120)  # Default
        self.assertEqual(context['instrument'], 'bass')
    
    def test_extract_context_emotional_prompt(self):
        """Test context extraction with emotional descriptors."""
        prompt = "Create a melancholic melody that makes me feel intrigued and scared"
        context = self.processor.extract_basic_context(prompt)
        
        # Should handle emotional language without errors
        self.assertEqual(context['original_prompt'], prompt)
        self.assertEqual(context['key'], 'C major')  # Default
        self.assertEqual(context['tempo'], 120)  # Default
        self.assertEqual(context['instrument'], 'melody')
    
    def test_extract_context_minimal(self):
        """Test context extraction with minimal information."""
        prompt = "Make something funky"
        context = self.processor.extract_basic_context(prompt)
        
        # Should use defaults gracefully
        self.assertEqual(context['original_prompt'], prompt)
        self.assertEqual(context['key'], 'C major')
        self.assertEqual(context['tempo'], 120)
        self.assertEqual(context['instrument'], 'bass')


class TestMusicalQualityFirstGenerator(unittest.TestCase):
    """Test the main generator class."""
    
    def setUp(self):
        # Mock OpenAI client
        self.mock_client = Mock()
        self.generator = MusicalQualityFirstGenerator("test_api_key")
        self.generator.client = self.mock_client
    
    def test_generate_midi_success(self):
        """Test successful MIDI generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "notes": [
                {"pitch": 60, "velocity": 80, "start_time": 0.0, "duration": 0.5, "track_index": 0}
            ],
            "tempo": 120,
            "key": "C major",
            "time_signature": "4/4",
            "duration": 2.0,
            "musical_description": "A simple but complete musical idea"
        })
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test generation
        result = self.generator.generate_midi("Create a simple bass line")
        
        self.assertTrue(result['success'])
        self.assertIn('midi_data', result)
        self.assertIn('quality_score', result)
        self.assertIn('musical_approach', result)
        self.assertEqual(result['musical_approach'], 'quality_first')
    
    def test_generate_midi_creative_prompt(self):
        """Test generation with creative, metaphorical prompts."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "notes": [
                {"pitch": 36, "velocity": 90, "start_time": 0.0, "duration": 0.5, "track_index": 0},
                {"pitch": 40, "velocity": 85, "start_time": 0.5, "duration": 0.5, "track_index": 0}
            ],
            "tempo": 120,
            "key": "G minor",
            "time_signature": "4/4",
            "duration": 4.0,
            "musical_description": "An anthemic bass line with grunge characteristics"
        })
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test with creative prompt
        creative_prompt = "I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby in g minor"
        result = self.generator.generate_midi(creative_prompt)
        
        self.assertTrue(result['success'])
        self.assertIn('midi_data', result)
        self.assertIn('musical_description', result['midi_data'])
    
    def test_generate_midi_json_parse_error(self):
        """Test handling of JSON parse errors."""
        # Mock OpenAI response with invalid JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is not valid JSON"
        
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # Test generation
        result = self.generator.generate_midi("Create a bass line")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)


class TestMVPMusicalQualityFirstGenerator(unittest.TestCase):
    """Test the main MVP system."""
    
    def setUp(self):
        # Mock the generator
        self.mock_generator = Mock()
        self.mvp_generator = MVPMusicalQualityFirstGenerator("test_api_key")
        self.mvp_generator.generator = self.mock_generator
    
    def test_generate_and_save_success(self):
        """Test successful generation and saving."""
        # Mock successful generation
        mock_result = {
            'success': True,
            'midi_data': {
                'notes': [{'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5, 'track_index': 0}],
                'tempo': 120,
                'key': 'C major',
                'duration': 2.0,
                'musical_description': 'A complete musical idea'
            },
            'quality_score': 0.8,
            'feedback': {'musical_completeness': 0.8, 'musical_interest': 0.7},
            'generation_id': 'test_123',
            'attempt': 1,
            'musical_approach': 'quality_first'
        }
        
        self.mock_generator.generate_midi.return_value = mock_result
        
        # Test generation
        with tempfile.TemporaryDirectory() as temp_dir:
            self.mvp_generator.output_dir = Path(temp_dir)
            # Mock the _prompt_user_feedback to avoid input during testing
            with patch.object(self.mvp_generator, '_prompt_user_feedback'):
                result = self.mvp_generator.generate_and_save("Create a bass line")
                
                self.assertTrue(result['success'])
                self.assertIn('filepath', result)
                self.assertIn('filename', result)
    
    def test_extract_instrument(self):
        """Test instrument extraction for display."""
        self.assertEqual(self.mvp_generator._extract_instrument("Create a bass line"), "bass")
        self.assertEqual(self.mvp_generator._extract_instrument("Make some drums"), "drums")
        self.assertEqual(self.mvp_generator._extract_instrument("Generate a melody"), "melody")
        self.assertEqual(self.mvp_generator._extract_instrument("Something creative"), "musical")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_creative_prompt_handling(self):
        """Test that creative prompts are handled without errors."""
        processor = SimplePromptProcessor()
        
        creative_prompts = [
            "I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby in g minor",
            "Create a melancholic melody that makes me feel intrigued and scared",
            "Generate a funky bass line that sounds like Bootsy Collins on a bad day",
            "Make a drum pattern that sounds like thunder rolling across the sky"
        ]
        
        for prompt in creative_prompts:
            # Should not raise any exceptions
            context = processor.extract_basic_context(prompt)
            self.assertIsInstance(context, dict)
            self.assertEqual(context['original_prompt'], prompt)
    
    def test_quality_assessment_focus(self):
        """Test that quality assessment focuses on musical aspects."""
        quality_gate = MusicalQualityFirstGate()
        
        # Test with musically complete data
        midi_data = {
            'notes': [
                {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5},
                {'pitch': 60, 'velocity': 70, 'start_time': 1.5, 'duration': 0.5}
            ],
            'duration': 2.0
        }
        
        context = {'style': 'jazz', 'user_id': 'test_user'}
        quality_score, feedback = quality_gate.assess_quality(midi_data, context, 'test_id')
        
        # Should focus on musical aspects
        self.assertIn('musical_completeness', feedback)
        self.assertIn('musical_interest', feedback)
        self.assertIn('style_authenticity', feedback)
        self.assertIn('technical_quality', feedback)
        
        # Musical aspects should have higher weights
        self.assertGreater(feedback['musical_completeness'], 0.5)
        self.assertGreater(feedback['musical_interest'], 0.5)


if __name__ == '__main__':
    unittest.main()
