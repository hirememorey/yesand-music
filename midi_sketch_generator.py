#!/usr/bin/env python3
"""
MIDI Sketch Generator

This system generates quick MIDI sketches for testing musical suggestions.
It creates simple, playable MIDI patterns that users can quickly test and iterate on.

Key Features:
- Quick MIDI generation for testing ideas
- Multiple variations of the same suggestion
- Simple, playable patterns
- Easy integration with DAW workflows
"""

import json
import os
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import mido
import random


@dataclass
class MIDISketch:
    """A MIDI sketch for testing musical suggestions"""
    sketch_id: str
    title: str
    description: str
    midi_data: List[Dict[str, Any]]
    tempo: int
    time_signature: str
    key_signature: str
    duration_seconds: float
    track_count: int
    created_at: datetime


class MIDISketchGenerator:
    """Generates MIDI sketches for testing musical suggestions"""
    
    def __init__(self):
        self.output_dir = "generated_sketches"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Musical knowledge for sketch generation
        self.chord_progressions = {
            'I-V-vi-IV': [0, 7, 9, 5],  # C-G-Am-F
            'I-vi-IV-V': [0, 9, 5, 7],  # C-Am-F-G
            'ii-V-I': [2, 7, 0],         # Dm-G-C
            'I-IV-V': [0, 5, 7],         # C-F-G
            'vi-IV-I-V': [9, 5, 0, 7]    # Am-F-C-G
        }
        
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic_major': [0, 2, 4, 7, 9],
            'pentatonic_minor': [0, 3, 5, 7, 10],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        self.rhythmic_patterns = {
            'straight_eighths': [1, 1, 1, 1, 1, 1, 1, 1],
            'swung_eighths': [1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 0.5],
            'syncopated': [1, 0.5, 0.5, 1, 0.5, 0.5, 1, 1],
            'quarter_notes': [2, 2, 2, 2],
            'half_notes': [4, 4],
            'whole_notes': [8]
        }
    
    def generate_sketch(self, 
                       suggestion_type: str,
                       key_signature: str = "C major",
                       tempo: int = 120,
                       time_signature: str = "4/4",
                       duration_bars: int = 4,
                       style: str = "general") -> MIDISketch:
        """Generate a MIDI sketch based on suggestion type and parameters"""
        
        sketch_id = str(uuid.uuid4())
        title = f"{suggestion_type.replace('_', ' ').title()} Sketch"
        description = f"MIDI sketch for {suggestion_type} in {key_signature} at {tempo} BPM"
        
        # Generate MIDI data based on suggestion type
        if suggestion_type == "chord_progression":
            midi_data = self._generate_chord_progression_sketch(key_signature, tempo, duration_bars)
        elif suggestion_type == "melody":
            midi_data = self._generate_melody_sketch(key_signature, tempo, duration_bars, style)
        elif suggestion_type == "bass_line":
            midi_data = self._generate_bass_line_sketch(key_signature, tempo, duration_bars, style)
        elif suggestion_type == "rhythm_pattern":
            midi_data = self._generate_rhythm_pattern_sketch(tempo, duration_bars, style)
        elif suggestion_type == "bridge":
            midi_data = self._generate_bridge_sketch(key_signature, tempo, duration_bars)
        elif suggestion_type == "intro":
            midi_data = self._generate_intro_sketch(key_signature, tempo, duration_bars)
        else:
            midi_data = self._generate_general_sketch(key_signature, tempo, duration_bars)
        
        # Calculate duration
        duration_seconds = (duration_bars * 4 * 60) / tempo  # Assuming 4/4 time
        
        # Count tracks
        track_count = len(set(note.get('track', 0) for note in midi_data))
        
        sketch = MIDISketch(
            sketch_id=sketch_id,
            title=title,
            description=description,
            midi_data=midi_data,
            tempo=tempo,
            time_signature=time_signature,
            key_signature=key_signature,
            duration_seconds=duration_seconds,
            track_count=track_count,
            created_at=datetime.now()
        )
        
        return sketch
    
    def _generate_chord_progression_sketch(self, key: str, tempo: int, bars: int) -> List[Dict[str, Any]]:
        """Generate a chord progression sketch"""
        midi_data = []
        
        # Get chord progression
        progression = self._get_chord_progression(key)
        
        # Calculate timing
        beat_duration = 60 / tempo  # seconds per beat
        bar_duration = beat_duration * 4  # 4 beats per bar
        
        for bar in range(bars):
            chord = progression[bar % len(progression)]
            start_time = bar * bar_duration
            
            # Generate chord notes
            chord_notes = self._get_chord_notes(chord, key)
            
            for i, note in enumerate(chord_notes):
                midi_data.append({
                    'pitch': note,
                    'velocity': 80,
                    'start_time_seconds': start_time,
                    'duration_seconds': bar_duration,
                    'track': 0,
                    'note_type': 'chord'
                })
        
        return midi_data
    
    def _generate_melody_sketch(self, key: str, tempo: int, bars: int, style: str) -> List[Dict[str, Any]]:
        """Generate a melody sketch"""
        midi_data = []
        
        # Get scale for the key
        scale = self._get_scale_for_key(key)
        
        # Get rhythmic pattern
        rhythm_pattern = self._get_rhythm_pattern(style)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        note_index = 0
        time_offset = 0
        
        for bar in range(bars):
            for beat in range(4):  # 4 beats per bar
                for note_duration in rhythm_pattern:
                    if time_offset >= bar_duration:
                        break
                    
                    # Get note from scale
                    note = scale[note_index % len(scale)]
                    octave = 4 + (note_index // len(scale))
                    midi_note = note + (octave * 12)
                    
                    # Add some variation
                    if random.random() < 0.3:  # 30% chance of variation
                        midi_note += random.choice([-1, 1])
                    
                    midi_data.append({
                        'pitch': midi_note,
                        'velocity': 70 + random.randint(-10, 10),
                        'start_time_seconds': time_offset + (bar * bar_duration),
                        'duration_seconds': note_duration * beat_duration,
                        'track': 1,
                        'note_type': 'melody'
                    })
                    
                    time_offset += note_duration * beat_duration
                    note_index += 1
                
                if time_offset >= bar_duration:
                    break
            
            time_offset = 0
        
        return midi_data
    
    def _generate_bass_line_sketch(self, key: str, tempo: int, bars: int, style: str) -> List[Dict[str, Any]]:
        """Generate a bass line sketch"""
        midi_data = []
        
        # Get chord progression
        progression = self._get_chord_progression(key)
        
        # Get scale for the key
        scale = self._get_scale_for_key(key)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        for bar in range(bars):
            chord = progression[bar % len(progression)]
            
            # Generate bass line for this chord
            if style == "walking":
                # Walking bass line
                chord_notes = self._get_chord_notes(chord, key)
                for beat in range(4):
                    note = chord_notes[beat % len(chord_notes)]
                    octave = 2  # Bass octave
                    midi_note = note + (octave * 12)
                    
                    midi_data.append({
                        'pitch': midi_note,
                        'velocity': 90,
                        'start_time_seconds': (bar * bar_duration) + (beat * beat_duration),
                        'duration_seconds': beat_duration,
                        'track': 2,
                        'note_type': 'bass'
                    })
            else:
                # Simple root note bass
                root_note = self._get_root_note(chord, key)
                octave = 2
                midi_note = root_note + (octave * 12)
                
                midi_data.append({
                    'pitch': midi_note,
                    'velocity': 85,
                    'start_time_seconds': bar * bar_duration,
                    'duration_seconds': bar_duration,
                    'track': 2,
                    'note_type': 'bass'
                })
        
        return midi_data
    
    def _generate_rhythm_pattern_sketch(self, tempo: int, bars: int, style: str) -> List[Dict[str, Any]]:
        """Generate a rhythm pattern sketch"""
        midi_data = []
        
        # Get rhythmic pattern
        rhythm_pattern = self._get_rhythm_pattern(style)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        time_offset = 0
        
        for bar in range(bars):
            for note_duration in rhythm_pattern:
                if time_offset >= bar_duration:
                    break
                
                # Generate drum pattern
                if random.random() < 0.7:  # 70% chance of note
                    midi_data.append({
                        'pitch': 36,  # Kick drum
                        'velocity': 100,
                        'start_time_seconds': time_offset + (bar * bar_duration),
                        'duration_seconds': 0.1,  # Short drum hit
                        'track': 3,
                        'note_type': 'drums'
                    })
                
                time_offset += note_duration * beat_duration
            
            time_offset = 0
        
        return midi_data
    
    def _generate_bridge_sketch(self, key: str, tempo: int, bars: int) -> List[Dict[str, Any]]:
        """Generate a bridge sketch"""
        midi_data = []
        
        # Bridge typically uses contrasting harmony
        contrast_key = self._get_contrast_key(key)
        progression = self._get_chord_progression(contrast_key)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        for bar in range(bars):
            chord = progression[bar % len(progression)]
            start_time = bar * bar_duration
            
            # Generate chord notes
            chord_notes = self._get_chord_notes(chord, contrast_key)
            
            for i, note in enumerate(chord_notes):
                midi_data.append({
                    'pitch': note,
                    'velocity': 75,
                    'start_time_seconds': start_time,
                    'duration_seconds': bar_duration,
                    'track': 0,
                    'note_type': 'bridge_chord'
                })
        
        return midi_data
    
    def _generate_intro_sketch(self, key: str, tempo: int, bars: int) -> List[Dict[str, Any]]:
        """Generate an intro sketch"""
        midi_data = []
        
        # Intro typically establishes the key and mood
        progression = self._get_chord_progression(key)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        for bar in range(bars):
            chord = progression[bar % len(progression)]
            start_time = bar * bar_duration
            
            # Generate chord notes with softer dynamics
            chord_notes = self._get_chord_notes(chord, key)
            
            for i, note in enumerate(chord_notes):
                midi_data.append({
                    'pitch': note,
                    'velocity': 60,  # Softer for intro
                    'start_time_seconds': start_time,
                    'duration_seconds': bar_duration,
                    'track': 0,
                    'note_type': 'intro_chord'
                })
        
        return midi_data
    
    def _generate_general_sketch(self, key: str, tempo: int, bars: int) -> List[Dict[str, Any]]:
        """Generate a general musical sketch"""
        midi_data = []
        
        # Simple chord progression
        progression = self._get_chord_progression(key)
        
        # Calculate timing
        beat_duration = 60 / tempo
        bar_duration = beat_duration * 4
        
        for bar in range(bars):
            chord = progression[bar % len(progression)]
            start_time = bar * bar_duration
            
            # Generate chord notes
            chord_notes = self._get_chord_notes(chord, key)
            
            for i, note in enumerate(chord_notes):
                midi_data.append({
                    'pitch': note,
                    'velocity': 80,
                    'start_time_seconds': start_time,
                    'duration_seconds': bar_duration,
                    'track': 0,
                    'note_type': 'general'
                })
        
        return midi_data
    
    def _get_chord_progression(self, key: str) -> List[str]:
        """Get a chord progression for the given key"""
        # Simple chord progression mapping
        progressions = {
            'C major': ['C', 'G', 'Am', 'F'],
            'G major': ['G', 'D', 'Em', 'C'],
            'D major': ['D', 'A', 'Bm', 'G'],
            'A major': ['A', 'E', 'F#m', 'D'],
            'E major': ['E', 'B', 'C#m', 'A'],
            'B major': ['B', 'F#', 'G#m', 'E'],
            'F# major': ['F#', 'C#', 'D#m', 'B'],
            'F major': ['F', 'C', 'Dm', 'Bb'],
            'Bb major': ['Bb', 'F', 'Gm', 'Eb'],
            'Eb major': ['Eb', 'Bb', 'Cm', 'Ab'],
            'Ab major': ['Ab', 'Eb', 'Fm', 'Db'],
            'Db major': ['Db', 'Ab', 'Bbm', 'Gb']
        }
        
        return progressions.get(key, ['C', 'G', 'Am', 'F'])
    
    def _get_scale_for_key(self, key: str) -> List[int]:
        """Get the scale for the given key"""
        # Extract root note and mode
        if 'minor' in key.lower():
            return self.scales['minor']
        else:
            return self.scales['major']
    
    def _get_chord_notes(self, chord: str, key: str) -> List[int]:
        """Get MIDI note numbers for a chord"""
        # Simple chord mapping (C major)
        chord_notes = {
            'C': [60, 64, 67],      # C-E-G
            'Dm': [62, 65, 69],     # D-F-A
            'Em': [64, 67, 71],     # E-G-B
            'F': [65, 69, 72],      # F-A-C
            'G': [67, 71, 74],      # G-B-D
            'Am': [69, 72, 76],     # A-C-E
            'Bdim': [71, 74, 77]    # B-D-F
        }
        
        return chord_notes.get(chord, [60, 64, 67])
    
    def _get_root_note(self, chord: str, key: str) -> int:
        """Get the root note of a chord"""
        root_notes = {
            'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71
        }
        
        root = chord[0] if chord[0] in root_notes else 'C'
        return root_notes[root]
    
    def _get_rhythm_pattern(self, style: str) -> List[float]:
        """Get a rhythmic pattern for the given style"""
        if style == "jazz":
            return self.rhythmic_patterns['swung_eighths']
        elif style == "rock":
            return self.rhythmic_patterns['straight_eighths']
        elif style == "blues":
            return self.rhythmic_patterns['syncopated']
        else:
            return self.rhythmic_patterns['quarter_notes']
    
    def _get_contrast_key(self, key: str) -> str:
        """Get a contrasting key for bridges"""
        contrasts = {
            'C major': 'A minor',
            'G major': 'E minor',
            'D major': 'B minor',
            'A major': 'F# minor',
            'E major': 'C# minor',
            'B major': 'G# minor',
            'F# major': 'D# minor',
            'F major': 'D minor',
            'Bb major': 'G minor',
            'Eb major': 'C minor',
            'Ab major': 'F minor',
            'Db major': 'Bb minor'
        }
        return contrasts.get(key, 'A minor')
    
    def save_sketch(self, sketch: MIDISketch, filename: Optional[str] = None) -> str:
        """Save a MIDI sketch to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{sketch.title.replace(' ', '_')}_{timestamp}.mid"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create MIDI file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)
        
        # Add tempo
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(sketch.tempo)))
        
        # Add time signature
        track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
        
        # Add notes
        for note_data in sketch.midi_data:
            # Note on
            track.append(mido.Message('note_on', 
                                    channel=note_data.get('track', 0),
                                    note=note_data['pitch'],
                                    velocity=note_data['velocity'],
                                    time=0))
            
            # Note off
            track.append(mido.Message('note_off',
                                    channel=note_data.get('track', 0),
                                    note=note_data['pitch'],
                                    velocity=0,
                                    time=int(note_data['duration_seconds'] * 1000)))
        
        # Save file
        midi_file.save(filepath)
        
        return filepath
    
    def generate_multiple_sketches(self, 
                                 suggestion_type: str,
                                 key_signature: str = "C major",
                                 tempo: int = 120,
                                 count: int = 3) -> List[MIDISketch]:
        """Generate multiple variations of a sketch"""
        sketches = []
        
        for i in range(count):
            # Vary the style slightly
            style_variations = ["general", "jazz", "rock", "blues"]
            style = style_variations[i % len(style_variations)]
            
            sketch = self.generate_sketch(
                suggestion_type=suggestion_type,
                key_signature=key_signature,
                tempo=tempo,
                style=style
            )
            
            sketch.title = f"{sketch.title} (Variation {i+1})"
            sketches.append(sketch)
        
        return sketches


def demo_sketch_generator():
    """Demo the MIDI sketch generator"""
    generator = MIDISketchGenerator()
    
    # Generate different types of sketches
    sketch_types = ["chord_progression", "melody", "bass_line", "bridge", "intro"]
    
    for sketch_type in sketch_types:
        print(f"\nGenerating {sketch_type} sketch...")
        
        sketch = generator.generate_sketch(
            suggestion_type=sketch_type,
            key_signature="G minor",
            tempo=120,
            duration_bars=4
        )
        
        print(f"Title: {sketch.title}")
        print(f"Description: {sketch.description}")
        print(f"Duration: {sketch.duration_seconds:.1f} seconds")
        print(f"Tracks: {sketch.track_count}")
        print(f"Notes: {len(sketch.midi_data)}")
        
        # Save the sketch
        filepath = generator.save_sketch(sketch)
        print(f"Saved to: {filepath}")


if __name__ == "__main__":
    demo_sketch_generator()
