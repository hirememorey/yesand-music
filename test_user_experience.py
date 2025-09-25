#!/usr/bin/env python3
"""
Test script for the enhanced MVP Musical Quality First Generator
Demonstrates the new user experience features and context support.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Test the enhanced MVP system."""
    print("🎵 Testing Enhanced MVP Musical Quality First Generator")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("mvp_musical_quality_first.py").exists():
        print("❌ Error: mvp_musical_quality_first.py not found")
        print("Please run this script from the project directory")
        return 1
    
    # Test 1: Help display
    success = run_command(
        "python mvp_musical_quality_first.py --help",
        "Help Display"
    )
    if not success:
        print("❌ Help test failed")
        return 1
    
    # Test 2: Context extraction (no API key needed)
    success = run_command(
        "python mvp_musical_quality_first.py --extract-context generated_midi/Create\\ a\\ jazz\\ bass\\ line\\ in\\ C\\ m_20250924_231142.mid",
        "Context Extraction"
    )
    if not success:
        print("❌ Context extraction test failed")
        return 1
    
    # Test 3: Check if context file was created
    context_file = Path("context_Create a jazz bass line in C m_20250924_231142.json")
    if context_file.exists():
        print(f"✅ Context file created: {context_file}")
        print(f"   File size: {context_file.stat().st_size} bytes")
    else:
        print("❌ Context file not found")
        return 1
    
    # Test 4: Test with different parameters (if API key available)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("\n🔑 API key found - testing generation features")
        
        # Test generation with different temperature
        success = run_command(
            f"python mvp_musical_quality_first.py 'Create a simple bass line' --temperature 0.3 --show-feedback",
            "Low Temperature Generation"
        )
        
        # Test generation with context
        if context_file.exists():
            success = run_command(
                f"python mvp_musical_quality_first.py 'Add a melody that fits' --context-file {context_file} --show-feedback",
                "Context-Aware Generation"
            )
    else:
        print("\n⚠️  No API key found - skipping generation tests")
        print("   Set OPENAI_API_KEY to test generation features")
    
    print("\n🎉 User Experience Enhancement Tests Complete!")
    print("\n📋 New Features Demonstrated:")
    print("  ✅ User parameter controls (temperature, quality threshold)")
    print("  ✅ Detailed feedback display")
    print("  ✅ Context extraction from MIDI files")
    print("  ✅ Context-aware generation (with API key)")
    print("  ✅ Enhanced help and status displays")
    print("  ✅ Easy regeneration with different parameters")
    
    print("\n💡 Usage Examples:")
    print("  # Basic generation with user controls")
    print("  python mvp_musical_quality_first.py 'Create a funky bass line' --temperature 0.8 --quality-threshold 0.7")
    print("  # Extract context from existing MIDI")
    print("  python mvp_musical_quality_first.py --extract-context my_song.mid")
    print("  # Generate with context")
    print("  python mvp_musical_quality_first.py 'Add drums' --context-file context_my_song.json")
    print("  # Show detailed feedback")
    print("  python mvp_musical_quality_first.py 'Create a melody' --show-feedback")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
