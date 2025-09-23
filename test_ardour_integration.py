#!/usr/bin/env python3
"""
Test script for Ardour file-based integration.

This script tests the Ardour integration functionality without requiring
a running Ardour instance.
"""

import sys
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ardour_integration import ArdourIntegration, ArdourTrack, ArdourRegion, ArdourProject


class TestArdourIntegration(unittest.TestCase):
    """Test cases for Ardour integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ardour = ArdourIntegration()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.ardour.cleanup()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ardour_track_creation(self):
        """Test ArdourTrack creation."""
        track = ArdourTrack(
            id="1",
            name="Test Track",
            type="midi",
            armed=True,
            muted=False,
            solo=False
        )
        
        self.assertEqual(track.id, "1")
        self.assertEqual(track.name, "Test Track")
        self.assertEqual(track.type, "midi")
        self.assertTrue(track.armed)
        self.assertFalse(track.muted)
        self.assertFalse(track.solo)
    
    def test_ardour_region_creation(self):
        """Test ArdourRegion creation."""
        region = ArdourRegion(
            id="1",
            name="Test Region",
            track_id="1",
            start_time=0.0,
            length=4.0,
            position=0.0,
            selected=True
        )
        
        self.assertEqual(region.id, "1")
        self.assertEqual(region.name, "Test Region")
        self.assertEqual(region.track_id, "1")
        self.assertEqual(region.start_time, 0.0)
        self.assertEqual(region.length, 4.0)
        self.assertEqual(region.position, 0.0)
        self.assertTrue(region.selected)
    
    def test_ardour_project_creation(self):
        """Test ArdourProject creation."""
        tracks = [
            ArdourTrack(id="1", name="Track 1", type="midi"),
            ArdourTrack(id="2", name="Track 2", type="audio")
        ]
        regions = [
            ArdourRegion(id="1", name="Region 1", track_id="1", 
                        start_time=0.0, length=4.0, position=0.0)
        ]
        
        project = ArdourProject(
            name="Test Project",
            path="/test/project",
            tempo=120.0,
            time_signature="4/4",
            tracks=tracks,
            regions=regions
        )
        
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.path, "/test/project")
        self.assertEqual(project.tempo, 120.0)
        self.assertEqual(project.time_signature, "4/4")
        self.assertEqual(len(project.tracks), 2)
        self.assertEqual(len(project.regions), 1)
    
    @patch('subprocess.run')
    def test_connect_success(self, mock_run):
        """Test successful connection to Ardour."""
        # Mock successful process check
        mock_run.return_value.returncode = 0
        
        result = self.ardour.connect()
        
        self.assertTrue(result)
        self.assertTrue(self.ardour.connected)
    
    @patch('subprocess.run')
    def test_connect_failure(self, mock_run):
        """Test failed connection to Ardour."""
        # Mock failed process check
        mock_run.return_value.returncode = 1
        
        result = self.ardour.connect()
        
        self.assertFalse(result)
        self.assertFalse(self.ardour.connected)
    
    def test_disconnect(self):
        """Test disconnection from Ardour."""
        self.ardour.connected = True
        
        result = self.ardour.disconnect()
        
        self.assertTrue(result)
        self.assertFalse(self.ardour.connected)
        self.assertIsNone(self.ardour.current_project)
    
    def test_list_tracks_not_connected(self):
        """Test listing tracks when not connected."""
        tracks = self.ardour.list_tracks()
        
        self.assertEqual(tracks, [])
    
    def test_export_selected_region_not_connected(self):
        """Test exporting when not connected."""
        result = self.ardour.export_selected_region()
        
        self.assertIsNone(result)
    
    def test_import_midi_file_not_found(self):
        """Test importing non-existent MIDI file."""
        result = self.ardour.import_midi_file("nonexistent.mid")
        
        self.assertFalse(result)
    
    def test_analyze_selected_region_not_connected(self):
        """Test analyzing when not connected."""
        result = self.ardour.analyze_selected_region()
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Not connected to Ardour")
    
    def test_improve_selected_region_not_connected(self):
        """Test improving when not connected."""
        result = self.ardour.improve_selected_region("groove")
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Not connected to Ardour")
    
    def test_create_lua_script_export(self):
        """Test creating export Lua script."""
        script_path = os.path.join(self.temp_dir, "export.lua")
        result = self.ardour.create_lua_script("export_selected", script_path)
        
        self.assertEqual(result, script_path)
        self.assertTrue(os.path.exists(script_path))
        
        # Check script content
        with open(script_path, 'r') as f:
            content = f.read()
            self.assertIn("export_selected_region", content)
            self.assertIn("Session:get()", content)
    
    def test_create_lua_script_import(self):
        """Test creating import Lua script."""
        script_path = os.path.join(self.temp_dir, "import.lua")
        result = self.ardour.create_lua_script("import_midi", script_path)
        
        self.assertEqual(result, script_path)
        self.assertTrue(os.path.exists(script_path))
        
        # Check script content
        with open(script_path, 'r') as f:
            content = f.read()
            self.assertIn("import_midi_file", content)
            self.assertIn("Session:get()", content)
    
    def test_create_lua_script_analyze(self):
        """Test creating analyze Lua script."""
        script_path = os.path.join(self.temp_dir, "analyze.lua")
        result = self.ardour.create_lua_script("analyze", script_path)
        
        self.assertEqual(result, script_path)
        self.assertTrue(os.path.exists(script_path))
        
        # Check script content
        with open(script_path, 'r') as f:
            content = f.read()
            self.assertIn("analyze_selected_region", content)
            self.assertIn("Session:get()", content)
    
    def test_create_lua_script_invalid_type(self):
        """Test creating Lua script with invalid type."""
        script_path = os.path.join(self.temp_dir, "invalid.lua")
        result = self.ardour.create_lua_script("invalid_type", script_path)
        
        self.assertIsNone(result)
    
    def test_context_manager(self):
        """Test context manager functionality."""
        with ArdourIntegration() as ardour:
            self.assertIsInstance(ardour, ArdourIntegration)
        
        # Should not raise any exceptions


class TestArdourCommands(unittest.TestCase):
    """Test cases for Ardour command integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        from commands.control_plane import ControlPlane
        self.cp = ControlPlane()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.cp.close()
    
    def test_ardour_connect_command(self):
        """Test ardour connect command."""
        result = self.cp.execute("ardour connect")
        
        self.assertIn("Ardour:", result)
        # Should either succeed or fail gracefully
        self.assertTrue("Connected successfully" in result or "Failed to connect" in result)
    
    def test_ardour_disconnect_command(self):
        """Test ardour disconnect command."""
        result = self.cp.execute("ardour disconnect")
        
        self.assertIn("Ardour:", result)
        self.assertIn("Disconnected successfully", result)
    
    def test_ardour_tracks_command(self):
        """Test ardour tracks command."""
        result = self.cp.execute("ardour tracks")
        
        self.assertIn("Ardour", result)
        # Should either show tracks or indicate not connected
        self.assertTrue("Tracks:" in result or "not connected" in result)
    
    def test_ardour_export_command(self):
        """Test ardour export selected command."""
        result = self.cp.execute("ardour export selected")
        
        self.assertIn("Ardour:", result)
        # Should either succeed or fail gracefully
        self.assertTrue("exported" in result or "Failed" in result)
    
    def test_ardour_import_command(self):
        """Test ardour import command."""
        result = self.cp.execute("ardour import test.mid")
        
        self.assertIn("Ardour:", result)
        # Should either succeed or fail gracefully
        self.assertTrue("imported" in result or "Failed" in result)
    
    def test_ardour_analyze_command(self):
        """Test ardour analyze selected command."""
        result = self.cp.execute("ardour analyze selected")
        
        self.assertIn("Ardour", result)
        # Should either show analysis or indicate error
        self.assertTrue("Analysis" in result or "error" in result)
    
    def test_ardour_improve_command(self):
        """Test ardour improve selected command."""
        result = self.cp.execute("ardour improve selected")
        
        self.assertIn("Ardour", result)
        # Should either show improvement or indicate error
        self.assertTrue("Improvement" in result or "error" in result)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
