"""
Real-Time Ardour OSC Monitor

Monitors Ardour's OSC interface for real-time project state changes.
Provides live updates of tracks, regions, selections, and MIDI data.
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from threading import Thread, Event
import socket
from python_osc import osc_message_builder, osc_bundle_builder
from python_osc.osc_message import OscMessage
from python_osc.osc_server import OSCUDPServer
from python_osc.dispatcher import Dispatcher


@dataclass
class LiveTrack:
    """Real-time track information from Ardour."""
    id: str
    name: str
    type: str  # "audio", "midi", "bus"
    armed: bool
    muted: bool
    solo: bool
    record_enabled: bool
    volume: float
    pan: float
    last_updated: float


@dataclass
class LiveRegion:
    """Real-time region information from Ardour."""
    id: str
    name: str
    track_id: str
    start_time: float
    length: float
    position: float
    selected: bool
    muted: bool
    last_updated: float


@dataclass
class LiveSelection:
    """Real-time selection information from Ardour."""
    start_time: float
    end_time: float
    track_ids: List[str]
    region_ids: List[str]
    last_updated: float


@dataclass
class LiveProjectState:
    """Complete real-time project state."""
    project_name: str
    tempo: float
    time_signature: str
    sample_rate: float
    tracks: List[LiveTrack]
    regions: List[LiveRegion]
    selection: Optional[LiveSelection]
    midi_data: List[Dict[str, Any]]
    last_updated: float


class ArdourOSCMonitor:
    """
    Real-time OSC monitor for Ardour DAW.
    
    Monitors Ardour's OSC interface to capture live project state changes
    including tracks, regions, selections, and MIDI data.
    """
    
    def __init__(self, ardour_host: str = "127.0.0.1", ardour_port: int = 3819, 
                 monitor_port: int = 3820):
        """
        Initialize OSC monitor.
        
        Args:
            ardour_host: Ardour OSC host address
            ardour_port: Ardour OSC port
            monitor_port: Local port for receiving OSC messages
        """
        self.ardour_host = ardour_host
        self.ardour_port = ardour_port
        self.monitor_port = monitor_port
        
        # State storage
        self.current_state = LiveProjectState(
            project_name="",
            tempo=120.0,
            time_signature="4/4",
            sample_rate=44100.0,
            tracks=[],
            regions=[],
            selection=None,
            midi_data=[],
            last_updated=0.0
        )
        
        # OSC setup
        self.osc_client = None
        self.osc_server = None
        self.dispatcher = Dispatcher()
        self._setup_osc_handlers()
        
        # Monitoring control
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        
        # Callbacks
        self.state_change_callbacks: List[Callable[[LiveProjectState], None]] = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _setup_osc_handlers(self):
        """Setup OSC message handlers."""
        # Track information handlers
        self.dispatcher.map("/ardour/track/*/name", self._handle_track_name)
        self.dispatcher.map("/ardour/track/*/type", self._handle_track_type)
        self.dispatcher.map("/ardour/track/*/armed", self._handle_track_armed)
        self.dispatcher.map("/ardour/track/*/muted", self._handle_track_muted)
        self.dispatcher.map("/ardour/track/*/solo", self._handle_track_solo)
        self.dispatcher.map("/ardour/track/*/volume", self._handle_track_volume)
        self.dispatcher.map("/ardour/track/*/pan", self._handle_track_pan)
        
        # Region information handlers
        self.dispatcher.map("/ardour/region/*/name", self._handle_region_name)
        self.dispatcher.map("/ardour/region/*/position", self._handle_region_position)
        self.dispatcher.map("/ardour/region/*/length", self._handle_region_length)
        self.dispatcher.map("/ardour/region/*/selected", self._handle_region_selected)
        
        # Project information handlers
        self.dispatcher.map("/ardour/tempo", self._handle_tempo)
        self.dispatcher.map("/ardour/time_signature", self._handle_time_signature)
        self.dispatcher.map("/ardour/sample_rate", self._handle_sample_rate)
        
        # Selection handlers
        self.dispatcher.map("/ardour/selection/start", self._handle_selection_start)
        self.dispatcher.map("/ardour/selection/end", self._handle_selection_end)
        self.dispatcher.map("/ardour/selection/tracks", self._handle_selection_tracks)
        
        # MIDI data handlers
        self.dispatcher.map("/ardour/midi/note", self._handle_midi_note)
        self.dispatcher.map("/ardour/midi/cc", self._handle_midi_cc)
    
    def start_monitoring(self) -> bool:
        """Start real-time monitoring of Ardour."""
        try:
            # Setup OSC client for sending requests
            self.osc_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Setup OSC server for receiving updates
            self.osc_server = OSCUDPServer((self.ardour_host, self.monitor_port), self.dispatcher)
            
            # Start monitoring thread
            self.monitoring = True
            self.stop_event.clear()
            self.monitor_thread = Thread(target=self._monitoring_loop, daemon=True)
            self.monitor_thread.start()
            
            # Request initial state from Ardour
            self._request_initial_state()
            
            self.logger.info(f"Started OSC monitoring on {self.ardour_host}:{self.monitor_port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start OSC monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.monitoring = False
        self.stop_event.set()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        
        if self.osc_server:
            self.osc_server.shutdown()
        
        if self.osc_client:
            self.osc_client.close()
        
        self.logger.info("Stopped OSC monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring and not self.stop_event.is_set():
            try:
                # Process OSC messages
                if self.osc_server:
                    self.osc_server.handle_request()
                
                # Request periodic updates
                if time.time() - self.current_state.last_updated > 1.0:
                    self._request_state_update()
                
                time.sleep(0.01)  # 100Hz update rate
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(0.1)
    
    def _request_initial_state(self):
        """Request initial project state from Ardour."""
        try:
            # Request project information
            self._send_osc_message("/ardour/request/tempo")
            self._send_osc_message("/ardour/request/time_signature")
            self._send_osc_message("/ardour/request/sample_rate")
            
            # Request track information
            self._send_osc_message("/ardour/request/tracks")
            
            # Request region information
            self._send_osc_message("/ardour/request/regions")
            
            # Request selection information
            self._send_osc_message("/ardour/request/selection")
            
        except Exception as e:
            self.logger.error(f"Error requesting initial state: {e}")
    
    def _request_state_update(self):
        """Request state update from Ardour."""
        try:
            # Request updated track information
            self._send_osc_message("/ardour/request/tracks")
            
            # Request updated region information
            self._send_osc_message("/ardour/request/regions")
            
            # Request updated selection
            self._send_osc_message("/ardour/request/selection")
            
        except Exception as e:
            self.logger.error(f"Error requesting state update: {e}")
    
    def _send_osc_message(self, address: str, *args):
        """Send OSC message to Ardour."""
        try:
            msg = osc_message_builder.OscMessageBuilder(address)
            for arg in args:
                msg.add_arg(arg)
            msg = msg.build()
            
            self.osc_client.sendto(msg.dgram, (self.ardour_host, self.ardour_port))
            
        except Exception as e:
            self.logger.error(f"Error sending OSC message {address}: {e}")
    
    def add_state_change_callback(self, callback: Callable[[LiveProjectState], None]):
        """Add callback for state change notifications."""
        self.state_change_callbacks.append(callback)
    
    def remove_state_change_callback(self, callback: Callable[[LiveProjectState], None]):
        """Remove state change callback."""
        if callback in self.state_change_callbacks:
            self.state_change_callbacks.remove(callback)
    
    def _notify_state_change(self):
        """Notify all callbacks of state change."""
        for callback in self.state_change_callbacks:
            try:
                callback(self.current_state)
            except Exception as e:
                self.logger.error(f"Error in state change callback: {e}")
    
    def get_current_state(self) -> LiveProjectState:
        """Get current project state."""
        return self.current_state
    
    def get_track_by_id(self, track_id: str) -> Optional[LiveTrack]:
        """Get track by ID."""
        for track in self.current_state.tracks:
            if track.id == track_id:
                return track
        return None
    
    def get_regions_by_track(self, track_id: str) -> List[LiveRegion]:
        """Get regions for specific track."""
        return [region for region in self.current_state.regions if region.track_id == track_id]
    
    def get_selected_regions(self) -> List[LiveRegion]:
        """Get currently selected regions."""
        return [region for region in self.current_state.regions if region.selected]
    
    # OSC Message Handlers
    
    def _handle_track_name(self, address: str, *args):
        """Handle track name update."""
        track_id = address.split('/')[-2]
        name = args[0] if args else f"Track {track_id}"
        
        track = self.get_track_by_id(track_id)
        if track:
            track.name = name
            track.last_updated = time.time()
        else:
            # Create new track
            track = LiveTrack(
                id=track_id,
                name=name,
                type="unknown",
                armed=False,
                muted=False,
                solo=False,
                record_enabled=False,
                volume=0.0,
                pan=0.0,
                last_updated=time.time()
            )
            self.current_state.tracks.append(track)
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_type(self, address: str, *args):
        """Handle track type update."""
        track_id = address.split('/')[-2]
        track_type = args[0] if args else "unknown"
        
        track = self.get_track_by_id(track_id)
        if track:
            track.type = track_type
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_armed(self, address: str, *args):
        """Handle track armed state update."""
        track_id = address.split('/')[-2]
        armed = bool(args[0]) if args else False
        
        track = self.get_track_by_id(track_id)
        if track:
            track.armed = armed
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_muted(self, address: str, *args):
        """Handle track muted state update."""
        track_id = address.split('/')[-2]
        muted = bool(args[0]) if args else False
        
        track = self.get_track_by_id(track_id)
        if track:
            track.muted = muted
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_solo(self, address: str, *args):
        """Handle track solo state update."""
        track_id = address.split('/')[-2]
        solo = bool(args[0]) if args else False
        
        track = self.get_track_by_id(track_id)
        if track:
            track.solo = solo
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_volume(self, address: str, *args):
        """Handle track volume update."""
        track_id = address.split('/')[-2]
        volume = float(args[0]) if args else 0.0
        
        track = self.get_track_by_id(track_id)
        if track:
            track.volume = volume
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_track_pan(self, address: str, *args):
        """Handle track pan update."""
        track_id = address.split('/')[-2]
        pan = float(args[0]) if args else 0.0
        
        track = self.get_track_by_id(track_id)
        if track:
            track.pan = pan
            track.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_region_name(self, address: str, *args):
        """Handle region name update."""
        region_id = address.split('/')[-2]
        name = args[0] if args else f"Region {region_id}"
        
        # Find or create region
        region = None
        for r in self.current_state.regions:
            if r.id == region_id:
                region = r
                break
        
        if not region:
            region = LiveRegion(
                id=region_id,
                name=name,
                track_id="",
                start_time=0.0,
                length=0.0,
                position=0.0,
                selected=False,
                muted=False,
                last_updated=time.time()
            )
            self.current_state.regions.append(region)
        else:
            region.name = name
            region.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_region_position(self, address: str, *args):
        """Handle region position update."""
        region_id = address.split('/')[-2]
        position = float(args[0]) if args else 0.0
        
        for region in self.current_state.regions:
            if region.id == region_id:
                region.position = position
                region.last_updated = time.time()
                break
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_region_length(self, address: str, *args):
        """Handle region length update."""
        region_id = address.split('/')[-2]
        length = float(args[0]) if args else 0.0
        
        for region in self.current_state.regions:
            if region.id == region_id:
                region.length = length
                region.last_updated = time.time()
                break
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_region_selected(self, address: str, *args):
        """Handle region selection update."""
        region_id = address.split('/')[-2]
        selected = bool(args[0]) if args else False
        
        for region in self.current_state.regions:
            if region.id == region_id:
                region.selected = selected
                region.last_updated = time.time()
                break
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_tempo(self, address: str, *args):
        """Handle tempo update."""
        tempo = float(args[0]) if args else 120.0
        self.current_state.tempo = tempo
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_time_signature(self, address: str, *args):
        """Handle time signature update."""
        time_sig = args[0] if args else "4/4"
        self.current_state.time_signature = time_sig
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_sample_rate(self, address: str, *args):
        """Handle sample rate update."""
        sample_rate = float(args[0]) if args else 44100.0
        self.current_state.sample_rate = sample_rate
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_selection_start(self, address: str, *args):
        """Handle selection start update."""
        start_time = float(args[0]) if args else 0.0
        
        if not self.current_state.selection:
            self.current_state.selection = LiveSelection(
                start_time=start_time,
                end_time=start_time,
                track_ids=[],
                region_ids=[],
                last_updated=time.time()
            )
        else:
            self.current_state.selection.start_time = start_time
            self.current_state.selection.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_selection_end(self, address: str, *args):
        """Handle selection end update."""
        end_time = float(args[0]) if args else 0.0
        
        if self.current_state.selection:
            self.current_state.selection.end_time = end_time
            self.current_state.selection.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_selection_tracks(self, address: str, *args):
        """Handle selection tracks update."""
        track_ids = list(args) if args else []
        
        if self.current_state.selection:
            self.current_state.selection.track_ids = track_ids
            self.current_state.selection.last_updated = time.time()
        
        self.current_state.last_updated = time.time()
        self._notify_state_change()
    
    def _handle_midi_note(self, address: str, *args):
        """Handle MIDI note update."""
        if len(args) >= 4:
            note_data = {
                'pitch': int(args[0]),
                'velocity': int(args[1]),
                'start_time': float(args[2]),
                'duration': float(args[3]),
                'track_index': int(args[4]) if len(args) > 4 else 0,
                'timestamp': time.time()
            }
            self.current_state.midi_data.append(note_data)
            self.current_state.last_updated = time.time()
            self._notify_state_change()
    
    def _handle_midi_cc(self, address: str, *args):
        """Handle MIDI CC update."""
        if len(args) >= 3:
            cc_data = {
                'controller': int(args[0]),
                'value': int(args[1]),
                'track_index': int(args[2]),
                'timestamp': time.time()
            }
            self.current_state.midi_data.append(cc_data)
            self.current_state.last_updated = time.time()
            self._notify_state_change()
    
    def export_state_to_json(self, file_path: str) -> bool:
        """Export current state to JSON file."""
        try:
            state_dict = asdict(self.current_state)
            with open(file_path, 'w') as f:
                json.dump(state_dict, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Error exporting state to JSON: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.start_monitoring()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_monitoring()
