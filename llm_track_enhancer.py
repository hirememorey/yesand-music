"""
LLM Track Enhancement Engine

Uses OpenAI's GPT models to enhance musical tracks based on real-time project context.
Provides intelligent track enhancement suggestions and generates MIDI patterns.
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import openai
from openai import OpenAI

from project_state_capture import LiveProjectContext, EnhancementOpportunity
from midi_stream_analyzer import TrackStreamAnalysis


@dataclass
class EnhancementRequest:
    """Request for track enhancement."""
    user_request: str
    track_id: Optional[str] = None
    enhancement_type: str = "general"
    priority: int = 5
    context: Optional[LiveProjectContext] = None


@dataclass
class MIDIPattern:
    """Generated MIDI pattern."""
    name: str
    description: str
    midi_data: List[Dict[str, Any]]
    confidence_score: float
    enhancement_type: str
    musical_justification: str
    track_id: str
    duration: float
    tempo: float
    time_signature: str


@dataclass
class EnhancementResult:
    """Result of track enhancement."""
    success: bool
    patterns: List[MIDIPattern]
    enhancement_type: str
    track_id: str
    user_request: str
    musical_analysis: str
    suggestions: List[str]
    confidence: float
    processing_time: float
    error_message: Optional[str] = None


class LLMTrackEnhancer:
    """
    LLM-powered track enhancement engine.
    
    Uses OpenAI's GPT models to analyze musical context and generate
    enhanced MIDI patterns for track improvement.
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        """
        Initialize LLM track enhancer.
        
        Args:
            api_key: OpenAI API key (uses environment variable if None)
            model: OpenAI model to use
        """
        self.api_key = api_key
        self.model = model
        
        # Initialize OpenAI client
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()  # Uses OPENAI_API_KEY environment variable
        
        # Enhancement templates
        self.enhancement_templates = self._initialize_enhancement_templates()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def enhance_track(self, request: EnhancementRequest) -> EnhancementResult:
        """
        Enhance a track using LLM analysis.
        
        Args:
            request: Enhancement request with context
            
        Returns:
            EnhancementResult: Generated patterns and analysis
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting track enhancement: {request.user_request}")
            
            # Build context for LLM
            llm_context = self._build_llm_context(request)
            
            # Generate enhancement prompt
            prompt = self._build_enhancement_prompt(request, llm_context)
            
            # Call LLM
            response = self._call_llm(prompt)
            
            # Parse response
            patterns = self._parse_llm_response(response, request)
            
            # Generate musical analysis
            musical_analysis = self._generate_musical_analysis(patterns, request)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(patterns, request)
            
            # Calculate confidence
            confidence = self._calculate_confidence(patterns, request)
            
            processing_time = time.time() - start_time
            
            result = EnhancementResult(
                success=True,
                patterns=patterns,
                enhancement_type=request.enhancement_type,
                track_id=request.track_id or "unknown",
                user_request=request.user_request,
                musical_analysis=musical_analysis,
                suggestions=suggestions,
                confidence=confidence,
                processing_time=processing_time
            )
            
            self.logger.info(f"Track enhancement completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Track enhancement failed: {e}")
            processing_time = time.time() - start_time
            
            return EnhancementResult(
                success=False,
                patterns=[],
                enhancement_type=request.enhancement_type,
                track_id=request.track_id or "unknown",
                user_request=request.user_request,
                musical_analysis="",
                suggestions=[],
                confidence=0.0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def _build_llm_context(self, request: EnhancementRequest) -> Dict[str, Any]:
        """Build context for LLM from project state."""
        if not request.context:
            return {"error": "No project context available"}
        
        context = request.context
        
        # Build comprehensive context
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
            "user_request": request.user_request,
            "enhancement_type": request.enhancement_type,
            "track_id": request.track_id
        }
        
        return llm_context
    
    def _build_enhancement_prompt(self, request: EnhancementRequest, context: Dict[str, Any]) -> str:
        """Build enhancement prompt for LLM."""
        template = self.enhancement_templates.get(request.enhancement_type, 
                                                self.enhancement_templates["general"])
        
        # Format template with context
        prompt = template.format(
            project_context=json.dumps(context, indent=2),
            user_request=request.user_request,
            track_id=request.track_id or "any track",
            enhancement_type=request.enhancement_type
        )
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call OpenAI LLM with prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert music producer and session musician with deep knowledge of music theory, arrangement, and production. You help musicians enhance their tracks by providing intelligent musical suggestions and generating MIDI patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            raise
    
    def _parse_llm_response(self, response: str, request: EnhancementRequest) -> List[MIDIPattern]:
        """Parse LLM response to extract MIDI patterns."""
        patterns = []
        
        try:
            # Try to parse as JSON first
            if response.strip().startswith('{') or response.strip().startswith('['):
                data = json.loads(response)
                if isinstance(data, list):
                    for item in data:
                        pattern = self._create_pattern_from_dict(item, request)
                        if pattern:
                            patterns.append(pattern)
                elif isinstance(data, dict):
                    pattern = self._create_pattern_from_dict(data, request)
                    if pattern:
                        patterns.append(pattern)
            else:
                # Parse text response for MIDI patterns
                patterns = self._parse_text_response(response, request)
                
        except json.JSONDecodeError:
            # Fallback to text parsing
            patterns = self._parse_text_response(response, request)
        
        return patterns
    
    def _create_pattern_from_dict(self, data: Dict[str, Any], request: EnhancementRequest) -> Optional[MIDIPattern]:
        """Create MIDIPattern from dictionary data."""
        try:
            return MIDIPattern(
                name=data.get('name', f'{request.enhancement_type} Pattern'),
                description=data.get('description', 'Generated pattern'),
                midi_data=data.get('midi_data', []),
                confidence_score=data.get('confidence_score', 0.7),
                enhancement_type=request.enhancement_type,
                musical_justification=data.get('musical_justification', 'Generated by LLM'),
                track_id=request.track_id or "unknown",
                duration=data.get('duration', 4.0),
                tempo=data.get('tempo', 120.0),
                time_signature=data.get('time_signature', '4/4')
            )
        except Exception as e:
            self.logger.warning(f"Failed to create pattern from dict: {str(e)}")
            return None
    
    def _parse_text_response(self, response: str, request: EnhancementRequest) -> List[MIDIPattern]:
        """Parse text response for MIDI patterns (fallback)."""
        patterns = []
        
        # Create a basic pattern based on the enhancement type
        if request.enhancement_type == "bass":
            patterns.append(self._create_basic_bass_pattern(request))
        elif request.enhancement_type == "drums":
            patterns.append(self._create_basic_drum_pattern(request))
        elif request.enhancement_type == "melody":
            patterns.append(self._create_basic_melody_pattern(request))
        elif request.enhancement_type == "harmony":
            patterns.append(self._create_basic_harmony_pattern(request))
        else:
            patterns.append(self._create_basic_general_pattern(request))
        
        return patterns
    
    def _generate_musical_analysis(self, patterns: List[MIDIPattern], request: EnhancementRequest) -> str:
        """Generate musical analysis of the patterns."""
        if not patterns:
            return "No patterns generated for analysis."
        
        analysis_parts = []
        
        for pattern in patterns:
            analysis_parts.append(f"Pattern: {pattern.name}")
            analysis_parts.append(f"Description: {pattern.description}")
            analysis_parts.append(f"Musical Justification: {pattern.musical_justification}")
            analysis_parts.append(f"Confidence: {pattern.confidence_score:.2f}")
            analysis_parts.append(f"Duration: {pattern.duration}s")
            analysis_parts.append(f"Tempo: {pattern.tempo} BPM")
            analysis_parts.append("")
        
        return "\n".join(analysis_parts)
    
    def _generate_suggestions(self, patterns: List[MIDIPattern], request: EnhancementRequest) -> List[str]:
        """Generate suggestions based on patterns."""
        suggestions = []
        
        if not patterns:
            suggestions.append("Try a different enhancement approach")
            return suggestions
        
        # Analyze patterns for suggestions
        for pattern in patterns:
            if pattern.confidence_score < 0.6:
                suggestions.append(f"Consider refining {pattern.name} for better musical coherence")
            
            if pattern.duration < 2.0:
                suggestions.append(f"Extend {pattern.name} for longer musical phrases")
            
            if pattern.tempo < 80:
                suggestions.append(f"Increase tempo of {pattern.name} for more energy")
            elif pattern.tempo > 160:
                suggestions.append(f"Reduce tempo of {pattern.name} for better groove")
        
        # General suggestions
        if request.enhancement_type == "bass":
            suggestions.append("Consider adding walking bass lines for jazz feel")
            suggestions.append("Try syncopated rhythms for funk style")
        elif request.enhancement_type == "drums":
            suggestions.append("Add ghost notes for more realistic drum feel")
            suggestions.append("Consider adding fills at phrase endings")
        elif request.enhancement_type == "melody":
            suggestions.append("Add melodic variations to avoid repetition")
            suggestions.append("Consider call-and-response patterns")
        
        return suggestions
    
    def _calculate_confidence(self, patterns: List[MIDIPattern], request: EnhancementRequest) -> float:
        """Calculate overall confidence in the enhancement."""
        if not patterns:
            return 0.0
        
        # Average confidence of all patterns
        avg_confidence = sum(pattern.confidence_score for pattern in patterns) / len(patterns)
        
        # Adjust based on context availability
        context_factor = 1.0
        if request.context:
            context_factor = 1.2  # Boost confidence with context
        
        # Adjust based on enhancement type
        type_factor = 1.0
        if request.enhancement_type in ["bass", "drums"]:
            type_factor = 1.1  # These are well-defined enhancement types
        
        return min(avg_confidence * context_factor * type_factor, 1.0)
    
    def _initialize_enhancement_templates(self) -> Dict[str, str]:
        """Initialize enhancement prompt templates."""
        return {
            "bass": """
You are an expert bassist brought in to enhance this musical project. Your role is to provide foundational rhythm and harmonic support that complements the existing arrangement.

PROJECT CONTEXT:
{project_context}

CLIENT REQUEST: {user_request}

As an expert bassist, please generate 2-3 different bass line options that:
1. Provide solid rhythmic foundation for the track
2. Support the harmonic progression appropriately
3. Complement the existing musical elements
4. Enhance the overall groove and feel
5. Fit the musical style and complexity level

Consider the existing arrangement density, tempo, and musical style when creating your bass lines. Each option should offer a different approach (e.g., simple vs. complex, different rhythmic patterns, different harmonic approaches).

Please provide your bass lines as MIDI patterns in JSON format with the following structure:
{{
    "name": "Pattern Name",
    "description": "Description of the pattern",
    "midi_data": [
        {{"pitch": 36, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0}},
        {{"pitch": 40, "velocity": 75, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0}}
    ],
    "confidence_score": 0.8,
    "musical_justification": "Explanation of musical choices",
    "duration": 4.0,
    "tempo": 120.0,
    "time_signature": "4/4"
}}

Include clear explanations of your musical choices and how they enhance the track.
""",
            
            "drums": """
You are an expert drummer brought in to enhance this musical project. Your role is to provide rhythmic foundation and groove that drives the music forward.

PROJECT CONTEXT:
{project_context}

CLIENT REQUEST: {user_request}

As an expert drummer, please generate 2-3 different drum pattern options that:
1. Provide solid rhythmic foundation
2. Enhance the groove and feel of the track
3. Support the musical style and tempo
4. Complement the existing musical elements
5. Add appropriate dynamic variation

Consider the existing arrangement, musical style, and complexity level when creating your drum patterns. Each option should offer a different approach (e.g., simple vs. complex, different groove styles, different dynamic approaches).

Please provide your drum patterns as MIDI patterns in JSON format with the following structure:
{{
    "name": "Pattern Name",
    "description": "Description of the pattern",
    "midi_data": [
        {{"pitch": 36, "velocity": 100, "start_time_seconds": 0.0, "duration_seconds": 0.1, "track_index": 0}},
        {{"pitch": 38, "velocity": 80, "start_time_seconds": 0.5, "duration_seconds": 0.1, "track_index": 0}}
    ],
    "confidence_score": 0.8,
    "musical_justification": "Explanation of musical choices",
    "duration": 4.0,
    "tempo": 120.0,
    "time_signature": "4/4"
}}

Include clear explanations of your musical choices and how they enhance the track.
""",
            
            "melody": """
You are an expert composer brought in to enhance this musical project. Your role is to create compelling melodic content that enhances the overall musical narrative.

PROJECT CONTEXT:
{project_context}

CLIENT REQUEST: {user_request}

As an expert composer, please generate 2-3 different melodic options that:
1. Create compelling melodic content
2. Enhance the overall musical narrative
3. Complement the existing harmonic progression
4. Add musical interest and development
5. Fit the musical style and complexity level

Consider the existing harmony, rhythm, and arrangement when creating your melodies. Each option should offer different musical approaches (e.g., simple vs. complex, different melodic contours, different rhythmic approaches).

Please provide your melodies as MIDI patterns in JSON format with the following structure:
{{
    "name": "Pattern Name",
    "description": "Description of the pattern",
    "midi_data": [
        {{"pitch": 60, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0}},
        {{"pitch": 64, "velocity": 75, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0}}
    ],
    "confidence_score": 0.8,
    "musical_justification": "Explanation of musical choices",
    "duration": 4.0,
    "tempo": 120.0,
    "time_signature": "4/4"
}}

Include clear explanations of your musical choices and how they enhance the track.
""",
            
            "harmony": """
You are an expert pianist and arranger brought in to enhance this musical project. Your role is to provide harmonic support and enrichment that enhances the overall musical arrangement.

PROJECT CONTEXT:
{project_context}

CLIENT REQUEST: {user_request}

As an expert pianist, please generate 2-3 different harmonic options that:
1. Provide harmonic support for the track
2. Add harmonic interest and development
3. Complement the existing musical elements
4. Enhance the overall musical coherence
5. Fit the musical style and complexity level

Consider the existing harmony, melody, and arrangement when creating your harmonic parts. Each option should offer different approaches (e.g., simple vs. complex, different harmonic voicings, different rhythmic approaches).

Please provide your harmonic parts as MIDI patterns in JSON format with the following structure:
{{
    "name": "Pattern Name",
    "description": "Description of the pattern",
    "midi_data": [
        {{"pitch": 60, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0}},
        {{"pitch": 64, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0}},
        {{"pitch": 67, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0}}
    ],
    "confidence_score": 0.8,
    "musical_justification": "Explanation of musical choices",
    "duration": 4.0,
    "tempo": 120.0,
    "time_signature": "4/4"
}}

Include clear explanations of your musical choices and how they enhance the track.
""",
            
            "general": """
You are an expert music producer brought in to enhance this musical project. Your role is to improve the overall musical quality and coherence of the arrangement.

PROJECT CONTEXT:
{project_context}

CLIENT REQUEST: {user_request}

As an expert producer, please provide 2-3 different enhancement options that:
1. Improve the overall musical coherence
2. Enhance the arrangement and structure
3. Address any weak areas in the production
4. Add missing musical elements
5. Improve the overall musical impact

Consider the entire musical context when making your recommendations. Each option should focus on different aspects (e.g., arrangement, harmony, rhythm, production quality).

Please provide your enhancements as MIDI patterns in JSON format with the following structure:
{{
    "name": "Pattern Name",
    "description": "Description of the pattern",
    "midi_data": [
        {{"pitch": 60, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0}}
    ],
    "confidence_score": 0.8,
    "musical_justification": "Explanation of musical choices",
    "duration": 4.0,
    "tempo": 120.0,
    "time_signature": "4/4"
}}

Include clear explanations of your musical choices and how they improve the track.
"""
        }
    
    # Pattern creation methods
    
    def _create_basic_bass_pattern(self, request: EnhancementRequest) -> MIDIPattern:
        """Create a basic bass pattern."""
        return MIDIPattern(
            name="Basic Bass Pattern",
            description="Simple bass line with root notes",
            midi_data=[
                {"pitch": 36, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 36, "velocity": 80, "start_time_seconds": 1.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 36, "velocity": 80, "start_time_seconds": 2.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 36, "velocity": 80, "start_time_seconds": 3.0, "duration_seconds": 0.5, "track_index": 0}
            ],
            confidence_score=0.8,
            enhancement_type="bass",
            musical_justification="Provides solid rhythmic foundation with root notes",
            track_id=request.track_id or "unknown",
            duration=4.0,
            tempo=120.0,
            time_signature="4/4"
        )
    
    def _create_basic_drum_pattern(self, request: EnhancementRequest) -> MIDIPattern:
        """Create a basic drum pattern."""
        return MIDIPattern(
            name="Basic Drum Pattern",
            description="Simple 4/4 drum pattern",
            midi_data=[
                {"pitch": 36, "velocity": 100, "start_time_seconds": 0.0, "duration_seconds": 0.1, "track_index": 0},  # Kick
                {"pitch": 38, "velocity": 80, "start_time_seconds": 0.5, "duration_seconds": 0.1, "track_index": 0},   # Snare
                {"pitch": 36, "velocity": 100, "start_time_seconds": 1.0, "duration_seconds": 0.1, "track_index": 0},  # Kick
                {"pitch": 38, "velocity": 80, "start_time_seconds": 1.5, "duration_seconds": 0.1, "track_index": 0}    # Snare
            ],
            confidence_score=0.9,
            enhancement_type="drums",
            musical_justification="Provides solid rhythmic foundation with kick and snare",
            track_id=request.track_id or "unknown",
            duration=4.0,
            tempo=120.0,
            time_signature="4/4"
        )
    
    def _create_basic_melody_pattern(self, request: EnhancementRequest) -> MIDIPattern:
        """Create a basic melody pattern."""
        return MIDIPattern(
            name="Basic Melody Pattern",
            description="Simple melodic line",
            midi_data=[
                {"pitch": 60, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 64, "velocity": 75, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 67, "velocity": 80, "start_time_seconds": 1.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 72, "velocity": 85, "start_time_seconds": 1.5, "duration_seconds": 0.5, "track_index": 0}
            ],
            confidence_score=0.7,
            enhancement_type="melody",
            musical_justification="Provides melodic interest with ascending contour",
            track_id=request.track_id or "unknown",
            duration=4.0,
            tempo=120.0,
            time_signature="4/4"
        )
    
    def _create_basic_harmony_pattern(self, request: EnhancementRequest) -> MIDIPattern:
        """Create a basic harmony pattern."""
        return MIDIPattern(
            name="Basic Harmony Pattern",
            description="Simple chord progression",
            midi_data=[
                {"pitch": 60, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0},  # C
                {"pitch": 64, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0},  # E
                {"pitch": 67, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 1.0, "track_index": 0},  # G
                {"pitch": 57, "velocity": 70, "start_time_seconds": 1.0, "duration_seconds": 1.0, "track_index": 0},  # A
                {"pitch": 60, "velocity": 70, "start_time_seconds": 1.0, "duration_seconds": 1.0, "track_index": 0},  # C
                {"pitch": 64, "velocity": 70, "start_time_seconds": 1.0, "duration_seconds": 1.0, "track_index": 0}   # E
            ],
            confidence_score=0.8,
            enhancement_type="harmony",
            musical_justification="Provides harmonic foundation with basic chord progression",
            track_id=request.track_id or "unknown",
            duration=4.0,
            tempo=120.0,
            time_signature="4/4"
        )
    
    def _create_basic_general_pattern(self, request: EnhancementRequest) -> MIDIPattern:
        """Create a basic general pattern."""
        return MIDIPattern(
            name="General Enhancement Pattern",
            description="Basic musical enhancement pattern",
            midi_data=[
                {"pitch": 60, "velocity": 70, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 64, "velocity": 70, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 67, "velocity": 70, "start_time_seconds": 1.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 72, "velocity": 70, "start_time_seconds": 1.5, "duration_seconds": 0.5, "track_index": 0}
            ],
            confidence_score=0.6,
            enhancement_type="general",
            musical_justification="Provides basic musical enhancement",
            track_id=request.track_id or "unknown",
            duration=4.0,
            tempo=120.0,
            time_signature="4/4"
        )
