"""
Real-Time MIDI Stream Analyzer

Analyzes MIDI streams in real-time to provide musical context for LLM enhancement.
Monitors MIDI input/output streams and provides analysis for track enhancement.
"""

import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from collections import defaultdict, deque
import numpy as np
import mido
from threading import Thread, Event, Lock


@dataclass
class MIDINote:
    """Real-time MIDI note information."""
    pitch: int
    velocity: int
    start_time: float
    duration: float
    track_index: int
    channel: int
    timestamp: float


@dataclass
class MIDIStreamAnalysis:
    """Analysis of MIDI stream."""
    note_count: int
    note_density: float
    pitch_range: Tuple[int, int]
    velocity_range: Tuple[int, int]
    rhythmic_complexity: float
    harmonic_content: List[int]
    melodic_contour: List[int]
    groove_quality: float
    swing_ratio: float
    syncopation_level: float
    last_updated: float


@dataclass
class TrackStreamAnalysis:
    """Analysis of a specific track's MIDI stream."""
    track_id: str
    track_name: str
    stream_analysis: MIDIStreamAnalysis
    recent_notes: List[MIDINote]
    musical_role: str
    enhancement_suggestions: List[str]
    last_updated: float


class MIDIStreamAnalyzer:
    """
    Real-time MIDI stream analyzer.
    
    Monitors MIDI input/output streams and provides real-time analysis
    for musical context and track enhancement suggestions.
    """
    
    def __init__(self, input_port: str = None, output_port: str = None):
        """
        Initialize MIDI stream analyzer.
        
        Args:
            input_port: MIDI input port name (None for auto-detect)
            output_port: MIDI output port name (None for auto-detect)
        """
        self.input_port = input_port
        self.output_port = output_port
        
        # MIDI ports
        self.midi_input = None
        self.midi_output = None
        
        # Analysis data
        self.track_analyses: Dict[str, TrackStreamAnalysis] = {}
        self.global_analysis: Optional[MIDIStreamAnalysis] = None
        
        # Real-time data
        self.recent_notes: deque = deque(maxlen=1000)  # Last 1000 notes
        self.track_notes: Dict[str, deque] = defaultdict(lambda: deque(maxlen=500))
        
        # Analysis control
        self.analyzing = False
        self.analysis_thread = None
        self.stop_event = Event()
        self.analysis_lock = Lock()
        
        # Callbacks
        self.note_callbacks: List[Callable[[MIDINote], None]] = []
        self.analysis_callbacks: List[Callable[[Dict[str, TrackStreamAnalysis]], None]] = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def start_analysis(self) -> bool:
        """Start real-time MIDI stream analysis."""
        try:
            # Setup MIDI ports
            if not self._setup_midi_ports():
                return False
            
            # Start analysis thread
            self.analyzing = True
            self.stop_event.clear()
            self.analysis_thread = Thread(target=self._analysis_loop, daemon=True)
            self.analysis_thread.start()
            
            self.logger.info("Started MIDI stream analysis")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start MIDI analysis: {e}")
            return False
    
    def stop_analysis(self):
        """Stop MIDI stream analysis."""
        self.analyzing = False
        self.stop_event.set()
        
        if self.analysis_thread:
            self.analysis_thread.join(timeout=2.0)
        
        # Close MIDI ports
        if self.midi_input:
            self.midi_input.close()
        if self.midi_output:
            self.midi_output.close()
        
        self.logger.info("Stopped MIDI stream analysis")
    
    def _setup_midi_ports(self) -> bool:
        """Setup MIDI input and output ports."""
        try:
            # Setup input port
            if self.input_port:
                self.midi_input = mido.open_input(self.input_port)
            else:
                # Auto-detect input port
                input_names = mido.get_input_names()
                if input_names:
                    self.midi_input = mido.open_input(input_names[0])
                else:
                    self.logger.warning("No MIDI input ports available")
            
            # Setup output port
            if self.output_port:
                self.midi_output = mido.open_output(self.output_port)
            else:
                # Auto-detect output port
                output_names = mido.get_output_names()
                if output_names:
                    self.midi_output = mido.open_output(output_names[0])
                else:
                    self.logger.warning("No MIDI output ports available")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up MIDI ports: {e}")
            return False
    
    def _analysis_loop(self):
        """Main analysis loop."""
        while self.analyzing and not self.stop_event.is_set():
            try:
                # Process MIDI input
                if self.midi_input:
                    self._process_midi_input()
                
                # Perform periodic analysis
                self._perform_analysis()
                
                time.sleep(0.01)  # 100Hz analysis rate
                
            except Exception as e:
                self.logger.error(f"Error in analysis loop: {e}")
                time.sleep(0.1)
    
    def _process_midi_input(self):
        """Process incoming MIDI messages."""
        try:
            for msg in self.midi_input.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Note on
                    note = MIDINote(
                        pitch=msg.note,
                        velocity=msg.velocity,
                        start_time=time.time(),
                        duration=0.0,  # Will be updated on note_off
                        track_index=0,  # Default track
                        channel=msg.channel,
                        timestamp=time.time()
                    )
                    self._add_note(note)
                    
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    # Note off
                    self._end_note(msg.note, msg.channel)
                    
        except Exception as e:
            self.logger.error(f"Error processing MIDI input: {e}")
    
    def _add_note(self, note: MIDINote):
        """Add a new note to the analysis."""
        with self.analysis_lock:
            # Add to global notes
            self.recent_notes.append(note)
            
            # Add to track-specific notes
            track_key = f"track_{note.track_index}"
            self.track_notes[track_key].append(note)
            
            # Notify callbacks
            for callback in self.note_callbacks:
                try:
                    callback(note)
                except Exception as e:
                    self.logger.error(f"Error in note callback: {e}")
    
    def _end_note(self, pitch: int, channel: int):
        """End a note (update duration)."""
        with self.analysis_lock:
            current_time = time.time()
            
            # Find the most recent note with this pitch and channel
            for note in reversed(self.recent_notes):
                if (note.pitch == pitch and note.channel == channel and 
                    note.duration == 0.0):
                    note.duration = current_time - note.start_time
                    break
    
    def _perform_analysis(self):
        """Perform periodic analysis of MIDI streams."""
        with self.analysis_lock:
            # Analyze global stream
            self.global_analysis = self._analyze_stream(list(self.recent_notes))
            
            # Analyze each track
            for track_key, notes in self.track_notes.items():
                if notes:
                    track_id = track_key.replace("track_", "")
                    track_name = f"Track {track_id}"
                    
                    stream_analysis = self._analyze_stream(list(notes))
                    musical_role = self._determine_musical_role(stream_analysis)
                    enhancement_suggestions = self._generate_enhancement_suggestions(
                        stream_analysis, musical_role
                    )
                    
                    self.track_analyses[track_id] = TrackStreamAnalysis(
                        track_id=track_id,
                        track_name=track_name,
                        stream_analysis=stream_analysis,
                        recent_notes=list(notes)[-50:],  # Last 50 notes
                        musical_role=musical_role,
                        enhancement_suggestions=enhancement_suggestions,
                        last_updated=time.time()
                    )
            
            # Notify analysis callbacks
            for callback in self.analysis_callbacks:
                try:
                    callback(self.track_analyses.copy())
                except Exception as e:
                    self.logger.error(f"Error in analysis callback: {e}")
    
    def _analyze_stream(self, notes: List[MIDINote]) -> MIDIStreamAnalysis:
        """Analyze a stream of MIDI notes."""
        if not notes:
            return MIDIStreamAnalysis(
                note_count=0,
                note_density=0.0,
                pitch_range=(0, 0),
                velocity_range=(0, 0),
                rhythmic_complexity=0.0,
                harmonic_content=[],
                melodic_contour=[],
                groove_quality=0.0,
                swing_ratio=0.5,
                syncopation_level=0.0,
                last_updated=time.time()
            )
        
        # Basic statistics
        note_count = len(notes)
        pitches = [note.pitch for note in notes]
        velocities = [note.velocity for note in notes]
        
        # Calculate note density (notes per second)
        if notes:
            time_span = max(note.start_time for note in notes) - min(note.start_time for note in notes)
            note_density = note_count / max(time_span, 0.1)
        else:
            note_density = 0.0
        
        # Pitch and velocity ranges
        pitch_range = (min(pitches), max(pitches)) if pitches else (0, 0)
        velocity_range = (min(velocities), max(velocities)) if velocities else (0, 0)
        
        # Rhythmic complexity
        rhythmic_complexity = self._calculate_rhythmic_complexity(notes)
        
        # Harmonic content
        harmonic_content = self._extract_harmonic_content(pitches)
        
        # Melodic contour
        melodic_contour = self._extract_melodic_contour(pitches)
        
        # Groove quality
        groove_quality = self._calculate_groove_quality(notes)
        
        # Swing ratio
        swing_ratio = self._calculate_swing_ratio(notes)
        
        # Syncopation level
        syncopation_level = self._calculate_syncopation_level(notes)
        
        return MIDIStreamAnalysis(
            note_count=note_count,
            note_density=note_density,
            pitch_range=pitch_range,
            velocity_range=velocity_range,
            rhythmic_complexity=rhythmic_complexity,
            harmonic_content=harmonic_content,
            melodic_contour=melodic_contour,
            groove_quality=groove_quality,
            swing_ratio=swing_ratio,
            syncopation_level=syncopation_level,
            last_updated=time.time()
        )
    
    def _calculate_rhythmic_complexity(self, notes: List[MIDINote]) -> float:
        """Calculate rhythmic complexity of a note stream."""
        if len(notes) < 2:
            return 0.0
        
        # Calculate intervals between note starts
        start_times = sorted([note.start_time for note in notes])
        intervals = [start_times[i+1] - start_times[i] for i in range(len(start_times)-1)]
        
        if not intervals:
            return 0.0
        
        # Calculate coefficient of variation
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if mean_interval == 0:
            return 0.0
        
        return min(std_interval / mean_interval, 1.0)
    
    def _extract_harmonic_content(self, pitches: List[int]) -> List[int]:
        """Extract harmonic content from pitches."""
        if not pitches:
            return []
        
        # Convert to pitch classes (0-11)
        pitch_classes = [pitch % 12 for pitch in pitches]
        
        # Count frequency of each pitch class
        pitch_class_counts = defaultdict(int)
        for pc in pitch_classes:
            pitch_class_counts[pc] += 1
        
        # Return most common pitch classes
        return sorted(pitch_class_counts.keys(), key=lambda x: pitch_class_counts[x], reverse=True)[:7]
    
    def _extract_melodic_contour(self, pitches: List[int]) -> List[int]:
        """Extract melodic contour from pitches."""
        if len(pitches) < 2:
            return []
        
        # Calculate pitch intervals
        intervals = [pitches[i+1] - pitches[i] for i in range(len(pitches)-1)]
        
        # Quantize intervals to contour directions
        contour = []
        for interval in intervals:
            if interval > 2:
                contour.append(1)  # Up
            elif interval < -2:
                contour.append(-1)  # Down
            else:
                contour.append(0)  # Same
        
        return contour
    
    def _calculate_groove_quality(self, notes: List[MIDINote]) -> float:
        """Calculate groove quality of a note stream."""
        if len(notes) < 4:
            return 0.0
        
        # Analyze timing consistency
        start_times = [note.start_time for note in notes]
        intervals = [start_times[i+1] - start_times[i] for i in range(len(start_times)-1)]
        
        if not intervals:
            return 0.0
        
        # Calculate timing consistency
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if mean_interval == 0:
            return 0.0
        
        # Groove quality is inverse of timing variation
        timing_consistency = 1.0 - min(std_interval / mean_interval, 1.0)
        
        # Analyze velocity consistency
        velocities = [note.velocity for note in notes]
        velocity_consistency = 1.0 - min(np.std(velocities) / np.mean(velocities), 1.0)
        
        # Combine timing and velocity consistency
        return (timing_consistency + velocity_consistency) / 2.0
    
    def _calculate_swing_ratio(self, notes: List[MIDINote]) -> float:
        """Calculate swing ratio of a note stream."""
        if len(notes) < 4:
            return 0.5  # Default to straight
        
        # Analyze timing patterns
        start_times = [note.start_time for note in notes]
        intervals = [start_times[i+1] - start_times[i] for i in range(len(start_times)-1)]
        
        if not intervals:
            return 0.5
        
        # Look for swing patterns (long-short-long-short)
        swing_indicators = 0
        total_patterns = 0
        
        for i in range(len(intervals) - 1):
            if i % 2 == 0:  # Even positions should be longer
                if intervals[i] > intervals[i+1]:
                    swing_indicators += 1
                total_patterns += 1
        
        if total_patterns == 0:
            return 0.5
        
        swing_ratio = swing_indicators / total_patterns
        return max(0.0, min(1.0, swing_ratio))
    
    def _calculate_syncopation_level(self, notes: List[MIDINote]) -> float:
        """Calculate syncopation level of a note stream."""
        if len(notes) < 4:
            return 0.0
        
        # Analyze off-beat emphasis
        start_times = [note.start_time for note in notes]
        
        # Calculate beat positions (assuming 4/4 time)
        beat_length = 1.0  # 1 second per beat (will be adjusted based on tempo)
        beat_positions = [time % beat_length for time in start_times]
        
        # Count notes on off-beats (0.25, 0.75 of beat)
        off_beat_notes = 0
        for pos in beat_positions:
            if 0.2 < pos < 0.3 or 0.7 < pos < 0.8:  # Off-beat positions
                off_beat_notes += 1
        
        return min(off_beat_notes / len(notes), 1.0)
    
    def _determine_musical_role(self, analysis: MIDIStreamAnalysis) -> str:
        """Determine musical role based on stream analysis."""
        if analysis.note_count == 0:
            return "unknown"
        
        # Analyze pitch range
        pitch_center = (analysis.pitch_range[0] + analysis.pitch_range[1]) / 2
        
        if pitch_center < 60:  # Below middle C
            return "bass"
        elif pitch_center > 80:  # Above middle C
            return "melody"
        else:
            return "harmony"
    
    def _generate_enhancement_suggestions(
        self, 
        analysis: MIDIStreamAnalysis, 
        musical_role: str
    ) -> List[str]:
        """Generate enhancement suggestions based on analysis."""
        suggestions = []
        
        if analysis.note_count == 0:
            suggestions.append("add_musical_content")
            return suggestions
        
        # Check note density
        if analysis.note_density < 0.5:
            suggestions.append("increase_note_density")
        
        # Check rhythmic complexity
        if analysis.rhythmic_complexity < 0.3:
            suggestions.append("add_rhythmic_variation")
        
        # Check groove quality
        if analysis.groove_quality < 0.6:
            suggestions.append("improve_groove")
        
        # Check velocity range
        velocity_range = analysis.velocity_range[1] - analysis.velocity_range[0]
        if velocity_range < 30:
            suggestions.append("add_dynamic_variation")
        
        # Check swing
        if analysis.swing_ratio < 0.3:
            suggestions.append("add_swing")
        elif analysis.swing_ratio > 0.7:
            suggestions.append("reduce_swing")
        
        # Check syncopation
        if analysis.syncopation_level < 0.2:
            suggestions.append("add_syncopation")
        
        return suggestions
    
    def add_note_callback(self, callback: Callable[[MIDINote], None]):
        """Add callback for new notes."""
        self.note_callbacks.append(callback)
    
    def add_analysis_callback(self, callback: Callable[[Dict[str, TrackStreamAnalysis]], None]):
        """Add callback for analysis updates."""
        self.analysis_callbacks.append(callback)
    
    def get_track_analysis(self, track_id: str) -> Optional[TrackStreamAnalysis]:
        """Get analysis for a specific track."""
        return self.track_analyses.get(track_id)
    
    def get_global_analysis(self) -> Optional[MIDIStreamAnalysis]:
        """Get global stream analysis."""
        return self.global_analysis
    
    def get_all_analyses(self) -> Dict[str, TrackStreamAnalysis]:
        """Get all track analyses."""
        return self.track_analyses.copy()
    
    def send_midi_note(self, pitch: int, velocity: int, duration: float, channel: int = 0):
        """Send a MIDI note to the output port."""
        if not self.midi_output:
            return
        
        try:
            # Send note on
            note_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
            self.midi_output.send(note_on)
            
            # Schedule note off
            def send_note_off():
                time.sleep(duration)
                note_off = mido.Message('note_off', note=pitch, velocity=0, channel=channel)
                self.midi_output.send(note_off)
            
            Thread(target=send_note_off, daemon=True).start()
            
        except Exception as e:
            self.logger.error(f"Error sending MIDI note: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.start_analysis()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_analysis()
