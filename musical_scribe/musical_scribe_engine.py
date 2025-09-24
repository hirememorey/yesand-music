"""
Musical Scribe Engine

Main orchestrator for the Musical Scribe architecture.
Coordinates project parsing, context analysis, prompt building, and LLM integration
to provide contextually appropriate musical enhancements.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from .project_state_parser import ProjectStateParser, ProjectState
from .musical_context_engine import MusicalContextEngine, MusicalContext
from .contextual_prompt_builder import ContextualPromptBuilder, ContextualPrompt


@dataclass
class MIDIPattern:
    """Represents a generated MIDI pattern."""
    name: str
    description: str
    midi_data: List[Dict[str, Any]]
    confidence_score: float
    enhancement_type: str
    musical_justification: str


@dataclass
class MusicalScribeResult:
    """Result of Musical Scribe enhancement."""
    success: bool
    patterns: List[MIDIPattern]
    project_context: str
    musical_analysis: str
    enhancement_opportunities: str
    confidence_score: float
    error_message: Optional[str] = None


class MusicalScribeEngine:
    """
    Main orchestrator for the Musical Scribe architecture.
    
    This is the core engine that coordinates all Musical Scribe components
    to provide contextually appropriate musical enhancements, inspired by
    Sully.ai's medical scribe model.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Musical Scribe Engine.
        
        Args:
            openai_api_key: OpenAI API key for LLM integration
        """
        self.project_parser = ProjectStateParser()
        self.context_engine = MusicalContextEngine()
        self.prompt_builder = ContextualPromptBuilder()
        self.openai_api_key = openai_api_key
        
        # Initialize LLM client if API key is provided
        self.llm_client = None
        if openai_api_key:
            try:
                from musical_conversation_engine import MusicalConversationEngine
                self.llm_client = MusicalConversationEngine(api_key=openai_api_key)
            except ImportError:
                logging.warning("MusicalConversationEngine not available. LLM features will be limited.")
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def enhance_music(self, project_path: str, user_request: str) -> MusicalScribeResult:
        """
        Main entry point for Musical Scribe enhancement.
        
        This is the core workflow that:
        1. Parses the entire DAW project
        2. Analyzes musical context
        3. Builds contextual prompts
        4. Generates enhanced MIDI patterns
        
        Args:
            project_path: Path to the DAW project
            user_request: User's enhancement request
            
        Returns:
            MusicalScribeResult: Complete enhancement result
        """
        try:
            self.logger.info(f"Starting Musical Scribe enhancement for project: {project_path}")
            self.logger.info(f"User request: {user_request}")
            
            # Step 1: Parse entire project state
            self.logger.info("Step 1: Parsing project state...")
            project_state = self.project_parser.parse_project(project_path)
            self.logger.info(f"Parsed project with {len(project_state.tracks)} tracks")
            
            # Step 2: Analyze musical context
            self.logger.info("Step 2: Analyzing musical context...")
            musical_context = self.context_engine.analyze_project_context(project_state)
            self.logger.info(f"Musical coherence score: {musical_context.musical_coherence_score:.2f}")
            
            # Step 3: Build contextual prompt
            self.logger.info("Step 3: Building contextual prompt...")
            contextual_prompt = self.prompt_builder.build_enhancement_prompt(
                project_state, musical_context, user_request
            )
            self.logger.info(f"Selected role: {contextual_prompt.role.name}")
            self.logger.info(f"Prompt confidence: {contextual_prompt.confidence_score:.2f}")
            
            # Step 4: Generate enhanced MIDI patterns
            self.logger.info("Step 4: Generating enhanced MIDI patterns...")
            patterns = self._generate_enhanced_patterns(contextual_prompt, musical_context)
            self.logger.info(f"Generated {len(patterns)} MIDI patterns")
            
            # Step 5: Build result
            result = MusicalScribeResult(
                success=True,
                patterns=patterns,
                project_context=contextual_prompt.project_context,
                musical_analysis=contextual_prompt.musical_analysis,
                enhancement_opportunities=contextual_prompt.enhancement_opportunities,
                confidence_score=contextual_prompt.confidence_score
            )
            
            self.logger.info("Musical Scribe enhancement completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Musical Scribe enhancement failed: {str(e)}")
            return MusicalScribeResult(
                success=False,
                patterns=[],
                project_context="",
                musical_analysis="",
                enhancement_opportunities="",
                confidence_score=0.0,
                error_message=str(e)
            )
    
    def _generate_enhanced_patterns(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate enhanced MIDI patterns using LLM or fallback methods."""
        
        if self.llm_client:
            # Use LLM for pattern generation
            return self._generate_patterns_with_llm(contextual_prompt, musical_context)
        else:
            # Use fallback pattern generation
            return self._generate_patterns_fallback(contextual_prompt, musical_context)
    
    def _generate_patterns_with_llm(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate patterns using LLM integration."""
        try:
            # Send contextual prompt to LLM
            response = self.llm_client.generate_musical_response(
                prompt=contextual_prompt.full_prompt,
                context={
                    'project_context': contextual_prompt.project_context,
                    'musical_analysis': contextual_prompt.musical_analysis,
                    'enhancement_opportunities': contextual_prompt.enhancement_opportunities,
                    'user_request': contextual_prompt.user_request
                }
            )
            
            # Parse LLM response to extract MIDI patterns
            patterns = self._parse_llm_response(response, contextual_prompt.role.name)
            
            return patterns
            
        except Exception as e:
            self.logger.warning(f"LLM pattern generation failed: {str(e)}. Falling back to rule-based generation.")
            return self._generate_patterns_fallback(contextual_prompt, musical_context)
    
    def _generate_patterns_fallback(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate patterns using rule-based fallback methods."""
        patterns = []
        
        # Generate patterns based on the musical role
        role_name = contextual_prompt.role.name.lower()
        
        if 'bassist' in role_name:
            patterns = self._generate_bass_patterns(contextual_prompt, musical_context)
        elif 'drummer' in role_name:
            patterns = self._generate_drum_patterns(contextual_prompt, musical_context)
        elif 'pianist' in role_name:
            patterns = self._generate_piano_patterns(contextual_prompt, musical_context)
        elif 'producer' in role_name:
            patterns = self._generate_production_enhancements(contextual_prompt, musical_context)
        elif 'arranger' in role_name:
            patterns = self._generate_arrangement_enhancements(contextual_prompt, musical_context)
        elif 'composer' in role_name:
            patterns = self._generate_composition_enhancements(contextual_prompt, musical_context)
        else:
            # Default to general enhancement
            patterns = self._generate_general_enhancements(contextual_prompt, musical_context)
        
        return patterns
    
    def _parse_llm_response(self, response: str, role_name: str) -> List[MIDIPattern]:
        """Parse LLM response to extract MIDI patterns."""
        patterns = []
        
        try:
            # Try to parse as JSON first
            if response.strip().startswith('{') or response.strip().startswith('['):
                data = json.loads(response)
                if isinstance(data, list):
                    for item in data:
                        pattern = self._create_pattern_from_dict(item, role_name)
                        if pattern:
                            patterns.append(pattern)
                elif isinstance(data, dict):
                    pattern = self._create_pattern_from_dict(data, role_name)
                    if pattern:
                        patterns.append(pattern)
            else:
                # Parse text response for MIDI patterns
                patterns = self._parse_text_response(response, role_name)
                
        except json.JSONDecodeError:
            # Fallback to text parsing
            patterns = self._parse_text_response(response, role_name)
        
        return patterns
    
    def _create_pattern_from_dict(self, data: Dict[str, Any], role_name: str) -> Optional[MIDIPattern]:
        """Create MIDIPattern from dictionary data."""
        try:
            return MIDIPattern(
                name=data.get('name', f'{role_name} Pattern'),
                description=data.get('description', 'Generated pattern'),
                midi_data=data.get('midi_data', []),
                confidence_score=data.get('confidence_score', 0.7),
                enhancement_type=data.get('enhancement_type', 'general'),
                musical_justification=data.get('musical_justification', 'Generated by Musical Scribe')
            )
        except Exception as e:
            self.logger.warning(f"Failed to create pattern from dict: {str(e)}")
            return None
    
    def _parse_text_response(self, response: str, role_name: str) -> List[MIDIPattern]:
        """Parse text response for MIDI patterns (fallback)."""
        # This is a simplified text parser
        # In practice, this would need more sophisticated parsing
        patterns = []
        
        # Create a basic pattern based on the role
        if 'bassist' in role_name.lower():
            patterns.append(self._create_basic_bass_pattern())
        elif 'drummer' in role_name.lower():
            patterns.append(self._create_basic_drum_pattern())
        elif 'pianist' in role_name.lower():
            patterns.append(self._create_basic_piano_pattern())
        else:
            patterns.append(self._create_basic_general_pattern())
        
        return patterns
    
    def _generate_bass_patterns(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate bass line patterns."""
        patterns = []
        
        # Simple bass pattern
        simple_bass = self._create_simple_bass_pattern(musical_context)
        patterns.append(simple_bass)
        
        # Complex bass pattern
        complex_bass = self._create_complex_bass_pattern(musical_context)
        patterns.append(complex_bass)
        
        return patterns
    
    def _generate_drum_patterns(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate drum patterns."""
        patterns = []
        
        # Basic drum pattern
        basic_drums = self._create_basic_drum_pattern(musical_context)
        patterns.append(basic_drums)
        
        # Advanced drum pattern
        advanced_drums = self._create_advanced_drum_pattern(musical_context)
        patterns.append(advanced_drums)
        
        return patterns
    
    def _generate_piano_patterns(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate piano patterns."""
        patterns = []
        
        # Simple piano pattern
        simple_piano = self._create_simple_piano_pattern(musical_context)
        patterns.append(simple_piano)
        
        # Complex piano pattern
        complex_piano = self._create_complex_piano_pattern(musical_context)
        patterns.append(complex_piano)
        
        return patterns
    
    def _generate_production_enhancements(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate production enhancement suggestions."""
        patterns = []
        
        # This would generate production-focused enhancements
        # For now, return general patterns
        general_pattern = self._create_basic_general_pattern()
        patterns.append(general_pattern)
        
        return patterns
    
    def _generate_arrangement_enhancements(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate arrangement enhancements."""
        patterns = []
        
        # This would generate arrangement-focused enhancements
        # For now, return general patterns
        general_pattern = self._create_basic_general_pattern()
        patterns.append(general_pattern)
        
        return patterns
    
    def _generate_composition_enhancements(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate composition enhancements."""
        patterns = []
        
        # This would generate composition-focused enhancements
        # For now, return general patterns
        general_pattern = self._create_basic_general_pattern()
        patterns.append(general_pattern)
        
        return patterns
    
    def _generate_general_enhancements(
        self, 
        contextual_prompt: ContextualPrompt, 
        musical_context: MusicalContext
    ) -> List[MIDIPattern]:
        """Generate general enhancements."""
        patterns = []
        
        general_pattern = self._create_basic_general_pattern()
        patterns.append(general_pattern)
        
        return patterns
    
    # Pattern creation methods (simplified implementations)
    
    def _create_basic_bass_pattern(self) -> MIDIPattern:
        """Create a basic bass pattern."""
        return MIDIPattern(
            name="Basic Bass Pattern",
            description="Simple bass line with root notes",
            midi_data=[
                {'pitch': 36, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 36, 'velocity': 80, 'start_time': 1.0, 'duration': 0.5},
                {'pitch': 36, 'velocity': 80, 'start_time': 2.0, 'duration': 0.5},
                {'pitch': 36, 'velocity': 80, 'start_time': 3.0, 'duration': 0.5}
            ],
            confidence_score=0.8,
            enhancement_type="bass_line",
            musical_justification="Provides solid rhythmic foundation with root notes"
        )
    
    def _create_simple_bass_pattern(self, musical_context: MusicalContext) -> MIDIPattern:
        """Create a simple bass pattern based on musical context."""
        # This would analyze the musical context to create appropriate bass patterns
        return self._create_basic_bass_pattern()
    
    def _create_complex_bass_pattern(self, musical_context: MusicalContext) -> MIDIPattern:
        """Create a complex bass pattern based on musical context."""
        # This would create more sophisticated bass patterns
        return MIDIPattern(
            name="Complex Bass Pattern",
            description="Advanced bass line with chord tones and rhythm variations",
            midi_data=[
                {'pitch': 36, 'velocity': 85, 'start_time': 0.0, 'duration': 0.25},
                {'pitch': 40, 'velocity': 80, 'start_time': 0.5, 'duration': 0.25},
                {'pitch': 36, 'velocity': 85, 'start_time': 1.0, 'duration': 0.25},
                {'pitch': 43, 'velocity': 80, 'start_time': 1.5, 'duration': 0.25},
                {'pitch': 36, 'velocity': 85, 'start_time': 2.0, 'duration': 0.25},
                {'pitch': 40, 'velocity': 80, 'start_time': 2.5, 'duration': 0.25},
                {'pitch': 36, 'velocity': 85, 'start_time': 3.0, 'duration': 0.25},
                {'pitch': 43, 'velocity': 80, 'start_time': 3.5, 'duration': 0.25}
            ],
            confidence_score=0.7,
            enhancement_type="bass_line",
            musical_justification="Adds harmonic interest with chord tones and rhythmic variation"
        )
    
    def _create_basic_drum_pattern(self) -> MIDIPattern:
        """Create a basic drum pattern."""
        return MIDIPattern(
            name="Basic Drum Pattern",
            description="Simple 4/4 drum pattern",
            midi_data=[
                {'pitch': 36, 'velocity': 100, 'start_time': 0.0, 'duration': 0.1},  # Kick
                {'pitch': 38, 'velocity': 80, 'start_time': 0.5, 'duration': 0.1},   # Snare
                {'pitch': 36, 'velocity': 100, 'start_time': 1.0, 'duration': 0.1},  # Kick
                {'pitch': 38, 'velocity': 80, 'start_time': 1.5, 'duration': 0.1},   # Snare
                {'pitch': 36, 'velocity': 100, 'start_time': 2.0, 'duration': 0.1},  # Kick
                {'pitch': 38, 'velocity': 80, 'start_time': 2.5, 'duration': 0.1},   # Snare
                {'pitch': 36, 'velocity': 100, 'start_time': 3.0, 'duration': 0.1},  # Kick
                {'pitch': 38, 'velocity': 80, 'start_time': 3.5, 'duration': 0.1}    # Snare
            ],
            confidence_score=0.9,
            enhancement_type="drum_pattern",
            musical_justification="Provides solid rhythmic foundation with kick and snare"
        )
    
    def _create_advanced_drum_pattern(self, musical_context: MusicalContext) -> MIDIPattern:
        """Create an advanced drum pattern."""
        return MIDIPattern(
            name="Advanced Drum Pattern",
            description="Complex drum pattern with fills and variations",
            midi_data=[
                {'pitch': 36, 'velocity': 100, 'start_time': 0.0, 'duration': 0.1},  # Kick
                {'pitch': 42, 'velocity': 60, 'start_time': 0.25, 'duration': 0.1},  # Hi-hat
                {'pitch': 38, 'velocity': 80, 'start_time': 0.5, 'duration': 0.1},   # Snare
                {'pitch': 42, 'velocity': 60, 'start_time': 0.75, 'duration': 0.1},  # Hi-hat
                {'pitch': 36, 'velocity': 100, 'start_time': 1.0, 'duration': 0.1},  # Kick
                {'pitch': 42, 'velocity': 60, 'start_time': 1.25, 'duration': 0.1},  # Hi-hat
                {'pitch': 38, 'velocity': 80, 'start_time': 1.5, 'duration': 0.1},   # Snare
                {'pitch': 42, 'velocity': 60, 'start_time': 1.75, 'duration': 0.1},  # Hi-hat
                {'pitch': 36, 'velocity': 100, 'start_time': 2.0, 'duration': 0.1},  # Kick
                {'pitch': 42, 'velocity': 60, 'start_time': 2.25, 'duration': 0.1},  # Hi-hat
                {'pitch': 38, 'velocity': 80, 'start_time': 2.5, 'duration': 0.1},   # Snare
                {'pitch': 42, 'velocity': 60, 'start_time': 2.75, 'duration': 0.1},  # Hi-hat
                {'pitch': 36, 'velocity': 100, 'start_time': 3.0, 'duration': 0.1},  # Kick
                {'pitch': 42, 'velocity': 60, 'start_time': 3.25, 'duration': 0.1},  # Hi-hat
                {'pitch': 38, 'velocity': 80, 'start_time': 3.5, 'duration': 0.1},   # Snare
                {'pitch': 42, 'velocity': 60, 'start_time': 3.75, 'duration': 0.1}   # Hi-hat
            ],
            confidence_score=0.8,
            enhancement_type="drum_pattern",
            musical_justification="Adds rhythmic complexity with hi-hat patterns and consistent groove"
        )
    
    def _create_simple_piano_pattern(self, musical_context: MusicalContext) -> MIDIPattern:
        """Create a simple piano pattern."""
        return MIDIPattern(
            name="Simple Piano Pattern",
            description="Basic piano chord progression",
            midi_data=[
                {'pitch': 60, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},  # C
                {'pitch': 64, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},  # E
                {'pitch': 67, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},  # G
                {'pitch': 57, 'velocity': 70, 'start_time': 1.0, 'duration': 1.0},  # A
                {'pitch': 60, 'velocity': 70, 'start_time': 1.0, 'duration': 1.0},  # C
                {'pitch': 64, 'velocity': 70, 'start_time': 1.0, 'duration': 1.0},  # E
                {'pitch': 62, 'velocity': 70, 'start_time': 2.0, 'duration': 1.0},  # D
                {'pitch': 65, 'velocity': 70, 'start_time': 2.0, 'duration': 1.0},  # F
                {'pitch': 69, 'velocity': 70, 'start_time': 2.0, 'duration': 1.0},  # A
                {'pitch': 59, 'velocity': 70, 'start_time': 3.0, 'duration': 1.0},  # B
                {'pitch': 62, 'velocity': 70, 'start_time': 3.0, 'duration': 1.0},  # D
                {'pitch': 67, 'velocity': 70, 'start_time': 3.0, 'duration': 1.0}   # G
            ],
            confidence_score=0.8,
            enhancement_type="piano_chords",
            musical_justification="Provides harmonic foundation with basic chord progression"
        )
    
    def _create_complex_piano_pattern(self, musical_context: MusicalContext) -> MIDIPattern:
        """Create a complex piano pattern."""
        return MIDIPattern(
            name="Complex Piano Pattern",
            description="Advanced piano with melody and harmony",
            midi_data=[
                # This would be a more sophisticated piano pattern
                {'pitch': 60, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},
                {'pitch': 64, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},
                {'pitch': 67, 'velocity': 70, 'start_time': 0.0, 'duration': 1.0},
                {'pitch': 72, 'velocity': 80, 'start_time': 0.5, 'duration': 0.5}  # Melody note
            ],
            confidence_score=0.7,
            enhancement_type="piano_melody",
            musical_justification="Combines harmonic support with melodic interest"
        )
    
    def _create_basic_general_pattern(self) -> MIDIPattern:
        """Create a basic general pattern."""
        return MIDIPattern(
            name="General Enhancement",
            description="Basic musical enhancement pattern",
            midi_data=[
                {'pitch': 60, 'velocity': 70, 'start_time': 0.0, 'duration': 0.5},
                {'pitch': 64, 'velocity': 70, 'start_time': 0.5, 'duration': 0.5},
                {'pitch': 67, 'velocity': 70, 'start_time': 1.0, 'duration': 0.5},
                {'pitch': 72, 'velocity': 70, 'start_time': 1.5, 'duration': 0.5}
            ],
            confidence_score=0.6,
            enhancement_type="general",
            musical_justification="Provides basic musical enhancement"
        )
    
    def export_result(self, result: MusicalScribeResult, output_path: str) -> None:
        """Export Musical Scribe result to JSON file."""
        result_dict = {
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
            'error_message': result.error_message
        }
        
        with open(output_path, 'w') as f:
            json.dump(result_dict, f, indent=2)
    
    def get_supported_daws(self) -> List[str]:
        """Get list of supported DAWs."""
        return self.project_parser.supported_daws
    
    def is_llm_available(self) -> bool:
        """Check if LLM integration is available."""
        return self.llm_client is not None
