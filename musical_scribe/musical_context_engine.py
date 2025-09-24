"""
Musical Context Engine

Analyzes project-wide musical relationships and context for Musical Scribe.
This is the core intelligence that understands how musical elements work together
in the context of the entire project, not just individual tracks.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from .project_state_parser import ProjectState, TrackInfo


@dataclass
class HarmonicAnalysis:
    """Analysis of harmonic content across the project."""
    key_signature: Optional[str]
    chord_progression: List[str]
    harmonic_rhythm: str  # 'fast', 'medium', 'slow'
    voice_leading_quality: str  # 'good', 'fair', 'poor'
    dissonance_level: str  # 'low', 'medium', 'high'
    harmonic_complexity: str  # 'simple', 'moderate', 'complex'


@dataclass
class RhythmicAnalysis:
    """Analysis of rhythmic patterns across the project."""
    primary_time_signature: str
    tempo_consistency: str  # 'consistent', 'variable', 'rushed'
    swing_feel: str  # 'straight', 'light_swing', 'heavy_swing'
    syncopation_level: str  # 'low', 'medium', 'high'
    groove_quality: str  # 'tight', 'loose', 'inconsistent'
    rhythmic_density: str  # 'sparse', 'medium', 'dense'


@dataclass
class ArrangementAnalysis:
    """Analysis of arrangement and structure."""
    overall_density: str  # 'sparse', 'medium', 'dense'
    dynamic_range: str  # 'narrow', 'medium', 'wide'
    frequency_balance: str  # 'balanced', 'bass_heavy', 'treble_heavy', 'mid_heavy'
    arrangement_complexity: str  # 'simple', 'moderate', 'complex'
    section_transitions: str  # 'smooth', 'abrupt', 'varied'
    instrumental_balance: Dict[str, float]  # Track balance ratios


@dataclass
class StyleAnalysis:
    """Analysis of musical style and genre characteristics."""
    primary_genre: str
    secondary_genres: List[str]
    era_characteristics: List[str]  # e.g., 'modern', 'vintage', 'retro'
    production_style: str  # 'live', 'electronic', 'hybrid', 'minimal'
    mood_characteristics: List[str]  # e.g., 'energetic', 'melancholic', 'aggressive'
    complexity_level: str  # 'beginner', 'intermediate', 'advanced'


@dataclass
class EnhancementOpportunities:
    """Identified opportunities for musical enhancement."""
    missing_elements: List[str]  # e.g., 'bass_line', 'melody', 'harmony'
    weak_areas: List[str]  # e.g., 'rhythm', 'harmony', 'arrangement'
    enhancement_suggestions: List[str]
    priority_level: str  # 'low', 'medium', 'high'
    confidence_score: float  # 0.0 to 1.0


@dataclass
class MusicalContext:
    """Complete musical context analysis for a project."""
    harmonic_analysis: HarmonicAnalysis
    rhythmic_analysis: RhythmicAnalysis
    arrangement_analysis: ArrangementAnalysis
    style_analysis: StyleAnalysis
    enhancement_opportunities: EnhancementOpportunities
    track_relationships: Dict[str, Dict[str, Any]]
    musical_coherence_score: float  # 0.0 to 1.0


class MusicalContextEngine:
    """
    Analyzes project-wide musical relationships and context.
    
    This is the core intelligence that understands how musical elements work together
    in the context of the entire project, enabling contextually appropriate enhancements.
    """
    
    def __init__(self):
        self.genre_indicators = {
            'jazz': ['swing', 'syncopation', 'complex_harmony', 'improvisation'],
            'rock': ['power_chords', 'driving_rhythm', 'distortion', 'aggressive'],
            'blues': ['blues_scale', 'bent_notes', 'call_response', '12_bar'],
            'classical': ['orchestral', 'complex_counterpoint', 'formal_structure'],
            'electronic': ['synthesized', 'repetitive_patterns', 'sidechain_compression'],
            'funk': ['syncopated_bass', 'percussive_guitar', 'tight_rhythm'],
            'pop': ['catchy_melody', 'simple_harmony', 'verse_chorus', 'commercial']
        }
        
        self.complexity_indicators = {
            'beginner': ['simple_chords', 'straight_rhythm', 'basic_arrangement'],
            'intermediate': ['moderate_harmony', 'some_syncopation', 'varied_arrangement'],
            'advanced': ['complex_harmony', 'irregular_rhythm', 'sophisticated_arrangement']
        }
    
    def analyze_project_context(self, project_state: ProjectState) -> MusicalContext:
        """
        Analyze project-wide musical relationships and context.
        
        Args:
            project_state: Complete project state from ProjectStateParser
            
        Returns:
            MusicalContext: Comprehensive musical context analysis
        """
        # Analyze harmonic content
        harmonic_analysis = self._analyze_harmonic_content(project_state)
        
        # Analyze rhythmic patterns
        rhythmic_analysis = self._analyze_rhythmic_patterns(project_state)
        
        # Analyze arrangement and structure
        arrangement_analysis = self._analyze_arrangement_structure(project_state)
        
        # Analyze musical style and genre
        style_analysis = self._analyze_musical_style(project_state)
        
        # Identify enhancement opportunities
        enhancement_opportunities = self._identify_enhancement_opportunities(
            project_state, harmonic_analysis, rhythmic_analysis, arrangement_analysis
        )
        
        # Analyze track relationships
        track_relationships = self._analyze_track_relationships(project_state)
        
        # Calculate overall musical coherence
        musical_coherence_score = self._calculate_musical_coherence(
            harmonic_analysis, rhythmic_analysis, arrangement_analysis, track_relationships
        )
        
        return MusicalContext(
            harmonic_analysis=harmonic_analysis,
            rhythmic_analysis=rhythmic_analysis,
            arrangement_analysis=arrangement_analysis,
            style_analysis=style_analysis,
            enhancement_opportunities=enhancement_opportunities,
            track_relationships=track_relationships,
            musical_coherence_score=musical_coherence_score
        )
    
    def _analyze_harmonic_content(self, project_state: ProjectState) -> HarmonicAnalysis:
        """Analyze harmonic content across all tracks."""
        # Extract all MIDI notes from all tracks
        all_notes = []
        for track in project_state.tracks:
            if track.musical_analysis and track.musical_analysis.get('has_midi_content'):
                for region in track.regions:
                    if region.get('type') == 'midi' and 'midi_data' in region:
                        all_notes.extend(region['midi_data'].get('notes', []))
        
        # Analyze key signature (simplified)
        key_signature = self._detect_key_signature(all_notes)
        
        # Analyze chord progression (simplified)
        chord_progression = self._detect_chord_progression(all_notes)
        
        # Analyze harmonic rhythm
        harmonic_rhythm = self._analyze_harmonic_rhythm(chord_progression)
        
        # Analyze voice leading
        voice_leading_quality = self._analyze_voice_leading(all_notes)
        
        # Analyze dissonance level
        dissonance_level = self._analyze_dissonance_level(all_notes)
        
        # Analyze harmonic complexity
        harmonic_complexity = self._analyze_harmonic_complexity(chord_progression, all_notes)
        
        return HarmonicAnalysis(
            key_signature=key_signature,
            chord_progression=chord_progression,
            harmonic_rhythm=harmonic_rhythm,
            voice_leading_quality=voice_leading_quality,
            dissonance_level=dissonance_level,
            harmonic_complexity=harmonic_complexity
        )
    
    def _analyze_rhythmic_patterns(self, project_state: ProjectState) -> RhythmicAnalysis:
        """Analyze rhythmic patterns across all tracks."""
        # Get project tempo and time signature
        tempo = project_state.project_info.tempo
        time_signature = project_state.project_info.time_signature
        
        # Analyze tempo consistency
        tempo_consistency = self._analyze_tempo_consistency(project_state)
        
        # Analyze swing feel
        swing_feel = self._analyze_swing_feel(project_state)
        
        # Analyze syncopation level
        syncopation_level = self._analyze_syncopation_level(project_state)
        
        # Analyze groove quality
        groove_quality = self._analyze_groove_quality(project_state)
        
        # Analyze rhythmic density
        rhythmic_density = self._analyze_rhythmic_density(project_state)
        
        return RhythmicAnalysis(
            primary_time_signature=time_signature,
            tempo_consistency=tempo_consistency,
            swing_feel=swing_feel,
            syncopation_level=syncopation_level,
            groove_quality=groove_quality,
            rhythmic_density=rhythmic_density
        )
    
    def _analyze_arrangement_structure(self, project_state: ProjectState) -> ArrangementAnalysis:
        """Analyze arrangement and structural elements."""
        # Calculate overall density
        overall_density = self._calculate_overall_density(project_state)
        
        # Analyze dynamic range
        dynamic_range = self._analyze_dynamic_range(project_state)
        
        # Analyze frequency balance
        frequency_balance = self._analyze_frequency_balance(project_state)
        
        # Analyze arrangement complexity
        arrangement_complexity = self._analyze_arrangement_complexity(project_state)
        
        # Analyze section transitions
        section_transitions = self._analyze_section_transitions(project_state)
        
        # Calculate instrumental balance
        instrumental_balance = self._calculate_instrumental_balance(project_state)
        
        return ArrangementAnalysis(
            overall_density=overall_density,
            dynamic_range=dynamic_range,
            frequency_balance=frequency_balance,
            arrangement_complexity=arrangement_complexity,
            section_transitions=section_transitions,
            instrumental_balance=instrumental_balance
        )
    
    def _analyze_musical_style(self, project_state: ProjectState) -> StyleAnalysis:
        """Analyze musical style and genre characteristics."""
        # Detect primary genre
        primary_genre = self._detect_primary_genre(project_state)
        
        # Detect secondary genres
        secondary_genres = self._detect_secondary_genres(project_state)
        
        # Analyze era characteristics
        era_characteristics = self._analyze_era_characteristics(project_state)
        
        # Analyze production style
        production_style = self._analyze_production_style(project_state)
        
        # Analyze mood characteristics
        mood_characteristics = self._analyze_mood_characteristics(project_state)
        
        # Determine complexity level
        complexity_level = self._determine_complexity_level(project_state)
        
        return StyleAnalysis(
            primary_genre=primary_genre,
            secondary_genres=secondary_genres,
            era_characteristics=era_characteristics,
            production_style=production_style,
            mood_characteristics=mood_characteristics,
            complexity_level=complexity_level
        )
    
    def _identify_enhancement_opportunities(
        self, 
        project_state: ProjectState,
        harmonic_analysis: HarmonicAnalysis,
        rhythmic_analysis: RhythmicAnalysis,
        arrangement_analysis: ArrangementAnalysis
    ) -> EnhancementOpportunities:
        """Identify specific opportunities for musical enhancement."""
        missing_elements = []
        weak_areas = []
        enhancement_suggestions = []
        
        # Check for missing musical elements
        if not any('bass' in track.name.lower() for track in project_state.tracks):
            missing_elements.append('bass_line')
            enhancement_suggestions.append('Add a bass line to provide harmonic foundation')
        
        if not any('melody' in track.name.lower() or 'lead' in track.name.lower() for track in project_state.tracks):
            missing_elements.append('melody')
            enhancement_suggestions.append('Add a melody line to provide musical interest')
        
        if not any('drum' in track.name.lower() or 'percussion' in track.name.lower() for track in project_state.tracks):
            missing_elements.append('rhythm_section')
            enhancement_suggestions.append('Add drums or percussion for rhythmic foundation')
        
        # Identify weak areas based on analysis
        if harmonic_analysis.voice_leading_quality == 'poor':
            weak_areas.append('harmony')
            enhancement_suggestions.append('Improve voice leading for smoother harmonic movement')
        
        if rhythmic_analysis.groove_quality == 'loose':
            weak_areas.append('rhythm')
            enhancement_suggestions.append('Tighten up the rhythm for better groove')
        
        if arrangement_analysis.overall_density == 'sparse':
            weak_areas.append('arrangement')
            enhancement_suggestions.append('Add more musical elements to fill out the arrangement')
        
        # Determine priority level
        if missing_elements or len(weak_areas) > 2:
            priority_level = 'high'
        elif len(weak_areas) > 0:
            priority_level = 'medium'
        else:
            priority_level = 'low'
        
        # Calculate confidence score
        confidence_score = min(1.0, len(enhancement_suggestions) * 0.2)
        
        return EnhancementOpportunities(
            missing_elements=missing_elements,
            weak_areas=weak_areas,
            enhancement_suggestions=enhancement_suggestions,
            priority_level=priority_level,
            confidence_score=confidence_score
        )
    
    def _analyze_track_relationships(self, project_state: ProjectState) -> Dict[str, Dict[str, Any]]:
        """Analyze relationships between tracks."""
        relationships = {}
        
        for i, track1 in enumerate(project_state.tracks):
            for j, track2 in enumerate(project_state.tracks):
                if i != j:
                    relationship_key = f"{track1.name}_{track2.name}"
                    
                    # Analyze frequency relationship
                    freq_relationship = self._analyze_frequency_relationship(track1, track2)
                    
                    # Analyze rhythmic relationship
                    rhythm_relationship = self._analyze_rhythmic_relationship(track1, track2)
                    
                    # Analyze harmonic relationship
                    harmonic_relationship = self._analyze_harmonic_relationship(track1, track2)
                    
                    relationships[relationship_key] = {
                        'frequency_relationship': freq_relationship,
                        'rhythmic_relationship': rhythm_relationship,
                        'harmonic_relationship': harmonic_relationship,
                        'compatibility_score': self._calculate_track_compatibility(
                            freq_relationship, rhythm_relationship, harmonic_relationship
                        )
                    }
        
        return relationships
    
    def _calculate_musical_coherence(
        self,
        harmonic_analysis: HarmonicAnalysis,
        rhythmic_analysis: RhythmicAnalysis,
        arrangement_analysis: ArrangementAnalysis,
        track_relationships: Dict[str, Dict[str, Any]]
    ) -> float:
        """Calculate overall musical coherence score."""
        coherence_factors = []
        
        # Harmonic coherence
        if harmonic_analysis.voice_leading_quality == 'good':
            coherence_factors.append(1.0)
        elif harmonic_analysis.voice_leading_quality == 'fair':
            coherence_factors.append(0.7)
        else:
            coherence_factors.append(0.3)
        
        # Rhythmic coherence
        if rhythmic_analysis.groove_quality == 'tight':
            coherence_factors.append(1.0)
        elif rhythmic_analysis.groove_quality == 'loose':
            coherence_factors.append(0.5)
        else:
            coherence_factors.append(0.7)
        
        # Arrangement coherence
        if arrangement_analysis.overall_density in ['medium', 'dense']:
            coherence_factors.append(0.8)
        else:
            coherence_factors.append(0.6)
        
        # Track relationship coherence
        if track_relationships:
            avg_compatibility = sum(
                rel['compatibility_score'] for rel in track_relationships.values()
            ) / len(track_relationships)
            coherence_factors.append(avg_compatibility)
        
        return sum(coherence_factors) / len(coherence_factors) if coherence_factors else 0.5
    
    # Helper methods for specific analyses
    
    def _detect_key_signature(self, notes: List[Dict[str, Any]]) -> Optional[str]:
        """Detect key signature from note data (simplified)."""
        if not notes:
            return None
        
        # Simple key detection based on note frequency
        note_counts = {}
        for note in notes:
            pitch = note['pitch']
            note_name = self._pitch_to_note_name(pitch)
            note_counts[note_name] = note_counts.get(note_name, 0) + 1
        
        # Find most common notes (simplified key detection)
        if note_counts:
            most_common = max(note_counts, key=note_counts.get)
            return f"{most_common} major"  # Simplified
        
        return None
    
    def _detect_chord_progression(self, notes: List[Dict[str, Any]]) -> List[str]:
        """Detect chord progression from note data (simplified)."""
        if not notes:
            return []
        
        # Group notes by time to find chords
        time_groups = {}
        for note in notes:
            start_time = note['start_time']
            time_key = round(start_time, 1)  # Group by 0.1 second intervals
            if time_key not in time_groups:
                time_groups[time_key] = []
            time_groups[time_key].append(note['pitch'])
        
        # Convert pitch groups to chord names (simplified)
        chord_progression = []
        for time_key in sorted(time_groups.keys()):
            pitches = time_groups[time_key]
            chord_name = self._pitches_to_chord_name(pitches)
            if chord_name:
                chord_progression.append(chord_name)
        
        return chord_progression
    
    def _analyze_harmonic_rhythm(self, chord_progression: List[str]) -> str:
        """Analyze harmonic rhythm from chord progression."""
        if len(chord_progression) <= 2:
            return 'slow'
        elif len(chord_progression) <= 4:
            return 'medium'
        else:
            return 'fast'
    
    def _analyze_voice_leading(self, notes: List[Dict[str, Any]]) -> str:
        """Analyze voice leading quality (simplified)."""
        if not notes:
            return 'fair'
        
        # Simple analysis based on pitch movement
        pitches = [note['pitch'] for note in notes]
        if len(pitches) < 2:
            return 'fair'
        
        # Check for large jumps (poor voice leading)
        large_jumps = 0
        for i in range(1, len(pitches)):
            if abs(pitches[i] - pitches[i-1]) > 12:  # More than an octave
                large_jumps += 1
        
        jump_ratio = large_jumps / (len(pitches) - 1)
        
        if jump_ratio < 0.1:
            return 'good'
        elif jump_ratio < 0.3:
            return 'fair'
        else:
            return 'poor'
    
    def _analyze_dissonance_level(self, notes: List[Dict[str, Any]]) -> str:
        """Analyze dissonance level (simplified)."""
        if not notes:
            return 'low'
        
        # Simple dissonance analysis based on interval relationships
        dissonant_intervals = 0
        total_intervals = 0
        
        for i in range(len(notes)):
            for j in range(i + 1, len(notes)):
                interval = abs(notes[i]['pitch'] - notes[j]['pitch']) % 12
                total_intervals += 1
                
                # Check for dissonant intervals (simplified)
                if interval in [1, 2, 6, 10, 11]:  # Minor 2nd, major 2nd, tritone, minor 7th, major 7th
                    dissonant_intervals += 1
        
        if total_intervals == 0:
            return 'low'
        
        dissonance_ratio = dissonant_intervals / total_intervals
        
        if dissonance_ratio < 0.2:
            return 'low'
        elif dissonance_ratio < 0.4:
            return 'medium'
        else:
            return 'high'
    
    def _analyze_harmonic_complexity(self, chord_progression: List[str], notes: List[Dict[str, Any]]) -> str:
        """Analyze harmonic complexity."""
        if not chord_progression and not notes:
            return 'simple'
        
        # Consider chord progression length and note density
        chord_complexity = len(chord_progression) / 4  # Normalize by 4 chords
        note_density = len(notes) / 100  # Normalize by 100 notes
        
        complexity_score = (chord_complexity + note_density) / 2
        
        if complexity_score < 0.3:
            return 'simple'
        elif complexity_score < 0.7:
            return 'moderate'
        else:
            return 'complex'
    
    def _analyze_tempo_consistency(self, project_state: ProjectState) -> str:
        """Analyze tempo consistency across the project."""
        # For now, assume consistent tempo
        return 'consistent'
    
    def _analyze_swing_feel(self, project_state: ProjectState) -> str:
        """Analyze swing feel in the project."""
        # Simple swing detection based on note timing patterns
        all_notes = []
        for track in project_state.tracks:
            if track.musical_analysis and track.musical_analysis.get('has_midi_content'):
                for region in track.regions:
                    if region.get('type') == 'midi' and 'midi_data' in region:
                        all_notes.extend(region['midi_data'].get('notes', []))
        
        if not all_notes:
            return 'straight'
        
        # Analyze timing patterns for swing (simplified)
        # This would need more sophisticated analysis in practice
        return 'straight'  # Placeholder
    
    def _analyze_syncopation_level(self, project_state: ProjectState) -> str:
        """Analyze syncopation level."""
        # Simplified syncopation analysis
        return 'medium'  # Placeholder
    
    def _analyze_groove_quality(self, project_state: ProjectState) -> str:
        """Analyze groove quality."""
        # Simplified groove analysis
        return 'tight'  # Placeholder
    
    def _analyze_rhythmic_density(self, project_state: ProjectState) -> str:
        """Analyze rhythmic density."""
        total_notes = sum(t.musical_analysis.get('note_count', 0) for t in project_state.tracks)
        project_duration = project_state.musical_context.get('project_duration', 1.0)
        
        if project_duration == 0:
            return 'sparse'
        
        notes_per_second = total_notes / project_duration
        
        if notes_per_second < 2:
            return 'sparse'
        elif notes_per_second < 6:
            return 'medium'
        else:
            return 'dense'
    
    def _calculate_overall_density(self, project_state: ProjectState) -> str:
        """Calculate overall musical density."""
        return project_state.musical_context.get('musical_style_indicators', {}).get('complexity_level', 'medium')
    
    def _analyze_dynamic_range(self, project_state: ProjectState) -> str:
        """Analyze dynamic range."""
        # Simplified dynamic range analysis
        return 'medium'  # Placeholder
    
    def _analyze_frequency_balance(self, project_state: ProjectState) -> str:
        """Analyze frequency balance."""
        # Simplified frequency balance analysis
        return 'balanced'  # Placeholder
    
    def _analyze_arrangement_complexity(self, project_state: ProjectState) -> str:
        """Analyze arrangement complexity."""
        track_count = len(project_state.tracks)
        region_count = sum(len(t.regions) for t in project_state.tracks)
        
        if track_count < 3 and region_count < 10:
            return 'simple'
        elif track_count < 6 and region_count < 20:
            return 'moderate'
        else:
            return 'complex'
    
    def _analyze_section_transitions(self, project_state: ProjectState) -> str:
        """Analyze section transitions."""
        # Simplified section transition analysis
        return 'smooth'  # Placeholder
    
    def _calculate_instrumental_balance(self, project_state: ProjectState) -> Dict[str, float]:
        """Calculate instrumental balance ratios."""
        balance = {}
        total_tracks = len(project_state.tracks)
        
        if total_tracks == 0:
            return balance
        
        for track in project_state.tracks:
            track_type = track.track_type
            balance[track_type] = balance.get(track_type, 0) + (1.0 / total_tracks)
        
        return balance
    
    def _detect_primary_genre(self, project_state: ProjectState) -> str:
        """Detect primary musical genre."""
        # Simplified genre detection based on track names and characteristics
        track_names = [track.name.lower() for track in project_state.tracks]
        
        genre_scores = {}
        for genre, indicators in self.genre_indicators.items():
            score = 0
            for indicator in indicators:
                for track_name in track_names:
                    if indicator in track_name:
                        score += 1
            genre_scores[genre] = score
        
        if genre_scores:
            return max(genre_scores, key=genre_scores.get)
        
        return 'unknown'
    
    def _detect_secondary_genres(self, project_state: ProjectState) -> List[str]:
        """Detect secondary genres."""
        # Simplified secondary genre detection
        return []  # Placeholder
    
    def _analyze_era_characteristics(self, project_state: ProjectState) -> List[str]:
        """Analyze era characteristics."""
        # Simplified era analysis
        return ['modern']  # Placeholder
    
    def _analyze_production_style(self, project_state: ProjectState) -> str:
        """Analyze production style."""
        # Simplified production style analysis
        return 'hybrid'  # Placeholder
    
    def _analyze_mood_characteristics(self, project_state: ProjectState) -> List[str]:
        """Analyze mood characteristics."""
        # Simplified mood analysis
        return ['neutral']  # Placeholder
    
    def _determine_complexity_level(self, project_state: ProjectState) -> str:
        """Determine overall complexity level."""
        indicators = project_state.musical_context.get('musical_style_indicators', {})
        complexity = indicators.get('complexity_level', 'medium')
        
        if complexity == 'high':
            return 'advanced'
        elif complexity == 'medium':
            return 'intermediate'
        else:
            return 'beginner'
    
    def _analyze_frequency_relationship(self, track1: TrackInfo, track2: TrackInfo) -> str:
        """Analyze frequency relationship between two tracks."""
        # Simplified frequency relationship analysis
        return 'complementary'  # Placeholder
    
    def _analyze_rhythmic_relationship(self, track1: TrackInfo, track2: TrackInfo) -> str:
        """Analyze rhythmic relationship between two tracks."""
        # Simplified rhythmic relationship analysis
        return 'synchronized'  # Placeholder
    
    def _analyze_harmonic_relationship(self, track1: TrackInfo, track2: TrackInfo) -> str:
        """Analyze harmonic relationship between two tracks."""
        # Simplified harmonic relationship analysis
        return 'harmonious'  # Placeholder
    
    def _calculate_track_compatibility(self, freq_rel: str, rhythm_rel: str, harmonic_rel: str) -> float:
        """Calculate track compatibility score."""
        # Simplified compatibility calculation
        scores = {
            'complementary': 0.8,
            'synchronized': 0.9,
            'harmonious': 0.8
        }
        
        return (scores.get(freq_rel, 0.5) + scores.get(rhythm_rel, 0.5) + scores.get(harmonic_rel, 0.5)) / 3
    
    def _pitch_to_note_name(self, pitch: int) -> str:
        """Convert MIDI pitch to note name."""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[pitch % 12]
    
    def _pitches_to_chord_name(self, pitches: List[int]) -> Optional[str]:
        """Convert a list of pitches to a chord name (simplified)."""
        if not pitches:
            return None
        
        # Simplified chord detection
        if len(pitches) == 1:
            return self._pitch_to_note_name(pitches[0])
        elif len(pitches) == 2:
            interval = abs(pitches[0] - pitches[1]) % 12
            if interval == 0:
                return self._pitch_to_note_name(pitches[0])
            elif interval == 7:
                return f"{self._pitch_to_note_name(pitches[0])}5"
            else:
                return f"{self._pitch_to_note_name(pitches[0])}?"
        else:
            # More complex chord detection would go here
            return f"{self._pitch_to_note_name(pitches[0])}?"
