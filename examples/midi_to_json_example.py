#!/usr/bin/env python3
"""
Example usage of the MIDI to JSON workflow system.

This example demonstrates how the new MIDI to JSON workflow will work
once implemented according to MIDI_TO_JSON_IMPLEMENTATION.md
"""

import json
from typing import Dict, List, Any

# Example of what the musical notation JSON format will look like
def create_example_musical_notation() -> Dict[str, Any]:
    """Create an example musical notation JSON structure."""
    return {
        "project": {
            "tempo": 120,
            "key": "G minor",
            "timeSignature": "4/4",
            "name": "Alice In Chains Style Project"
        },
        "tracks": [
            {
                "name": "Drums",
                "type": "midi",
                "channel": 9,
                "notes": [
                    {
                        "pitch": "C4",  # Kick drum
                        "startTime": 0.0,
                        "duration": 0.5,
                        "velocity": 80,
                        "channel": 9
                    },
                    {
                        "pitch": "D4",  # Snare drum
                        "startTime": 0.5,
                        "duration": 0.3,
                        "velocity": 75,
                        "channel": 9
                    },
                    {
                        "pitch": "C4",  # Kick drum
                        "startTime": 1.0,
                        "duration": 0.5,
                        "velocity": 80,
                        "channel": 9
                    },
                    {
                        "pitch": "D4",  # Snare drum
                        "startTime": 1.5,
                        "duration": 0.3,
                        "velocity": 75,
                        "channel": 9
                    }
                ]
            },
            {
                "name": "Guitar",
                "type": "midi",
                "channel": 0,
                "notes": [
                    {
                        "pitch": "G3",  # G minor chord
                        "startTime": 0.0,
                        "duration": 2.0,
                        "velocity": 70,
                        "channel": 0
                    },
                    {
                        "pitch": "Bb3",
                        "startTime": 0.0,
                        "duration": 2.0,
                        "velocity": 65,
                        "channel": 0
                    },
                    {
                        "pitch": "D4",
                        "startTime": 0.0,
                        "duration": 2.0,
                        "velocity": 60,
                        "channel": 0
                    }
                ]
            }
        ],
        "musicalContext": {
            "harmonicProgression": "Gm-Bb-F-Gm",
            "rhythmicFeel": "straight 4/4 rock",
            "style": "grunge/alternative rock",
            "complexity": "intermediate",
            "mood": "dark, heavy, brooding"
        }
    }

def create_example_openai_prompt() -> str:
    """Create an example OpenAI prompt with musical context."""
    musical_notation = create_example_musical_notation()
    
    return f"""
You are a professional bassist. Generate a bass pattern in G minor that sounds like Alice In Chains.

Musical Context:
{json.dumps(musical_notation, indent=2)}

Requirements:
- Key: G minor
- Style: Alice In Chains (grunge/alternative rock)
- Pattern type: Bass line that complements the existing guitar and drums
- Mood: Dark, heavy, brooding
- Output format: JSON with musical notation

Generate the bass pattern as JSON in this format:
{{
  "tracks": [
    {{
      "name": "Bass",
      "notes": [
        {{
          "pitch": "G2",
          "startTime": 0.0,
          "duration": 0.5,
          "velocity": 80,
          "channel": 0
        }}
      ]
    }}
  ]
}}
"""

def create_example_generated_bass() -> Dict[str, Any]:
    """Create an example of what OpenAI might generate."""
    return {
        "tracks": [
            {
                "name": "Bass",
                "type": "midi",
                "channel": 0,
                "notes": [
                    {
                        "pitch": "G2",  # Root note
                        "startTime": 0.0,
                        "duration": 0.5,
                        "velocity": 85,
                        "channel": 0
                    },
                    {
                        "pitch": "Bb2",  # Minor third
                        "startTime": 0.5,
                        "duration": 0.5,
                        "velocity": 80,
                        "channel": 0
                    },
                    {
                        "pitch": "D3",  # Fifth
                        "startTime": 1.0,
                        "duration": 0.5,
                        "velocity": 75,
                        "channel": 0
                    },
                    {
                        "pitch": "G2",  # Root note
                        "startTime": 1.5,
                        "duration": 0.5,
                        "velocity": 85,
                        "channel": 0
                    }
                ]
            }
        ]
    }

def main():
    """Demonstrate the MIDI to JSON workflow."""
    print("=== MIDI to JSON Workflow Example ===\n")
    
    # 1. Show existing project context
    print("1. Existing Project Context:")
    musical_notation = create_example_musical_notation()
    print(json.dumps(musical_notation, indent=2))
    print()
    
    # 2. Show OpenAI prompt
    print("2. OpenAI Prompt with Context:")
    prompt = create_example_openai_prompt()
    print(prompt)
    print()
    
    # 3. Show generated result
    print("3. Generated Bass Pattern:")
    generated_bass = create_example_generated_bass()
    print(json.dumps(generated_bass, indent=2))
    print()
    
    # 4. Show workflow summary
    print("4. Complete Workflow:")
    print("   User: 'generate a bass pattern like Alice In Chains in GMinor'")
    print("   System: Extracts existing MIDI from Ardour project")
    print("   System: Converts MIDI to musical notation JSON")
    print("   System: Sends context + prompt to OpenAI")
    print("   System: OpenAI generates contextually appropriate bass pattern")
    print("   System: Converts generated JSON back to MIDI file")
    print("   System: Imports MIDI file to Ardour track")
    print("   Result: New bass track that fits with existing music")

if __name__ == "__main__":
    main()