#!/usr/bin/env python3
"""
Unit tests for analysis.py module.

Tests the pure functions for musical analysis and transformation.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis import filter_notes_by_pitch, apply_swing


class TestAnalysis(unittest.TestCase):
    """Test cases for musical analysis functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_notes = [
            {
                'pitch': 48,  # C3 (bass range)
                'velocity': 80,
                'start_time_seconds': 0.0,
                'duration_seconds': 1.0,
                'track_index': 0
            },
            {
                'pitch': 60,  # C4 (middle range)
                'velocity': 90,
                'start_time_seconds': 1.0,
                'duration_seconds': 0.5,
                'track_index': 0
            },
            {
                'pitch': 72,  # C5 (high range)
                'velocity': 100,
                'start_time_seconds': 2.0,
                'duration_seconds': 1.0,
                'track_index': 0
            }
        ]
    
    def test_filter_notes_by_pitch_valid_input(self):
        """Test filtering notes by pitch with valid input."""
        bass_notes = filter_notes_by_pitch(self.sample_notes, max_pitch=60)
        
        self.assertEqual(len(bass_notes), 2)  # Should include C3 and C4
        self.assertEqual(bass_notes[0]['pitch'], 48)
        self.assertEqual(bass_notes[1]['pitch'], 60)
    
    def test_filter_notes_by_pitch_no_matches(self):
        """Test filtering notes by pitch with no matches."""
        high_notes = filter_notes_by_pitch(self.sample_notes, max_pitch=40)
        
        self.assertEqual(len(high_notes), 1)  # Should only include C3
        self.assertEqual(high_notes[0]['pitch'], 48)
    
    def test_filter_notes_by_pitch_all_matches(self):
        """Test filtering notes by pitch with all matches."""
        all_notes = filter_notes_by_pitch(self.sample_notes, max_pitch=80)
        
        self.assertEqual(len(all_notes), 3)  # Should include all notes
    
    def test_filter_notes_by_pitch_invalid_input(self):
        """Test filtering notes by pitch with invalid input."""
        with self.assertRaises(TypeError):
            filter_notes_by_pitch("not a list", 60)
        
        with self.assertRaises(TypeError):
            filter_notes_by_pitch(self.sample_notes, "not an int")
    
    def test_filter_notes_by_pitch_malformed_notes(self):
        """Test filtering notes by pitch with malformed note data."""
        malformed_notes = [
            {'pitch': 48, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 1.0, 'track_index': 0},
            {'invalid': 'note'},  # Missing pitch
            {'pitch': 'not_a_number', 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 1.0, 'track_index': 0},  # Invalid pitch type
            {'pitch': 60, 'velocity': 90, 'start_time_seconds': 1.0, 'duration_seconds': 0.5, 'track_index': 0}
        ]
        
        filtered = filter_notes_by_pitch(malformed_notes, max_pitch=60)
        
        # Should only include valid notes
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['pitch'], 48)
        self.assertEqual(filtered[1]['pitch'], 60)
    
    def test_apply_swing_valid_input(self):
        """Test applying swing with valid input."""
        swung_notes = apply_swing(self.sample_notes, swing_ratio=0.6, beat_duration=0.5)
        
        self.assertEqual(len(swung_notes), 3)  # Should have same number of notes
        self.assertEqual(swung_notes[0]['pitch'], 48)  # First note unchanged
        self.assertEqual(swung_notes[1]['pitch'], 60)  # Second note unchanged
        self.assertEqual(swung_notes[2]['pitch'], 72)  # Third note unchanged
    
    def test_apply_swing_off_beat_notes(self):
        """Test applying swing to off-beat notes."""
        off_beat_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': 0.0,  # On-beat
                'duration_seconds': 0.25,
                'track_index': 0
            },
            {
                'pitch': 62,
                'velocity': 80,
                'start_time_seconds': 0.25,  # Off-beat (0.5 of beat)
                'duration_seconds': 0.25,
                'track_index': 0
            },
            {
                'pitch': 64,
                'velocity': 80,
                'start_time_seconds': 0.5,  # On-beat
                'duration_seconds': 0.25,
                'track_index': 0
            }
        ]
        
        swung_notes = apply_swing(off_beat_notes, swing_ratio=0.6, beat_duration=0.5)
        
        # On-beat notes should be unchanged
        self.assertEqual(swung_notes[0]['start_time_seconds'], 0.0)
        self.assertEqual(swung_notes[2]['start_time_seconds'], 0.5)
        
        # Off-beat note should be delayed
        self.assertGreater(swung_notes[1]['start_time_seconds'], 0.25)
    
    def test_apply_swing_straight_ratio(self):
        """Test applying swing with straight ratio (no swing)."""
        swung_notes = apply_swing(self.sample_notes, swing_ratio=0.5, beat_duration=0.5)
        
        # All notes should be unchanged
        for i, note in enumerate(swung_notes):
            self.assertEqual(note['start_time_seconds'], self.sample_notes[i]['start_time_seconds'])
    
    def test_apply_swing_invalid_input(self):
        """Test applying swing with invalid input."""
        with self.assertRaises(TypeError):
            apply_swing("not a list", 0.6, 0.5)
        
        with self.assertRaises(TypeError):
            apply_swing(self.sample_notes, "not a number", 0.5)
        
        with self.assertRaises(TypeError):
            apply_swing(self.sample_notes, 0.6, "not a number")
        
        with self.assertRaises(ValueError):
            apply_swing(self.sample_notes, 0.6, 0)  # Zero beat duration
    
    def test_apply_swing_malformed_notes(self):
        """Test applying swing with malformed note data."""
        malformed_notes = [
            {'pitch': 60, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 0.25, 'track_index': 0},
            {'invalid': 'note'},  # Missing start_time_seconds
            {'pitch': 62, 'velocity': 80, 'start_time_seconds': 'not_a_number', 'duration_seconds': 0.25, 'track_index': 0},  # Invalid timing type
            {'pitch': 64, 'velocity': 80, 'start_time_seconds': 0.5, 'duration_seconds': 0.25, 'track_index': 0}
        ]
        
        swung_notes = apply_swing(malformed_notes, swing_ratio=0.6, beat_duration=0.5)
        
        # Should only process valid notes
        self.assertEqual(len(swung_notes), 2)
        self.assertEqual(swung_notes[0]['pitch'], 60)
        self.assertEqual(swung_notes[1]['pitch'], 64)
    
    def test_apply_swing_preserves_original(self):
        """Test that apply_swing doesn't modify the original notes."""
        original_notes = self.sample_notes.copy()
        swung_notes = apply_swing(self.sample_notes, swing_ratio=0.6, beat_duration=0.5)
        
        # Original notes should be unchanged
        for i, note in enumerate(original_notes):
            self.assertEqual(note['start_time_seconds'], self.sample_notes[i]['start_time_seconds'])
    
    def test_apply_swing_extreme_swing(self):
        """Test applying swing with extreme swing ratio."""
        off_beat_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': 0.25,  # Off-beat
                'duration_seconds': 0.25,
                'track_index': 0
            }
        ]
        
        # Test maximum swing
        swung_notes = apply_swing(off_beat_notes, swing_ratio=1.0, beat_duration=0.5)
        
        # Should be delayed but not more than 25% of beat duration
        max_delay = 0.5 * 0.25  # 25% of beat duration
        expected_max_time = 0.25 + max_delay
        self.assertLessEqual(swung_notes[0]['start_time_seconds'], expected_max_time)


if __name__ == '__main__':
    unittest.main()
