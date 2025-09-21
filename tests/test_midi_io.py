#!/usr/bin/env python3
"""
Unit tests for midi_io.py module.

Tests the universal note format and MIDI file I/O functionality.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi_io import parse_midi_file, save_midi_file, validate_notes_data, get_file_info


class TestMidiIO(unittest.TestCase):
    """Test cases for MIDI I/O functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': 0.0,
                'duration_seconds': 1.0,
                'track_index': 0
            },
            {
                'pitch': 64,
                'velocity': 90,
                'start_time_seconds': 1.0,
                'duration_seconds': 0.5,
                'track_index': 0
            }
        ]
    
    def test_validate_notes_data_valid(self):
        """Test validation of valid notes data."""
        self.assertTrue(validate_notes_data(self.sample_notes))
    
    def test_validate_notes_data_invalid_structure(self):
        """Test validation of invalid notes data structure."""
        invalid_notes = [
            {'pitch': 60, 'velocity': 80},  # Missing required fields
            {'pitch': 60, 'velocity': 80, 'start_time_seconds': 0.0, 'duration_seconds': 1.0}  # Missing track_index
        ]
        self.assertFalse(validate_notes_data(invalid_notes))
    
    def test_validate_notes_data_invalid_ranges(self):
        """Test validation of notes data with invalid ranges."""
        invalid_notes = [
            {
                'pitch': 200,  # Invalid pitch
                'velocity': 80,
                'start_time_seconds': 0.0,
                'duration_seconds': 1.0,
                'track_index': 0
            }
        ]
        self.assertFalse(validate_notes_data(invalid_notes))
    
    def test_validate_notes_data_negative_time(self):
        """Test validation of notes data with negative time."""
        invalid_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': -1.0,  # Invalid negative time
                'duration_seconds': 1.0,
                'track_index': 0
            }
        ]
        self.assertFalse(validate_notes_data(invalid_notes))
    
    def test_validate_notes_data_zero_duration(self):
        """Test validation of notes data with zero duration."""
        invalid_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': 0.0,
                'duration_seconds': 0.0,  # Invalid zero duration
                'track_index': 0
            }
        ]
        self.assertFalse(validate_notes_data(invalid_notes))
    
    def test_validate_notes_data_invalid_track_index(self):
        """Test validation of notes data with invalid track index."""
        invalid_notes = [
            {
                'pitch': 60,
                'velocity': 80,
                'start_time_seconds': 0.0,
                'duration_seconds': 1.0,
                'track_index': -1  # Invalid negative track index
            }
        ]
        self.assertFalse(validate_notes_data(invalid_notes))
    
    def test_validate_notes_data_empty_list(self):
        """Test validation of empty notes list."""
        self.assertTrue(validate_notes_data([]))
    
    def test_validate_notes_data_not_list(self):
        """Test validation of non-list input."""
        self.assertFalse(validate_notes_data("not a list"))
        self.assertFalse(validate_notes_data(None))
        self.assertFalse(validate_notes_data({}))
    
    @patch('midi_io.mido.MidiFile')
    def test_parse_midi_file_success(self, mock_midi_file):
        """Test successful MIDI file parsing."""
        # Mock MIDI file structure
        mock_track = MagicMock()
        mock_track.__iter__ = lambda self: iter([
            MagicMock(type='note_on', channel=0, note=60, velocity=80, time=0),
            MagicMock(type='note_off', channel=0, note=60, velocity=0, time=480),
            MagicMock(type='note_on', channel=0, note=64, velocity=90, time=0),
            MagicMock(type='note_off', channel=0, note=64, velocity=0, time=240)
        ])
        
        mock_file = MagicMock()
        mock_file.ticks_per_beat = 480
        mock_file.tracks = [mock_track]
        mock_midi_file.return_value = mock_file
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            notes = parse_midi_file(tmp_path)
            self.assertIsInstance(notes, list)
            # Note: The actual parsing logic would need to be tested with real MIDI files
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_parse_midi_file_not_found(self):
        """Test MIDI file parsing with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            parse_midi_file("nonexistent.mid")
    
    def test_save_midi_file_success(self):
        """Test successful MIDI file saving."""
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            save_midi_file(tmp_path, self.sample_notes)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 0)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_save_midi_file_empty_notes(self):
        """Test MIDI file saving with empty notes."""
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            with self.assertRaises(ValueError):
                save_midi_file(tmp_path, [])
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_save_midi_file_invalid_notes(self):
        """Test MIDI file saving with invalid notes data."""
        invalid_notes = [{'invalid': 'data'}]
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            with self.assertRaises(ValueError):
                save_midi_file(tmp_path, invalid_notes)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_save_midi_file_invalid_path(self):
        """Test MIDI file saving with invalid path."""
        invalid_notes = self.sample_notes
        
        with self.assertRaises(OSError):
            save_midi_file("/invalid/path/that/does/not/exist.mid", invalid_notes)


if __name__ == '__main__':
    unittest.main()
