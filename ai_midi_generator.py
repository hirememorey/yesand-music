"""
AI-First MIDI Generation Engine

This module implements AI-powered MIDI generation using OpenAI's GPT models
with security-first architecture and context-aware intelligence.

Key Features:
- Pure AI generation without templates
- Security-first architecture with validation
- Context-aware prompt engineering
- Real-time generation capabilities
- Quality assessment and validation
"""

import json
import time
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Generator, Tuple
from dataclasses import dataclass
from pathlib import Path

from security_first_architecture import (
    SecurityFirstComponent, SecurityContext, SecurityResult, SecurityLevel,
    SecurityError, InputValidationError, RateLimitExceededError, SystemUnhealthyError
)
from secure_llm_client import SecureLLMClient, LLMConfig, LLMRequest, LLMResponse
from midi_io import save_midi_file, parse_midi_file
from theory import create_scale, Mode


@dataclass
class MIDIGenerationRequest:
    """Request structure for MIDI generation"""
    prompt: str
    context: Dict[str, Any]
    style_characteristics: Dict[str, Any]
    musical_context: Dict[str, Any]
    security_level: SecurityLevel
    request_id: str
    timestamp: float


@dataclass
class MIDIGenerationResult:
    """Result structure for MIDI generation"""
    success: bool
    midi_data: List[Dict[str, Any]]
    filename: str
    quality_score: float
    style_accuracy: float
    musical_coherence: float
    processing_time: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None


class AIMIDIGenerator(SecurityFirstComponent):
    """
    AI-First MIDI Generation Engine
    
    Generates MIDI content using OpenAI's GPT models with context-aware
    intelligence and security-first architecture.
    """
    
    def __init__(self, openai_api_key: str, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        super().__init__(security_level)
        self.llm_client = SecureLLMClient(LLMConfig(
            api_key=openai_api_key,
            max_tokens=4000,
            max_response_length=8000,  # Increased for longer pieces
            model="gpt-4"
        ))
        self.generation_history: List[MIDIGenerationResult] = []
        self.style_database = self._initialize_style_database()
        self.musical_context = {}
        
    def _initialize_style_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize database of musical styles and characteristics"""
        return {
            "jeff_ament": {
                "artist": "Jeff Ament (Pearl Jam)",
                "characteristics": [
                    "raw, energetic bass lines",
                    "syncopated rhythms",
                    "aggressive attack",
                    "complex harmonic movement",
                    "grunge aesthetic",
                    "unpredictable phrasing",
                    "heavy use of root notes with chromatic passing tones",
                    "dynamic range from soft to very loud",
                    "use of slides and hammer-ons",
                    "rhythmic complexity with off-beat emphasis"
                ],
                "tempo_range": (80, 140),
                "key_preferences": ["minor", "dorian", "mixolydian"],
                "rhythmic_patterns": ["syncopated", "off-beat", "complex"],
                "dynamic_range": "wide",
                "technique_characteristics": ["slides", "hammer-ons", "palm muting"]
            },
            "pearl_jam": {
                "band": "Pearl Jam",
                "characteristics": [
                    "grunge rock foundation",
                    "alternative rock sensibilities",
                    "raw, unpolished sound",
                    "emotional intensity",
                    "complex song structures",
                    "dynamic contrast",
                    "use of power chords with melodic bass lines",
                    "rhythmic complexity",
                    "unconventional time signatures"
                ],
                "tempo_range": (70, 160),
                "key_preferences": ["minor", "dorian", "mixolydian", "major"],
                "rhythmic_patterns": ["syncopated", "complex", "unconventional"],
                "dynamic_range": "very_wide",
                "technique_characteristics": ["power_chords", "melodic_bass", "dynamic_contrast"]
            }
        }
    
    def generate_midi(self, prompt: str, context: Dict[str, Any] = None) -> MIDIGenerationResult:
        """
        Generate MIDI content from a natural language prompt
        
        Args:
            prompt: Natural language description of desired MIDI content
            context: Additional musical context (key, tempo, style, etc.)
            
        Returns:
            MIDIGenerationResult with generated MIDI data and metadata
        """
        start_time = time.time()
        request_id = self._generate_request_id(prompt)
        
        try:
            # Create security context
            security_context = SecurityContext(
                user_id="mvp_user",
                session_id="mvp_session",
                security_level=self.security_level,
                timestamp=datetime.now(),
                request_id=request_id
            )
            
            # Validate input
            self._validate_prompt(prompt, security_context)
            
            # Analyze prompt for musical elements
            musical_context = self._analyze_prompt(prompt, context or {})
            
            # Extract style characteristics
            style_characteristics = self._extract_style_characteristics(prompt, musical_context)
            
            # Build context-aware prompt
            enhanced_prompt = self._build_musical_prompt(prompt, musical_context, style_characteristics)
            
            # Generate MIDI using AI
            midi_data = self._generate_midi_with_ai(enhanced_prompt, musical_context, security_context)
            
            # Validate and assess quality
            quality_assessment = self._assess_midi_quality(midi_data, style_characteristics)
            
            # Generate filename
            filename = self._generate_filename(prompt, musical_context)
            
            # Create result
            result = MIDIGenerationResult(
                success=True,
                midi_data=midi_data,
                filename=filename,
                quality_score=quality_assessment["quality_score"],
                style_accuracy=quality_assessment["style_accuracy"],
                musical_coherence=quality_assessment["musical_coherence"],
                processing_time=time.time() - start_time,
                metadata={
                    "prompt": prompt,
                    "musical_context": musical_context,
                    "style_characteristics": style_characteristics,
                    "request_id": request_id
                }
            )
            
            # Store in history
            self.generation_history.append(result)
            
            return result
            
        except Exception as e:
            return MIDIGenerationResult(
                success=False,
                midi_data=[],
                filename="",
                quality_score=0.0,
                style_accuracy=0.0,
                musical_coherence=0.0,
                processing_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def generate_live(self, prompt: str, context: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Generate MIDI content in real-time with streaming updates
        
        Args:
            prompt: Natural language description of desired MIDI content
            context: Additional musical context
            
        Yields:
            Progress updates and partial results
        """
        try:
            # Analyze prompt
            yield {"status": "analyzing", "message": "Analyzing prompt and extracting musical context..."}
            musical_context = self._analyze_prompt(prompt, context or {})
            
            # Extract style characteristics
            yield {"status": "style_analysis", "message": "Analyzing style characteristics..."}
            style_characteristics = self._extract_style_characteristics(prompt, musical_context)
            
            # Build enhanced prompt
            yield {"status": "prompt_engineering", "message": "Building context-aware prompt..."}
            enhanced_prompt = self._build_musical_prompt(prompt, musical_context, style_characteristics)
            
            # Generate MIDI
            yield {"status": "generating", "message": "Generating MIDI with AI..."}
            midi_data = self._generate_midi_with_ai(enhanced_prompt, musical_context, None)
            
            # Validate quality
            yield {"status": "validating", "message": "Validating and assessing quality..."}
            quality_assessment = self._assess_midi_quality(midi_data, style_characteristics)
            
            # Final result
            yield {
                "status": "complete",
                "message": "MIDI generation complete",
                "midi_data": midi_data,
                "quality_assessment": quality_assessment,
                "musical_context": musical_context,
                "style_characteristics": style_characteristics
            }
            
        except Exception as e:
            yield {
                "status": "error",
                "message": f"Generation failed: {str(e)}",
                "error": str(e)
            }
    
    def _validate_prompt(self, prompt: str, security_context: SecurityContext) -> None:
        """Validate input prompt for security and content"""
        if not prompt or len(prompt.strip()) == 0:
            raise InputValidationError("Prompt cannot be empty")
        
        if len(prompt) > 1000:
            raise InputValidationError("Prompt too long (max 1000 characters)")
        
        # Check for potentially harmful content
        harmful_patterns = [
            r"<script.*?>",
            r"javascript:",
            r"data:",
            r"vbscript:",
            r"onload\s*=",
            r"onerror\s*="
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                raise InputValidationError("Prompt contains potentially harmful content")
    
    def _analyze_prompt(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prompt to extract musical context"""
        musical_context = {
            "key": "C major",  # Default
            "tempo": 120,      # Default
            "time_signature": "4/4",
            "instrument": "bass",
            "style": "unknown",
            "mood": "neutral",
            "complexity": "medium"
        }
        
        # Extract key information
        key_patterns = {
            r"in\s+([A-G][#b]?\s+minor)": lambda m: m.group(1),
            r"in\s+([A-G][#b]?\s+major)": lambda m: m.group(1),
            r"([A-G][#b]?\s+minor)": lambda m: m.group(1),
            r"([A-G][#b]?\s+major)": lambda m: m.group(1),
        }
        
        for pattern, extractor in key_patterns.items():
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                musical_context["key"] = extractor(match)
                break
        
        # Extract tempo
        tempo_match = re.search(r"(\d+)\s*bpm", prompt, re.IGNORECASE)
        if tempo_match:
            musical_context["tempo"] = int(tempo_match.group(1))
        
        # Extract length (measures/bars)
        length_patterns = {
            r"(\d+)\s*measures?": lambda m: int(m.group(1)),
            r"(\d+)\s*bars?": lambda m: int(m.group(1)),
            r"(\d+)\s*beats?": lambda m: int(m.group(1)),
        }
        
        musical_context["length_measures"] = 4  # Default to 4 measures (2-4 bars)
        for pattern, extractor in length_patterns.items():
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                musical_context["length_measures"] = extractor(match)
                break
        
        # Extract instrument
        if "bass" in prompt.lower():
            musical_context["instrument"] = "bass"
        elif "drum" in prompt.lower():
            musical_context["instrument"] = "drums"
        elif "melody" in prompt.lower():
            musical_context["instrument"] = "melody"
        
        # Extract style references
        for style_name, style_data in self.style_database.items():
            if style_name in prompt.lower() or any(char in prompt.lower() for char in style_data.get("characteristics", [])):
                musical_context["style"] = style_name
                break
        
        # Extract mood/characteristics
        mood_indicators = {
            "energetic": ["energetic", "energetic", "fast", "upbeat", "intense"],
            "chaotic": ["chaotic", "chaos", "unpredictable", "wild", "crazy"],
            "raw": ["raw", "rough", "unpolished", "gritty"],
            "aggressive": ["aggressive", "heavy", "intense", "powerful"],
            "melancholic": ["sad", "melancholic", "dark", "moody"]
        }
        
        for mood, indicators in mood_indicators.items():
            if any(indicator in prompt.lower() for indicator in indicators):
                musical_context["mood"] = mood
                break
        
        # Merge with provided context
        musical_context.update(context)
        
        return musical_context
    
    def _extract_style_characteristics(self, prompt: str, musical_context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract style characteristics from prompt and context"""
        style_name = musical_context.get("style", "unknown")
        
        if style_name in self.style_database:
            base_characteristics = self.style_database[style_name].copy()
        else:
            base_characteristics = {
                "characteristics": ["standard", "generic"],
                "tempo_range": (100, 120),
                "key_preferences": ["major", "minor"],
                "rhythmic_patterns": ["standard"],
                "dynamic_range": "medium",
                "technique_characteristics": ["standard"]
            }
        
        # Enhance with mood characteristics
        mood = musical_context.get("mood", "neutral")
        if mood == "energetic":
            base_characteristics["characteristics"].extend(["fast", "intense", "driving"])
            base_characteristics["tempo_range"] = (base_characteristics["tempo_range"][0] + 20, base_characteristics["tempo_range"][1] + 20)
        elif mood == "chaotic":
            base_characteristics["characteristics"].extend(["unpredictable", "complex", "irregular"])
            base_characteristics["rhythmic_patterns"].extend(["syncopated", "off-beat", "irregular"])
        elif mood == "raw":
            base_characteristics["characteristics"].extend(["unpolished", "gritty", "aggressive"])
            base_characteristics["technique_characteristics"].extend(["palm_muting", "slides", "hammer-ons"])
        
        return base_characteristics
    
    def _build_musical_prompt(self, prompt: str, musical_context: Dict[str, Any], style_characteristics: Dict[str, Any]) -> str:
        """Build context-aware prompt for AI generation"""
        
        # Extract key information
        key = musical_context.get("key", "C major")
        tempo = musical_context.get("tempo", 120)
        instrument = musical_context.get("instrument", "bass")
        length_measures = musical_context.get("length_measures", 4)
        
        # Build the enhanced prompt
        enhanced_prompt = f"""You are a professional {instrument} player and music producer. Generate a {instrument} line that matches the following request:

ORIGINAL REQUEST: "{prompt}"

MUSICAL CONTEXT:
- Key: {key}
- Tempo: {tempo} BPM
- Time Signature: {musical_context.get('time_signature', '4/4')}
- Instrument: {instrument}

STYLE CHARACTERISTICS:
{json.dumps(style_characteristics, indent=2)}

REQUIREMENTS:
1. Generate exactly {length_measures} measures of {instrument} content
2. Use the specified key ({key}) as the foundation
3. Match the tempo ({tempo} BPM)
4. Incorporate the style characteristics listed above
5. Make it musically coherent and playable
6. Use appropriate note velocities (60-127 for bass, 80-127 for drums)
7. Include rhythmic variety and interest
8. Ensure the bass line supports the harmonic context

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
    "time_signature": "{musical_context.get('time_signature', '4/4')}",
    "style_notes": "Brief description of how this matches the requested style"
}}

Generate the {instrument} line now:"""

        return enhanced_prompt
    
    def _generate_midi_with_ai(self, enhanced_prompt: str, musical_context: Dict[str, Any], security_context: SecurityContext = None) -> List[Dict[str, Any]]:
        """Generate MIDI data using AI"""
        
        # Create LLM request
        llm_request = LLMRequest(
            prompt=enhanced_prompt,
            model="gpt-4",
            max_tokens=4000,  # Increased for longer pieces
            temperature=0.8,
            request_id=self._generate_request_id(enhanced_prompt),
            timestamp=time.time(),
            user_id="mvp_user",
            session_id="mvp_session",
            security_level=self.security_level,
            metadata={"type": "midi_generation", "context": musical_context}
        )
        
        # Make request to LLM
        response = self.llm_client.process(llm_request, security_context)
        
        if not response.is_safe:
            raise Exception(f"LLM request failed: Response marked as unsafe")
        
        # Parse response
        try:
            response_data = json.loads(response.content)
            if "notes" not in response_data:
                raise ValueError("Response missing 'notes' field")
            
            # Validate and clean MIDI data
            midi_data = self._validate_midi_data(response_data["notes"])
            
            return midi_data
            
        except json.JSONDecodeError as e:
            # Debug: Show the response content that failed to parse
            print(f"DEBUG: JSON parse error: {e}")
            print(f"DEBUG: Response content (first 500 chars): {response.content[:500]}")
            print(f"DEBUG: Response content (last 500 chars): {response.content[-500:]}")
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise ValueError(f"Failed to process LLM response: {e}")
    
    def _validate_midi_data(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean MIDI data"""
        if not isinstance(notes, list):
            raise ValueError("Notes must be a list")
        
        validated_notes = []
        for i, note in enumerate(notes):
            if not isinstance(note, dict):
                continue
            
            # Validate required fields
            required_fields = ["pitch", "velocity", "start_time_seconds", "duration_seconds"]
            if not all(field in note for field in required_fields):
                continue
            
            # Validate values
            try:
                validated_note = {
                    "pitch": max(0, min(127, int(note["pitch"]))),
                    "velocity": max(1, min(127, int(note["velocity"]))),
                    "start_time_seconds": max(0.0, float(note["start_time_seconds"])),
                    "duration_seconds": max(0.1, float(note["duration_seconds"])),
                    "track_index": int(note.get("track_index", 0))
                }
                validated_notes.append(validated_note)
            except (ValueError, TypeError):
                continue
        
        if not validated_notes:
            raise ValueError("No valid notes found in response")
        
        return validated_notes
    
    def _assess_midi_quality(self, midi_data: List[Dict[str, Any]], style_characteristics: Dict[str, Any]) -> Dict[str, float]:
        """Assess the quality of generated MIDI data"""
        
        if not midi_data:
            return {"quality_score": 0.0, "style_accuracy": 0.0, "musical_coherence": 0.0}
        
        # Basic quality metrics
        note_count = len(midi_data)
        pitch_range = max(note["pitch"] for note in midi_data) - min(note["pitch"] for note in midi_data)
        velocity_variety = len(set(note["velocity"] for note in midi_data))
        
        # Quality score (0-1)
        quality_score = min(1.0, (note_count / 20.0) * 0.4 + (pitch_range / 24.0) * 0.3 + (velocity_variety / 10.0) * 0.3)
        
        # Style accuracy (simplified)
        style_accuracy = 0.7  # Placeholder - would need more sophisticated analysis
        
        # Musical coherence (simplified)
        musical_coherence = 0.8  # Placeholder - would need harmonic analysis
        
        return {
            "quality_score": quality_score,
            "style_accuracy": style_accuracy,
            "musical_coherence": musical_coherence
        }
    
    def _generate_filename(self, prompt: str, musical_context: Dict[str, Any]) -> str:
        """Generate intelligent filename based on prompt and context"""
        
        # Extract key elements
        key = musical_context.get("key", "unknown").replace(" ", "_").lower()
        instrument = musical_context.get("instrument", "unknown")
        style = musical_context.get("style", "unknown")
        
        # Create base filename
        timestamp = int(time.time())
        base_name = f"{instrument}_{style}_{key}_{timestamp}"
        
        # Clean up filename
        base_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)
        base_name = re.sub(r'_+', '_', base_name)
        
        return f"{base_name}.mid"
    
    def _generate_request_id(self, prompt: str) -> str:
        """Generate unique request ID"""
        content = f"{prompt}_{time.time()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def save_midi_file(self, result: MIDIGenerationResult, output_dir: str = "generated_midi") -> bool:
        """Save MIDI generation result to file"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            file_path = output_path / result.filename
            save_midi_file(result.midi_data, str(file_path))
            
            return True
        except Exception as e:
            print(f"Failed to save MIDI file: {e}")
            return False
    
    def get_generation_history(self) -> List[MIDIGenerationResult]:
        """Get history of MIDI generations"""
        return self.generation_history.copy()
    
    def clear_history(self) -> None:
        """Clear generation history"""
        self.generation_history.clear()
    
    def _process_secure(self, request: Any, security_context: SecurityContext) -> SecurityResult:
        """Process secure request - required by SecurityFirstComponent"""
        try:
            # This is a placeholder implementation
            # In a real implementation, this would handle secure processing
            return SecurityResult(
                success=True,
                message="Secure processing completed",
                data={"processed": True}
            )
        except Exception as e:
            return SecurityResult(
                success=False,
                message=f"Secure processing failed: {str(e)}",
                data={"error": str(e)}
            )
    
    def _validate_input(self, input_data: Any, security_context: SecurityContext) -> bool:
        """Validate input data - required by SecurityFirstComponent"""
        try:
            # Basic validation - in a real implementation, this would be more comprehensive
            if isinstance(input_data, str):
                return len(input_data) > 0 and len(input_data) < 10000
            return True
        except Exception:
            return False