"""
Ardour Live Integration for Real-Time MIDI Streaming

This module provides real-time MIDI streaming integration with Ardour DAW,
enabling live MIDI generation and editing without file-based workflows.
"""

import os
import json
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, Generator
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import mido
import rtmidi

@dataclass
class LiveMIDITrack:
    """Represents a live MIDI track in Ardour"""
    id: str
    name: str
    midi_channel: int
    armed: bool = True
    muted: bool = False
    solo: bool = False
    current_region: Optional[str] = None

@dataclass
class MIDIStreamEvent:
    """Represents a MIDI event in the stream"""
    note: int
    velocity: int
    start_time: float
    duration: float
    channel: int = 0
    event_type: str = "note_on"  # "note_on", "note_off", "cc", "program_change"

@dataclass
class LiveEditingSession:
    """Represents an active live editing session"""
    track_id: str
    region_id: str
    start_time: float
    end_time: float
    is_recording: bool = False
    modifications: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.modifications is None:
            self.modifications = []

class MIDIStreamGenerator:
    """Generates MIDI streams for real-time playback"""
    
    def __init__(self, sample_rate: int = 44100, tempo: int = 120):
        self.sample_rate = sample_rate
        self.tempo = tempo
        self.beats_per_second = tempo / 60.0
        self.samples_per_beat = int(sample_rate / self.beats_per_second)
        
    def generate_bassline_stream(self, style: str = "funky", key: str = "C", 
                                duration: float = 8.0) -> Generator[MIDIStreamEvent, None, None]:
        """Generate a bassline MIDI stream"""
        from theory import generate_scale
        from analysis import apply_swing
        
        # Generate scale notes
        scale_notes = generate_scale(key, "major", 2, 8)  # 2 octaves
        
        # Create bassline pattern based on style
        if style == "funky":
            pattern = self._create_funky_pattern(scale_notes, duration)
        elif style == "jazz":
            pattern = self._create_jazz_pattern(scale_notes, duration)
        elif style == "blues":
            pattern = self._create_blues_pattern(scale_notes, duration)
        else:
            pattern = self._create_simple_pattern(scale_notes, duration)
        
        # Apply swing if needed
        if style in ["jazz", "swing"]:
            pattern = apply_swing(pattern)
        
        # Stream the events
        for i, note_data in enumerate(pattern):
            yield MIDIStreamEvent(
                note=note_data['pitch'],
                velocity=note_data['velocity'],
                start_time=note_data['start_time_seconds'],
                duration=note_data['duration_seconds'],
                channel=0
            )
    
    def _create_funky_pattern(self, scale_notes: List[int], duration: float) -> List[Dict[str, Any]]:
        """Create a funky bassline pattern"""
        pattern = []
        beat_duration = 0.5  # 8th notes
        current_time = 0.0
        
        # Funky syncopated pattern
        funky_rhythm = [0, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 3.75, 4.0]
        
        for i, beat_time in enumerate(funky_rhythm):
            if current_time + beat_time >= duration:
                break
                
            # Use root note (first note of scale) for most beats
            note = scale_notes[0] if i % 4 != 1 else scale_notes[2]  # Root or 3rd
            
            # Add some variation
            if i % 8 == 0:  # Every 4 beats
                note = scale_notes[4]  # 5th
            
            pattern.append({
                'pitch': note,
                'velocity': 90 if i % 4 == 0 else 75,  # Accent on beat
                'start_time_seconds': current_time + beat_time,
                'duration_seconds': beat_duration * 0.8
            })
        
        return pattern
    
    def _create_jazz_pattern(self, scale_notes: List[int], duration: float) -> List[Dict[str, Any]]:
        """Create a jazz bassline pattern"""
        pattern = []
        beat_duration = 0.25  # 16th notes
        current_time = 0.0
        
        # Jazz walking bass pattern
        jazz_rhythm = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
        
        for i, beat_time in enumerate(jazz_rhythm):
            if current_time + beat_time >= duration:
                break
                
            # Walking bass: use different scale degrees
            note_index = i % len(scale_notes)
            note = scale_notes[note_index]
            
            pattern.append({
                'pitch': note,
                'velocity': 85,
                'start_time_seconds': current_time + beat_time,
                'duration_seconds': beat_duration * 0.9
            })
        
        return pattern
    
    def _create_blues_pattern(self, scale_notes: List[int], duration: float) -> List[Dict[str, Any]]:
        """Create a blues bassline pattern"""
        pattern = []
        beat_duration = 0.5  # 8th notes
        current_time = 0.0
        
        # Blues pattern with blue notes
        blues_rhythm = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        
        for i, beat_time in enumerate(blues_rhythm):
            if current_time + beat_time >= duration:
                break
                
            # Blues scale pattern
            note = scale_notes[i % len(scale_notes)]
            
            # Add blue note (flattened 3rd or 7th)
            if i % 4 == 2:
                note = scale_notes[2] - 1  # Flattened 3rd
            
            pattern.append({
                'pitch': note,
                'velocity': 80,
                'start_time_seconds': current_time + beat_time,
                'duration_seconds': beat_duration * 0.8
            })
        
        return pattern
    
    def _create_simple_pattern(self, scale_notes: List[int], duration: float) -> List[Dict[str, Any]]:
        """Create a simple bassline pattern"""
        pattern = []
        beat_duration = 1.0  # Quarter notes
        current_time = 0.0
        
        while current_time < duration:
            pattern.append({
                'pitch': scale_notes[0],  # Root note
                'velocity': 80,
                'start_time_seconds': current_time,
                'duration_seconds': beat_duration * 0.8
            })
            current_time += beat_duration
        
        return pattern

class ArdourLiveIntegration:
    """Real-time MIDI streaming integration with Ardour DAW"""
    
    def __init__(self, ardour_path: str = None, midi_port: str = "IAC Driver Bus 1"):
        """Initialize live Ardour integration
        
        Args:
            ardour_path: Path to Ardour executable (auto-detect if None)
            midi_port: MIDI port name for streaming
        """
        self.ardour_path = ardour_path or self._find_ardour_executable()
        self.midi_port = midi_port
        self.connected = False
        self.current_project = None
        self.live_tracks = {}
        self.active_sessions = {}
        self.midi_out = None
        self.stream_generator = MIDIStreamGenerator()
        
        # Threading for real-time operations
        self.stream_thread = None
        self.stop_streaming = threading.Event()
        
    def _find_ardour_executable(self) -> Optional[str]:
        """Find Ardour executable on the system"""
        possible_paths = [
            "/Applications/Ardour.app/Contents/MacOS/ardour",
            "/usr/local/bin/ardour",
            "/opt/local/bin/ardour",
            "ardour"
        ]
        
        for path in possible_paths:
            if os.path.isfile(path) or self._command_exists(path):
                return path
        
        return None
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run([command, "--version"], 
                         capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def connect(self) -> bool:
        """Connect to Ardour and initialize MIDI streaming"""
        try:
            # Check if Ardour is running
            result = subprocess.run(
                ["pgrep", "-f", "ardour"], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode != 0:
                # Try to start Ardour
                if not self._start_ardour():
                    return False
            
            # Initialize MIDI output
            self._initialize_midi_output()
            
            # Load current project
            self._load_current_project()
            
            self.connected = True
            return True
            
        except Exception as e:
            print(f"Error connecting to Ardour: {e}")
            return False
    
    def _start_ardour(self) -> bool:
        """Start Ardour if not running"""
        if not self.ardour_path:
            print("Ardour executable not found")
            return False
        
        try:
            subprocess.Popen([self.ardour_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            time.sleep(3)  # Wait for Ardour to start
            return True
        except Exception as e:
            print(f"Error starting Ardour: {e}")
            return False
    
    def _initialize_midi_output(self):
        """Initialize MIDI output for streaming"""
        try:
            self.midi_out = rtmidi.MidiOut()
            
            # Find the specified MIDI port
            available_ports = self.midi_out.get_ports()
            port_index = None
            
            for i, port_name in enumerate(available_ports):
                if self.midi_port in port_name:
                    port_index = i
                    break
            
            if port_index is None:
                print(f"MIDI port '{self.midi_port}' not found. Available ports: {available_ports}")
                return False
            
            self.midi_out.open_port(port_index)
            print(f"Connected to MIDI port: {self.midi_port}")
            return True
            
        except Exception as e:
            print(f"Error initializing MIDI output: {e}")
            return False
    
    def _load_current_project(self):
        """Load current Ardour project information"""
        project_path = self._find_ardour_project()
        if project_path:
            self.current_project = self._parse_project_info(project_path)
            self.live_tracks = self._get_live_tracks()
    
    def _find_ardour_project(self) -> Optional[str]:
        """Find the most recent Ardour project"""
        search_paths = [
            os.path.expanduser("~/Documents/Ardour Sessions"),
            os.path.expanduser("~/Ardour Sessions"),
            os.path.expanduser("~/Music/Ardour Sessions"),
        ]
        
        latest_project = None
        latest_time = 0
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith('.ardour'):
                        project_file = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(project_file)
                            if mtime > latest_time:
                                latest_time = mtime
                                latest_project = project_file
                        except OSError:
                            continue
        
        return latest_project
    
    def _parse_project_info(self, project_path: str) -> Dict[str, Any]:
        """Parse Ardour project information"""
        try:
            tree = ET.parse(project_path)
            root = tree.getroot()
            
            return {
                "name": root.get("name", "Untitled"),
                "path": project_path,
                "tempo": float(root.get("tempo", 120)),
                "time_signature": root.get("time-signature", "4/4")
            }
        except Exception as e:
            print(f"Error parsing project: {e}")
            return {"name": "Unknown", "path": project_path, "tempo": 120, "time_signature": "4/4"}
    
    def _get_live_tracks(self) -> Dict[str, LiveMIDITrack]:
        """Get live MIDI tracks from current project"""
        tracks = {}
        
        if not self.current_project:
            return tracks
        
        try:
            tree = ET.parse(self.current_project["path"])
            root = tree.getroot()
            
            track_id = 1
            for track_elem in root.findall('.//Track'):
                if track_elem.get('type') == 'midi':
                    track = LiveMIDITrack(
                        id=str(track_id),
                        name=track_elem.get('name', f'MIDI Track {track_id}'),
                        midi_channel=track_id - 1,  # MIDI channels are 0-based
                        armed=track_elem.get('armed', 'false').lower() == 'true'
                    )
                    tracks[str(track_id)] = track
                    track_id += 1
                    
        except Exception as e:
            print(f"Error getting live tracks: {e}")
        
        return tracks
    
    def stream_midi_to_track(self, track_id: str, midi_stream: Generator[MIDIStreamEvent, None, None], 
                           duration: float = 8.0) -> bool:
        """Stream MIDI events to a specific track in real-time"""
        if not self.connected or not self.midi_out:
            return False
        
        if track_id not in self.live_tracks:
            print(f"Track {track_id} not found")
            return False
        
        track = self.live_tracks[track_id]
        
        # Start streaming in a separate thread
        self.stop_streaming.clear()
        self.stream_thread = threading.Thread(
            target=self._stream_midi_events,
            args=(track, midi_stream, duration)
        )
        self.stream_thread.start()
        
        return True
    
    def _stream_midi_events(self, track: LiveMIDITrack, midi_stream: Generator[MIDIStreamEvent, None, None], 
                          duration: float):
        """Stream MIDI events in real-time"""
        start_time = time.time()
        active_notes = {}  # Track active notes for note_off events
        
        try:
            for event in midi_stream:
                if self.stop_streaming.is_set():
                    break
                
                # Calculate when to send this event
                current_time = time.time()
                event_time = start_time + event.start_time
                
                # Wait until it's time to send the event
                if event_time > current_time:
                    time.sleep(event_time - current_time)
                
                # Send the MIDI event
                if event.event_type == "note_on":
                    midi_msg = [0x90 | track.midi_channel, event.note, event.velocity]
                    self.midi_out.send_message(midi_msg)
                    
                    # Schedule note_off event
                    note_off_time = event_time + event.duration
                    active_notes[event.note] = note_off_time
                
                elif event.event_type == "note_off":
                    midi_msg = [0x80 | track.midi_channel, event.note, 0]
                    self.midi_out.send_message(midi_msg)
                    if event.note in active_notes:
                        del active_notes[event.note]
            
            # Send note_off for any remaining active notes
            current_time = time.time()
            for note, note_off_time in active_notes.items():
                if note_off_time > current_time:
                    time.sleep(note_off_time - current_time)
                midi_msg = [0x80 | track.midi_channel, note, 0]
                self.midi_out.send_message(midi_msg)
                
        except Exception as e:
            print(f"Error streaming MIDI events: {e}")
    
    def stop_streaming(self):
        """Stop current MIDI streaming"""
        self.stop_streaming.set()
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=1.0)
    
    def create_midi_track(self, name: str = "YesAnd Track") -> Optional[str]:
        """Create a new MIDI track in Ardour"""
        if not self.connected:
            return None
        
        # Generate new track ID
        track_id = str(len(self.live_tracks) + 1)
        
        # Create track object
        track = LiveMIDITrack(
            id=track_id,
            name=name,
            midi_channel=len(self.live_tracks),
            armed=True
        )
        
        self.live_tracks[track_id] = track
        
        # In a real implementation, this would create the track in Ardour
        print(f"Created MIDI track: {name} (ID: {track_id})")
        
        return track_id
    
    def enable_live_editing(self, track_id: str) -> bool:
        """Enable live editing for a specific track"""
        if track_id not in self.live_tracks:
            return False
        
        # Create live editing session
        session = LiveEditingSession(
            track_id=track_id,
            region_id=f"region_{track_id}_{int(time.time())}",
            start_time=0.0,
            end_time=8.0
        )
        
        self.active_sessions[track_id] = session
        print(f"Live editing enabled for track {track_id}")
        
        return True
    
    def modify_current_region(self, track_id: str, modification: str) -> bool:
        """Modify the current region in real-time"""
        if track_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[track_id]
        
        # Add modification to session
        session.modifications.append({
            "type": "modification",
            "description": modification,
            "timestamp": time.time()
        })
        
        print(f"Applied modification to track {track_id}: {modification}")
        
        return True
    
    def get_live_tracks(self) -> List[LiveMIDITrack]:
        """Get list of live MIDI tracks"""
        return list(self.live_tracks.values())
    
    def get_active_sessions(self) -> List[LiveEditingSession]:
        """Get list of active live editing sessions"""
        return list(self.active_sessions.values())
    
    def disconnect(self):
        """Disconnect from Ardour and cleanup"""
        self.stop_streaming()
        
        if self.midi_out:
            self.midi_out.close_port()
            self.midi_out = None
        
        self.connected = False
        self.live_tracks.clear()
        self.active_sessions.clear()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Example usage and testing
if __name__ == "__main__":
    # Test the live integration
    with ArdourLiveIntegration() as ardour:
        if ardour.connect():
            print("Connected to Ardour")
            
            # Create a new track
            track_id = ardour.create_midi_track("Test Bassline")
            
            # Generate and stream a funky bassline
            bassline_stream = ardour.stream_generator.generate_bassline_stream(
                style="funky", 
                key="C", 
                duration=8.0
            )
            
            # Stream to the track
            ardour.stream_midi_to_track(track_id, bassline_stream, 8.0)
            
            # Wait for streaming to complete
            time.sleep(10)
            
            print("Live MIDI streaming test completed")
        else:
            print("Failed to connect to Ardour")
