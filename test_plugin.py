#!/usr/bin/env python3
"""
Test script for StyleTransfer JUCE Plugin
Tests the plugin's MIDI transformation capabilities
"""

import subprocess
import sys
import os

def test_plugin_installation():
    """Test if the plugin is properly installed"""
    print("🎵 Testing StyleTransfer Plugin Installation...")
    
    # Check AudioUnit installation
    au_path = "/Users/harrisgordon/Library/Audio/Plug-Ins/Components/Style Transfer.component"
    if os.path.exists(au_path):
        print("✅ AudioUnit plugin installed successfully")
    else:
        print("❌ AudioUnit plugin not found")
        return False
    
    # Check VST3 installation
    vst3_path = "/Users/harrisgordon/Library/Audio/Plug-Ins/VST3/Style Transfer.vst3"
    if os.path.exists(vst3_path):
        print("✅ VST3 plugin installed successfully")
    else:
        print("❌ VST3 plugin not found")
        return False
    
    return True

def test_plugin_functionality():
    """Test the plugin's MIDI transformation functionality"""
    print("\n🎹 Testing Plugin Functionality...")
    
    # Test the Python control plane integration
    try:
        result = subprocess.run([
            sys.executable, "control_plane_cli.py", "status"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Python control plane is working")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print("❌ Python control plane failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Python control plane timed out")
        return False
    except Exception as e:
        print(f"❌ Python control plane error: {e}")
        return False
    
    return True

def test_midi_transformations():
    """Test MIDI transformation algorithms"""
    print("\n🎼 Testing MIDI Transformations...")
    
    try:
        # Test swing transformation
        result = subprocess.run([
            sys.executable, "control_plane_cli.py", "set swing to 0.7"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Swing parameter setting works")
        else:
            print("❌ Swing parameter setting failed")
            return False
        
        # Test accent transformation
        result = subprocess.run([
            sys.executable, "control_plane_cli.py", "set accent to 25"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Accent parameter setting works")
        else:
            print("❌ Accent parameter setting failed")
            return False
        
        # Test MIDI playback
        result = subprocess.run([
            sys.executable, "control_plane_cli.py", "play scale C major"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ MIDI playback works")
        else:
            print("❌ MIDI playback failed")
            return False
            
    except Exception as e:
        print(f"❌ MIDI transformation test error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 StyleTransfer Plugin Test Suite")
    print("=" * 50)
    
    # Test 1: Plugin Installation
    if not test_plugin_installation():
        print("\n❌ Plugin installation test failed")
        return False
    
    # Test 2: Plugin Functionality
    if not test_plugin_functionality():
        print("\n❌ Plugin functionality test failed")
        return False
    
    # Test 3: MIDI Transformations
    if not test_midi_transformations():
        print("\n❌ MIDI transformation test failed")
        return False
    
    print("\n🎉 All tests passed! Plugin is ready for use.")
    print("\nNext steps:")
    print("1. Open Logic Pro, GarageBand, or Reaper")
    print("2. Load the 'Style Transfer' plugin on a MIDI track")
    print("3. Adjust swing and accent parameters")
    print("4. Play MIDI notes to hear the transformations")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
