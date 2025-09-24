"""
Context-Aware Prompt Engineering System

This module provides intelligent prompt engineering for AI-powered MIDI generation,
building context-aware prompts that incorporate musical intelligence and style
characteristics for optimal AI generation results.

Key Features:
- Context-aware prompt building
- Style characteristic integration
- Musical context incorporation
- Prompt optimization and validation
- Multi-stage prompt engineering
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from musical_intelligence_engine import MusicalContext, StyleCharacteristics, MusicalMood, MusicalComplexity


@dataclass
class PromptContext:
    """Context information for prompt engineering"""
    user_prompt: str
    musical_context: MusicalContext
    style_characteristics: StyleCharacteristics
    generation_parameters: Dict[str, Any]
    session_context: Dict[str, Any]


@dataclass
class EnhancedPrompt:
    """Enhanced prompt with context and metadata"""
    original_prompt: str
    enhanced_prompt: str
    context: PromptContext
    prompt_type: str
    optimization_level: str
    expected_output_format: str


class ContextAwarePromptBuilder:
    """
    Context-Aware Prompt Builder for AI MIDI Generation
    
    Builds intelligent prompts that incorporate musical context, style
    characteristics, and user intent for optimal AI generation results.
    """
    
    def __init__(self):
        self.prompt_templates = self._initialize_prompt_templates()
        self.optimization_rules = self._initialize_optimization_rules()
        self.output_formats = self._initialize_output_formats()
        
    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize prompt templates for different generation types"""
        return {
            "bass_generation": """You are a professional bassist with expertise in {style_characteristics}. Generate a {instrument} line that matches the following request:

ORIGINAL REQUEST: "{user_prompt}"

MUSICAL CONTEXT:
- Key: {key}
- Tempo: {tempo} BPM
- Time Signature: {time_signature}
- Instrument: {instrument}
- Style: {style}
- Mood: {mood}
- Complexity: {complexity}

STYLE CHARACTERISTICS:
{style_details}

HARMONIC CONTEXT:
{harmonic_context}

RHYTHMIC CONTEXT:
{rhythmic_context}

DYNAMIC CONTEXT:
{dynamic_context}

REQUIREMENTS:
1. Generate exactly 2-4 bars of {instrument} content
2. Use the specified key ({key}) as the foundation
3. Match the tempo ({tempo} BPM) and time signature ({time_signature})
4. Incorporate the style characteristics listed above
5. Make it musically coherent and playable
6. Use appropriate note velocities for {instrument}
7. Include rhythmic variety and interest
8. Ensure the {instrument} line supports the harmonic context
9. Match the mood and complexity level specified

OUTPUT FORMAT:
Return ONLY a JSON object with this exact structure:
{{
    "notes": [
        {{
            "pitch": 36,
            "velocity": 80,
            "start_time_seconds": 0.0,
            "duration_seconds": 0.5,
            "track_index": 0
        }}
    ],
    "tempo": {tempo},
    "key": "{key}",
    "time_signature": "{time_signature}",
    "style_notes": "Brief description of how this matches the requested style",
    "musical_justification": "Brief explanation of musical choices made"
}}

Generate the {instrument} line now:""",
            
            "drum_generation": """You are a professional drummer with expertise in {style_characteristics}. Generate a {instrument} pattern that matches the following request:

ORIGINAL REQUEST: "{user_prompt}"

MUSICAL CONTEXT:
- Key: {key}
- Tempo: {tempo} BPM
- Time Signature: {time_signature}
- Instrument: {instrument}
- Style: {style}
- Mood: {mood}
- Complexity: {complexity}

STYLE CHARACTERISTICS:
{style_details}

RHYTHMIC CONTEXT:
{rhythmic_context}

DYNAMIC CONTEXT:
{dynamic_context}

REQUIREMENTS:
1. Generate exactly 2-4 bars of {instrument} content
2. Match the tempo ({tempo} BPM) and time signature ({time_signature})
3. Incorporate the style characteristics listed above
4. Make it musically coherent and playable
5. Use appropriate note velocities for {instrument}
6. Include rhythmic variety and interest
7. Match the mood and complexity level specified
8. Use standard drum mapping (kick=36, snare=38, hi-hat=42, etc.)

OUTPUT FORMAT:
Return ONLY a JSON object with this exact structure:
{{
    "notes": [
        {{
            "pitch": 36,
            "velocity": 80,
            "start_time_seconds": 0.0,
            "duration_seconds": 0.5,
            "track_index": 0
        }}
    ],
    "tempo": {tempo},
    "key": "{key}",
    "time_signature": "{time_signature}",
    "style_notes": "Brief description of how this matches the requested style",
    "musical_justification": "Brief explanation of musical choices made"
}}

Generate the {instrument} pattern now:""",
            
            "melody_generation": """You are a professional musician with expertise in {style_characteristics}. Generate a {instrument} line that matches the following request:

ORIGINAL REQUEST: "{user_prompt}"

MUSICAL CONTEXT:
- Key: {key}
- Tempo: {tempo} BPM
- Time Signature: {time_signature}
- Instrument: {instrument}
- Style: {style}
- Mood: {mood}
- Complexity: {complexity}

STYLE CHARACTERISTICS:
{style_details}

HARMONIC CONTEXT:
{harmonic_context}

RHYTHMIC CONTEXT:
{rhythmic_context}

DYNAMIC CONTEXT:
{dynamic_context}

REQUIREMENTS:
1. Generate exactly 2-4 bars of {instrument} content
2. Use the specified key ({key}) as the foundation
3. Match the tempo ({tempo} BPM) and time signature ({time_signature})
4. Incorporate the style characteristics listed above
5. Make it musically coherent and playable
6. Use appropriate note velocities for {instrument}
7. Include melodic interest and development
8. Ensure the {instrument} line works harmonically
9. Match the mood and complexity level specified

OUTPUT FORMAT:
Return ONLY a JSON object with this exact structure:
{{
    "notes": [
        {{
            "pitch": 60,
            "velocity": 80,
            "start_time_seconds": 0.0,
            "duration_seconds": 0.5,
            "track_index": 0
        }}
    ],
    "tempo": {tempo},
    "key": "{key}",
    "time_signature": "{time_signature}",
    "style_notes": "Brief description of how this matches the requested style",
    "musical_justification": "Brief explanation of musical choices made"
}}

Generate the {instrument} line now:"""
        }
    
    def _initialize_optimization_rules(self) -> Dict[str, List[str]]:
        """Initialize optimization rules for different prompt types"""
        return {
            "bass_optimization": [
                "Emphasize root note movement and harmonic support",
                "Include rhythmic interest and syncopation",
                "Use appropriate bass range (E1-A5)",
                "Consider walking bass patterns for jazz styles",
                "Include palm muting and slides for rock styles"
            ],
            "drum_optimization": [
                "Use standard drum mapping and velocities",
                "Include ghost notes and dynamic variation",
                "Consider fills and pattern variations",
                "Match the style's rhythmic characteristics",
                "Include appropriate cymbal work"
            ],
            "melody_optimization": [
                "Create melodic interest and development",
                "Use appropriate melodic range for instrument",
                "Include phrasing and articulation",
                "Consider harmonic implications",
                "Match the style's melodic characteristics"
            ]
        }
    
    def _initialize_output_formats(self) -> Dict[str, Dict[str, Any]]:
        """Initialize output format specifications"""
        return {
            "midi_json": {
                "description": "MIDI data in JSON format",
                "required_fields": ["notes", "tempo", "key", "time_signature"],
                "note_fields": ["pitch", "velocity", "start_time_seconds", "duration_seconds", "track_index"],
                "validation_rules": {
                    "pitch_range": (0, 127),
                    "velocity_range": (1, 127),
                    "time_positive": True,
                    "duration_positive": True
                }
            }
        }
    
    def build_musical_prompt(self, user_prompt: str, musical_context: MusicalContext, 
                           style_characteristics: StyleCharacteristics, 
                           generation_parameters: Dict[str, Any] = None) -> EnhancedPrompt:
        """
        Build a context-aware musical prompt for AI generation
        
        Args:
            user_prompt: Original user prompt
            musical_context: Analyzed musical context
            style_characteristics: Style characteristics
            generation_parameters: Additional generation parameters
            
        Returns:
            EnhancedPrompt with context-aware prompt
        """
        if generation_parameters is None:
            generation_parameters = {}
        
        # Determine prompt type based on instrument
        instrument = musical_context.instrument.lower()
        if "bass" in instrument:
            prompt_type = "bass_generation"
        elif "drum" in instrument:
            prompt_type = "drum_generation"
        else:
            prompt_type = "melody_generation"
        
        # Get base template
        template = self.prompt_templates[prompt_type]
        
        # Build context data
        context_data = self._build_context_data(user_prompt, musical_context, style_characteristics)
        
        # Format the template
        enhanced_prompt = template.format(**context_data)
        
        # Optimize the prompt
        optimized_prompt = self._optimize_prompt(enhanced_prompt, prompt_type, musical_context)
        
        # Create prompt context
        prompt_context = PromptContext(
            user_prompt=user_prompt,
            musical_context=musical_context,
            style_characteristics=style_characteristics,
            generation_parameters=generation_parameters,
            session_context={}
        )
        
        # Create enhanced prompt
        enhanced_prompt_obj = EnhancedPrompt(
            original_prompt=user_prompt,
            enhanced_prompt=optimized_prompt,
            context=prompt_context,
            prompt_type=prompt_type,
            optimization_level="high",
            expected_output_format="midi_json"
        )
        
        return enhanced_prompt_obj
    
    def _build_context_data(self, user_prompt: str, musical_context: MusicalContext, 
                           style_characteristics: StyleCharacteristics) -> Dict[str, Any]:
        """Build context data for prompt formatting"""
        
        # Style characteristics details
        style_details = self._format_style_characteristics(style_characteristics)
        
        # Harmonic context
        harmonic_context = self._format_harmonic_context(musical_context.harmonic_context)
        
        # Rhythmic context
        rhythmic_context = self._format_rhythmic_context(musical_context.rhythmic_context)
        
        # Dynamic context
        dynamic_context = self._format_dynamic_context(musical_context.dynamic_context)
        
        return {
            "user_prompt": user_prompt,
            "key": musical_context.key,
            "tempo": musical_context.tempo,
            "time_signature": musical_context.time_signature,
            "instrument": musical_context.instrument,
            "style": musical_context.style,
            "mood": musical_context.mood.value,
            "complexity": musical_context.complexity.value,
            "style_characteristics": style_characteristics.artist,
            "style_details": style_details,
            "harmonic_context": harmonic_context,
            "rhythmic_context": rhythmic_context,
            "dynamic_context": dynamic_context
        }
    
    def _format_style_characteristics(self, style_characteristics: StyleCharacteristics) -> str:
        """Format style characteristics for prompt"""
        characteristics = style_characteristics.characteristics
        techniques = style_characteristics.technique_characteristics
        rhythmic_patterns = style_characteristics.rhythmic_patterns
        harmonic_preferences = style_characteristics.harmonic_preferences
        melodic_preferences = style_characteristics.melodic_preferences
        
        formatted = f"Artist: {style_characteristics.artist}\n"
        formatted += f"Characteristics: {', '.join(characteristics[:5])}\n"
        formatted += f"Techniques: {', '.join(techniques[:5])}\n"
        formatted += f"Rhythmic Patterns: {', '.join(rhythmic_patterns[:3])}\n"
        formatted += f"Harmonic Preferences: {', '.join(harmonic_preferences[:3])}\n"
        formatted += f"Melodic Preferences: {', '.join(melodic_preferences[:3])}\n"
        formatted += f"Tempo Range: {style_characteristics.tempo_range[0]}-{style_characteristics.tempo_range[1]} BPM\n"
        formatted += f"Dynamic Range: {style_characteristics.dynamic_range}"
        
        return formatted
    
    def _format_harmonic_context(self, harmonic_context: Dict[str, Any]) -> str:
        """Format harmonic context for prompt"""
        formatted = f"Key: {harmonic_context.get('key', 'Unknown')}\n"
        formatted += f"Root Note: {harmonic_context.get('root_note', 'Unknown')}\n"
        formatted += f"Mode: {harmonic_context.get('mode', 'Unknown')}\n"
        formatted += f"Scale Notes: {harmonic_context.get('scale_notes', [])[:8]}\n"
        formatted += f"Chord Tones: {harmonic_context.get('chord_tones', [])}\n"
        formatted += f"Passing Tones: {harmonic_context.get('passing_tones', [])[:5]}"
        
        return formatted
    
    def _format_rhythmic_context(self, rhythmic_context: Dict[str, Any]) -> str:
        """Format rhythmic context for prompt"""
        formatted = f"Tempo: {rhythmic_context.get('tempo', 120)} BPM\n"
        formatted += f"Time Signature: {rhythmic_context.get('time_signature', '4/4')}\n"
        formatted += f"Beat Duration: {rhythmic_context.get('beat_duration', 0.5):.3f} seconds\n"
        formatted += f"Beats Per Measure: {rhythmic_context.get('beats_per_measure', 4)}\n"
        formatted += f"Characteristics: {', '.join(rhythmic_context.get('characteristics', []))}"
        
        return formatted
    
    def _format_dynamic_context(self, dynamic_context: Dict[str, Any]) -> str:
        """Format dynamic context for prompt"""
        formatted = f"Dynamic Range: {dynamic_context.get('range', 'medium')}\n"
        formatted += f"Typical Level: {dynamic_context.get('typical', 'mf')}\n"
        formatted += f"Variation: {dynamic_context.get('variation', 'medium')}"
        
        return formatted
    
    def _optimize_prompt(self, prompt: str, prompt_type: str, musical_context: MusicalContext) -> str:
        """Optimize prompt based on type and context"""
        
        # Get optimization rules
        optimization_rules = self.optimization_rules.get(f"{prompt_type}_optimization", [])
        
        # Apply optimizations
        optimized_prompt = prompt
        
        # Add instrument-specific optimizations
        if musical_context.instrument.lower() == "bass":
            optimized_prompt += "\n\nBASS-SPECIFIC REQUIREMENTS:\n"
            optimized_prompt += "- Focus on root note movement and harmonic support\n"
            optimized_prompt += "- Use appropriate bass range (E1-A5)\n"
            optimized_prompt += "- Include rhythmic interest and syncopation\n"
            optimized_prompt += "- Consider walking bass patterns for jazz styles\n"
        elif musical_context.instrument.lower() == "drums":
            optimized_prompt += "\n\nDRUM-SPECIFIC REQUIREMENTS:\n"
            optimized_prompt += "- Use standard drum mapping (kick=36, snare=38, hi-hat=42)\n"
            optimized_prompt += "- Include ghost notes and dynamic variation\n"
            optimized_prompt += "- Consider fills and pattern variations\n"
            optimized_prompt += "- Match the style's rhythmic characteristics\n"
        else:
            optimized_prompt += "\n\nMELODY-SPECIFIC REQUIREMENTS:\n"
            optimized_prompt += "- Create melodic interest and development\n"
            optimized_prompt += "- Use appropriate melodic range for instrument\n"
            optimized_prompt += "- Include phrasing and articulation\n"
            optimized_prompt += "- Consider harmonic implications\n"
        
        # Add mood-specific optimizations
        mood_optimizations = {
            MusicalMood.NEUTRAL: "- Use standard rhythms and moderate velocities\n- Include balanced phrasing and dynamics\n",
            MusicalMood.ENERGETIC: "- Use driving rhythms and higher velocities\n- Include syncopation and off-beat emphasis\n",
            MusicalMood.CHAOTIC: "- Use irregular rhythms and unpredictable phrasing\n- Include wide dynamic range and complex patterns\n",
            MusicalMood.RAW: "- Use aggressive attack and palm muting\n- Include slides and hammer-ons\n",
            MusicalMood.AGGRESSIVE: "- Use heavy attack and power chords\n- Include driving rhythms and high velocities\n",
            MusicalMood.MELANCHOLIC: "- Use sustained notes and legato phrasing\n- Include lower velocities and slower rhythms\n",
            MusicalMood.PEACEFUL: "- Use smooth, gentle phrasing\n- Include lower velocities and sustained notes\n",
            MusicalMood.DRAMATIC: "- Use wide dynamic range and varied phrasing\n- Include complex rhythms and emotional intensity\n",
            MusicalMood.FUNKY: "- Use syncopated rhythms and off-beat emphasis\n- Include ghost notes and rhythmic complexity\n",
            MusicalMood.JAZZY: "- Use swing feel and sophisticated phrasing\n- Include chromatic movement and complex harmony\n",
            MusicalMood.ROCK: "- Use driving rhythms and power chords\n- Include aggressive attack and high velocities\n"
        }
        
        if musical_context.mood in mood_optimizations:
            optimized_prompt += f"\nMOOD-SPECIFIC REQUIREMENTS:\n{mood_optimizations[musical_context.mood]}"
        
        # Add complexity-specific optimizations
        complexity_optimizations = {
            MusicalComplexity.SIMPLE: "- Keep patterns simple and straightforward\n- Use basic rhythms and harmonies\n",
            MusicalComplexity.MEDIUM: "- Use balanced complexity with some interest\n- Include moderate rhythmic and harmonic variety\n",
            MusicalComplexity.COMPLEX: "- Use sophisticated patterns and techniques\n- Include complex rhythms and harmonies\n",
            MusicalComplexity.EXPERT: "- Use advanced techniques and virtuosic patterns\n- Include complex rhythms, harmonies, and phrasing\n"
        }
        
        if musical_context.complexity in complexity_optimizations:
            optimized_prompt += f"\nCOMPLEXITY-SPECIFIC REQUIREMENTS:\n{complexity_optimizations[musical_context.complexity]}"
        
        return optimized_prompt
    
    def validate_prompt(self, prompt: str) -> Tuple[bool, List[str]]:
        """Validate prompt for quality and completeness"""
        issues = []
        
        # Check length
        if len(prompt) < 100:
            issues.append("Prompt too short - may not provide enough context")
        elif len(prompt) > 4000:
            issues.append("Prompt too long - may exceed model limits")
        
        # Check for required elements
        required_elements = [
            "ORIGINAL REQUEST:",
            "MUSICAL CONTEXT:",
            "STYLE CHARACTERISTICS:",
            "REQUIREMENTS:",
            "OUTPUT FORMAT:"
        ]
        
        for element in required_elements:
            if element not in prompt:
                issues.append(f"Missing required element: {element}")
        
        # Check for JSON format specification
        if "JSON object" not in prompt:
            issues.append("Missing JSON format specification")
        
        # Check for musical context
        if "Key:" not in prompt or "Tempo:" not in prompt:
            issues.append("Missing essential musical context")
        
        return len(issues) == 0, issues
    
    def get_prompt_statistics(self, prompt: str) -> Dict[str, Any]:
        """Get statistics about the prompt"""
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "line_count": len(prompt.split('\n')),
            "has_musical_context": "MUSICAL CONTEXT:" in prompt,
            "has_style_characteristics": "STYLE CHARACTERISTICS:" in prompt,
            "has_requirements": "REQUIREMENTS:" in prompt,
            "has_output_format": "OUTPUT FORMAT:" in prompt,
            "has_json_spec": "JSON object" in prompt
        }