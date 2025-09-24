"""
Real-Time Ardour Enhancement System

Integrates all components for real-time track enhancement in Ardour.
Provides complete workflow from OSC monitoring to LLM enhancement to MIDI generation.
"""

import os
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path

from ardour_osc_monitor import ArdourOSCMonitor, LiveProjectState
from project_state_capture import ProjectStateCapture, LiveProjectContext
from midi_stream_analyzer import MIDIStreamAnalyzer, TrackStreamAnalysis
from llm_track_enhancer import LLMTrackEnhancer, EnhancementRequest, EnhancementResult
from midi_pattern_parser import MIDIPatternParser, MIDIGenerationOptions
from ardour_lua_importer import ArdourLuaImporter, ImportResult, TrackConfig
from track_manager import TrackManager, EnhancementType


@dataclass
class EnhancementSession:
    """Active enhancement session."""
    session_id: str
    start_time: float
    project_context: Optional[LiveProjectContext]
    enhancement_results: List[EnhancementResult]
    generated_files: List[Dict[str, Any]]
    import_results: List[ImportResult]
    is_active: bool = True


class RealTimeArdourEnhancer:
    """
    Real-time Ardour enhancement system.
    
    Integrates OSC monitoring, state capture, MIDI analysis, and LLM enhancement
    to provide real-time track enhancement in Ardour.
    """
    
    def __init__(self, openai_api_key: str = None, ardour_host: str = "127.0.0.1", 
                 ardour_port: int = 3819, monitor_port: int = 3820):
        """
        Initialize real-time Ardour enhancer.
        
        Args:
            openai_api_key: OpenAI API key
            ardour_host: Ardour OSC host
            ardour_port: Ardour OSC port
            monitor_port: Local monitor port
        """
        # Initialize components
        self.osc_monitor = ArdourOSCMonitor(ardour_host, ardour_port, monitor_port)
        self.state_capture = ProjectStateCapture()
        self.midi_analyzer = MIDIStreamAnalyzer()
        self.llm_enhancer = LLMTrackEnhancer(openai_api_key)
        self.pattern_parser = MIDIPatternParser()
        self.lua_importer = ArdourLuaImporter()
        self.track_manager = TrackManager()
        
        # Session management
        self.current_session: Optional[EnhancementSession] = None
        self.enhancement_history: List[EnhancementSession] = []
        
        # Callbacks
        self.enhancement_callbacks: List[Callable[[EnhancementResult], None]] = []
        self.state_change_callbacks: List[Callable[[LiveProjectContext], None]] = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def start_enhancement_session(self, session_id: str = None) -> str:
        """
        Start a new enhancement session.
        
        Args:
            session_id: Optional session ID (auto-generated if None)
            
        Returns:
            Session ID
        """
        if not session_id:
            session_id = f"session_{int(time.time())}"
        
        # Create new session
        self.current_session = EnhancementSession(
            session_id=session_id,
            start_time=time.time(),
            project_context=None,
            enhancement_results=[],
            generated_files=[],
            import_results=[]
        )
        
        # Start monitoring
        if not self.osc_monitor.start_monitoring():
            self.logger.error("Failed to start OSC monitoring")
            return None
        
        # Start MIDI analysis
        if not self.midi_analyzer.start_analysis():
            self.logger.error("Failed to start MIDI analysis")
            return None
        
        # Setup callbacks
        self.osc_monitor.add_state_change_callback(self._on_project_state_change)
        self.midi_analyzer.add_analysis_callback(self._on_midi_analysis_update)
        
        self.logger.info(f"Started enhancement session: {session_id}")
        return session_id
    
    def stop_enhancement_session(self):
        """Stop current enhancement session."""
        if self.current_session:
            self.current_session.is_active = False
            self.enhancement_history.append(self.current_session)
            self.current_session = None
        
        # Stop monitoring
        self.osc_monitor.stop_monitoring()
        self.midi_analyzer.stop_analysis()
        
        self.logger.info("Stopped enhancement session")
    
    def enhance_track(self, user_request: str, track_id: str = None, 
                     enhancement_type: str = "general") -> EnhancementResult:
        """
        Enhance a track using LLM analysis.
        
        Args:
            user_request: User's enhancement request
            track_id: Specific track ID (None for any track)
            enhancement_type: Type of enhancement
            
        Returns:
            EnhancementResult: Enhancement result
        """
        if not self.current_session:
            return EnhancementResult(
                success=False,
                patterns=[],
                enhancement_type=enhancement_type,
                track_id=track_id or "unknown",
                user_request=user_request,
                musical_analysis="",
                suggestions=[],
                confidence=0.0,
                processing_time=0.0,
                error_message="No active enhancement session"
            )
        
        # Get current project context
        project_state = self.osc_monitor.get_current_state()
        if not project_state:
            return EnhancementResult(
                success=False,
                patterns=[],
                enhancement_type=enhancement_type,
                track_id=track_id or "unknown",
                user_request=user_request,
                musical_analysis="",
                suggestions=[],
                confidence=0.0,
                processing_time=0.0,
                error_message="No project state available"
            )
        
        # Update project context
        project_context = self.state_capture.update_project_state(project_state)
        self.current_session.project_context = project_context
        
        # Create enhancement request
        request = EnhancementRequest(
            user_request=user_request,
            track_id=track_id,
            enhancement_type=enhancement_type,
            context=project_context
        )
        
        # Perform enhancement
        result = self.llm_enhancer.enhance_track(request)
        
        # Parse and generate MIDI files
        if result.success:
            generated_files = self.pattern_parser.parse_enhancement_result(result)
            self.current_session.enhancement_results.append(result)
            self.current_session.generated_files.extend(generated_files)
            
            # Auto-import to Ardour
            import_results = self._auto_import_enhancement(result, generated_files)
            self.current_session.import_results.extend(import_results)
            
            # Notify callbacks
            for callback in self.enhancement_callbacks:
                try:
                    callback(result)
                except Exception as e:
                    self.logger.error(f"Error in enhancement callback: {e}")
        
        return result
    
    def get_enhancement_suggestions(self, track_id: str = None) -> List[str]:
        """Get enhancement suggestions for current project state."""
        if not self.current_session or not self.current_session.project_context:
            return []
        
        context = self.current_session.project_context
        suggestions = []
        
        # Get suggestions from enhancement opportunities
        for opportunity in context.enhancement_opportunities:
            if not track_id or opportunity.track_id == track_id:
                suggestions.append(f"{opportunity.description} (Priority: {opportunity.priority})")
        
        # Get suggestions from track analyses
        for analysis in context.track_analyses:
            if not track_id or analysis.track_id == track_id:
                suggestions.extend(analysis.enhancement_opportunities)
        
        return suggestions
    
    def _auto_import_enhancement(self, result: EnhancementResult, 
                                generated_files: List[Dict[str, Any]]) -> List[ImportResult]:
        """
        Automatically import enhancement result to Ardour.
        
        Args:
            result: Enhancement result
            generated_files: Generated MIDI files
            
        Returns:
            List of import results
        """
        import_results = []
        
        if not result.success or not generated_files:
            return import_results
        
        try:
            # Determine enhancement type
            enhancement_type = self._determine_enhancement_type(result.enhancement_type)
            
            # Get track configuration
            track_name, was_created = self.track_manager.get_track_for_enhancement(
                enhancement_type, result.track_id
            )
            
            # Create track if needed
            if was_created:
                track_config = self.track_manager.create_track_config(
                    enhancement_type, track_name
                )
                self.lua_importer.create_track_if_needed(
                    TrackConfig(
                        name=track_config["name"],
                        type=track_config["type"],
                        channel_count=track_config["channel_count"],
                        auto_create=track_config.get("auto_create", True)
                    )
                )
            
            # Import each generated file
            for i, file_info in enumerate(generated_files):
                if not os.path.exists(file_info["file_path"]):
                    self.logger.warning(f"Generated file not found: {file_info['file_path']}")
                    continue
                
                # Create track config for this pattern
                pattern_track_name = f"{track_name}_{i+1}" if len(generated_files) > 1 else track_name
                track_config = TrackConfig(
                    name=pattern_track_name,
                    type="midi",
                    auto_create=True
                )
                
                # Import MIDI file
                import_result = self.lua_importer.auto_import_midi(
                    file_info["file_path"],
                    track_config,
                    position=i * 32  # 32 beats apart
                )
                
                import_results.append(import_result)
                
                if import_result.success:
                    self.logger.info(f"Successfully imported {file_info['file_path']} to {pattern_track_name}")
                else:
                    self.logger.error(f"Failed to import {file_info['file_path']}: {import_result.error_message}")
            
        except Exception as e:
            self.logger.error(f"Error in auto-import: {e}")
        
        return import_results
    
    def _determine_enhancement_type(self, enhancement_type_str: str) -> EnhancementType:
        """Determine enhancement type from string."""
        type_mapping = {
            "bass": EnhancementType.BASS,
            "drums": EnhancementType.DRUMS,
            "melody": EnhancementType.MELODY,
            "harmony": EnhancementType.HARMONY,
            "general": EnhancementType.GENERAL
        }
        
        return type_mapping.get(enhancement_type_str.lower(), EnhancementType.GENERAL)
    
    def import_enhancement_to_ardour(self, result: EnhancementResult, 
                                   pattern_index: int = 0) -> bool:
        """Import enhancement result to Ardour (legacy method for compatibility)."""
        if not result.success or not result.patterns:
            return False
        
        if pattern_index >= len(result.patterns):
            return False
        
        # Use auto-import functionality
        generated_files = self.pattern_parser.parse_enhancement_result(result)
        import_results = self._auto_import_enhancement(result, generated_files)
        
        return any(ir.success for ir in import_results)
    
    def get_current_project_state(self) -> Optional[LiveProjectState]:
        """Get current project state."""
        return self.osc_monitor.get_current_state()
    
    def get_current_project_context(self) -> Optional[LiveProjectContext]:
        """Get current project context."""
        return self.current_session.project_context if self.current_session else None
    
    def get_enhancement_history(self) -> List[EnhancementSession]:
        """Get enhancement history."""
        return self.enhancement_history.copy()
    
    def get_import_results(self) -> List[ImportResult]:
        """Get import results from current session."""
        if self.current_session:
            return self.current_session.import_results.copy()
        return []
    
    def get_import_history(self) -> List[ImportResult]:
        """Get all import results from all sessions."""
        all_imports = []
        for session in self.enhancement_history:
            all_imports.extend(session.import_results)
        if self.current_session:
            all_imports.extend(self.current_session.import_results)
        return all_imports
    
    def add_enhancement_callback(self, callback: Callable[[EnhancementResult], None]):
        """Add callback for enhancement results."""
        self.enhancement_callbacks.append(callback)
    
    def add_state_change_callback(self, callback: Callable[[LiveProjectContext], None]):
        """Add callback for state changes."""
        self.state_change_callbacks.append(callback)
    
    def _on_project_state_change(self, project_state: LiveProjectState):
        """Handle project state changes."""
        # Update project context
        project_context = self.state_capture.update_project_state(project_state)
        
        if self.current_session:
            self.current_session.project_context = project_context
        
        # Notify callbacks
        for callback in self.state_change_callbacks:
            try:
                callback(project_context)
            except Exception as e:
                self.logger.error(f"Error in state change callback: {e}")
    
    def _on_midi_analysis_update(self, track_analyses: Dict[str, TrackStreamAnalysis]):
        """Handle MIDI analysis updates."""
        # Update project context with MIDI analysis
        if self.current_session and self.current_session.project_context:
            # This would integrate MIDI analysis with project context
            # For now, just log the update
            self.logger.debug(f"MIDI analysis updated: {len(track_analyses)} tracks")
    
    def export_session_summary(self, session_id: str = None) -> Optional[str]:
        """Export session summary."""
        session = self.current_session if not session_id else None
        
        if session_id:
            for s in self.enhancement_history:
                if s.session_id == session_id:
                    session = s
                    break
        
        if not session:
            return None
        
        # Create summary
        summary_parts = []
        summary_parts.append(f"# Enhancement Session Summary")
        summary_parts.append(f"")
        summary_parts.append(f"**Session ID:** {session.session_id}")
        summary_parts.append(f"**Start Time:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.start_time))}")
        summary_parts.append(f"**Duration:** {time.time() - session.start_time:.2f}s")
        summary_parts.append(f"**Enhancements:** {len(session.enhancement_results)}")
        summary_parts.append(f"**Generated Files:** {len(session.generated_files)}")
        summary_parts.append(f"**Imports:** {len(session.import_results)}")
        summary_parts.append(f"**Successful Imports:** {len([ir for ir in session.import_results if ir.success])}")
        summary_parts.append(f"")
        
        # Add enhancement results
        for i, result in enumerate(session.enhancement_results, 1):
            summary_parts.append(f"## Enhancement {i}")
            summary_parts.append(f"")
            summary_parts.append(f"**Type:** {result.enhancement_type}")
            summary_parts.append(f"**Track:** {result.track_id}")
            summary_parts.append(f"**Request:** {result.user_request}")
            summary_parts.append(f"**Confidence:** {result.confidence:.2f}")
            summary_parts.append(f"**Processing Time:** {result.processing_time:.2f}s")
            
            # Add import information
            related_imports = [ir for ir in session.import_results if ir.track_name.startswith(result.track_id or "")]
            if related_imports:
                summary_parts.append(f"**Imports:** {len(related_imports)}")
                for j, import_result in enumerate(related_imports, 1):
                    status = "✅ Success" if import_result.success else "❌ Failed"
                    summary_parts.append(f"  - Import {j}: {import_result.track_name} {status}")
                    if not import_result.success and import_result.error_message:
                        summary_parts.append(f"    Error: {import_result.error_message}")
            
            summary_parts.append(f"")
        
        # Save summary
        summary_path = Path("enhancement_sessions") / f"{session.session_id}_summary.md"
        summary_path.parent.mkdir(exist_ok=True)
        
        with open(summary_path, 'w') as f:
            f.write("\n".join(summary_parts))
        
        return str(summary_path)
    
    def __enter__(self):
        """Context manager entry."""
        self.start_enhancement_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_enhancement_session()
