"""
Musical Intelligence Engine

This module provides context-aware musical analysis and intelligence for the MVP
MIDI generation system. It analyzes prompts, extracts musical context, and
provides intelligent suggestions for MIDI generation.

Key Features:
- Prompt analysis and musical context extraction
- Style characteristic analysis
- Musical coherence assessment
- Context-aware suggestions
- Real-time musical intelligence
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from theory import create_scale, Mode


class MusicalComplexity(Enum):
    """Musical complexity levels"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    EXPERT = "expert"


class MusicalMood(Enum):
    """Musical mood categories"""
    NEUTRAL = "neutral"
    ENERGETIC = "energetic"
    CHAOTIC = "chaotic"
    RAW = "raw"
    AGGRESSIVE = "aggressive"
    MELANCHOLIC = "melancholic"
    PEACEFUL = "peaceful"
    DRAMATIC = "dramatic"
    FUNKY = "funky"
    JAZZY = "jazzy"
    ROCK = "rock"


@dataclass
class MusicalContext:
    """Musical context information"""
    key: str
    tempo: int
    time_signature: str
    instrument: str
    style: str
    mood: MusicalMood
    complexity: MusicalComplexity
    harmonic_context: Dict[str, Any]
    rhythmic_context: Dict[str, Any]
    dynamic_context: Dict[str, Any]


@dataclass
class StyleCharacteristics:
    """Style characteristics for musical generation"""
    artist: str
    characteristics: List[str]
    tempo_range: Tuple[int, int]
    key_preferences: List[str]
    rhythmic_patterns: List[str]
    dynamic_range: str
    technique_characteristics: List[str]
    harmonic_preferences: List[str]
    melodic_preferences: List[str]


class MusicalIntelligenceEngine:
    """
    Musical Intelligence Engine for context-aware MIDI generation
    
    Provides intelligent analysis of musical prompts and context to enhance
    MIDI generation with appropriate style, mood, and musical characteristics.
    """
    
    def __init__(self):
        self.style_database = self._initialize_style_database()
        self.mood_indicators = self._initialize_mood_indicators()
        self.complexity_indicators = self._initialize_complexity_indicators()
        self.instrument_characteristics = self._initialize_instrument_characteristics()
        
    def _initialize_style_database(self) -> Dict[str, StyleCharacteristics]:
        """Initialize comprehensive style database"""
        return {
            "jeff_ament": StyleCharacteristics(
                artist="Jeff Ament (Pearl Jam)",
                characteristics=[
                    "raw, energetic bass lines",
                    "syncopated rhythms",
                    "aggressive attack",
                    "complex harmonic movement",
                    "grunge aesthetic",
                    "unpredictable phrasing",
                    "heavy use of root notes with chromatic passing tones",
                    "dynamic range from soft to very loud",
                    "use of slides and hammer-ons",
                    "rhythmic complexity with off-beat emphasis",
                    "palm muting techniques",
                    "use of power chords in bass lines",
                    "unconventional time signatures",
                    "emotional intensity"
                ],
                tempo_range=(80, 140),
                key_preferences=["minor", "dorian", "mixolydian", "phrygian"],
                rhythmic_patterns=["syncopated", "off-beat", "complex", "irregular", "unconventional"],
                dynamic_range="very_wide",
                technique_characteristics=["slides", "hammer-ons", "palm_muting", "power_chords", "chromatic_passing_tones"],
                harmonic_preferences=["minor_tonality", "dorian_mode", "power_chords", "chromatic_movement"],
                melodic_preferences=["root_note_focus", "chromatic_passing_tones", "unpredictable_phrasing"]
            ),
            "pearl_jam": StyleCharacteristics(
                artist="Pearl Jam",
                characteristics=[
                    "grunge rock foundation",
                    "alternative rock sensibilities",
                    "raw, unpolished sound",
                    "emotional intensity",
                    "complex song structures",
                    "dynamic contrast",
                    "use of power chords with melodic bass lines",
                    "rhythmic complexity",
                    "unconventional time signatures",
                    "grunge aesthetic",
                    "alternative rock edge",
                    "emotional depth"
                ],
                tempo_range=(70, 160),
                key_preferences=["minor", "dorian", "mixolydian", "major", "phrygian"],
                rhythmic_patterns=["syncopated", "complex", "unconventional", "off-beat"],
                dynamic_range="very_wide",
                technique_characteristics=["power_chords", "melodic_bass", "dynamic_contrast", "palm_muting"],
                harmonic_preferences=["minor_tonality", "power_chords", "modal_harmony"],
                melodic_preferences=["melodic_bass_lines", "emotional_phrasing", "dynamic_contrast"]
            ),
            "generic_bass": StyleCharacteristics(
                artist="Generic Bass",
                characteristics=[
                    "solid rhythmic foundation",
                    "root note emphasis",
                    "harmonic support",
                    "steady tempo",
                    "clear articulation"
                ],
                tempo_range=(60, 180),
                key_preferences=["major", "minor"],
                rhythmic_patterns=["straight", "syncopated"],
                dynamic_range="medium",
                technique_characteristics=["standard_technique"],
                harmonic_preferences=["root_notes", "fifth_notes"],
                melodic_preferences=["simple_melodic_movement"]
            )
        }
    
    def _initialize_mood_indicators(self) -> Dict[MusicalMood, List[str]]:
        """Initialize mood indicator keywords"""
        return {
            MusicalMood.NEUTRAL: ["neutral", "standard", "normal", "regular", "typical", "basic"],
            MusicalMood.ENERGETIC: ["energetic", "energetic", "fast", "upbeat", "intense", "driving", "powerful", "dynamic"],
            MusicalMood.CHAOTIC: ["chaotic", "chaos", "unpredictable", "wild", "crazy", "disordered", "random", "irregular"],
            MusicalMood.RAW: ["raw", "rough", "unpolished", "gritty", "dirty", "unrefined", "natural", "organic"],
            MusicalMood.AGGRESSIVE: ["aggressive", "heavy", "intense", "powerful", "angry", "fierce", "brutal", "harsh"],
            MusicalMood.MELANCHOLIC: ["sad", "melancholic", "dark", "moody", "depressed", "sorrowful", "gloomy", "bleak"],
            MusicalMood.PEACEFUL: ["peaceful", "calm", "serene", "gentle", "soft", "quiet", "tranquil", "relaxed"],
            MusicalMood.DRAMATIC: ["dramatic", "theatrical", "epic", "grand", "cinematic", "emotional", "intense", "powerful"],
            MusicalMood.FUNKY: ["funky", "groovy", "rhythmic", "danceable", "syncopated", "soulful", "rhythmic", "bouncy"],
            MusicalMood.JAZZY: ["jazzy", "swing", "sophisticated", "complex", "improvisational", "smooth", "cool", "refined"],
            MusicalMood.ROCK: ["rock", "rocking", "heavy", "powerful", "driving", "energetic", "aggressive", "loud"]
        }
    
    def _initialize_complexity_indicators(self) -> Dict[MusicalComplexity, List[str]]:
        """Initialize complexity indicator keywords"""
        return {
            MusicalComplexity.SIMPLE: ["simple", "basic", "easy", "straightforward", "minimal", "clean", "sparse"],
            MusicalComplexity.MEDIUM: ["medium", "moderate", "balanced", "standard", "typical", "normal"],
            MusicalComplexity.COMPLEX: ["complex", "complicated", "intricate", "sophisticated", "advanced", "detailed"],
            MusicalComplexity.EXPERT: ["expert", "master", "professional", "advanced", "sophisticated", "virtuoso", "technical"]
        }
    
    def _initialize_instrument_characteristics(self) -> Dict[str, Dict[str, Any]]:
        """Initialize instrument-specific characteristics"""
        return {
            "bass": {
                "pitch_range": (21, 81),  # E1 to A5
                "typical_techniques": ["plucking", "slapping", "popping", "palm_muting", "slides", "hammer-ons"],
                "rhythmic_role": "rhythmic_foundation",
                "harmonic_role": "harmonic_support",
                "dynamic_range": "wide"
            },
            "drums": {
                "pitch_range": (35, 81),  # B1 to A5
                "typical_techniques": ["hitting", "ghost_notes", "rolls", "fills", "syncopation"],
                "rhythmic_role": "rhythmic_driver",
                "harmonic_role": "rhythmic_support",
                "dynamic_range": "very_wide"
            },
            "melody": {
                "pitch_range": (48, 96),  # C3 to C7
                "typical_techniques": ["legato", "staccato", "vibrato", "bends", "slides"],
                "rhythmic_role": "melodic_lead",
                "harmonic_role": "melodic_expression",
                "dynamic_range": "wide"
            }
        }
    
    def analyze_prompt(self, prompt: str, context: Dict[str, Any] = None) -> MusicalContext:
        """
        Analyze a musical prompt to extract comprehensive musical context
        
        Args:
            prompt: Natural language musical prompt
            context: Additional context information
            
        Returns:
            MusicalContext with extracted musical information
        """
        # Initialize with defaults
        musical_context = MusicalContext(
            key="C major",
            tempo=120,
            time_signature="4/4",
            instrument="bass",
            style="unknown",
            mood=MusicalMood.NEUTRAL,
            complexity=MusicalComplexity.MEDIUM,
            harmonic_context={},
            rhythmic_context={},
            dynamic_context={}
        )
        
        # Extract key information
        musical_context.key = self._extract_key(prompt)
        
        # Extract tempo
        musical_context.tempo = self._extract_tempo(prompt)
        
        # Extract time signature
        musical_context.time_signature = self._extract_time_signature(prompt)
        
        # Extract instrument
        musical_context.instrument = self._extract_instrument(prompt)
        
        # Extract style
        musical_context.style = self._extract_style(prompt)
        
        # Extract mood
        musical_context.mood = self._extract_mood(prompt)
        
        # Extract complexity
        musical_context.complexity = self._extract_complexity(prompt)
        
        # Build harmonic context
        musical_context.harmonic_context = self._build_harmonic_context(musical_context)
        
        # Build rhythmic context
        musical_context.rhythmic_context = self._build_rhythmic_context(musical_context)
        
        # Build dynamic context
        musical_context.dynamic_context = self._build_dynamic_context(musical_context)
        
        # Merge with provided context
        if context:
            for key, value in context.items():
                if hasattr(musical_context, key):
                    setattr(musical_context, key, value)
        
        return musical_context
    
    def extract_style_characteristics(self, prompt: str, musical_context: MusicalContext) -> StyleCharacteristics:
        """
        Extract detailed style characteristics from prompt and context
        
        Args:
            prompt: Original musical prompt
            musical_context: Analyzed musical context
            
        Returns:
            StyleCharacteristics with detailed style information
        """
        style_name = musical_context.style
        
        if style_name in self.style_database:
            base_characteristics = self.style_database[style_name]
        else:
            base_characteristics = self.style_database["generic_bass"]
        
        # Enhance with mood characteristics
        enhanced_characteristics = self._enhance_with_mood(base_characteristics, musical_context.mood)
        
        # Enhance with complexity characteristics
        enhanced_characteristics = self._enhance_with_complexity(enhanced_characteristics, musical_context.complexity)
        
        # Enhance with instrument characteristics
        enhanced_characteristics = self._enhance_with_instrument(enhanced_characteristics, musical_context.instrument)
        
        return enhanced_characteristics
    
    def _extract_key(self, prompt: str) -> str:
        """Extract musical key from prompt"""
        key_patterns = {
            r"in\s+([A-G][#b]?\s+minor)": lambda m: m.group(1),
            r"in\s+([A-G][#b]?\s+major)": lambda m: m.group(1),
            r"([A-G][#b]?\s+minor)": lambda m: m.group(1),
            r"([A-G][#b]?\s+major)": lambda m: m.group(1),
            r"([A-G][#b]?m)": lambda m: m.group(1) + " minor",
            r"([A-G][#b]?M)": lambda m: m.group(1) + " major",
        }
        
        for pattern, extractor in key_patterns.items():
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                return extractor(match)
        
        return "C major"
    
    def _extract_tempo(self, prompt: str) -> int:
        """Extract tempo from prompt"""
        tempo_match = re.search(r"(\d+)\s*bpm", prompt, re.IGNORECASE)
        if tempo_match:
            return int(tempo_match.group(1))
        
        # Extract tempo from descriptive words
        tempo_indicators = {
            "slow": 60,
            "moderate": 100,
            "fast": 140,
            "very fast": 180,
            "lento": 60,
            "andante": 80,
            "moderato": 100,
            "allegro": 140,
            "presto": 180
        }
        
        for indicator, tempo in tempo_indicators.items():
            if indicator in prompt.lower():
                return tempo
        
        return 120
    
    def _extract_time_signature(self, prompt: str) -> str:
        """Extract time signature from prompt"""
        time_sig_match = re.search(r"(\d+)/(\d+)", prompt)
        if time_sig_match:
            return f"{time_sig_match.group(1)}/{time_sig_match.group(2)}"
        
        return "4/4"
    
    def _extract_instrument(self, prompt: str) -> str:
        """Extract instrument from prompt"""
        instrument_indicators = {
            "bass": ["bass", "bassline", "bass line", "bassist"],
            "drums": ["drum", "drums", "drummer", "percussion", "beat"],
            "melody": ["melody", "melodic", "melodious", "lead", "solo"],
            "guitar": ["guitar", "guitarist", "guitar line"],
            "piano": ["piano", "pianist", "keyboard"]
        }
        
        for instrument, indicators in instrument_indicators.items():
            if any(indicator in prompt.lower() for indicator in indicators):
                return instrument
        
        return "bass"
    
    def _extract_style(self, prompt: str) -> str:
        """Extract musical style from prompt"""
        prompt_lower = prompt.lower()
        
        for style_name, style_data in self.style_database.items():
            # Check for direct style name match
            if style_name in prompt_lower:
                return style_name
            
            # Check for artist name match
            if style_data.artist.lower() in prompt_lower:
                return style_name
            
            # Check for characteristic match
            for characteristic in style_data.characteristics:
                if any(word in prompt_lower for word in characteristic.lower().split()):
                    return style_name
        
        return "generic_bass"
    
    def _extract_mood(self, prompt: str) -> MusicalMood:
        """Extract musical mood from prompt"""
        prompt_lower = prompt.lower()
        
        for mood, indicators in self.mood_indicators.items():
            if any(indicator in prompt_lower for indicator in indicators):
                return mood
        
        return MusicalMood.NEUTRAL
    
    def _extract_complexity(self, prompt: str) -> MusicalComplexity:
        """Extract musical complexity from prompt"""
        prompt_lower = prompt.lower()
        
        for complexity, indicators in self.complexity_indicators.items():
            if any(indicator in prompt_lower for indicator in indicators):
                return complexity
        
        return MusicalComplexity.MEDIUM
    
    def _build_harmonic_context(self, musical_context: MusicalContext) -> Dict[str, Any]:
        """Build harmonic context from musical context"""
        key = musical_context.key
        style = musical_context.style
        
        # Extract key information
        key_match = re.match(r"([A-G][#b]?)\s+(major|minor)", key, re.IGNORECASE)
        if key_match:
            root_note = key_match.group(1)
            mode = key_match.group(2).lower()
        else:
            root_note = "C"
            mode = "major"
        
        # Get scale notes
        root_midi = self._note_to_midi(root_note)
        if mode == "major":
            scale_notes = create_scale(root_midi, Mode.MAJOR)
        else:
            scale_notes = create_scale(root_midi, Mode.MINOR)
        
        return {
            "key": key,
            "root_note": root_note,
            "mode": mode,
            "scale_notes": scale_notes,
            "chord_tones": self._get_chord_tones(scale_notes, mode),
            "passing_tones": self._get_passing_tones(scale_notes)
        }
    
    def _build_rhythmic_context(self, musical_context: MusicalContext) -> Dict[str, Any]:
        """Build rhythmic context from musical context"""
        tempo = musical_context.tempo
        time_sig = musical_context.time_signature
        mood = musical_context.mood
        
        # Calculate rhythmic values
        beat_duration = 60.0 / tempo
        time_sig_parts = time_sig.split("/")
        beats_per_measure = int(time_sig_parts[0])
        beat_unit = int(time_sig_parts[1])
        
        # Determine rhythmic characteristics based on mood
        rhythmic_characteristics = {
            MusicalMood.ENERGETIC: ["syncopated", "driving", "upbeat"],
            MusicalMood.CHAOTIC: ["irregular", "unpredictable", "complex"],
            MusicalMood.RAW: ["straight", "aggressive", "simple"],
            MusicalMood.AGGRESSIVE: ["driving", "powerful", "syncopated"],
            MusicalMood.MELANCHOLIC: ["slow", "sustained", "legato"],
            MusicalMood.PEACEFUL: ["smooth", "gentle", "legato"],
            MusicalMood.DRAMATIC: ["varied", "dynamic", "complex"],
            MusicalMood.FUNKY: ["syncopated", "groovy", "off-beat"],
            MusicalMood.JAZZY: ["swing", "syncopated", "complex"],
            MusicalMood.ROCK: ["driving", "straight", "powerful"]
        }.get(mood, ["standard"])
        
        return {
            "tempo": tempo,
            "time_signature": time_sig,
            "beat_duration": beat_duration,
            "beats_per_measure": beats_per_measure,
            "beat_unit": beat_unit,
            "characteristics": rhythmic_characteristics
        }
    
    def _build_dynamic_context(self, musical_context: MusicalContext) -> Dict[str, Any]:
        """Build dynamic context from musical context"""
        mood = musical_context.mood
        complexity = musical_context.complexity
        
        # Determine dynamic characteristics
        dynamic_characteristics = {
            MusicalMood.NEUTRAL: {"range": "medium", "typical": "mf", "variation": "medium"},
            MusicalMood.ENERGETIC: {"range": "wide", "typical": "mf-f", "variation": "high"},
            MusicalMood.CHAOTIC: {"range": "very_wide", "typical": "p-ff", "variation": "very_high"},
            MusicalMood.RAW: {"range": "wide", "typical": "mf-ff", "variation": "medium"},
            MusicalMood.AGGRESSIVE: {"range": "wide", "typical": "f-ff", "variation": "high"},
            MusicalMood.MELANCHOLIC: {"range": "medium", "typical": "p-mf", "variation": "low"},
            MusicalMood.PEACEFUL: {"range": "narrow", "typical": "p-mp", "variation": "low"},
            MusicalMood.DRAMATIC: {"range": "very_wide", "typical": "pp-ff", "variation": "very_high"},
            MusicalMood.FUNKY: {"range": "wide", "typical": "mf-f", "variation": "high"},
            MusicalMood.JAZZY: {"range": "wide", "typical": "mp-f", "variation": "high"},
            MusicalMood.ROCK: {"range": "wide", "typical": "f-ff", "variation": "medium"}
        }.get(mood, {"range": "medium", "typical": "mf", "variation": "medium"})
        
        return dynamic_characteristics
    
    def _enhance_with_mood(self, characteristics: StyleCharacteristics, mood: MusicalMood) -> StyleCharacteristics:
        """Enhance style characteristics with mood information"""
        enhanced = StyleCharacteristics(
            artist=characteristics.artist,
            characteristics=characteristics.characteristics.copy(),
            tempo_range=characteristics.tempo_range,
            key_preferences=characteristics.key_preferences.copy(),
            rhythmic_patterns=characteristics.rhythmic_patterns.copy(),
            dynamic_range=characteristics.dynamic_range,
            technique_characteristics=characteristics.technique_characteristics.copy(),
            harmonic_preferences=characteristics.harmonic_preferences.copy(),
            melodic_preferences=characteristics.melodic_preferences.copy()
        )
        
        # Add mood-specific characteristics
        mood_enhancements = {
            MusicalMood.NEUTRAL: ["standard", "balanced", "moderate", "regular"],
            MusicalMood.ENERGETIC: ["fast", "intense", "driving", "powerful"],
            MusicalMood.CHAOTIC: ["unpredictable", "complex", "irregular", "wild"],
            MusicalMood.RAW: ["unpolished", "gritty", "aggressive", "rough"],
            MusicalMood.AGGRESSIVE: ["heavy", "intense", "powerful", "harsh"],
            MusicalMood.MELANCHOLIC: ["slow", "sustained", "emotional", "dark"],
            MusicalMood.PEACEFUL: ["smooth", "gentle", "soft", "calm"],
            MusicalMood.DRAMATIC: ["varied", "dynamic", "epic", "theatrical"],
            MusicalMood.FUNKY: ["groovy", "syncopated", "rhythmic", "bouncy"],
            MusicalMood.JAZZY: ["sophisticated", "swing", "smooth", "cool"],
            MusicalMood.ROCK: ["driving", "powerful", "aggressive", "loud"]
        }
        
        if mood in mood_enhancements:
            enhanced.characteristics.extend(mood_enhancements[mood])
        
        return enhanced
    
    def _enhance_with_complexity(self, characteristics: StyleCharacteristics, complexity: MusicalComplexity) -> StyleCharacteristics:
        """Enhance style characteristics with complexity information"""
        enhanced = StyleCharacteristics(
            artist=characteristics.artist,
            characteristics=characteristics.characteristics.copy(),
            tempo_range=characteristics.tempo_range,
            key_preferences=characteristics.key_preferences.copy(),
            rhythmic_patterns=characteristics.rhythmic_patterns.copy(),
            dynamic_range=characteristics.dynamic_range,
            technique_characteristics=characteristics.technique_characteristics.copy(),
            harmonic_preferences=characteristics.harmonic_preferences.copy(),
            melodic_preferences=characteristics.melodic_preferences.copy()
        )
        
        # Add complexity-specific characteristics
        complexity_enhancements = {
            MusicalComplexity.SIMPLE: ["simple", "basic", "minimal", "clean"],
            MusicalComplexity.MEDIUM: ["balanced", "standard", "moderate"],
            MusicalComplexity.COMPLEX: ["complex", "intricate", "sophisticated", "detailed"],
            MusicalComplexity.EXPERT: ["advanced", "master", "professional", "virtuoso"]
        }
        
        if complexity in complexity_enhancements:
            enhanced.characteristics.extend(complexity_enhancements[complexity])
        
        return enhanced
    
    def _enhance_with_instrument(self, characteristics: StyleCharacteristics, instrument: str) -> StyleCharacteristics:
        """Enhance style characteristics with instrument information"""
        enhanced = StyleCharacteristics(
            artist=characteristics.artist,
            characteristics=characteristics.characteristics.copy(),
            tempo_range=characteristics.tempo_range,
            key_preferences=characteristics.key_preferences.copy(),
            rhythmic_patterns=characteristics.rhythmic_patterns.copy(),
            dynamic_range=characteristics.dynamic_range,
            technique_characteristics=characteristics.technique_characteristics.copy(),
            harmonic_preferences=characteristics.harmonic_preferences.copy(),
            melodic_preferences=characteristics.melodic_preferences.copy()
        )
        
        # Add instrument-specific characteristics
        if instrument in self.instrument_characteristics:
            instrument_info = self.instrument_characteristics[instrument]
            enhanced.technique_characteristics.extend(instrument_info["typical_techniques"])
        
        return enhanced
    
    def _note_to_midi(self, note: str) -> int:
        """Convert note name to MIDI number"""
        note_map = {
            "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
            "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
        }
        
        # Extract note and octave
        note_match = re.match(r"([A-G][#b]?)(\d+)", note)
        if note_match:
            note_name = note_match.group(1)
            octave = int(note_match.group(2))
            return note_map.get(note_name, 0) + (octave + 1) * 12
        else:
            # Default to C4
            return 60
    
    def _get_chord_tones(self, scale_notes: List[int], mode: str) -> List[int]:
        """Get chord tones from scale"""
        if mode == "major":
            # Major scale chord tones: 1, 3, 5
            return [scale_notes[0], scale_notes[2], scale_notes[4]]
        else:
            # Minor scale chord tones: 1, 3, 5
            return [scale_notes[0], scale_notes[2], scale_notes[4]]
    
    def _get_passing_tones(self, scale_notes: List[int]) -> List[int]:
        """Get passing tones from scale"""
        # All scale notes except chord tones
        chord_tones = self._get_chord_tones(scale_notes, "major")
        return [note for note in scale_notes if note not in chord_tones]