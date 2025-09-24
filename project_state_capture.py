"""
Live Project State Capture

Captures and analyzes real-time project state from Ardour OSC monitor.
Provides context for LLM track enhancement with current musical state.
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np

from ardour_osc_monitor import LiveProjectState, LiveTrack, LiveRegion, LiveSelection


@dataclass
class MusicalContext:
    """Musical context derived from live project state."""
    key_signature: str
    tempo: float
    time_signature: str
    harmonic_progression: List[str]
    rhythmic_patterns: Dict[str, Any]
    track_density: Dict[str, float]
    frequency_balance: Dict[str, float]
    style_indicators: List[str]
    mood_characteristics: List[str]
    complexity_level: str
    last_updated: float


@dataclass
class TrackAnalysis:
    """Analysis of a specific track."""
    track_id: str
    track_name: str
    track_type: str
    note_count: int
    note_density: float
    pitch_range: Tuple[int, int]
    velocity_range: Tuple[int, int]
    rhythmic_complexity: float
    harmonic_function: str
    musical_role: str
    enhancement_opportunities: List[str]
    last_updated: float


@dataclass
class EnhancementOpportunity:
    """Specific enhancement opportunity identified."""
    track_id: str
    opportunity_type: str  # "add_bass", "improve_groove", "add_harmony", etc.
    priority: int  # 1-10, higher is more important
    description: str
    musical_justification: str
    suggested_approach: str
    confidence: float


@dataclass
class LiveProjectContext:
    """Complete live project context for LLM enhancement."""
    project_state: LiveProjectState
    musical_context: MusicalContext
    track_analyses: List[TrackAnalysis]
    enhancement_opportunities: List[EnhancementOpportunity]
    selected_regions: List[LiveRegion]
    midi_context: List[Dict[str, Any]]
    last_updated: float


class ProjectStateCapture:
    """
    Captures and analyzes live project state for LLM enhancement.
    
    Takes real-time project state from Ardour OSC monitor and provides
    rich musical context for LLM track enhancement.
    """
    
    def __init__(self):
        """Initialize project state capture."""
        self.current_context: Optional[LiveProjectContext] = None
        self.historical_states: List[LiveProjectState] = []
        self.max_history = 100  # Keep last 100 states
        
        # Analysis caches
        self._track_analysis_cache: Dict[str, TrackAnalysis] = {}
        self._musical_context_cache: Optional[MusicalContext] = None
        self._cache_timeout = 5.0  # 5 seconds cache timeout
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def update_project_state(self, project_state: LiveProjectState) -> LiveProjectContext:
        """
        Update project state and generate new context.
        
        Args:
            project_state: Current live project state from OSC monitor
            
        Returns:
            LiveProjectContext: Complete context for LLM enhancement
        """
        # Store historical state
        self.historical_states.append(project_state)
        if len(self.historical_states) > self.max_history:
            self.historical_states.pop(0)
        
        # Generate musical context
        musical_context = self._analyze_musical_context(project_state)
        
        # Analyze tracks
        track_analyses = self._analyze_tracks(project_state)
        
        # Identify enhancement opportunities
        enhancement_opportunities = self._identify_enhancement_opportunities(
            project_state, musical_context, track_analyses
        )
        
        # Get selected regions
        selected_regions = self._get_selected_regions(project_state)
        
        # Extract MIDI context
        midi_context = self._extract_midi_context(project_state)
        
        # Create complete context
        self.current_context = LiveProjectContext(
            project_state=project_state,
            musical_context=musical_context,
            track_analyses=track_analyses,
            enhancement_opportunities=enhancement_opportunities,
            selected_regions=selected_regions,
            midi_context=midi_context,
            last_updated=time.time()
        )
        
        return self.current_context
    
    def get_current_context(self) -> Optional[LiveProjectContext]:
        """Get current project context."""
        return self.current_context
    
    def get_context_for_llm(self, user_request: str) -> Dict[str, Any]:
        """
        Get context formatted for LLM enhancement.
        
        Args:
            user_request: User's enhancement request
            
        Returns:
            Dict containing context for LLM
        """
        if not self.current_context:
            return {"error": "No current project context available"}
        
        context = self.current_context
        
        # Build comprehensive context for LLM
        llm_context = {
            "project_info": {
                "name": context.project_state.project_name,
                "tempo": context.project_state.tempo,
                "time_signature": context.project_state.time_signature,
                "sample_rate": context.project_state.sample_rate
            },
            "musical_context": asdict(context.musical_context),
            "tracks": [
                {
                    "id": track.id,
                    "name": track.name,
                    "type": track.type,
                    "armed": track.armed,
                    "muted": track.muted,
                    "solo": track.solo,
                    "volume": track.volume,
                    "pan": track.pan
                }
                for track in context.project_state.tracks
            ],
            "track_analyses": [asdict(analysis) for analysis in context.track_analyses],
            "enhancement_opportunities": [
                {
                    "track_id": opp.track_id,
                    "type": opp.opportunity_type,
                    "priority": opp.priority,
                    "description": opp.description,
                    "musical_justification": opp.musical_justification,
                    "suggested_approach": opp.suggested_approach,
                    "confidence": opp.confidence
                }
                for opp in context.enhancement_opportunities
            ],
            "selected_regions": [
                {
                    "id": region.id,
                    "name": region.name,
                    "track_id": region.track_id,
                    "start_time": region.start_time,
                    "length": region.length,
                    "position": region.position,
                    "selected": region.selected
                }
                for region in context.selected_regions
            ],
            "midi_context": context.midi_context,
            "user_request": user_request,
            "timestamp": time.time()
        }
        
        return llm_context
    
    def _analyze_musical_context(self, project_state: LiveProjectState) -> MusicalContext:
        """Analyze musical context from project state."""
        # Check cache first
        if (self._musical_context_cache and 
            time.time() - self._musical_context_cache.last_updated < self._cache_timeout):
            return self._musical_context_cache
        
        # Analyze harmonic content
        harmonic_progression = self._analyze_harmonic_progression(project_state)
        key_signature = self._detect_key_signature(project_state)
        
        # Analyze rhythmic patterns
        rhythmic_patterns = self._analyze_rhythmic_patterns(project_state)
        
        # Analyze track density
        track_density = self._analyze_track_density(project_state)
        
        # Analyze frequency balance
        frequency_balance = self._analyze_frequency_balance(project_state)
        
        # Detect style indicators
        style_indicators = self._detect_style_indicators(project_state)
        
        # Detect mood characteristics
        mood_characteristics = self._detect_mood_characteristics(project_state)
        
        # Determine complexity level
        complexity_level = self._determine_complexity_level(project_state)
        
        musical_context = MusicalContext(
            key_signature=key_signature,
            tempo=project_state.tempo,
            time_signature=project_state.time_signature,
            harmonic_progression=harmonic_progression,
            rhythmic_patterns=rhythmic_patterns,
            track_density=track_density,
            frequency_balance=frequency_balance,
            style_indicators=style_indicators,
            mood_characteristics=mood_characteristics,
            complexity_level=complexity_level,
            last_updated=time.time()
        )
        
        self._musical_context_cache = musical_context
        return musical_context
    
    def _analyze_tracks(self, project_state: LiveProjectState) -> List[TrackAnalysis]:
        """Analyze all tracks in the project."""
        track_analyses = []
        
        for track in project_state.tracks:
            # Check cache first
            if (track.id in self._track_analysis_cache and 
                time.time() - self._track_analysis_cache[track.id].last_updated < self._cache_timeout):
                track_analyses.append(self._track_analysis_cache[track.id])
                continue
            
            # Analyze track
            analysis = self._analyze_single_track(track, project_state)
            track_analyses.append(analysis)
            
            # Cache analysis
            self._track_analysis_cache[track.id] = analysis
        
        return track_analyses
    
    def _analyze_single_track(self, track: LiveTrack, project_state: LiveProjectState) -> TrackAnalysis:
        """Analyze a single track."""
        # Get MIDI data for this track
        track_midi = [note for note in project_state.midi_data 
                     if note.get('track_index') == int(track.id)]
        
        # Analyze note content
        note_count = len(track_midi)
        note_density = self._calculate_note_density(track_midi, project_state.tempo)
        
        # Analyze pitch range
        if track_midi:
            pitches = [note['pitch'] for note in track_midi if 'pitch' in note]
            pitch_range = (min(pitches), max(pitches)) if pitches else (0, 0)
        else:
            pitch_range = (0, 0)
        
        # Analyze velocity range
        if track_midi:
            velocities = [note['velocity'] for note in track_midi if 'velocity' in note]
            velocity_range = (min(velocities), max(velocities)) if velocities else (0, 0)
        else:
            velocity_range = (0, 0)
        
        # Analyze rhythmic complexity
        rhythmic_complexity = self._calculate_rhythmic_complexity(track_midi)
        
        # Determine harmonic function
        harmonic_function = self._determine_harmonic_function(track_midi, project_state)
        
        # Determine musical role
        musical_role = self._determine_musical_role(track, track_midi)
        
        # Identify enhancement opportunities
        enhancement_opportunities = self._identify_track_enhancement_opportunities(
            track, track_midi, project_state
        )
        
        return TrackAnalysis(
            track_id=track.id,
            track_name=track.name,
            track_type=track.type,
            note_count=note_count,
            note_density=note_density,
            pitch_range=pitch_range,
            velocity_range=velocity_range,
            rhythmic_complexity=rhythmic_complexity,
            harmonic_function=harmonic_function,
            musical_role=musical_role,
            enhancement_opportunities=enhancement_opportunities,
            last_updated=time.time()
        )
    
    def _identify_enhancement_opportunities(
        self, 
        project_state: LiveProjectState, 
        musical_context: MusicalContext,
        track_analyses: List[TrackAnalysis]
    ) -> List[EnhancementOpportunity]:
        """Identify enhancement opportunities across the project."""
        opportunities = []
        
        # Check for missing elements
        track_types = {analysis.track_type for analysis in track_analyses}
        
        if 'midi' not in track_types or not any('bass' in analysis.musical_role.lower() 
                                               for analysis in track_analyses):
            opportunities.append(EnhancementOpportunity(
                track_id="",
                opportunity_type="add_bass",
                priority=8,
                description="Add bass line for rhythmic foundation",
                musical_justification="No bass line detected in current arrangement",
                suggested_approach="Create bass line that supports harmonic progression",
                confidence=0.9
            ))
        
        if not any('drum' in analysis.musical_role.lower() for analysis in track_analyses):
            opportunities.append(EnhancementOpportunity(
                track_id="",
                opportunity_type="add_drums",
                priority=7,
                description="Add drum pattern for rhythmic drive",
                musical_justification="No drum pattern detected in current arrangement",
                suggested_approach="Create drum pattern that matches tempo and style",
                confidence=0.8
            ))
        
        # Check for weak areas in existing tracks
        for analysis in track_analyses:
            if analysis.rhythmic_complexity < 0.3:
                opportunities.append(EnhancementOpportunity(
                    track_id=analysis.track_id,
                    opportunity_type="improve_groove",
                    priority=6,
                    description=f"Improve groove in {analysis.track_name}",
                    musical_justification="Track has low rhythmic complexity",
                    suggested_approach="Add syncopation and rhythmic variation",
                    confidence=0.7
                ))
            
            if analysis.note_density < 0.1:
                opportunities.append(EnhancementOpportunity(
                    track_id=analysis.track_id,
                    opportunity_type="add_melody",
                    priority=5,
                    description=f"Add melodic content to {analysis.track_name}",
                    musical_justification="Track has very low note density",
                    suggested_approach="Add melodic lines that complement harmony",
                    confidence=0.6
                ))
        
        return opportunities
    
    def _get_selected_regions(self, project_state: LiveProjectState) -> List[LiveRegion]:
        """Get currently selected regions."""
        return [region for region in project_state.regions if region.selected]
    
    def _extract_midi_context(self, project_state: LiveProjectState) -> List[Dict[str, Any]]:
        """Extract MIDI context for LLM."""
        # Get recent MIDI data (last 30 seconds)
        current_time = time.time()
        recent_midi = [
            note for note in project_state.midi_data
            if current_time - note.get('timestamp', 0) < 30.0
        ]
        
        # Convert to universal note format
        midi_context = []
        for note in recent_midi:
            if 'pitch' in note and 'velocity' in note:
                midi_context.append({
                    'pitch': note['pitch'],
                    'velocity': note['velocity'],
                    'start_time_seconds': note.get('start_time', 0.0),
                    'duration_seconds': note.get('duration', 0.5),
                    'track_index': note.get('track_index', 0)
                })
        
        return midi_context
    
    # Analysis helper methods
    
    def _analyze_harmonic_progression(self, project_state: LiveProjectState) -> List[str]:
        """Analyze harmonic progression from MIDI data."""
        # Simplified harmonic analysis
        # In a real implementation, this would use music theory analysis
        return ["C", "Am", "F", "G"]  # Placeholder
    
    def _detect_key_signature(self, project_state: LiveProjectState) -> str:
        """Detect key signature from MIDI data."""
        # Simplified key detection
        # In a real implementation, this would use music theory analysis
        return "C major"  # Placeholder
    
    def _analyze_rhythmic_patterns(self, project_state: LiveProjectState) -> Dict[str, Any]:
        """Analyze rhythmic patterns in the project."""
        # Simplified rhythmic analysis
        return {
            "swing_ratio": 0.5,
            "syncopation_level": 0.3,
            "groove_quality": 0.7
        }
    
    def _analyze_track_density(self, project_state: LiveProjectState) -> Dict[str, float]:
        """Analyze track density across the project."""
        density = {}
        for track in project_state.tracks:
            track_midi = [note for note in project_state.midi_data 
                         if note.get('track_index') == int(track.id)]
            density[track.name] = len(track_midi) / 100.0  # Normalized density
        return density
    
    def _analyze_frequency_balance(self, project_state: LiveProjectState) -> Dict[str, float]:
        """Analyze frequency balance across tracks."""
        # Simplified frequency analysis
        return {
            "low": 0.3,
            "mid": 0.4,
            "high": 0.3
        }
    
    def _detect_style_indicators(self, project_state: LiveProjectState) -> List[str]:
        """Detect musical style indicators."""
        # Simplified style detection
        indicators = []
        if project_state.tempo > 120:
            indicators.append("upbeat")
        if any('bass' in track.name.lower() for track in project_state.tracks):
            indicators.append("rhythmic")
        return indicators
    
    def _detect_mood_characteristics(self, project_state: LiveProjectState) -> List[str]:
        """Detect mood characteristics."""
        # Simplified mood detection
        characteristics = []
        if project_state.tempo < 80:
            characteristics.append("melancholic")
        elif project_state.tempo > 140:
            characteristics.append("energetic")
        else:
            characteristics.append("moderate")
        return characteristics
    
    def _determine_complexity_level(self, project_state: LiveProjectState) -> str:
        """Determine overall complexity level."""
        total_notes = len(project_state.midi_data)
        if total_notes < 50:
            return "simple"
        elif total_notes < 200:
            return "moderate"
        else:
            return "complex"
    
    def _calculate_note_density(self, track_midi: List[Dict], tempo: float) -> float:
        """Calculate note density for a track."""
        if not track_midi:
            return 0.0
        
        # Calculate notes per second
        total_duration = max(note.get('start_time', 0) + note.get('duration', 0) 
                           for note in track_midi) if track_midi else 1.0
        notes_per_second = len(track_midi) / max(total_duration, 1.0)
        
        # Normalize by tempo
        return notes_per_second / (tempo / 60.0)
    
    def _calculate_rhythmic_complexity(self, track_midi: List[Dict]) -> float:
        """Calculate rhythmic complexity for a track."""
        if not track_midi:
            return 0.0
        
        # Analyze timing variations
        start_times = [note.get('start_time', 0) for note in track_midi]
        if len(start_times) < 2:
            return 0.0
        
        # Calculate timing variation
        intervals = [start_times[i+1] - start_times[i] for i in range(len(start_times)-1)]
        if not intervals:
            return 0.0
        
        # Calculate coefficient of variation
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        if mean_interval == 0:
            return 0.0
        
        return min(std_interval / mean_interval, 1.0)
    
    def _determine_harmonic_function(self, track_midi: List[Dict], project_state: LiveProjectState) -> str:
        """Determine harmonic function of a track."""
        if not track_midi:
            return "unknown"
        
        # Analyze pitch content
        pitches = [note['pitch'] for note in track_midi if 'pitch' in note]
        if not pitches:
            return "unknown"
        
        # Determine if it's bass, melody, or harmony
        avg_pitch = np.mean(pitches)
        if avg_pitch < 60:  # Below middle C
            return "bass"
        elif avg_pitch > 80:  # Above middle C
            return "melody"
        else:
            return "harmony"
    
    def _determine_musical_role(self, track: LiveTrack, track_midi: List[Dict]) -> str:
        """Determine musical role of a track."""
        # Check track name for clues
        name_lower = track.name.lower()
        if 'bass' in name_lower:
            return "bass"
        elif 'drum' in name_lower or 'percussion' in name_lower:
            return "drums"
        elif 'piano' in name_lower or 'keyboard' in name_lower:
            return "piano"
        elif 'guitar' in name_lower:
            return "guitar"
        elif 'vocal' in name_lower or 'voice' in name_lower:
            return "vocals"
        else:
            # Determine by pitch content
            if track_midi:
                pitches = [note['pitch'] for note in track_midi if 'pitch' in note]
                if pitches:
                    avg_pitch = np.mean(pitches)
                    if avg_pitch < 60:
                        return "bass"
                    elif avg_pitch > 80:
                        return "melody"
                    else:
                        return "harmony"
            return "unknown"
    
    def _identify_track_enhancement_opportunities(
        self, 
        track: LiveTrack, 
        track_midi: List[Dict], 
        project_state: LiveProjectState
    ) -> List[str]:
        """Identify enhancement opportunities for a specific track."""
        opportunities = []
        
        if not track_midi:
            opportunities.append("add_musical_content")
            return opportunities
        
        # Check note density
        note_density = self._calculate_note_density(track_midi, project_state.tempo)
        if note_density < 0.1:
            opportunities.append("increase_note_density")
        
        # Check rhythmic complexity
        rhythmic_complexity = self._calculate_rhythmic_complexity(track_midi)
        if rhythmic_complexity < 0.3:
            opportunities.append("add_rhythmic_variation")
        
        # Check velocity range
        if track_midi:
            velocities = [note['velocity'] for note in track_midi if 'velocity' in note]
            if velocities:
                velocity_range = max(velocities) - min(velocities)
                if velocity_range < 30:
                    opportunities.append("add_dynamic_variation")
        
        return opportunities
    
    def export_context_to_json(self, file_path: str) -> bool:
        """Export current context to JSON file."""
        if not self.current_context:
            return False
        
        try:
            context_dict = asdict(self.current_context)
            with open(file_path, 'w') as f:
                json.dump(context_dict, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Error exporting context to JSON: {e}")
            return False
