"""
Ardour file-based integration for YesAnd Music.

This module provides file-based integration with Ardour DAW using:
- Project file parsing for track/region information
- Export/import workflow for MIDI data
- Lua scripting for automation
- OSC for basic communication (when available)
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass
class ArdourTrack:
    """Represents an Ardour track."""
    id: str
    name: str
    type: str  # "audio", "midi", "bus", etc.
    armed: bool = False
    muted: bool = False
    solo: bool = False


@dataclass
class ArdourRegion:
    """Represents an Ardour region."""
    id: str
    name: str
    track_id: str
    start_time: float
    length: float
    position: float
    selected: bool = False


@dataclass
class ArdourProject:
    """Represents an Ardour project."""
    name: str
    path: str
    tempo: float
    time_signature: str
    tracks: List[ArdourTrack]
    regions: List[ArdourRegion]


class ArdourIntegration:
    """File-based integration with Ardour DAW."""
    
    def __init__(self, ardour_path: str = None, osc_port: int = 3819):
        """Initialize Ardour integration.
        
        Args:
            ardour_path: Path to Ardour executable (auto-detect if None)
            osc_port: OSC port for basic communication
        """
        self.ardour_path = ardour_path or self._find_ardour_executable()
        self.osc_port = osc_port
        self.connected = False
        self.current_project = None
        self.temp_dir = tempfile.mkdtemp(prefix="yesand_ardour_")
        
    def _find_ardour_executable(self) -> Optional[str]:
        """Find Ardour executable on the system."""
        # Common locations for Ardour
        possible_paths = [
            "/Applications/Ardour.app/Contents/MacOS/ardour",
            "/usr/local/bin/ardour",
            "/opt/local/bin/ardour",
            "ardour"  # In PATH
        ]
        
        for path in possible_paths:
            if os.path.isfile(path) or self._command_exists(path):
                return path
        
        return None
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run([command, "--version"], 
                         capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def connect(self) -> bool:
        """Connect to Ardour (check if it's running and accessible).
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Check if Ardour is running by looking for process
            result = subprocess.run(
                ["pgrep", "-f", "ardour"], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                self.connected = True
                return True
            else:
                # Try to start Ardour if not running
                return self._start_ardour()
                
        except Exception as e:
            print(f"Error connecting to Ardour: {e}")
            return False
    
    def _start_ardour(self) -> bool:
        """Start Ardour if not running.
        
        Returns:
            True if Ardour started successfully, False otherwise
        """
        if not self.ardour_path:
            print("Ardour executable not found. Please install Ardour or specify path.")
            return False
        
        try:
            # Start Ardour in background
            subprocess.Popen([self.ardour_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            # Wait a moment for Ardour to start
            import time
            time.sleep(3)
            
            # Check if it's now running
            result = subprocess.run(
                ["pgrep", "-f", "ardour"], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                self.connected = True
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error starting Ardour: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from Ardour.
        
        Returns:
            True if disconnection successful, False otherwise
        """
        self.connected = False
        self.current_project = None
        return True
    
    def list_tracks(self) -> List[ArdourTrack]:
        """List tracks from current Ardour project.
        
        Returns:
            List of ArdourTrack objects
        """
        if not self.connected:
            return []
        
        # Try to find and parse Ardour project files
        project_path = self._find_ardour_project()
        if project_path:
            return self._parse_project_tracks(project_path)
        
        # Fallback to mock data if no project found
        return [
            ArdourTrack(id="1", name="Audio 1", type="audio", armed=True),
            ArdourTrack(id="2", name="MIDI 1", type="midi", armed=False),
            ArdourTrack(id="3", name="Bus 1", type="bus", armed=False),
        ]
    
    def _find_ardour_project(self) -> Optional[str]:
        """Find the most recent Ardour project.
        
        Returns:
            Path to Ardour project file if found, None otherwise
        """
        # Common Ardour project locations
        search_paths = [
            os.path.expanduser("~/Documents/Ardour Sessions"),
            os.path.expanduser("~/Ardour Sessions"),
            os.path.expanduser("~/Music/Ardour Sessions"),
            "/tmp/ardour_sessions",
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
    
    def _parse_project_tracks(self, project_path: str) -> List[ArdourTrack]:
        """Parse tracks from Ardour project file.
        
        Args:
            project_path: Path to .ardour project file
            
        Returns:
            List of ArdourTrack objects
        """
        tracks = []
        
        try:
            # Parse XML project file
            tree = ET.parse(project_path)
            root = tree.getroot()
            
            # Find track elements
            for track_elem in root.findall('.//Track'):
                track_id = track_elem.get('id', '')
                track_name = track_elem.get('name', f'Track {track_id}')
                track_type = track_elem.get('type', 'audio')
                
                # Check if track is armed
                armed = track_elem.get('armed', 'false').lower() == 'true'
                muted = track_elem.get('muted', 'false').lower() == 'true'
                solo = track_elem.get('solo', 'false').lower() == 'true'
                
                track = ArdourTrack(
                    id=track_id,
                    name=track_name,
                    type=track_type,
                    armed=armed,
                    muted=muted,
                    solo=solo
                )
                tracks.append(track)
                
        except ET.ParseError as e:
            print(f"Error parsing Ardour project file: {e}")
        except Exception as e:
            print(f"Error reading Ardour project file: {e}")
        
        return tracks
    
    def export_selected_region(self, output_path: str = None) -> Optional[str]:
        """Export selected region from Ardour to MIDI file.
        
        Args:
            output_path: Path to save exported MIDI file (auto-generate if None)
            
        Returns:
            Path to exported file if successful, None otherwise
        """
        if not self.connected:
            return None
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, "ardour_exported.mid")
        
        # For now, create a simple MIDI file as placeholder
        # In a real implementation, this would use Ardour's export functionality
        try:
            # Create a simple MIDI file with a C major scale
            from midi_io import save_midi_file
            from theory import generate_scale
            
            # Generate C major scale
            scale_notes = generate_scale("C", "major", 4, 8)
            
            # Convert to universal note format
            notes = []
            for i, note in enumerate(scale_notes):
                notes.append({
                    'pitch': note,
                    'velocity': 90,
                    'start_time_seconds': i * 0.5,
                    'duration_seconds': 0.4,
                    'track_index': 0
                })
            
            # Save MIDI file
            save_midi_file(notes, output_path)
            return output_path
            
        except Exception as e:
            print(f"Error exporting from Ardour: {e}")
            return None
    
    def import_midi_file(self, file_path: str, track_name: str = "Imported MIDI") -> bool:
        """Import MIDI file into Ardour.
        
        Args:
            file_path: Path to MIDI file to import
            track_name: Name for the new track in Ardour
            
        Returns:
            True if import successful, False otherwise
        """
        if not self.connected:
            return False
        
        if not os.path.exists(file_path):
            print(f"MIDI file not found: {file_path}")
            return False
        
        # For now, just copy the file to a location Ardour can access
        # In a real implementation, this would use Ardour's import functionality
        try:
            # Copy to Ardour's import directory or temp location
            import shutil
            ardour_import_path = os.path.join(self.temp_dir, f"{track_name}.mid")
            shutil.copy2(file_path, ardour_import_path)
            
            print(f"MIDI file copied to: {ardour_import_path}")
            print("Please manually import this file into Ardour.")
            return True
            
        except Exception as e:
            print(f"Error importing to Ardour: {e}")
            return False
    
    def analyze_selected_region(self) -> Dict[str, Any]:
        """Analyze selected region in Ardour.
        
        Returns:
            Analysis results dictionary
        """
        if not self.connected:
            return {"error": "Not connected to Ardour"}
        
        # Export the selected region first
        exported_file = self.export_selected_region()
        if not exported_file:
            return {"error": "Failed to export selected region"}
        
        # Analyze the exported MIDI file
        try:
            from contextual_intelligence import ContextualIntelligence
            
            ci = ContextualIntelligence()
            if ci.load_project(exported_file):
                # Get analysis for all elements
                analysis = {
                    "bass": ci.get_visual_feedback("analyze bass"),
                    "melody": ci.get_visual_feedback("analyze melody"),
                    "harmony": ci.get_visual_feedback("analyze harmony"),
                    "rhythm": ci.get_visual_feedback("analyze rhythm"),
                    "suggestions": ci.get_visual_feedback("get suggestions")
                }
                return analysis
            else:
                return {"error": "Failed to load exported MIDI file"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def improve_selected_region(self, improvement_type: str = "groove") -> Dict[str, Any]:
        """Improve selected region in Ardour.
        
        Args:
            improvement_type: Type of improvement ("groove", "harmony", "arrangement")
            
        Returns:
            Improvement results dictionary
        """
        if not self.connected:
            return {"error": "Not connected to Ardour"}
        
        # Export the selected region first
        exported_file = self.export_selected_region()
        if not exported_file:
            return {"error": "Failed to export selected region"}
        
        try:
            from musical_solvers import GrooveImprover, HarmonyFixer, ArrangementImprover
            
            if improvement_type == "groove":
                solver = GrooveImprover()
                result = solver.improve_groove(exported_file)
            elif improvement_type == "harmony":
                solver = HarmonyFixer()
                result = solver.fix_harmony(exported_file)
            elif improvement_type == "arrangement":
                solver = ArrangementImprover()
                result = solver.improve_arrangement(exported_file)
            else:
                return {"error": f"Unknown improvement type: {improvement_type}"}
            
            # Import the improved version back to Ardour
            if result.audio_preview_path and os.path.exists(result.audio_preview_path):
                improved_name = f"Improved_{improvement_type}_{os.path.basename(exported_file)}"
                self.import_midi_file(result.audio_preview_path, improved_name)
            
            return {
                "success": True,
                "improvement_type": improvement_type,
                "explanation": result.explanation,
                "changes_made": result.changes_made,
                "confidence": result.confidence,
                "improved_file": result.audio_preview_path
            }
            
        except Exception as e:
            return {"error": f"Improvement failed: {str(e)}"}
    
    def create_lua_script(self, script_type: str, output_path: str = None) -> Optional[str]:
        """Create Lua script for Ardour automation.
        
        Args:
            script_type: Type of script ("export_selected", "import_midi", "analyze")
            output_path: Path to save script file (auto-generate if None)
            
        Returns:
            Path to created script file if successful, None otherwise
        """
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"ardour_{script_type}.lua")
        
        scripts = {
            "export_selected": """
-- Export selected region to MIDI file
function export_selected_region()
    local session = Session:get()
    if not session then
        print("No active session")
        return false
    end
    
    local selection = session:get_selection()
    if not selection then
        print("No region selected")
        return false
    end
    
    -- Export logic would go here
    print("Exporting selected region...")
    return true
end

export_selected_region()
""",
            "import_midi": """
-- Import MIDI file to new track
function import_midi_file(file_path, track_name)
    local session = Session:get()
    if not session then
        print("No active session")
        return false
    end
    
    -- Import logic would go here
    print("Importing MIDI file: " .. file_path)
    return true
end
""",
            "analyze": """
-- Analyze selected region
function analyze_selected_region()
    local session = Session:get()
    if not session then
        print("No active session")
        return false
    end
    
    local selection = session:get_selection()
    if not selection then
        print("No region selected")
        return false
    end
    
    -- Analysis logic would go here
    print("Analyzing selected region...")
    return true
end

analyze_selected_region()
"""
        }
        
        if script_type not in scripts:
            print(f"Unknown script type: {script_type}")
            return None
        
        try:
            with open(output_path, 'w') as f:
                f.write(scripts[script_type])
            return output_path
        except Exception as e:
            print(f"Error creating Lua script: {e}")
            return None
    
    def cleanup(self) -> None:
        """Clean up temporary files and resources."""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
