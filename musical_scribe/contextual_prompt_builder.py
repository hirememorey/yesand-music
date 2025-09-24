"""
Contextual Prompt Builder

Builds specialized musical prompts for contextual enhancement, inspired by Sully.ai's medical scribe model.
Creates prompts that understand the full musical context and generate appropriate enhancements.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .project_state_parser import ProjectState
from .musical_context_engine import MusicalContext


@dataclass
class MusicalRole:
    """Defines a musical role for contextual enhancement."""
    name: str
    description: str
    expertise_areas: List[str]
    prompt_template: str
    enhancement_focus: List[str]


@dataclass
class ContextualPrompt:
    """A specialized prompt for musical enhancement."""
    role: MusicalRole
    project_context: str
    musical_analysis: str
    enhancement_opportunities: str
    user_request: str
    full_prompt: str
    confidence_score: float


class ContextualPromptBuilder:
    """
    Builds specialized musical prompts for contextual enhancement.
    
    This is the key innovation inspired by Sully.ai's medical scribe model:
    instead of generic musical generation, we create context-specific prompts
    that understand the entire musical project and generate appropriate enhancements.
    """
    
    def __init__(self):
        self.musical_roles = self._initialize_musical_roles()
        self.prompt_templates = self._initialize_prompt_templates()
    
    def build_enhancement_prompt(
        self, 
        project_state: ProjectState, 
        musical_context: MusicalContext, 
        user_request: str
    ) -> ContextualPrompt:
        """
        Build a specialized prompt for musical enhancement.
        
        Args:
            project_state: Complete project state
            musical_context: Musical context analysis
            user_request: User's enhancement request
            
        Returns:
            ContextualPrompt: Specialized prompt for LLM
        """
        # Determine the appropriate musical role
        role = self._determine_musical_role(user_request, musical_context)
        
        # Build project context description
        project_context = self._build_project_context(project_state, musical_context)
        
        # Build musical analysis description
        musical_analysis = self._build_musical_analysis(musical_context)
        
        # Build enhancement opportunities description
        enhancement_opportunities = self._build_enhancement_opportunities(musical_context)
        
        # Build the full contextual prompt
        full_prompt = self._build_full_prompt(
            role, project_context, musical_analysis, enhancement_opportunities, user_request
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            project_state, musical_context, user_request
        )
        
        return ContextualPrompt(
            role=role,
            project_context=project_context,
            musical_analysis=musical_analysis,
            enhancement_opportunities=enhancement_opportunities,
            user_request=user_request,
            full_prompt=full_prompt,
            confidence_score=confidence_score
        )
    
    def _initialize_musical_roles(self) -> Dict[str, MusicalRole]:
        """Initialize available musical roles for contextual enhancement."""
        return {
            'bassist': MusicalRole(
                name='Expert Bassist',
                description='Professional bassist specializing in foundational rhythm and harmony',
                expertise_areas=['rhythm', 'harmony', 'groove', 'foundation'],
                prompt_template='bassist_enhancement',
                enhancement_focus=['bass_line', 'rhythmic_foundation', 'harmonic_support']
            ),
            'drummer': MusicalRole(
                name='Expert Drummer',
                description='Professional drummer specializing in rhythm and groove',
                expertise_areas=['rhythm', 'groove', 'timing', 'dynamics'],
                prompt_template='drummer_enhancement',
                enhancement_focus=['drum_patterns', 'rhythmic_groove', 'dynamic_control']
            ),
            'pianist': MusicalRole(
                name='Expert Pianist',
                description='Professional pianist specializing in harmony and melody',
                expertise_areas=['harmony', 'melody', 'voicing', 'arrangement'],
                prompt_template='pianist_enhancement',
                enhancement_focus=['chord_voicings', 'melodic_lines', 'harmonic_progression']
            ),
            'producer': MusicalRole(
                name='Expert Producer',
                description='Professional music producer specializing in arrangement and production',
                expertise_areas=['arrangement', 'production', 'mixing', 'overall_vision'],
                prompt_template='producer_enhancement',
                enhancement_focus=['arrangement', 'production_quality', 'musical_coherence']
            ),
            'arranger': MusicalRole(
                name='Expert Arranger',
                description='Professional arranger specializing in musical structure and orchestration',
                expertise_areas=['arrangement', 'orchestration', 'structure', 'instrumentation'],
                prompt_template='arranger_enhancement',
                enhancement_focus=['musical_structure', 'instrumentation', 'arrangement_balance']
            ),
            'composer': MusicalRole(
                name='Expert Composer',
                description='Professional composer specializing in musical composition and development',
                expertise_areas=['composition', 'melody', 'harmony', 'musical_development'],
                prompt_template='composer_enhancement',
                enhancement_focus=['melodic_development', 'harmonic_progression', 'musical_ideas']
            )
        }
    
    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize prompt templates for different musical roles."""
        return {
            'bassist_enhancement': """
You are an expert bassist brought in to enhance this musical project. Your role is to provide foundational rhythm and harmonic support that complements the existing arrangement.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert bassist, please generate 2-3 different bass line options that:
1. Provide solid rhythmic foundation for the track
2. Support the harmonic progression appropriately
3. Complement the existing musical elements
4. Enhance the overall groove and feel
5. Fit the musical style and complexity level

Consider the existing arrangement density, tempo, and musical style when creating your bass lines. Each option should offer a different approach (e.g., simple vs. complex, different rhythmic patterns, different harmonic approaches).

Please provide your bass lines as MIDI patterns with clear explanations of your musical choices and how they enhance the track.
""",
            
            'drummer_enhancement': """
You are an expert drummer brought in to enhance this musical project. Your role is to provide rhythmic foundation and groove that drives the music forward.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert drummer, please generate 2-3 different drum pattern options that:
1. Provide solid rhythmic foundation
2. Enhance the groove and feel of the track
3. Support the musical style and tempo
4. Complement the existing musical elements
5. Add appropriate dynamic variation

Consider the existing arrangement, musical style, and complexity level when creating your drum patterns. Each option should offer a different approach (e.g., simple vs. complex, different groove styles, different dynamic approaches).

Please provide your drum patterns as MIDI patterns with clear explanations of your musical choices and how they enhance the track.
""",
            
            'pianist_enhancement': """
You are an expert pianist brought in to enhance this musical project. Your role is to provide harmonic support and melodic interest that enriches the musical arrangement.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert pianist, please generate 2-3 different piano part options that:
1. Provide harmonic support for the track
2. Add melodic interest and musical development
3. Complement the existing musical elements
4. Enhance the overall musical coherence
5. Fit the musical style and complexity level

Consider the existing harmony, melody, and arrangement when creating your piano parts. Each option should offer a different approach (e.g., simple vs. complex, different harmonic voicings, different melodic approaches).

Please provide your piano parts as MIDI patterns with clear explanations of your musical choices and how they enhance the track.
""",
            
            'producer_enhancement': """
You are an expert music producer brought in to enhance this musical project. Your role is to improve the overall production quality and musical coherence of the arrangement.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert producer, please provide 2-3 different enhancement options that:
1. Improve the overall musical coherence
2. Enhance the arrangement and structure
3. Address any weak areas in the production
4. Add missing musical elements
5. Improve the overall musical impact

Consider the entire musical context when making your recommendations. Each option should focus on different aspects (e.g., arrangement, harmony, rhythm, production quality).

Please provide your enhancements as specific recommendations with clear explanations of your production choices and how they improve the track.
""",
            
            'arranger_enhancement': """
You are an expert arranger brought in to enhance this musical project. Your role is to improve the musical structure, instrumentation, and overall arrangement.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert arranger, please provide 2-3 different arrangement enhancement options that:
1. Improve the musical structure and flow
2. Enhance the instrumentation and balance
3. Add appropriate musical elements
4. Improve the overall musical coherence
5. Create more engaging musical development

Consider the existing arrangement, musical style, and complexity level when making your recommendations. Each option should focus on different aspects (e.g., structure, instrumentation, musical development).

Please provide your arrangement enhancements as specific recommendations with clear explanations of your musical choices and how they improve the track.
""",
            
            'composer_enhancement': """
You are an expert composer brought in to enhance this musical project. Your role is to develop musical ideas and create compelling musical content that enhances the overall composition.

PROJECT CONTEXT:
{project_context}

MUSICAL ANALYSIS:
{musical_analysis}

ENHANCEMENT OPPORTUNITIES:
{enhancement_opportunities}

CLIENT REQUEST: {user_request}

As an expert composer, please provide 2-3 different compositional enhancement options that:
1. Develop and expand musical ideas
2. Create compelling melodic and harmonic content
3. Enhance the overall musical narrative
4. Add musical interest and development
5. Improve the overall musical impact

Consider the existing musical content, style, and complexity level when creating your enhancements. Each option should offer different musical approaches (e.g., melodic development, harmonic progression, musical structure).

Please provide your compositional enhancements as specific recommendations with clear explanations of your musical choices and how they improve the track.
"""
        }
    
    def _determine_musical_role(self, user_request: str, musical_context: MusicalContext) -> MusicalRole:
        """Determine the appropriate musical role based on user request and context."""
        request_lower = user_request.lower()
        
        # Check for specific role indicators in the request
        if any(word in request_lower for word in ['bass', 'bassline', 'bass line']):
            return self.musical_roles['bassist']
        elif any(word in request_lower for word in ['drum', 'percussion', 'rhythm', 'groove']):
            return self.musical_roles['drummer']
        elif any(word in request_lower for word in ['piano', 'keyboard', 'chord', 'harmony']):
            return self.musical_roles['pianist']
        elif any(word in request_lower for word in ['arrange', 'arrangement', 'structure', 'orchestrate']):
            return self.musical_roles['arranger']
        elif any(word in request_lower for word in ['compose', 'composition', 'melody', 'musical idea']):
            return self.musical_roles['composer']
        elif any(word in request_lower for word in ['produce', 'production', 'mix', 'overall']):
            return self.musical_roles['producer']
        
        # Default based on enhancement opportunities
        opportunities = musical_context.enhancement_opportunities
        if 'bass_line' in opportunities.missing_elements:
            return self.musical_roles['bassist']
        elif 'rhythm_section' in opportunities.missing_elements:
            return self.musical_roles['drummer']
        elif 'melody' in opportunities.missing_elements:
            return self.musical_roles['composer']
        elif 'arrangement' in opportunities.weak_areas:
            return self.musical_roles['arranger']
        else:
            return self.musical_roles['producer']
    
    def _build_project_context(self, project_state: ProjectState, musical_context: MusicalContext) -> str:
        """Build a comprehensive project context description."""
        context_parts = []
        
        # Basic project information
        project_info = project_state.project_info
        context_parts.append(f"Project: {project_info.name}")
        context_parts.append(f"Tempo: {project_info.tempo} BPM")
        context_parts.append(f"Time Signature: {project_info.time_signature}")
        context_parts.append(f"Sample Rate: {project_info.sample_rate} Hz")
        
        # Track information
        context_parts.append(f"Total Tracks: {len(project_state.tracks)}")
        context_parts.append(f"MIDI Tracks: {musical_context.arrangement_analysis.instrumental_balance.get('midi', 0):.1%}")
        context_parts.append(f"Audio Tracks: {musical_context.arrangement_analysis.instrumental_balance.get('audio', 0):.1%}")
        
        # Track details
        track_descriptions = []
        for track in project_state.tracks:
            track_desc = f"- {track.name} ({track.track_type})"
            if track.musical_analysis:
                analysis = track.musical_analysis
                if analysis.get('has_midi_content'):
                    track_desc += f" - {analysis.get('note_count', 0)} notes, {analysis.get('density', 'unknown')} density"
                if analysis.get('has_audio_content'):
                    track_desc += " - Audio content"
            track_descriptions.append(track_desc)
        
        if track_descriptions:
            context_parts.append("Tracks:")
            context_parts.extend(track_descriptions)
        
        # Project duration
        duration = project_state.musical_context.get('project_duration', 0)
        if duration > 0:
            context_parts.append(f"Duration: {duration:.1f} seconds")
        
        return "\n".join(context_parts)
    
    def _build_musical_analysis(self, musical_context: MusicalContext) -> str:
        """Build a comprehensive musical analysis description."""
        analysis_parts = []
        
        # Harmonic analysis
        harmonic = musical_context.harmonic_analysis
        analysis_parts.append("HARMONIC ANALYSIS:")
        analysis_parts.append(f"- Key: {harmonic.key_signature or 'Unknown'}")
        analysis_parts.append(f"- Chord Progression: {', '.join(harmonic.chord_progression) if harmonic.chord_progression else 'None detected'}")
        analysis_parts.append(f"- Harmonic Rhythm: {harmonic.harmonic_rhythm}")
        analysis_parts.append(f"- Voice Leading: {harmonic.voice_leading_quality}")
        analysis_parts.append(f"- Dissonance Level: {harmonic.dissonance_level}")
        analysis_parts.append(f"- Harmonic Complexity: {harmonic.harmonic_complexity}")
        
        # Rhythmic analysis
        rhythmic = musical_context.rhythmic_analysis
        analysis_parts.append("\nRHYTHMIC ANALYSIS:")
        analysis_parts.append(f"- Time Signature: {rhythmic.primary_time_signature}")
        analysis_parts.append(f"- Tempo Consistency: {rhythmic.tempo_consistency}")
        analysis_parts.append(f"- Swing Feel: {rhythmic.swing_feel}")
        analysis_parts.append(f"- Syncopation Level: {rhythmic.syncopation_level}")
        analysis_parts.append(f"- Groove Quality: {rhythmic.groove_quality}")
        analysis_parts.append(f"- Rhythmic Density: {rhythmic.rhythmic_density}")
        
        # Arrangement analysis
        arrangement = musical_context.arrangement_analysis
        analysis_parts.append("\nARRANGEMENT ANALYSIS:")
        analysis_parts.append(f"- Overall Density: {arrangement.overall_density}")
        analysis_parts.append(f"- Dynamic Range: {arrangement.dynamic_range}")
        analysis_parts.append(f"- Frequency Balance: {arrangement.frequency_balance}")
        analysis_parts.append(f"- Arrangement Complexity: {arrangement.arrangement_complexity}")
        analysis_parts.append(f"- Section Transitions: {arrangement.section_transitions}")
        
        # Style analysis
        style = musical_context.style_analysis
        analysis_parts.append("\nSTYLE ANALYSIS:")
        analysis_parts.append(f"- Primary Genre: {style.primary_genre}")
        if style.secondary_genres:
            analysis_parts.append(f"- Secondary Genres: {', '.join(style.secondary_genres)}")
        analysis_parts.append(f"- Production Style: {style.production_style}")
        analysis_parts.append(f"- Complexity Level: {style.complexity_level}")
        if style.mood_characteristics:
            analysis_parts.append(f"- Mood: {', '.join(style.mood_characteristics)}")
        
        # Musical coherence
        coherence_score = musical_context.musical_coherence_score
        analysis_parts.append(f"\nMUSICAL COHERENCE: {coherence_score:.2f}/1.0")
        
        return "\n".join(analysis_parts)
    
    def _build_enhancement_opportunities(self, musical_context: MusicalContext) -> str:
        """Build a description of enhancement opportunities."""
        opportunities = musical_context.enhancement_opportunities
        
        opp_parts = []
        
        if opportunities.missing_elements:
            opp_parts.append("MISSING ELEMENTS:")
            for element in opportunities.missing_elements:
                opp_parts.append(f"- {element.replace('_', ' ').title()}")
        
        if opportunities.weak_areas:
            opp_parts.append("\nWEAK AREAS:")
            for area in opportunities.weak_areas:
                opp_parts.append(f"- {area.replace('_', ' ').title()}")
        
        if opportunities.enhancement_suggestions:
            opp_parts.append("\nENHANCEMENT SUGGESTIONS:")
            for suggestion in opportunities.enhancement_suggestions:
                opp_parts.append(f"- {suggestion}")
        
        opp_parts.append(f"\nPRIORITY LEVEL: {opportunities.priority_level.upper()}")
        opp_parts.append(f"CONFIDENCE SCORE: {opportunities.confidence_score:.2f}/1.0")
        
        return "\n".join(opp_parts)
    
    def _build_full_prompt(
        self,
        role: MusicalRole,
        project_context: str,
        musical_analysis: str,
        enhancement_opportunities: str,
        user_request: str
    ) -> str:
        """Build the complete contextual prompt."""
        template = self.prompt_templates[role.prompt_template]
        
        return template.format(
            project_context=project_context,
            musical_analysis=musical_analysis,
            enhancement_opportunities=enhancement_opportunities,
            user_request=user_request
        )
    
    def _calculate_confidence_score(
        self,
        project_state: ProjectState,
        musical_context: MusicalContext,
        user_request: str
    ) -> float:
        """Calculate confidence score for the prompt."""
        confidence_factors = []
        
        # Project completeness factor
        if project_state.tracks:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.2)
        
        # Musical context richness factor
        if musical_context.musical_coherence_score > 0.7:
            confidence_factors.append(0.9)
        elif musical_context.musical_coherence_score > 0.4:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.3)
        
        # Enhancement opportunities clarity factor
        opportunities = musical_context.enhancement_opportunities
        if opportunities.enhancement_suggestions:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # User request specificity factor
        if len(user_request.split()) > 3:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.5)
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
