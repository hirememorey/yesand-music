"""
Musical Scribe Integration

Integration layer that bridges the Musical Scribe architecture with the existing YesAnd Music system.
Provides seamless integration while maintaining fallback to existing functionality.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from musical_scribe import MusicalScribeEngine, MusicalScribeResult
from musical_scribe.project_state_parser import ProjectState
from musical_scribe.musical_context_engine import MusicalContext


class MusicalScribeIntegration:
    """
    Integration layer for Musical Scribe with existing YesAnd Music system.
    
    This class provides a bridge between the new Musical Scribe architecture
    and the existing command-driven system, enabling seamless integration
    while maintaining fallback capabilities.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize Musical Scribe Integration.
        
        Args:
            openai_api_key: OpenAI API key for LLM integration
        """
        self.engine = MusicalScribeEngine(openai_api_key)
        self.logger = logging.getLogger(__name__)
        
        # Integration settings
        self.fallback_enabled = True
        self.export_debug_info = True
        self.debug_output_dir = Path("musical_scribe_debug")
        
        # Create debug output directory
        if self.export_debug_info:
            self.debug_output_dir.mkdir(exist_ok=True)
    
    def enhance_project(self, project_path: str, user_request: str) -> Dict[str, Any]:
        """
        Enhance a musical project using Musical Scribe.
        
        Args:
            project_path: Path to the DAW project
            user_request: User's enhancement request
            
        Returns:
            Dict containing enhancement results and metadata
        """
        try:
            self.logger.info(f"Starting Musical Scribe enhancement for: {project_path}")
            
            # Run Musical Scribe enhancement
            result = self.engine.enhance_music(project_path, user_request)
            
            if result.success:
                self.logger.info(f"Musical Scribe enhancement successful: {len(result.patterns)} patterns generated")
                
                # Export debug information if enabled
                if self.export_debug_info:
                    self._export_debug_info(result, project_path, user_request)
                
                # Convert result to integration format
                integration_result = self._convert_result_to_integration_format(result)
                
                return integration_result
            else:
                self.logger.error(f"Musical Scribe enhancement failed: {result.error_message}")
                
                if self.fallback_enabled:
                    self.logger.info("Falling back to existing system...")
                    return self._fallback_enhancement(project_path, user_request)
                else:
                    return {
                        'success': False,
                        'error': result.error_message,
                        'patterns': [],
                        'fallback_used': False
                    }
                    
        except Exception as e:
            self.logger.error(f"Musical Scribe integration error: {str(e)}")
            
            if self.fallback_enabled:
                self.logger.info("Falling back to existing system due to error...")
                return self._fallback_enhancement(project_path, user_request)
            else:
                return {
                    'success': False,
                    'error': str(e),
                    'patterns': [],
                    'fallback_used': False
                }
    
    def analyze_project_context(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze project context without generating enhancements.
        
        Args:
            project_path: Path to the DAW project
            
        Returns:
            Dict containing project analysis
        """
        try:
            # Parse project state
            project_state = self.engine.project_parser.parse_project(project_path)
            
            # Analyze musical context
            musical_context = self.engine.context_engine.analyze_project_context(project_state)
            
            # Convert to integration format
            analysis = {
                'success': True,
                'project_info': {
                    'name': project_state.project_info.name,
                    'tempo': project_state.project_info.tempo,
                    'time_signature': project_state.project_info.time_signature,
                    'tracks': len(project_state.tracks)
                },
                'musical_context': {
                    'harmonic_analysis': {
                        'key_signature': musical_context.harmonic_analysis.key_signature,
                        'harmonic_complexity': musical_context.harmonic_analysis.harmonic_complexity,
                        'voice_leading_quality': musical_context.harmonic_analysis.voice_leading_quality
                    },
                    'rhythmic_analysis': {
                        'tempo_consistency': musical_context.rhythmic_analysis.tempo_consistency,
                        'groove_quality': musical_context.rhythmic_analysis.groove_quality,
                        'rhythmic_density': musical_context.rhythmic_analysis.rhythmic_density
                    },
                    'style_analysis': {
                        'primary_genre': musical_context.style_analysis.primary_genre,
                        'complexity_level': musical_context.style_analysis.complexity_level,
                        'production_style': musical_context.style_analysis.production_style
                    },
                    'enhancement_opportunities': {
                        'missing_elements': musical_context.enhancement_opportunities.missing_elements,
                        'weak_areas': musical_context.enhancement_opportunities.weak_areas,
                        'priority_level': musical_context.enhancement_opportunities.priority_level
                    },
                    'musical_coherence_score': musical_context.musical_coherence_score
                },
                'tracks': [
                    {
                        'name': track.name,
                        'type': track.track_type,
                        'is_armed': track.is_armed,
                        'is_muted': track.is_muted,
                        'regions': len(track.regions),
                        'musical_analysis': track.musical_analysis
                    }
                    for track in project_state.tracks
                ]
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Project analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'project_info': {},
                'musical_context': {},
                'tracks': []
            }
    
    def generate_contextual_prompt(self, project_path: str, user_request: str) -> Dict[str, Any]:
        """
        Generate a contextual prompt for a project and user request.
        
        Args:
            project_path: Path to the DAW project
            user_request: User's enhancement request
            
        Returns:
            Dict containing the contextual prompt and metadata
        """
        try:
            # Parse project state
            project_state = self.engine.project_parser.parse_project(project_path)
            
            # Analyze musical context
            musical_context = self.engine.context_engine.analyze_project_context(project_state)
            
            # Build contextual prompt
            contextual_prompt = self.engine.prompt_builder.build_enhancement_prompt(
                project_state, musical_context, user_request
            )
            
            return {
                'success': True,
                'role': {
                    'name': contextual_prompt.role.name,
                    'description': contextual_prompt.role.description,
                    'expertise_areas': contextual_prompt.role.expertise_areas
                },
                'project_context': contextual_prompt.project_context,
                'musical_analysis': contextual_prompt.musical_analysis,
                'enhancement_opportunities': contextual_prompt.enhancement_opportunities,
                'full_prompt': contextual_prompt.full_prompt,
                'confidence_score': contextual_prompt.confidence_score
            }
            
        except Exception as e:
            self.logger.error(f"Contextual prompt generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'role': {},
                'project_context': '',
                'musical_analysis': '',
                'enhancement_opportunities': '',
                'full_prompt': '',
                'confidence_score': 0.0
            }
    
    def _convert_result_to_integration_format(self, result: MusicalScribeResult) -> Dict[str, Any]:
        """Convert Musical Scribe result to integration format."""
        return {
            'success': result.success,
            'patterns': [
                {
                    'name': pattern.name,
                    'description': pattern.description,
                    'midi_data': pattern.midi_data,
                    'confidence_score': pattern.confidence_score,
                    'enhancement_type': pattern.enhancement_type,
                    'musical_justification': pattern.musical_justification
                }
                for pattern in result.patterns
            ],
            'project_context': result.project_context,
            'musical_analysis': result.musical_analysis,
            'enhancement_opportunities': result.enhancement_opportunities,
            'confidence_score': result.confidence_score,
            'fallback_used': False,
            'musical_scribe_version': '1.0.0'
        }
    
    def _fallback_enhancement(self, project_path: str, user_request: str) -> Dict[str, Any]:
        """Fallback to existing system when Musical Scribe fails."""
        try:
            # Import existing control plane
            from commands.control_plane import ControlPlane
            
            # Create control plane instance
            control_plane = ControlPlane()
            
            # Try to execute the request using existing system
            # This is a simplified fallback - in practice, you'd need more sophisticated mapping
            if 'bass' in user_request.lower():
                result = control_plane.execute("play scale C major")
            elif 'drum' in user_request.lower():
                result = control_plane.execute("play scale C major")
            else:
                result = control_plane.execute("play scale C major")
            
            return {
                'success': True,
                'patterns': [
                    {
                        'name': 'Fallback Pattern',
                        'description': 'Generated using existing system',
                        'midi_data': [],
                        'confidence_score': 0.5,
                        'enhancement_type': 'fallback',
                        'musical_justification': 'Generated using existing YesAnd Music system as fallback'
                    }
                ],
                'project_context': 'Fallback mode - limited context available',
                'musical_analysis': 'Fallback mode - basic analysis only',
                'enhancement_opportunities': 'Fallback mode - limited enhancement suggestions',
                'confidence_score': 0.5,
                'fallback_used': True,
                'fallback_result': result
            }
            
        except Exception as e:
            self.logger.error(f"Fallback enhancement failed: {str(e)}")
            return {
                'success': False,
                'error': f"Both Musical Scribe and fallback failed: {str(e)}",
                'patterns': [],
                'fallback_used': True
            }
    
    def _export_debug_info(self, result: MusicalScribeResult, project_path: str, user_request: str) -> None:
        """Export debug information for analysis."""
        try:
            import json
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            debug_file = self.debug_output_dir / f"musical_scribe_debug_{timestamp}.json"
            
            debug_info = {
                'timestamp': timestamp,
                'project_path': project_path,
                'user_request': user_request,
                'result': {
                    'success': result.success,
                    'patterns_count': len(result.patterns),
                    'confidence_score': result.confidence_score,
                    'error_message': result.error_message
                },
                'patterns': [
                    {
                        'name': pattern.name,
                        'enhancement_type': pattern.enhancement_type,
                        'confidence_score': pattern.confidence_score
                    }
                    for pattern in result.patterns
                ]
            }
            
            with open(debug_file, 'w') as f:
                json.dump(debug_info, f, indent=2)
            
            self.logger.info(f"Debug information exported to: {debug_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to export debug information: {str(e)}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get Musical Scribe system status."""
        return {
            'musical_scribe_available': True,
            'llm_available': self.engine.is_llm_available(),
            'supported_daws': self.engine.get_supported_daws(),
            'fallback_enabled': self.fallback_enabled,
            'debug_export_enabled': self.export_debug_info,
            'debug_output_dir': str(self.debug_output_dir)
        }
    
    def enable_fallback(self, enabled: bool = True) -> None:
        """Enable or disable fallback to existing system."""
        self.fallback_enabled = enabled
        self.logger.info(f"Fallback {'enabled' if enabled else 'disabled'}")
    
    def enable_debug_export(self, enabled: bool = True) -> None:
        """Enable or disable debug information export."""
        self.export_debug_info = enabled
        if enabled:
            self.debug_output_dir.mkdir(exist_ok=True)
        self.logger.info(f"Debug export {'enabled' if enabled else 'disabled'}")
    
    def set_debug_output_dir(self, output_dir: str) -> None:
        """Set debug output directory."""
        self.debug_output_dir = Path(output_dir)
        if self.export_debug_info:
            self.debug_output_dir.mkdir(exist_ok=True)
        self.logger.info(f"Debug output directory set to: {self.debug_output_dir}")
