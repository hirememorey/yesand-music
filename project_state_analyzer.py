#!/usr/bin/env python3
"""
Project State Analyzer

This system analyzes existing DAW projects to extract musical context automatically.
It works with the Musical Context Interview to provide dual context sources.

Key Features:
- Analyzes MIDI files and DAW project files
- Extracts technical musical information (key, tempo, time signature)
- Identifies existing musical parts and patterns
- Provides context that complements user input
"""

import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import mido
from collections import Counter


@dataclass
class ProjectState:
    """Musical context extracted from project files"""
    project_path: str
    key_signature: Optional[str] = None
    tempo: Optional[int] = None
    time_signature: Optional[str] = None
    tracks: List[Dict[str, Any]] = None
    musical_parts: List[str] = None
    chord_progression: List[str] = None
    rhythmic_patterns: List[str] = None
    project_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tracks is None:
            self.tracks = []
        if self.musical_parts is None:
            self.musical_parts = []
        if self.chord_progression is None:
            self.chord_progression = []
        if self.rhythmic_patterns is None:
            self.rhythmic_patterns = []
        if self.project_metadata is None:
            self.project_metadata = {}


class ProjectStateAnalyzer:
    """Analyzes DAW projects to extract musical context"""
    
    def __init__(self):
        self.supported_formats = ['.mid', '.midi', '.ardour', '.logic', '.cubase']
        self.key_signatures = {
            'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6,
            'C#': 7, 'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6
        }
        self.chord_qualities = ['major', 'minor', 'maj7', 'min7', 'dom7', 'dim', 'aug']
    
    def analyze_project(self, project_path: str) -> ProjectState:
        """Analyze a DAW project and extract musical context"""
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        project_state = ProjectState(project_path=str(project_path))
        
        # Analyze based on file type
        if project_path.suffix.lower() in ['.mid', '.midi']:
            self._analyze_midi_file(project_path, project_state)
        elif project_path.suffix.lower() == '.ardour':
            self._analyze_ardour_project(project_path, project_state)
        elif project_path.suffix.lower() in ['.logic', '.cubase']:
            self._analyze_daw_project(project_path, project_state)
        else:
            # Try to find MIDI files in the directory
            self._analyze_directory(project_path, project_state)
        
        return project_state
    
    def _analyze_midi_file(self, midi_path: Path, project_state: ProjectState):
        """Analyze a MIDI file for musical context"""
        try:
            midi_file = mido.MidiFile(str(midi_path))
            
            # Extract tempo
            for track in midi_file.tracks:
                for msg in track:
                    if msg.type == 'set_tempo':
                        project_state.tempo = int(mido.tempo2bpm(msg.tempo))
                        break
                if project_state.tempo:
                    break
            
            # Extract time signature
            for track in midi_file.tracks:
                for msg in track:
                    if msg.type == 'time_signature':
                        project_state.time_signature = f"{msg.numerator}/{msg.denominator}"
                        break
                if project_state.time_signature:
                    break
            
            # Analyze tracks and musical content
            self._analyze_midi_tracks(midi_file, project_state)
            
            # Analyze chord progression
            self._analyze_chord_progression(midi_file, project_state)
            
            # Analyze rhythmic patterns
            self._analyze_rhythmic_patterns(midi_file, project_state)
            
        except Exception as e:
            print(f"Error analyzing MIDI file {midi_path}: {e}")
    
    def _analyze_midi_tracks(self, midi_file: mido.MidiFile, project_state: ProjectState):
        """Analyze MIDI tracks to identify musical parts"""
        track_analysis = []
        
        for i, track in enumerate(midi_file.tracks):
            track_info = {
                'track_number': i,
                'name': track.name or f"Track {i+1}",
                'instrument': None,
                'note_count': 0,
                'pitch_range': None,
                'rhythmic_complexity': 0,
                'musical_role': None
            }
            
            notes = []
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    notes.append({
                        'pitch': msg.note,
                        'velocity': msg.velocity,
                        'time': msg.time
                    })
                    track_info['note_count'] += 1
            
            if notes:
                # Analyze pitch range
                pitches = [note['pitch'] for note in notes]
                track_info['pitch_range'] = (min(pitches), max(pitches))
                
                # Determine musical role based on pitch range and note count
                track_info['musical_role'] = self._determine_musical_role(
                    track_info['pitch_range'], 
                    track_info['note_count'],
                    len(notes)
                )
                
                # Analyze rhythmic complexity
                track_info['rhythmic_complexity'] = self._calculate_rhythmic_complexity(notes)
            
            track_analysis.append(track_info)
        
        project_state.tracks = track_analysis
        
        # Extract musical parts from track analysis
        musical_parts = []
        for track in track_analysis:
            if track['musical_role']:
                musical_parts.append(f"{track['musical_role']} ({track['name']})")
        
        project_state.musical_parts = musical_parts
    
    def _determine_musical_role(self, pitch_range: Tuple[int, int], note_count: int, total_notes: int) -> Optional[str]:
        """Determine the musical role of a track based on pitch range and note density"""
        if not pitch_range:
            return None
        
        low_note, high_note = pitch_range
        
        # Bass range (C2 to C4, MIDI notes 36-60)
        if low_note <= 60 and high_note <= 72:
            if note_count < total_notes * 0.3:  # Sparse notes
                return "bass line"
            else:
                return "bass pattern"
        
        # Mid range (C4 to C6, MIDI notes 60-84)
        elif 60 <= low_note <= 84:
            if note_count < total_notes * 0.4:  # Sparse notes
                return "melody"
            else:
                return "chord progression"
        
        # High range (C6+, MIDI notes 84+)
        elif low_note >= 84:
            if note_count < total_notes * 0.3:  # Sparse notes
                return "lead melody"
            else:
                return "high harmony"
        
        # Drum range (typically low MIDI notes)
        elif low_note <= 40:
            return "drums"
        
        return "unknown"
    
    def _calculate_rhythmic_complexity(self, notes: List[Dict]) -> float:
        """Calculate rhythmic complexity of a track (0.0 to 1.0)"""
        if len(notes) < 2:
            return 0.0
        
        # Calculate note density
        total_time = sum(note['time'] for note in notes)
        note_density = len(notes) / max(total_time, 1)
        
        # Calculate velocity variation
        velocities = [note['velocity'] for note in notes]
        velocity_variance = len(set(velocities)) / len(velocities)
        
        # Calculate timing variation
        times = [note['time'] for note in notes]
        time_variance = len(set(times)) / len(times)
        
        # Combine factors
        complexity = (note_density * 0.4 + velocity_variance * 0.3 + time_variance * 0.3)
        return min(complexity, 1.0)
    
    def _analyze_chord_progression(self, midi_file: mido.MidiFile, project_state: ProjectState):
        """Analyze chord progression from MIDI file"""
        # This is a simplified chord analysis
        # In a real implementation, you'd use music theory libraries
        
        chord_notes = []
        for track in midi_file.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    chord_notes.append(msg.note)
        
        if chord_notes:
            # Simple chord detection based on note clusters
            chord_progression = self._detect_chord_progression(chord_notes)
            project_state.chord_progression = chord_progression
    
    def _detect_chord_progression(self, notes: List[int]) -> List[str]:
        """Detect chord progression from note list (simplified)"""
        # This is a very basic chord detection
        # In practice, you'd use proper music theory analysis
        
        # Group notes by octave and find common chord patterns
        chord_notes = [note % 12 for note in notes]  # Convert to pitch classes
        note_counts = Counter(chord_notes)
        
        # Find the most common notes (simplified chord detection)
        common_notes = [note for note, count in note_counts.most_common(3)]
        
        # Convert to chord names (simplified)
        chord_names = []
        for note in common_notes:
            chord_names.append(self._pitch_class_to_chord(note))
        
        return chord_names
    
    def _pitch_class_to_chord(self, pitch_class: int) -> str:
        """Convert pitch class to chord name (simplified)"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[pitch_class]
    
    def _analyze_rhythmic_patterns(self, midi_file: mido.MidiFile, project_state: ProjectState):
        """Analyze rhythmic patterns in the MIDI file"""
        # This is a simplified rhythmic analysis
        # In practice, you'd use more sophisticated rhythm analysis
        
        rhythmic_patterns = []
        
        for track in midi_file.tracks:
            track_notes = []
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    track_notes.append(msg.time)
            
            if track_notes:
                # Analyze note timing patterns
                pattern = self._analyze_timing_pattern(track_notes)
                if pattern:
                    rhythmic_patterns.append(pattern)
        
        project_state.rhythmic_patterns = rhythmic_patterns
    
    def _analyze_timing_pattern(self, note_times: List[int]) -> Optional[str]:
        """Analyze timing pattern of notes (simplified)"""
        if len(note_times) < 2:
            return None
        
        # Calculate intervals between notes
        intervals = [note_times[i+1] - note_times[i] for i in range(len(note_times)-1)]
        
        # Find common intervals
        interval_counts = Counter(intervals)
        most_common_interval = interval_counts.most_common(1)[0][0]
        
        # Classify pattern based on common interval
        if most_common_interval == 0:
            return "chord"
        elif most_common_interval < 100:
            return "fast pattern"
        elif most_common_interval < 500:
            return "medium pattern"
        else:
            return "slow pattern"
    
    def _analyze_ardour_project(self, ardour_path: Path, project_state: ProjectState):
        """Analyze Ardour project file (simplified)"""
        # This would parse Ardour's XML project files
        # For now, we'll look for MIDI files in the project directory
        
        project_dir = ardour_path.parent
        midi_files = list(project_dir.glob("*.mid")) + list(project_dir.glob("*.midi"))
        
        if midi_files:
            # Analyze the first MIDI file found
            self._analyze_midi_file(midi_files[0], project_state)
    
    def _analyze_daw_project(self, project_path: Path, project_state: ProjectState):
        """Analyze other DAW project files (simplified)"""
        # This would parse various DAW project formats
        # For now, we'll look for MIDI files in the project directory
        
        project_dir = project_path.parent
        midi_files = list(project_dir.glob("*.mid")) + list(project_dir.glob("*.midi"))
        
        if midi_files:
            # Analyze the first MIDI file found
            self._analyze_midi_file(midi_files[0], project_state)
    
    def _analyze_directory(self, directory_path: Path, project_state: ProjectState):
        """Analyze a directory for MIDI files"""
        midi_files = list(directory_path.glob("*.mid")) + list(directory_path.glob("*.midi"))
        
        if midi_files:
            # Analyze the first MIDI file found
            self._analyze_midi_file(midi_files[0], project_state)
    
    def get_context_summary(self, project_state: ProjectState) -> str:
        """Get a human-readable summary of the project state"""
        summary_parts = []
        
        if project_state.tempo:
            summary_parts.append(f"🎼 Tempo: {project_state.tempo} BPM")
        
        if project_state.time_signature:
            summary_parts.append(f"⏱️ Time Signature: {project_state.time_signature}")
        
        if project_state.musical_parts:
            summary_parts.append(f"🎸 Musical Parts: {', '.join(project_state.musical_parts)}")
        
        if project_state.chord_progression:
            summary_parts.append(f"🎵 Chord Progression: {' → '.join(project_state.chord_progression)}")
        
        if project_state.rhythmic_patterns:
            summary_parts.append(f"🥁 Rhythmic Patterns: {', '.join(project_state.rhythmic_patterns)}")
        
        return "\n".join(summary_parts)
    
    def get_context_for_ai(self, project_state: ProjectState) -> Dict[str, Any]:
        """Get project state in format suitable for AI processing"""
        return {
            "project_path": project_state.project_path,
            "key_signature": project_state.key_signature,
            "tempo": project_state.tempo,
            "time_signature": project_state.time_signature,
            "tracks": project_state.tracks,
            "musical_parts": project_state.musical_parts,
            "chord_progression": project_state.chord_progression,
            "rhythmic_patterns": project_state.rhythmic_patterns,
            "project_metadata": project_state.project_metadata
        }


def demo_analyzer():
    """Demo the project state analyzer"""
    analyzer = ProjectStateAnalyzer()
    
    # Look for MIDI files in the current directory
    current_dir = Path(".")
    midi_files = list(current_dir.glob("*.mid")) + list(current_dir.glob("*.midi"))
    
    if not midi_files:
        print("No MIDI files found in current directory")
        return
    
    # Analyze the first MIDI file
    midi_file = midi_files[0]
    print(f"Analyzing: {midi_file}")
    
    try:
        project_state = analyzer.analyze_project(str(midi_file))
        
        print("\n" + "="*50)
        print("🎵 PROJECT STATE ANALYSIS")
        print("="*50)
        print(analyzer.get_context_summary(project_state))
        
        print("\n" + "="*50)
        print("🤖 AI CONTEXT")
        print("="*50)
        print(json.dumps(analyzer.get_context_for_ai(project_state), indent=2))
        
    except Exception as e:
        print(f"Error analyzing project: {e}")


if __name__ == "__main__":
    demo_analyzer()
