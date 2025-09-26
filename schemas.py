"""
Dynamic Musical Intent Representation System

This module provides a flexible, context-aware system for capturing and representing
musical intent that can grow organically with musical concepts rather than being
constrained by rigid schemas.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class IntentType(str, Enum):
    """Types of musical intent that can be captured."""
    RHYTHMIC = "rhythmic"
    HARMONIC = "harmonic"
    MELODIC = "melodic"
    TIMBRAL = "timbral"
    STRUCTURAL = "structural"
    EMOTIONAL = "emotional"
    STYLISTIC = "stylistic"
    DYNAMIC = "dynamic"
    TEXTURAL = "textural"
    CUSTOM = "custom"


class IntentConfidence(str, Enum):
    """Confidence levels for captured intent."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    EXPLORATORY = "exploratory"


class MusicalIntent(BaseModel):
    """
    A single piece of musical intent with context awareness.
    
    This is the atomic unit of musical intent - flexible enough to capture
    any musical concept while maintaining structure for processing.
    """
    # Core identification
    intent_type: IntentType = Field(..., description="The type of musical intent")
    concept: str = Field(..., description="The musical concept (e.g., 'swung eighths', 'jazz sevenths')")
    
    # Context and relationships
    context: Dict[str, Any] = Field(default_factory=dict, description="Contextual information that affects interpretation")
    relationships: List[str] = Field(default_factory=list, description="Other intents this relates to")
    
    # Confidence and source
    confidence: IntentConfidence = Field(default=IntentConfidence.MEDIUM, description="Confidence in this intent")
    source: str = Field(..., description="How this intent was captured (e.g., 'user_input', 'inferred', 'conversation')")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now, description="When this intent was captured")
    tags: List[str] = Field(default_factory=list, description="Searchable tags for this intent")
    
    # Flexible data storage
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional structured data for this intent")
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MusicalContext(BaseModel):
    """
    The broader musical context that affects how intents are interpreted.
    
    This provides the situational awareness needed for context-aware
    musical term resolution.
    """
    # Project context
    project_name: Optional[str] = Field(None, description="Name of the musical project")
    tempo: Optional[int] = Field(None, description="Project tempo in BPM")
    key_signature: Optional[str] = Field(None, description="Project key signature")
    time_signature: Optional[str] = Field(None, description="Project time signature")
    
    # Musical style context
    genre: Optional[str] = Field(None, description="Musical genre or style")
    era: Optional[str] = Field(None, description="Musical era or period")
    cultural_context: Optional[str] = Field(None, description="Cultural or regional context")
    
    # Instrumentation context
    existing_instruments: List[str] = Field(default_factory=list, description="Instruments already in the project")
    target_instrument: Optional[str] = Field(None, description="Instrument we're generating for")
    
    # Emotional and stylistic context
    mood: Optional[str] = Field(None, description="Overall mood or emotional character")
    energy_level: Optional[str] = Field(None, description="Energy level (low, medium, high)")
    
    # Conversation context
    conversation_history: List[str] = Field(default_factory=list, description="Recent conversation topics")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User's musical preferences")
    
    # Technical context
    daw: Optional[str] = Field(None, description="Digital Audio Workstation being used")
    session_state: Optional[str] = Field(None, description="Current state of the session")


class IntentCollection(BaseModel):
    """
    A collection of musical intents that can be processed together.
    
    This represents the complete musical intent for a generation task,
    maintaining relationships between different musical elements.
    """
    # Core intents
    intents: List[MusicalIntent] = Field(default_factory=list, description="All captured musical intents")
    
    # Context
    context: MusicalContext = Field(default_factory=MusicalContext, description="Musical context for interpretation")
    
    # Processing metadata
    generation_id: str = Field(..., description="Unique identifier for this generation session")
    created_at: datetime = Field(default_factory=datetime.now, description="When this collection was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When this collection was last updated")
    
    # Intent relationships
    intent_graph: Dict[str, List[str]] = Field(default_factory=dict, description="Graph of intent relationships")
    
    def add_intent(self, intent: MusicalIntent) -> None:
        """Add a new intent to the collection."""
        self.intents.append(intent)
        self.updated_at = datetime.now()
        
        # Update relationships
        for related_intent in intent.relationships:
            if related_intent not in self.intent_graph:
                self.intent_graph[related_intent] = []
            self.intent_graph[related_intent].append(intent.concept)
    
    def get_intents_by_type(self, intent_type: IntentType) -> List[MusicalIntent]:
        """Get all intents of a specific type."""
        return [intent for intent in self.intents if intent.intent_type == intent_type]
    
    def get_related_intents(self, concept: str) -> List[MusicalIntent]:
        """Get all intents related to a specific concept."""
        related_concepts = self.intent_graph.get(concept, [])
        return [intent for intent in self.intents if intent.concept in related_concepts]
    
    def to_conversation_context(self) -> str:
        """Convert the intent collection to a conversational context string."""
        context_parts = []
        
        # Add basic context
        if self.context.tempo:
            context_parts.append(f"Tempo: {self.context.tempo} BPM")
        if self.context.key_signature:
            context_parts.append(f"Key: {self.context.key_signature}")
        if self.context.genre:
            context_parts.append(f"Style: {self.context.genre}")
        
        # Add intents by type
        for intent_type in IntentType:
            type_intents = self.get_intents_by_type(intent_type)
            if type_intents:
                concepts = [intent.concept for intent in type_intents]
                context_parts.append(f"{intent_type.value.title()}: {', '.join(concepts)}")
        
        return " | ".join(context_parts)


class IntentParser:
    """
    Parses natural language musical descriptions into structured intents.
    
    This class handles the conversion from conversational musical language
    to structured intent objects, with context awareness.
    """
    
    def __init__(self, context: MusicalContext):
        self.context = context
        self.intent_patterns = self._build_intent_patterns()
    
    def _build_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Build patterns for recognizing different types of musical intent."""
        return {
            IntentType.RHYTHMIC: [
                "rhythm", "beat", "groove", "feel", "timing", "syncopation",
                "straight", "swung", "eighths", "sixteenths", "triplets"
            ],
            IntentType.HARMONIC: [
                "chord", "harmony", "progression", "key", "scale", "mode",
                "major", "minor", "seventh", "ninth", "suspended", "diminished"
            ],
            IntentType.MELODIC: [
                "melody", "line", "phrase", "contour", "motion", "interval",
                "ascending", "descending", "leap", "step", "ornament"
            ],
            IntentType.TIMBRAL: [
                "sound", "tone", "timbre", "instrument", "articulation",
                "legato", "staccato", "marcato", "pizzicato", "muted"
            ],
            IntentType.STRUCTURAL: [
                "form", "section", "verse", "chorus", "bridge", "intro", "outro",
                "AABA", "ABAB", "through-composed"
            ],
            IntentType.EMOTIONAL: [
                "mood", "feeling", "emotion", "atmosphere", "character",
                "happy", "sad", "mysterious", "energetic", "calm"
            ],
            IntentType.STYLISTIC: [
                "style", "genre", "era", "period", "tradition",
                "jazz", "classical", "rock", "funk", "blues"
            ],
            IntentType.DYNAMIC: [
                "volume", "dynamics", "crescendo", "diminuendo", "forte", "piano",
                "loud", "soft", "accent", "emphasis"
            ],
            IntentType.TEXTURAL: [
                "texture", "density", "thickness", "sparse", "busy", "layered",
                "monophonic", "polyphonic", "homophonic"
            ]
        }
    
    def parse_intent(self, text: str, source: str = "user_input") -> List[MusicalIntent]:
        """
        Parse natural language text into musical intents.
        
        Args:
            text: The natural language description
            source: How this intent was captured
            
        Returns:
            List of parsed MusicalIntent objects
        """
        intents = []
        text_lower = text.lower()
        
        # Find intent types mentioned in the text
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    # Extract the concept around the pattern
                    concept = self._extract_concept(text, pattern)
                    if concept:
                        intent = MusicalIntent(
                            intent_type=intent_type,
                            concept=concept,
                            context=self._build_intent_context(intent_type, concept),
                            source=source,
                            confidence=self._assess_confidence(text, pattern)
                        )
                        intents.append(intent)
        
        # Handle custom intents not captured by patterns
        if not intents:
            intent = MusicalIntent(
                intent_type=IntentType.CUSTOM,
                concept=text.strip(),
                context=self.context.dict(),
                source=source,
                confidence=IntentConfidence.EXPLORATORY
            )
            intents.append(intent)
        
        return intents
    
    def _extract_concept(self, text: str, pattern: str) -> Optional[str]:
        """Extract the musical concept around a pattern."""
        # Simple extraction - in a real implementation, this would be more sophisticated
        words = text.split()
        pattern_words = pattern.split()
        
        for i, word in enumerate(words):
            if any(pw in word.lower() for pw in pattern_words):
                # Extract surrounding context
                start = max(0, i - 2)
                end = min(len(words), i + 3)
                concept = " ".join(words[start:end])
                return concept.strip()
        
        return None
    
    def _build_intent_context(self, intent_type: IntentType, concept: str) -> Dict[str, Any]:
        """Build context for a specific intent."""
        context = self.context.dict()
        context.update({
            "intent_type": intent_type.value,
            "concept": concept,
            "parsed_at": datetime.now().isoformat()
        })
        return context
    
    def _assess_confidence(self, text: str, pattern: str) -> IntentConfidence:
        """Assess confidence in the parsed intent."""
        # Simple confidence assessment
        if pattern in text.lower():
            return IntentConfidence.HIGH
        elif any(word in text.lower() for word in pattern.split()):
            return IntentConfidence.MEDIUM
        else:
            return IntentConfidence.LOW


# Convenience functions for common operations
def create_intent_collection(generation_id: str, context: Optional[MusicalContext] = None) -> IntentCollection:
    """Create a new intent collection."""
    if context is None:
        context = MusicalContext()
    return IntentCollection(generation_id=generation_id, context=context)


def parse_musical_description(text: str, context: MusicalContext, source: str = "user_input") -> IntentCollection:
    """Parse a musical description into an intent collection."""
    parser = IntentParser(context)
    intents = parser.parse_intent(text, source)
    
    collection = create_intent_collection(f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}", context)
    for intent in intents:
        collection.add_intent(intent)
    
    return collection
