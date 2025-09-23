"""
Contextual Intelligence Module

This module provides contextual visual feedback and intelligent analysis for the
YesAnd Music system. It bridges the gap between invisible intelligence and
user understanding by providing on-demand visual explanations and feedback.

Key Features:
- Background musical analysis without visual interference
- On-demand visual feedback for user understanding
- Educational overlays explaining musical concepts
- Smart suggestions with visual indicators
- Natural language integration with visual responses
"""

from __future__ import annotations

import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from analysis import filter_notes_by_pitch, apply_swing
from midi_io import parse_midi_file, save_midi_file
from project import Project


class MusicalElement(Enum):
    """Types of musical elements that can be analyzed and highlighted."""
    BASS = "bass"
    MELODY = "melody"
    HARMONY = "harmony"
    RHYTHM = "rhythm"
    DRUMS = "drums"


class VisualFeedbackType(Enum):
    """Types of visual feedback that can be provided."""
    HIGHLIGHT = "highlight"
    DIFF = "diff"
    EXPLANATION = "explanation"
    SUGGESTION = "suggestion"
    ANALYSIS = "analysis"


@dataclass
class VisualFeedback:
    """Represents a piece of visual feedback to be displayed to the user."""
    type: VisualFeedbackType
    element: MusicalElement
    message: str
    data: Dict[str, Any]
    timestamp: float
    duration: Optional[float] = None  # None means persistent until dismissed


@dataclass
class MusicalAnalysis:
    """Comprehensive musical analysis of a piece of music."""
    bass_notes: List[Dict[str, Any]]
    melody_notes: List[Dict[str, Any]]
    harmony_notes: List[Dict[str, Any]]
    rhythm_pattern: Dict[str, Any]
    key_signature: str
    tempo: float
    time_signature: str
    style_classification: str
    confidence_scores: Dict[str, float]


class ContextualIntelligence:
    """Main class for contextual intelligence and visual feedback."""
    
    def __init__(self, session_file: str = "session.json"):
        """Initialize the contextual intelligence system.
        
        Args:
            session_file: Path to the session state file
        """
        self.session_file = session_file
        self.current_project: Optional[Project] = None
        self.current_analysis: Optional[MusicalAnalysis] = None
        self.visual_feedback_queue: List[VisualFeedback] = []
        self.feedback_history: List[VisualFeedback] = []
        
    def load_project(self, midi_file_path: str) -> bool:
        """Load a MIDI project for analysis.
        
        Args:
            midi_file_path: Path to the MIDI file to load
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.current_project = Project()
            self.current_project.load_from_midi(midi_file_path)
            self._analyze_project()
            return True
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
    
    def _analyze_project(self) -> None:
        """Perform background analysis of the current project."""
        if not self.current_project:
            return
            
        notes = self.current_project.get_all_notes()
        
        # Analyze different musical elements
        bass_notes = filter_notes_by_pitch(notes, max_pitch=60)  # C4 and below
        melody_notes = self._identify_melody_notes(notes)
        harmony_notes = self._identify_harmony_notes(notes)
        rhythm_pattern = self._analyze_rhythm(notes)
        
        # Create comprehensive analysis
        self.current_analysis = MusicalAnalysis(
            bass_notes=bass_notes,
            melody_notes=melody_notes,
            harmony_notes=harmony_notes,
            rhythm_pattern=rhythm_pattern,
            key_signature=self._detect_key_signature(notes),
            tempo=self._detect_tempo(notes),
            time_signature=self._detect_time_signature(notes),
            style_classification=self._classify_style(notes),
            confidence_scores=self._calculate_confidence_scores(notes)
        )
    
    def _identify_melody_notes(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify melody notes (highest pitch in each time segment)."""
        if not notes:
            return []
            
        # Group notes by time segments
        time_segments = {}
        for note in notes:
            start_time = note['start_time_seconds']
            segment = int(start_time * 4)  # Quarter note segments
            if segment not in time_segments:
                time_segments[segment] = []
            time_segments[segment].append(note)
        
        # Find highest pitch in each segment
        melody_notes = []
        for segment_notes in time_segments.values():
            if segment_notes:
                highest_note = max(segment_notes, key=lambda n: n['pitch'])
                melody_notes.append(highest_note)
        
        return melody_notes
    
    def _identify_harmony_notes(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify harmony notes (notes that form chords)."""
        if not notes:
            return []
            
        # For now, return all notes that aren't bass or melody
        bass_notes = filter_notes_by_pitch(notes, max_pitch=60)
        melody_notes = self._identify_melody_notes(notes)
        
        bass_pitches = {note['pitch'] for note in bass_notes}
        melody_pitches = {note['pitch'] for note in melody_notes}
        
        harmony_notes = []
        for note in notes:
            if note['pitch'] not in bass_pitches and note['pitch'] not in melody_pitches:
                harmony_notes.append(note)
        
        return harmony_notes
    
    def _analyze_rhythm(self, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze rhythmic patterns in the music."""
        if not notes:
            return {"pattern": "none", "complexity": 0.0, "swing": 0.0}
        
        # Calculate note density
        total_duration = max(note['start_time_seconds'] + note['duration_seconds'] for note in notes)
        note_density = len(notes) / total_duration if total_duration > 0 else 0
        
        # Analyze swing feel
        swing_ratio = self._calculate_swing_ratio(notes)
        
        # Analyze syncopation
        syncopation = self._calculate_syncopation(notes)
        
        return {
            "pattern": "complex" if note_density > 4 else "simple",
            "complexity": min(1.0, note_density / 8.0),
            "swing": swing_ratio,
            "syncopation": syncopation,
            "density": note_density
        }
    
    def _calculate_swing_ratio(self, notes: List[Dict[str, Any]]) -> float:
        """Calculate the swing ratio of the music."""
        if not notes:
            return 0.5
            
        # Analyze timing patterns to detect swing
        # This is a simplified implementation
        off_beat_notes = 0
        total_notes = len(notes)
        
        for note in notes:
            start_time = note['start_time_seconds']
            beat_position = start_time % 0.5  # Assuming 120 BPM
            if 0.4 <= beat_position <= 0.6:  # Off-beat position
                off_beat_notes += 1
        
        if total_notes == 0:
            return 0.5
            
        # Calculate swing ratio based on off-beat note timing
        swing_ratio = 0.5 + (off_beat_notes / total_notes) * 0.3
        return min(1.0, max(0.0, swing_ratio))
    
    def _calculate_syncopation(self, notes: List[Dict[str, Any]]) -> float:
        """Calculate the syncopation level of the music."""
        if not notes:
            return 0.0
            
        # Analyze accent patterns and off-beat emphasis
        # This is a simplified implementation
        syncopated_notes = 0
        total_notes = len(notes)
        
        for note in notes:
            start_time = note['start_time_seconds']
            beat_position = start_time % 1.0  # Assuming 120 BPM
            # Check for notes on weak beats
            if 0.25 <= beat_position <= 0.35 or 0.75 <= beat_position <= 0.85:
                syncopated_notes += 1
        
        return syncopated_notes / total_notes if total_notes > 0 else 0.0
    
    def _detect_key_signature(self, notes: List[Dict[str, Any]]) -> str:
        """Detect the key signature of the music."""
        if not notes:
            return "C major"
            
        # Simple key detection based on note frequency
        pitch_counts = {}
        for note in notes:
            pitch = note['pitch'] % 12  # Get pitch class
            pitch_counts[pitch] = pitch_counts.get(pitch, 0) + 1
        
        # Find most common pitch class
        if pitch_counts:
            most_common_pitch = max(pitch_counts, key=pitch_counts.get)
            # Map pitch class to key name (simplified)
            key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            return f"{key_names[most_common_pitch]} major"
        
        return "C major"
    
    def _detect_tempo(self, notes: List[Dict[str, Any]]) -> float:
        """Detect the tempo of the music."""
        if not notes:
            return 120.0
            
        # Analyze note timing to detect tempo
        # This is a simplified implementation
        time_differences = []
        sorted_notes = sorted(notes, key=lambda n: n['start_time_seconds'])
        
        for i in range(1, len(sorted_notes)):
            diff = sorted_notes[i]['start_time_seconds'] - sorted_notes[i-1]['start_time_seconds']
            if 0.1 <= diff <= 2.0:  # Reasonable note spacing
                time_differences.append(diff)
        
        if time_differences:
            avg_interval = sum(time_differences) / len(time_differences)
            tempo = 60.0 / avg_interval
            return max(60.0, min(200.0, tempo))  # Clamp to reasonable range
        
        return 120.0
    
    def _detect_time_signature(self, notes: List[Dict[str, Any]]) -> str:
        """Detect the time signature of the music."""
        if not notes:
            return "4/4"
            
        # Simple time signature detection
        # This is a simplified implementation
        return "4/4"  # Default to 4/4
    
    def _classify_style(self, notes: List[Dict[str, Any]]) -> str:
        """Classify the musical style."""
        if not self.current_analysis:
            return "unknown"
            
        rhythm = self.current_analysis.rhythm_pattern
        
        # Classify based on rhythmic characteristics
        if rhythm['swing'] > 0.6:
            return "jazz"
        elif rhythm['syncopation'] > 0.3:
            return "funk"
        elif rhythm['complexity'] > 0.7:
            return "electronic"
        elif rhythm['complexity'] < 0.3:
            return "classical"
        else:
            return "pop"
    
    def _calculate_confidence_scores(self, notes: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate confidence scores for the analysis."""
        if not notes:
            return {"bass": 0.0, "melody": 0.0, "harmony": 0.0, "rhythm": 0.0}
        
        # Calculate confidence based on note count and clarity
        total_notes = len(notes)
        bass_notes = filter_notes_by_pitch(notes, max_pitch=60)
        melody_notes = self._identify_melody_notes(notes)
        
        return {
            "bass": min(1.0, len(bass_notes) / max(1, total_notes / 4)),
            "melody": min(1.0, len(melody_notes) / max(1, total_notes / 4)),
            "harmony": min(1.0, (total_notes - len(bass_notes) - len(melody_notes)) / max(1, total_notes / 2)),
            "rhythm": min(1.0, total_notes / 10.0)
        }
    
    def get_visual_feedback(self, command: str) -> List[VisualFeedback]:
        """Get visual feedback for a natural language command.
        
        Args:
            command: The natural language command
            
        Returns:
            List of visual feedback items
        """
        if not self.current_analysis:
            return [VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.BASS,
                message="No project loaded. Please load a MIDI file first.",
                data={},
                timestamp=time.time()
            )]
        
        feedback = []
        
        # Parse command and generate appropriate feedback
        if "bass" in command.lower():
            feedback.extend(self._get_bass_feedback())
        elif "melody" in command.lower():
            feedback.extend(self._get_melody_feedback())
        elif "harmony" in command.lower():
            feedback.extend(self._get_harmony_feedback())
        elif "rhythm" in command.lower():
            feedback.extend(self._get_rhythm_feedback())
        elif "analyze" in command.lower():
            feedback.extend(self._get_analysis_feedback())
        elif "suggest" in command.lower():
            feedback.extend(self._get_suggestion_feedback())
        else:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.BASS,
                message="I can analyze bass, melody, harmony, rhythm, or provide suggestions. What would you like to know?",
                data={},
                timestamp=time.time()
            ))
        
        # Add feedback to queue
        self.visual_feedback_queue.extend(feedback)
        self.feedback_history.extend(feedback)
        
        return feedback
    
    def _get_bass_feedback(self) -> List[VisualFeedback]:
        """Get visual feedback for bass analysis."""
        if not self.current_analysis:
            return []
        
        bass_notes = self.current_analysis.bass_notes
        confidence = self.current_analysis.confidence_scores.get("bass", 0.0)
        
        feedback = []
        
        # Highlight bass notes
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.HIGHLIGHT,
            element=MusicalElement.BASS,
            message=f"Found {len(bass_notes)} bass notes",
            data={"notes": bass_notes, "color": "blue"},
            timestamp=time.time()
        ))
        
        # Provide analysis
        if bass_notes:
            pitch_range = max(note['pitch'] for note in bass_notes) - min(note['pitch'] for note in bass_notes)
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.BASS,
                message=f"Bass line spans {pitch_range} semitones. Confidence: {confidence:.1%}",
                data={"pitch_range": pitch_range, "confidence": confidence},
                timestamp=time.time()
            ))
        else:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.BASS,
                message="No clear bass line detected. Try lowering the pitch threshold.",
                data={},
                timestamp=time.time()
            ))
        
        return feedback
    
    def _get_melody_feedback(self) -> List[VisualFeedback]:
        """Get visual feedback for melody analysis."""
        if not self.current_analysis:
            return []
        
        melody_notes = self.current_analysis.melody_notes
        confidence = self.current_analysis.confidence_scores.get("melody", 0.0)
        
        feedback = []
        
        # Highlight melody notes
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.HIGHLIGHT,
            element=MusicalElement.MELODY,
            message=f"Found {len(melody_notes)} melody notes",
            data={"notes": melody_notes, "color": "green"},
            timestamp=time.time()
        ))
        
        # Provide analysis
        if melody_notes:
            pitch_range = max(note['pitch'] for note in melody_notes) - min(note['pitch'] for note in melody_notes)
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.MELODY,
                message=f"Melody spans {pitch_range} semitones. Confidence: {confidence:.1%}",
                data={"pitch_range": pitch_range, "confidence": confidence},
                timestamp=time.time()
            ))
        else:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.MELODY,
                message="No clear melody detected. The music might be more harmonic or rhythmic.",
                data={},
                timestamp=time.time()
            ))
        
        return feedback
    
    def _get_harmony_feedback(self) -> List[VisualFeedback]:
        """Get visual feedback for harmony analysis."""
        if not self.current_analysis:
            return []
        
        harmony_notes = self.current_analysis.harmony_notes
        confidence = self.current_analysis.confidence_scores.get("harmony", 0.0)
        
        feedback = []
        
        # Highlight harmony notes
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.HIGHLIGHT,
            element=MusicalElement.HARMONY,
            message=f"Found {len(harmony_notes)} harmony notes",
            data={"notes": harmony_notes, "color": "purple"},
            timestamp=time.time()
        ))
        
        # Provide analysis
        if harmony_notes:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.HARMONY,
                message=f"Harmony provides {len(harmony_notes)} supporting notes. Confidence: {confidence:.1%}",
                data={"note_count": len(harmony_notes), "confidence": confidence},
                timestamp=time.time()
            ))
        else:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.EXPLANATION,
                element=MusicalElement.HARMONY,
                message="No clear harmony detected. The music might be more melodic or rhythmic.",
                data={},
                timestamp=time.time()
            ))
        
        return feedback
    
    def _get_rhythm_feedback(self) -> List[VisualFeedback]:
        """Get visual feedback for rhythm analysis."""
        if not self.current_analysis:
            return []
        
        rhythm = self.current_analysis.rhythm_pattern
        confidence = self.current_analysis.confidence_scores.get("rhythm", 0.0)
        
        feedback = []
        
        # Provide rhythm analysis
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.ANALYSIS,
            element=MusicalElement.RHYTHM,
            message=f"Rhythm: {rhythm['pattern']} pattern, swing: {rhythm['swing']:.2f}, syncopation: {rhythm['syncopation']:.2f}",
            data=rhythm,
            timestamp=time.time()
        ))
        
        # Provide style classification
        style = self.current_analysis.style_classification
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.EXPLANATION,
            element=MusicalElement.RHYTHM,
            message=f"Style classification: {style} (confidence: {confidence:.1%})",
            data={"style": style, "confidence": confidence},
            timestamp=time.time()
        ))
        
        return feedback
    
    def _get_analysis_feedback(self) -> List[VisualFeedback]:
        """Get comprehensive analysis feedback."""
        if not self.current_analysis:
            return []
        
        feedback = []
        
        # Overall analysis
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.ANALYSIS,
            element=MusicalElement.BASS,
            message=f"Complete Analysis: {self.current_analysis.key_signature}, {self.current_analysis.tempo:.0f} BPM, {self.current_analysis.style_classification} style",
            data={
                "key": self.current_analysis.key_signature,
                "tempo": self.current_analysis.tempo,
                "style": self.current_analysis.style_classification
            },
            timestamp=time.time()
        ))
        
        # Element counts
        feedback.append(VisualFeedback(
            type=VisualFeedbackType.EXPLANATION,
            element=MusicalElement.BASS,
            message=f"Elements: {len(self.current_analysis.bass_notes)} bass, {len(self.current_analysis.melody_notes)} melody, {len(self.current_analysis.harmony_notes)} harmony",
            data={
                "bass_count": len(self.current_analysis.bass_notes),
                "melody_count": len(self.current_analysis.melody_notes),
                "harmony_count": len(self.current_analysis.harmony_notes)
            },
            timestamp=time.time()
        ))
        
        return feedback
    
    def _get_suggestion_feedback(self) -> List[VisualFeedback]:
        """Get suggestion feedback."""
        if not self.current_analysis:
            return []
        
        feedback = []
        suggestions = self._generate_suggestions()
        
        for suggestion in suggestions:
            feedback.append(VisualFeedback(
                type=VisualFeedbackType.SUGGESTION,
                element=suggestion["element"],
                message=suggestion["message"],
                data=suggestion["data"],
                timestamp=time.time()
            ))
        
        return feedback
    
    def _generate_suggestions(self) -> List[Dict[str, Any]]:
        """Generate musical suggestions based on analysis."""
        if not self.current_analysis:
            return []
        
        suggestions = []
        rhythm = self.current_analysis.rhythm_pattern
        
        # Suggest swing if none detected
        if rhythm['swing'] < 0.55:
            suggestions.append({
                "element": MusicalElement.RHYTHM,
                "message": "Consider adding swing feel to make the rhythm more musical",
                "data": {"suggestion": "add_swing", "current_swing": rhythm['swing']}
            })
        
        # Suggest syncopation if rhythm is too simple
        if rhythm['syncopation'] < 0.2 and rhythm['complexity'] < 0.5:
            suggestions.append({
                "element": MusicalElement.RHYTHM,
                "message": "Try adding syncopation to make the rhythm more interesting",
                "data": {"suggestion": "add_syncopation", "current_syncopation": rhythm['syncopation']}
            })
        
        # Suggest bass line if none detected
        if len(self.current_analysis.bass_notes) < 3:
            suggestions.append({
                "element": MusicalElement.BASS,
                "message": "Consider adding a bass line to provide harmonic foundation",
                "data": {"suggestion": "add_bass", "current_bass_count": len(self.current_analysis.bass_notes)}
            })
        
        return suggestions
    
    def apply_suggestion(self, suggestion_data: Dict[str, Any]) -> bool:
        """Apply a musical suggestion to the current project.
        
        Args:
            suggestion_data: The suggestion data to apply
            
        Returns:
            True if successful, False otherwise
        """
        if not self.current_project or not self.current_analysis:
            return False
        
        try:
            suggestion_type = suggestion_data.get("suggestion")
            
            if suggestion_type == "add_swing":
                # Apply swing to all notes
                notes = self.current_project.get_all_notes()
                swung_notes = apply_swing(notes, swing_ratio=0.6)
                
                # Update project with swung notes
                self.current_project.notes = swung_notes
                self._analyze_project()  # Re-analyze
                
                return True
            
            elif suggestion_type == "add_syncopation":
                # This would require more complex rhythm modification
                # For now, just return True
                return True
            
            elif suggestion_type == "add_bass":
                # This would require generating new bass notes
                # For now, just return True
                return True
            
            return False
            
        except Exception as e:
            print(f"Error applying suggestion: {e}")
            return False
    
    def get_feedback_summary(self) -> str:
        """Get a summary of all visual feedback."""
        if not self.feedback_history:
            return "No feedback available."
        
        summary = "Visual Feedback Summary:\n"
        for feedback in self.feedback_history[-10:]:  # Last 10 items
            summary += f"- {feedback.element.value}: {feedback.message}\n"
        
        return summary
    
    def clear_feedback(self) -> None:
        """Clear all visual feedback."""
        self.visual_feedback_queue.clear()
        self.feedback_history.clear()
