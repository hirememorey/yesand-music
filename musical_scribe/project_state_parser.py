"""
Project State Parser

Converts entire DAW projects to structured JSON representation for Musical Scribe analysis.
Designed specifically for project-wide context awareness, not just selected regions.
"""

import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TrackInfo:
    """Information about a single track in the project."""
    name: str
    track_type: str  # 'audio', 'midi', 'bus', 'master'
    is_armed: bool
    is_muted: bool
    is_soloed: bool
    regions: List[Dict[str, Any]]
    musical_analysis: Optional[Dict[str, Any]] = None


@dataclass
class ProjectInfo:
    """Basic project information."""
    name: str
    tempo: float
    time_signature: str
    sample_rate: int
    bit_depth: int
    created_date: str
    modified_date: str


@dataclass
class ProjectState:
    """Complete project state representation."""
    project_info: ProjectInfo
    tracks: List[TrackInfo]
    musical_context: Dict[str, Any]
    file_path: str
    parsed_at: str


class ProjectStateParser:
    """
    Parses DAW project files to extract complete project state for Musical Scribe analysis.
    
    This is fundamentally different from the existing ardour_integration.py which only
    exports selected regions. This parser extracts the ENTIRE project context.
    """
    
    def __init__(self):
        self.supported_daws = ['ardour', 'logic_pro', 'pro_tools']
    
    def parse_project(self, project_path: str) -> ProjectState:
        """
        Parse a DAW project and return complete project state.
        
        Args:
            project_path: Path to the DAW project file or directory
            
        Returns:
            ProjectState: Complete project state for Musical Scribe analysis
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project not found: {project_path}")
        
        # Detect DAW type and parse accordingly
        daw_type = self._detect_daw_type(project_path)
        
        if daw_type == 'ardour':
            return self._parse_ardour_project(project_path)
        elif daw_type == 'logic_pro':
            return self._parse_logic_pro_project(project_path)
        elif daw_type == 'pro_tools':
            return self._parse_pro_tools_project(project_path)
        else:
            raise ValueError(f"Unsupported DAW type: {daw_type}")
    
    def _detect_daw_type(self, project_path: Path) -> str:
        """Detect the DAW type based on project file structure."""
        if project_path.is_file():
            if project_path.suffix == '.ardour':
                return 'ardour'
            elif project_path.suffix == '.logicx':
                return 'logic_pro'
            elif project_path.suffix == '.ptx':
                return 'pro_tools'
        elif project_path.is_dir():
            # Check for Ardour project directory
            if (project_path / 'project.ardour').exists():
                return 'ardour'
            # Check for Logic Pro project directory
            if any(f.suffix == '.logicx' for f in project_path.iterdir()):
                return 'logic_pro'
            # Check for Pro Tools project directory
            if any(f.suffix == '.ptx' for f in project_path.iterdir()):
                return 'pro_tools'
        
        # Default to Ardour for now
        return 'ardour'
    
    def _parse_ardour_project(self, project_path: Path) -> ProjectState:
        """Parse Ardour project file to extract complete project state."""
        import datetime
        
        # Find the main project file
        if project_path.is_file():
            project_file = project_path
        else:
            project_file = project_path / 'project.ardour'
        
        if not project_file.exists():
            raise FileNotFoundError(f"Ardour project file not found: {project_file}")
        
        # Parse the Ardour XML file
        tree = ET.parse(project_file)
        root = tree.getroot()
        
        # Extract project information
        project_info = self._extract_ardour_project_info(root)
        
        # Extract track information
        tracks = self._extract_ardour_tracks(root)
        
        # Extract musical context
        musical_context = self._extract_ardour_musical_context(root, tracks)
        
        return ProjectState(
            project_info=project_info,
            tracks=tracks,
            musical_context=musical_context,
            file_path=str(project_file),
            parsed_at=datetime.datetime.now().isoformat()
        )
    
    def _extract_ardour_project_info(self, root: ET.Element) -> ProjectInfo:
        """Extract basic project information from Ardour project."""
        # Get project name from root element
        project_name = root.get('name', 'Untitled Project')
        
        # Get tempo (default to 120 if not found)
        tempo_elem = root.find('.//tempo')
        tempo = float(tempo_elem.get('beats-per-minute', 120)) if tempo_elem is not None else 120.0
        
        # Get time signature (default to 4/4 if not found)
        time_sig_elem = root.find('.//time-signature')
        if time_sig_elem is not None:
            numerator = time_sig_elem.get('numerator', '4')
            denominator = time_sig_elem.get('denominator', '4')
            time_signature = f"{numerator}/{denominator}"
        else:
            time_signature = "4/4"
        
        # Get sample rate and bit depth
        sample_rate = int(root.get('sample-rate', 48000))
        bit_depth = int(root.get('bit-depth', 24))
        
        # Get creation and modification dates
        created_date = root.get('created-with-version', '')
        modified_date = root.get('modified-with-version', '')
        
        return ProjectInfo(
            name=project_name,
            tempo=tempo,
            time_signature=time_signature,
            sample_rate=sample_rate,
            bit_depth=bit_depth,
            created_date=created_date,
            modified_date=modified_date
        )
    
    def _extract_ardour_tracks(self, root: ET.Element) -> List[TrackInfo]:
        """Extract track information from Ardour project."""
        tracks = []
        
        # Find all track elements
        for track_elem in root.findall('.//track'):
            track_name = track_elem.get('name', 'Untitled Track')
            track_type = track_elem.get('type', 'audio')
            
            # Get track state
            is_armed = track_elem.get('rec-enabled', 'false').lower() == 'true'
            is_muted = track_elem.get('muted', 'false').lower() == 'true'
            is_soloed = track_elem.get('soloed', 'false').lower() == 'true'
            
            # Extract regions for this track
            regions = self._extract_ardour_regions(track_elem)
            
            # Basic musical analysis for this track
            musical_analysis = self._analyze_track_musical_content(regions, track_type)
            
            track_info = TrackInfo(
                name=track_name,
                track_type=track_type,
                is_armed=is_armed,
                is_muted=is_muted,
                is_soloed=is_soloed,
                regions=regions,
                musical_analysis=musical_analysis
            )
            
            tracks.append(track_info)
        
        return tracks
    
    def _extract_ardour_regions(self, track_elem: ET.Element) -> List[Dict[str, Any]]:
        """Extract region information from a track."""
        regions = []
        
        for region_elem in track_elem.findall('.//region'):
            region_info = {
                'name': region_elem.get('name', 'Untitled Region'),
                'start_time': float(region_elem.get('start', 0.0)),
                'length': float(region_elem.get('length', 0.0)),
                'position': float(region_elem.get('position', 0.0)),
                'type': region_elem.get('type', 'audio'),
                'muted': region_elem.get('muted', 'false').lower() == 'true',
                'locked': region_elem.get('locked', 'false').lower() == 'true'
            }
            
            # Extract MIDI data if this is a MIDI region
            if region_info['type'] == 'midi':
                midi_data = self._extract_midi_data(region_elem)
                region_info['midi_data'] = midi_data
            
            regions.append(region_info)
        
        return regions
    
    def _extract_midi_data(self, region_elem: ET.Element) -> Dict[str, Any]:
        """Extract MIDI data from a MIDI region."""
        midi_data = {
            'notes': [],
            'cc_events': [],
            'program_changes': []
        }
        
        # Look for MIDI events in the region
        for event_elem in region_elem.findall('.//event'):
            event_type = event_elem.get('type', '')
            
            if event_type == 'note':
                note_data = {
                    'pitch': int(event_elem.get('pitch', 60)),
                    'velocity': int(event_elem.get('velocity', 64)),
                    'start_time': float(event_elem.get('start', 0.0)),
                    'duration': float(event_elem.get('duration', 0.25))
                }
                midi_data['notes'].append(note_data)
            
            elif event_type == 'cc':
                cc_data = {
                    'controller': int(event_elem.get('controller', 0)),
                    'value': int(event_elem.get('value', 0)),
                    'time': float(event_elem.get('time', 0.0))
                }
                midi_data['cc_events'].append(cc_data)
            
            elif event_type == 'program':
                prog_data = {
                    'program': int(event_elem.get('program', 0)),
                    'time': float(event_elem.get('time', 0.0))
                }
                midi_data['program_changes'].append(prog_data)
        
        return midi_data
    
    def _analyze_track_musical_content(self, regions: List[Dict[str, Any]], track_type: str) -> Dict[str, Any]:
        """Perform basic musical analysis on track content."""
        analysis = {
            'has_midi_content': False,
            'has_audio_content': False,
            'note_count': 0,
            'pitch_range': {'min': 127, 'max': 0},
            'velocity_range': {'min': 127, 'max': 0},
            'duration_range': {'min': float('inf'), 'max': 0},
            'density': 'low'
        }
        
        total_notes = 0
        total_duration = 0.0
        
        for region in regions:
            if region['type'] == 'midi' and 'midi_data' in region:
                midi_data = region['midi_data']
                notes = midi_data.get('notes', [])
                
                analysis['has_midi_content'] = True
                analysis['note_count'] += len(notes)
                total_notes += len(notes)
                total_duration += region['length']
                
                # Analyze note characteristics
                for note in notes:
                    pitch = note['pitch']
                    velocity = note['velocity']
                    duration = note['duration']
                    
                    analysis['pitch_range']['min'] = min(analysis['pitch_range']['min'], pitch)
                    analysis['pitch_range']['max'] = max(analysis['pitch_range']['max'], pitch)
                    analysis['velocity_range']['min'] = min(analysis['velocity_range']['min'], velocity)
                    analysis['velocity_range']['max'] = max(analysis['velocity_range']['max'], velocity)
                    analysis['duration_range']['min'] = min(analysis['duration_range']['min'], duration)
                    analysis['duration_range']['max'] = max(analysis['duration_range']['max'], duration)
            
            elif region['type'] == 'audio':
                analysis['has_audio_content'] = True
        
        # Calculate density
        if total_duration > 0:
            notes_per_second = total_notes / total_duration
            if notes_per_second > 4:
                analysis['density'] = 'high'
            elif notes_per_second > 2:
                analysis['density'] = 'medium'
            else:
                analysis['density'] = 'low'
        
        return analysis
    
    def _extract_ardour_musical_context(self, root: ET.Element, tracks: List[TrackInfo]) -> Dict[str, Any]:
        """Extract project-wide musical context."""
        context = {
            'total_tracks': len(tracks),
            'midi_tracks': len([t for t in tracks if t.track_type == 'midi']),
            'audio_tracks': len([t for t in tracks if t.track_type == 'audio']),
            'bus_tracks': len([t for t in tracks if t.track_type == 'bus']),
            'master_tracks': len([t for t in tracks if t.track_type == 'master']),
            'total_regions': sum(len(t.regions) for t in tracks),
            'total_midi_notes': sum(t.musical_analysis.get('note_count', 0) for t in tracks),
            'project_duration': self._calculate_project_duration(tracks),
            'musical_style_indicators': self._detect_musical_style_indicators(tracks),
            'arrangement_structure': self._analyze_arrangement_structure(tracks)
        }
        
        return context
    
    def _calculate_project_duration(self, tracks: List[TrackInfo]) -> float:
        """Calculate the total duration of the project."""
        max_end_time = 0.0
        
        for track in tracks:
            for region in track.regions:
                end_time = region['position'] + region['length']
                max_end_time = max(max_end_time, end_time)
        
        return max_end_time
    
    def _detect_musical_style_indicators(self, tracks: List[TrackInfo]) -> Dict[str, Any]:
        """Detect musical style indicators from track analysis."""
        indicators = {
            'has_drums': False,
            'has_bass': False,
            'has_melody': False,
            'has_harmony': False,
            'tempo_range': 'unknown',
            'complexity_level': 'unknown'
        }
        
        # Analyze track names for instrument types
        for track in tracks:
            track_name_lower = track.name.lower()
            
            if any(word in track_name_lower for word in ['drum', 'kick', 'snare', 'hihat', 'percussion']):
                indicators['has_drums'] = True
            elif any(word in track_name_lower for word in ['bass', 'bassline']):
                indicators['has_bass'] = True
            elif any(word in track_name_lower for word in ['melody', 'lead', 'vocal', 'voice']):
                indicators['has_melody'] = True
            elif any(word in track_name_lower for word in ['piano', 'keyboard', 'chord', 'harmony']):
                indicators['has_harmony'] = True
        
        # Analyze complexity based on note density
        total_notes = sum(t.musical_analysis.get('note_count', 0) for t in tracks)
        total_duration = self._calculate_project_duration(tracks)
        
        if total_duration > 0:
            notes_per_second = total_notes / total_duration
            if notes_per_second > 8:
                indicators['complexity_level'] = 'high'
            elif notes_per_second > 4:
                indicators['complexity_level'] = 'medium'
            else:
                indicators['complexity_level'] = 'low'
        
        return indicators
    
    def _analyze_arrangement_structure(self, tracks: List[TrackInfo]) -> Dict[str, Any]:
        """Analyze the arrangement structure of the project."""
        structure = {
            'has_intro': False,
            'has_verse': False,
            'has_chorus': False,
            'has_bridge': False,
            'has_outro': False,
            'section_count': 0,
            'average_region_length': 0.0
        }
        
        # Analyze region names for section indicators
        all_regions = []
        for track in tracks:
            all_regions.extend(track.regions)
        
        if all_regions:
            structure['average_region_length'] = sum(r['length'] for r in all_regions) / len(all_regions)
            
            for region in all_regions:
                region_name_lower = region['name'].lower()
                
                if any(word in region_name_lower for word in ['intro', 'intro']):
                    structure['has_intro'] = True
                elif any(word in region_name_lower for word in ['verse', 'verse']):
                    structure['has_verse'] = True
                elif any(word in region_name_lower for word in ['chorus', 'chorus']):
                    structure['has_chorus'] = True
                elif any(word in region_name_lower for word in ['bridge', 'bridge']):
                    structure['has_bridge'] = True
                elif any(word in region_name_lower for word in ['outro', 'outro']):
                    structure['has_outro'] = True
            
            structure['section_count'] = sum([
                structure['has_intro'],
                structure['has_verse'],
                structure['has_chorus'],
                structure['has_bridge'],
                structure['has_outro']
            ])
        
        return structure
    
    def _parse_logic_pro_project(self, project_path: Path) -> ProjectState:
        """Parse Logic Pro project (placeholder for future implementation)."""
        raise NotImplementedError("Logic Pro project parsing not yet implemented")
    
    def _parse_pro_tools_project(self, project_path: Path) -> ProjectState:
        """Parse Pro Tools project (placeholder for future implementation)."""
        raise NotImplementedError("Pro Tools project parsing not yet implemented")
    
    def export_project_state(self, project_state: ProjectState, output_path: str) -> None:
        """Export project state to JSON file for debugging and analysis."""
        state_dict = {
            'project_info': {
                'name': project_state.project_info.name,
                'tempo': project_state.project_info.tempo,
                'time_signature': project_state.project_info.time_signature,
                'sample_rate': project_state.project_info.sample_rate,
                'bit_depth': project_state.project_info.bit_depth,
                'created_date': project_state.project_info.created_date,
                'modified_date': project_state.project_info.modified_date
            },
            'tracks': [
                {
                    'name': track.name,
                    'track_type': track.track_type,
                    'is_armed': track.is_armed,
                    'is_muted': track.is_muted,
                    'is_soloed': track.is_soloed,
                    'regions': track.regions,
                    'musical_analysis': track.musical_analysis
                }
                for track in project_state.tracks
            ],
            'musical_context': project_state.musical_context,
            'file_path': project_state.file_path,
            'parsed_at': project_state.parsed_at
        }
        
        with open(output_path, 'w') as f:
            json.dump(state_dict, f, indent=2)
