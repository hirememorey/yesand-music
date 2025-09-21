#!/usr/bin/env python3
"""
Unit tests for project.py module.

Tests the Project class for musical data management.
"""

import unittest
import tempfile
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import Project


class TestProject(unittest.TestCase):
    """Test cases for Project class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project = Project()
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
            },
            {
                'pitch': 48,
                'velocity': 100,
                'start_time_seconds': 2.0,
                'duration_seconds': 1.0,
                'track_index': 1
            }
        ]
    
    def test_project_initialization(self):
        """Test Project initialization with default values."""
        project = Project()
        
        self.assertEqual(project.tempo, 120)
        self.assertEqual(project.ticks_per_beat, 480)
        self.assertEqual(project.name, "Untitled Project")
        self.assertEqual(len(project.notes), 0)
        self.assertIsNone(project.filepath)
    
    def test_project_initialization_custom_values(self):
        """Test Project initialization with custom values."""
        project = Project(tempo=140, ticks_per_beat=960, name="Test Project")
        
        self.assertEqual(project.tempo, 140)
        self.assertEqual(project.ticks_per_beat, 960)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(len(project.notes), 0)
        self.assertIsNone(project.filepath)
    
    def test_add_note_valid(self):
        """Test adding a valid note."""
        self.project.add_note(60, 80, 0.0, 1.0, 0)
        
        self.assertEqual(len(self.project.notes), 1)
        note = self.project.notes[0]
        self.assertEqual(note['pitch'], 60)
        self.assertEqual(note['velocity'], 80)
        self.assertEqual(note['start_time_seconds'], 0.0)
        self.assertEqual(note['duration_seconds'], 1.0)
        self.assertEqual(note['track_index'], 0)
    
    def test_add_note_invalid_pitch(self):
        """Test adding a note with invalid pitch."""
        with self.assertRaises(ValueError):
            self.project.add_note(200, 80, 0.0, 1.0, 0)  # Pitch too high
        
        with self.assertRaises(ValueError):
            self.project.add_note(-1, 80, 0.0, 1.0, 0)  # Pitch too low
    
    def test_add_note_invalid_velocity(self):
        """Test adding a note with invalid velocity."""
        with self.assertRaises(ValueError):
            self.project.add_note(60, 200, 0.0, 1.0, 0)  # Velocity too high
        
        with self.assertRaises(ValueError):
            self.project.add_note(60, -1, 0.0, 1.0, 0)  # Velocity too low
    
    def test_add_note_invalid_time(self):
        """Test adding a note with invalid time."""
        with self.assertRaises(ValueError):
            self.project.add_note(60, 80, -1.0, 1.0, 0)  # Negative start time
    
    def test_add_note_invalid_duration(self):
        """Test adding a note with invalid duration."""
        with self.assertRaises(ValueError):
            self.project.add_note(60, 80, 0.0, 0.0, 0)  # Zero duration
        
        with self.assertRaises(ValueError):
            self.project.add_note(60, 80, 0.0, -1.0, 0)  # Negative duration
    
    def test_add_note_invalid_track_index(self):
        """Test adding a note with invalid track index."""
        with self.assertRaises(ValueError):
            self.project.add_note(60, 80, 0.0, 1.0, -1)  # Negative track index
    
    def test_clear_notes(self):
        """Test clearing all notes."""
        self.project.notes = self.sample_notes.copy()
        self.assertEqual(len(self.project.notes), 3)
        
        self.project.clear_notes()
        self.assertEqual(len(self.project.notes), 0)
    
    def test_get_all_notes(self):
        """Test getting all notes."""
        self.project.notes = self.sample_notes.copy()
        all_notes = self.project.get_all_notes()
        
        self.assertEqual(len(all_notes), 3)
        self.assertIsInstance(all_notes, list)
        # Should return a copy, not the original
        self.assertIsNot(all_notes, self.project.notes)
    
    def test_get_notes_by_track(self):
        """Test getting notes by track index."""
        self.project.notes = self.sample_notes.copy()
        
        track_0_notes = self.project.get_notes_by_track(0)
        self.assertEqual(len(track_0_notes), 2)
        self.assertEqual(track_0_notes[0]['pitch'], 60)
        self.assertEqual(track_0_notes[1]['pitch'], 64)
        
        track_1_notes = self.project.get_notes_by_track(1)
        self.assertEqual(len(track_1_notes), 1)
        self.assertEqual(track_1_notes[0]['pitch'], 48)
        
        track_2_notes = self.project.get_notes_by_track(2)
        self.assertEqual(len(track_2_notes), 0)
    
    def test_get_notes_in_time_range(self):
        """Test getting notes in a time range."""
        self.project.notes = self.sample_notes.copy()
        
        # Notes from 0.5 to 1.5 seconds
        notes_in_range = self.project.get_notes_in_time_range(0.5, 1.5)
        self.assertEqual(len(notes_in_range), 2)  # Should include notes at 0.0 and 1.0
        
        # Notes from 0.0 to 0.5 seconds
        notes_in_range = self.project.get_notes_in_time_range(0.0, 0.5)
        self.assertEqual(len(notes_in_range), 1)  # Should include note at 0.0
        
        # Notes from 3.0 to 4.0 seconds
        notes_in_range = self.project.get_notes_in_time_range(3.0, 4.0)
        self.assertEqual(len(notes_in_range), 0)  # No notes in this range
    
    def test_get_duration(self):
        """Test getting project duration."""
        # Empty project
        self.assertEqual(self.project.get_duration(), 0.0)
        
        # Project with notes
        self.project.notes = self.sample_notes.copy()
        duration = self.project.get_duration()
        self.assertEqual(duration, 3.0)  # Last note ends at 3.0 seconds
    
    def test_get_track_count(self):
        """Test getting track count."""
        # Empty project
        self.assertEqual(self.project.get_track_count(), 0)
        
        # Project with notes
        self.project.notes = self.sample_notes.copy()
        track_count = self.project.get_track_count()
        self.assertEqual(track_count, 2)  # Tracks 0 and 1
    
    def test_get_note_count(self):
        """Test getting note count."""
        # Empty project
        self.assertEqual(self.project.get_note_count(), 0)
        
        # Project with notes
        self.project.notes = self.sample_notes.copy()
        note_count = self.project.get_note_count()
        self.assertEqual(note_count, 3)
    
    def test_is_empty(self):
        """Test checking if project is empty."""
        # Empty project
        self.assertTrue(self.project.is_empty())
        
        # Project with notes
        self.project.notes = self.sample_notes.copy()
        self.assertFalse(self.project.is_empty())
    
    def test_get_metadata(self):
        """Test getting project metadata."""
        self.project.notes = self.sample_notes.copy()
        self.project.name = "Test Project"
        self.project.filepath = "/path/to/test.mid"
        
        metadata = self.project.get_metadata()
        
        self.assertEqual(metadata['name'], "Test Project")
        self.assertEqual(metadata['tempo'], 120)
        self.assertEqual(metadata['ticks_per_beat'], 480)
        self.assertEqual(metadata['filepath'], "/path/to/test.mid")
        self.assertEqual(metadata['note_count'], 3)
        self.assertEqual(metadata['track_count'], 2)
        self.assertEqual(metadata['duration_seconds'], 3.0)
    
    def test_str_representation(self):
        """Test string representation of project."""
        self.project.notes = self.sample_notes.copy()
        self.project.name = "Test Project"
        
        str_repr = str(self.project)
        self.assertIn("Test Project", str_repr)
        self.assertIn("3 notes", str_repr)
        self.assertIn("2 tracks", str_repr)
        self.assertIn("3.00s", str_repr)
    
    def test_repr_representation(self):
        """Test detailed string representation of project."""
        self.project.notes = self.sample_notes.copy()
        self.project.name = "Test Project"
        
        repr_str = repr(self.project)
        self.assertIn("Project", repr_str)
        self.assertIn("Test Project", repr_str)
        self.assertIn("tempo=120", repr_str)
        self.assertIn("ticks_per_beat=480", repr_str)
        self.assertIn("notes=3", repr_str)


if __name__ == '__main__':
    unittest.main()
