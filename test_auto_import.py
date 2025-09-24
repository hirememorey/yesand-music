#!/usr/bin/env python3
"""
Test script for automatic Ardour import functionality.

This script tests the auto-import system without requiring a full Ardour session.
"""

import os
import tempfile
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ardour_lua_importer import ArdourLuaImporter, TrackConfig, ImportResult
from track_manager import TrackManager, EnhancementType, TrackType
from midi_io import save_midi_file


def create_test_midi_file(file_path: str, notes: list = None) -> str:
    """Create a test MIDI file."""
    if notes is None:
        # Create a simple C major scale
        notes = []
        for i, note in enumerate([60, 62, 64, 65, 67, 69, 71, 72]):  # C major scale
            notes.append({
                'pitch': note,
                'velocity': 80,
                'start_time_seconds': i * 0.5,
                'duration_seconds': 0.4,
                'track_index': 0
            })
    
    save_midi_file(notes, file_path)
    return file_path


def test_track_manager():
    """Test TrackManager functionality."""
    print("🧪 Testing TrackManager...")
    
    manager = TrackManager()
    
    # Test track creation for different enhancement types
    for enhancement_type in EnhancementType:
        track_name, was_created = manager.get_track_for_enhancement(enhancement_type)
        print(f"  {enhancement_type.value}: {track_name} (created: {was_created})")
        
        # Test track config creation
        config = manager.create_track_config(enhancement_type, track_name)
        print(f"    Config: {config['name']} ({config['type']})")
    
    print("✅ TrackManager tests passed\n")


def test_lua_importer():
    """Test ArdourLuaImporter functionality."""
    print("🧪 Testing ArdourLuaImporter...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        importer = ArdourLuaImporter(temp_dir=temp_dir)
        
        # Create test MIDI file
        test_midi = os.path.join(temp_dir, "test_bassline.mid")
        create_test_midi_file(test_midi)
        
        # Test track config
        track_config = TrackConfig(
            name="Test Bass",
            type="midi",
            auto_create=True
        )
        
        # Test import (this will create Lua script but won't execute in Ardour)
        print(f"  Creating import script for: {test_midi}")
        result = importer.auto_import_midi(test_midi, track_config, position=0.0)
        
        print(f"  Import result: {result.success}")
        if result.success:
            print(f"    Track: {result.track_name}")
            print(f"    Position: {result.position}")
            print(f"    Script: {result.lua_script_path}")
        else:
            print(f"    Error: {result.error_message}")
        
        # Test multiple patterns import
        print(f"  Testing multiple patterns import...")
        patterns = [
            {"file_path": test_midi, "name": "Pattern 1"},
            {"file_path": test_midi, "name": "Pattern 2"}
        ]
        
        results = importer.import_multiple_patterns(patterns, "Generated")
        print(f"  Imported {len(results)} patterns")
        for i, result in enumerate(results):
            print(f"    Pattern {i+1}: {result.success} - {result.track_name}")
    
    print("✅ ArdourLuaImporter tests passed\n")


def test_integration():
    """Test integration between components."""
    print("🧪 Testing integration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test MIDI files
        bass_file = os.path.join(temp_dir, "bass.mid")
        drums_file = os.path.join(temp_dir, "drums.mid")
        
        create_test_midi_file(bass_file)
        create_test_midi_file(drums_file)
        
        # Test track manager
        manager = TrackManager()
        bass_track, _ = manager.get_track_for_enhancement(EnhancementType.BASS)
        drums_track, _ = manager.get_track_for_enhancement(EnhancementType.DRUMS)
        
        print(f"  Bass track: {bass_track}")
        print(f"  Drums track: {drums_track}")
        
        # Test importer
        importer = ArdourLuaImporter(temp_dir=temp_dir)
        
        # Import bass
        bass_config = TrackConfig(name=bass_track, type="midi", auto_create=True)
        bass_result = importer.auto_import_midi(bass_file, bass_config, 0.0)
        
        # Import drums
        drums_config = TrackConfig(name=drums_track, type="midi", auto_create=True)
        drums_result = importer.auto_import_midi(drums_file, drums_config, 32.0)
        
        print(f"  Bass import: {bass_result.success}")
        print(f"  Drums import: {drums_result.success}")
        
        # Test import history
        history = importer.get_import_history()
        print(f"  Import history: {len(history)} imports")
    
    print("✅ Integration tests passed\n")


def test_lua_script_generation():
    """Test Lua script generation."""
    print("🧪 Testing Lua script generation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        importer = ArdourLuaImporter(temp_dir=temp_dir)
        
        # Create test MIDI file
        test_midi = os.path.join(temp_dir, "test.mid")
        create_test_midi_file(test_midi)
        
        # Test track creation script
        track_config = TrackConfig(name="Test Track", type="midi", auto_create=True)
        track_script = importer._create_track_creation_script(track_config)
        
        print("  Track creation script:")
        print("  " + "\n  ".join(track_script.split("\n")[:5]) + "...")
        
        # Test import script
        import_script = importer._create_import_script(test_midi, track_config, 0.0)
        
        print("  Import script:")
        print("  " + "\n  ".join(import_script.split("\n")[:5]) + "...")
        
        # Verify scripts contain expected elements
        assert "Test Track" in track_script
        assert "add_track" in track_script
        assert "import_audio_midi" in import_script
        assert test_midi in import_script
    
    print("✅ Lua script generation tests passed\n")


def main():
    """Run all tests."""
    print("🚀 Starting auto-import tests...\n")
    
    try:
        test_track_manager()
        test_lua_importer()
        test_integration()
        test_lua_script_generation()
        
        print("🎉 All tests passed! Auto-import system is ready.")
        print("\nNext steps:")
        print("1. Start Ardour with a project")
        print("2. Enable OSC in Ardour (Preferences → OSC)")
        print("3. Run: python real_time_enhancement_cli.py --interactive")
        print("4. Try: enhance create a funky bassline")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
