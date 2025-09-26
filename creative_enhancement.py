"""
Context-Aware Creative Enhancement System

This module provides musical creativity through understanding rather than
chaos mutations, working with discovered musical intents and conversational
context to suggest creative variations and generate rich prompts.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import random

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence, IntentCollection
from intent_parser import ConversationalIntentParser


class MusicalCreativityEngine:
    """
    A context-aware creative enhancement system that suggests musical variations
    based on understanding musical principles and relationships rather than
    random mutations.
    """
    
    def __init__(self):
        self.musical_principles = self._build_musical_principles()
        self.creative_patterns = self._build_creative_patterns()
        self.style_enhancements = self._build_style_enhancements()
    
    def _build_musical_principles(self) -> Dict[str, List[str]]:
        """Build musical principles for creative enhancement."""
        return {
            "rhythmic_enhancements": [
                "add syncopation",
                "introduce polyrhythms",
                "vary note density",
                "add rhythmic displacement",
                "create call and response patterns"
            ],
            "harmonic_enhancements": [
                "add chord extensions",
                "introduce modal interchange",
                "create harmonic rhythm variation",
                "add passing chords",
                "use secondary dominants"
            ],
            "melodic_enhancements": [
                "add melodic ornamentation",
                "create melodic sequences",
                "vary melodic contour",
                "add chromatic passing tones",
                "create melodic development"
            ],
            "textural_enhancements": [
                "vary register placement",
                "add countermelodies",
                "create textural layers",
                "vary articulation",
                "add dynamic contrast"
            ],
            "structural_enhancements": [
                "add transitional material",
                "create formal variation",
                "add developmental sections",
                "create motivic development",
                "add structural contrast"
            ]
        }
    
    def _build_creative_patterns(self) -> Dict[str, List[str]]:
        """Build creative patterns based on musical styles and contexts."""
        return {
            "jazz_enhancements": [
                "add jazz articulation",
                "introduce swing feel",
                "add blue notes",
                "create bebop lines",
                "add jazz harmony"
            ],
            "classical_enhancements": [
                "add classical ornamentation",
                "create motivic development",
                "add contrapuntal elements",
                "vary dynamics expressively",
                "add classical phrasing"
            ],
            "rock_enhancements": [
                "add power chords",
                "create driving rhythms",
                "add distortion effects",
                "create anthemic melodies",
                "add rock articulation"
            ],
            "electronic_enhancements": [
                "add electronic textures",
                "create rhythmic patterns",
                "add filter sweeps",
                "create arpeggiated patterns",
                "add electronic effects"
            ]
        }
    
    def _build_style_enhancements(self) -> Dict[str, Dict[str, List[str]]]:
        """Build style-specific enhancement patterns."""
        return {
            "mysterious": {
                "harmonic": ["add minor chords", "use diminished chords", "add chromaticism"],
                "melodic": ["use descending lines", "add tritones", "create tension"],
                "rhythmic": ["add rubato", "use irregular patterns", "create suspense"]
            },
            "aggressive": {
                "harmonic": ["use power chords", "add dissonance", "create tension"],
                "melodic": ["use wide intervals", "add chromaticism", "create intensity"],
                "rhythmic": ["use driving patterns", "add syncopation", "create energy"]
            },
            "gentle": {
                "harmonic": ["use major chords", "add extensions", "create warmth"],
                "melodic": ["use stepwise motion", "add smooth lines", "create flow"],
                "rhythmic": ["use flowing patterns", "add rubato", "create relaxation"]
            }
        }
    
    def suggest_creative_enhancements(
        self, 
        intent_collection: IntentCollection,
        enhancement_level: str = "medium"
    ) -> List[Dict[str, Any]]:
        """
        Suggest creative enhancements based on discovered musical intents.
        
        Args:
            intent_collection: The discovered musical intents
            enhancement_level: Level of enhancement (low, medium, high)
            
        Returns:
            List of suggested creative enhancements
        """
        enhancements = []
        
        # Analyze the musical context
        context = intent_collection.context
        intents = intent_collection.intents
        
        # Get enhancement patterns based on style
        style_enhancements = self._get_style_enhancements(context, intents)
        
        # Get enhancement patterns based on musical elements
        element_enhancements = self._get_element_enhancements(intents)
        
        # Combine and prioritize enhancements
        all_enhancements = style_enhancements + element_enhancements
        
        # Filter by enhancement level
        filtered_enhancements = self._filter_by_level(all_enhancements, enhancement_level)
        
        # Add contextual reasoning
        for enhancement in filtered_enhancements:
            enhancement["reasoning"] = self._generate_enhancement_reasoning(
                enhancement, context, intents
            )
        
        return filtered_enhancements[:5]  # Return top 5 enhancements
    
    def _get_style_enhancements(
        self, 
        context: MusicalContext, 
        intents: List[MusicalIntent]
    ) -> List[Dict[str, Any]]:
        """Get style-based enhancements."""
        enhancements = []
        
        # Get genre-based enhancements
        if context.genre:
            genre_enhancements = self.creative_patterns.get(
                f"{context.genre.lower()}_enhancements", []
            )
            for enhancement in genre_enhancements:
                enhancements.append({
                    "type": "style",
                    "enhancement": enhancement,
                    "category": "genre",
                    "priority": "medium",
                    "context": f"Based on {context.genre} style"
                })
        
        # Get mood-based enhancements
        if context.mood:
            mood_enhancements = self.style_enhancements.get(context.mood, {})
            for category, enhancement_list in mood_enhancements.items():
                for enhancement in enhancement_list:
                    enhancements.append({
                        "type": "style",
                        "enhancement": enhancement,
                        "category": category,
                        "priority": "high",
                        "context": f"To enhance {context.mood} mood"
                    })
        
        return enhancements
    
    def _get_element_enhancements(self, intents: List[MusicalIntent]) -> List[Dict[str, Any]]:
        """Get element-based enhancements."""
        enhancements = []
        
        # Group intents by type
        intent_groups = {}
        for intent in intents:
            if intent.intent_type not in intent_groups:
                intent_groups[intent.intent_type] = []
            intent_groups[intent.intent_type].append(intent)
        
        # Get enhancements for each element type
        for intent_type, type_intents in intent_groups.items():
            if intent_type == IntentType.RHYTHMIC:
                enhancements.extend(self._get_rhythmic_enhancements(type_intents))
            elif intent_type == IntentType.HARMONIC:
                enhancements.extend(self._get_harmonic_enhancements(type_intents))
            elif intent_type == IntentType.MELODIC:
                enhancements.extend(self._get_melodic_enhancements(type_intents))
            elif intent_type == IntentType.TIMBRAL:
                enhancements.extend(self._get_timbral_enhancements(type_intents))
        
        return enhancements
    
    def _get_rhythmic_enhancements(self, intents: List[MusicalIntent]) -> List[Dict[str, Any]]:
        """Get rhythmic enhancements based on discovered intents."""
        enhancements = []
        
        for intent in intents:
            if "swung" in intent.concept.lower():
                enhancements.append({
                    "type": "rhythmic",
                    "enhancement": "add rhythmic displacement",
                    "category": "rhythm",
                    "priority": "medium",
                    "context": "To enhance the swung feel"
                })
            elif "syncopated" in intent.concept.lower():
                enhancements.append({
                    "type": "rhythmic",
                    "enhancement": "add polyrhythmic elements",
                    "category": "rhythm",
                    "priority": "medium",
                    "context": "To build on the syncopated foundation"
                })
        
        return enhancements
    
    def _get_harmonic_enhancements(self, intents: List[MusicalIntent]) -> List[Dict[str, Any]]:
        """Get harmonic enhancements based on discovered intents."""
        enhancements = []
        
        for intent in intents:
            if "jazz" in intent.concept.lower():
                enhancements.append({
                    "type": "harmonic",
                    "enhancement": "add chord extensions",
                    "category": "harmony",
                    "priority": "high",
                    "context": "To enhance the jazz harmony"
                })
            elif "seventh" in intent.concept.lower():
                enhancements.append({
                    "type": "harmonic",
                    "enhancement": "add secondary dominants",
                    "category": "harmony",
                    "priority": "medium",
                    "context": "To build on the seventh chord foundation"
                })
        
        return enhancements
    
    def _get_melodic_enhancements(self, intents: List[MusicalIntent]) -> List[Dict[str, Any]]:
        """Get melodic enhancements based on discovered intents."""
        enhancements = []
        
        for intent in intents:
            if "ascending" in intent.concept.lower():
                enhancements.append({
                    "type": "melodic",
                    "enhancement": "add melodic sequences",
                    "category": "melody",
                    "priority": "medium",
                    "context": "To develop the ascending melodic idea"
                })
            elif "sparse" in intent.concept.lower():
                enhancements.append({
                    "type": "melodic",
                    "enhancement": "add melodic ornamentation",
                    "category": "melody",
                    "priority": "low",
                    "context": "To add detail to the sparse melody"
                })
        
        return enhancements
    
    def _get_timbral_enhancements(self, intents: List[MusicalIntent]) -> List[Dict[str, Any]]:
        """Get timbral enhancements based on discovered intents."""
        enhancements = []
        
        for intent in intents:
            if "mysterious" in intent.concept.lower():
                enhancements.append({
                    "type": "timbral",
                    "enhancement": "add reverb and delay",
                    "category": "timbre",
                    "priority": "high",
                    "context": "To enhance the mysterious atmosphere"
                })
            elif "dark" in intent.concept.lower():
                enhancements.append({
                    "type": "timbral",
                    "enhancement": "use lower register",
                    "category": "timbre",
                    "priority": "medium",
                    "context": "To enhance the dark character"
                })
        
        return enhancements
    
    def _filter_by_level(
        self, 
        enhancements: List[Dict[str, Any]], 
        level: str
    ) -> List[Dict[str, Any]]:
        """Filter enhancements by level."""
        if level == "low":
            return [e for e in enhancements if e["priority"] == "low"]
        elif level == "medium":
            return [e for e in enhancements if e["priority"] in ["low", "medium"]]
        else:  # high
            return enhancements
    
    def _generate_enhancement_reasoning(
        self, 
        enhancement: Dict[str, Any], 
        context: MusicalContext, 
        intents: List[MusicalIntent]
    ) -> str:
        """Generate reasoning for why this enhancement makes musical sense."""
        reasoning_parts = []
        
        # Add context-based reasoning
        if context.genre:
            reasoning_parts.append(f"This fits the {context.genre} style")
        
        if context.mood:
            reasoning_parts.append(f"It enhances the {context.mood} mood")
        
        # Add intent-based reasoning
        relevant_intents = [
            intent for intent in intents 
            if intent.intent_type in enhancement["category"]
        ]
        
        if relevant_intents:
            concepts = [intent.concept for intent in relevant_intents]
            reasoning_parts.append(f"It builds on your ideas: {', '.join(concepts)}")
        
        return " and ".join(reasoning_parts) if reasoning_parts else "This enhances the musical expression"


class ContextualPromptGenerator:
    """
    Generates rich, contextual prompts for LLMs based on discovered
    musical intents and conversational context.
    """
    
    def __init__(self):
        self.prompt_templates = self._build_prompt_templates()
    
    def _build_prompt_templates(self) -> Dict[str, str]:
        """Build prompt templates for different musical contexts."""
        return {
            "jazz": """
You are a master jazz musician creating a {target_instrument} part for a {genre} piece.

Musical Context:
- Key: {key_signature}
- Tempo: {tempo} BPM
- Style: {genre}
- Mood: {mood}

Musical Vision:
{musical_vision}

Musical Examples:
{musical_examples}

Creative Enhancements:
{enhancements}

Please create a {length} {target_instrument} part that captures the essence of this musical vision. Focus on the {musical_focus} elements while incorporating the suggested enhancements.
""",
            "classical": """
You are a classical composer creating a {target_instrument} part for a {genre} piece.

Musical Context:
- Key: {key_signature}
- Tempo: {tempo} BPM
- Style: {genre}
- Mood: {mood}

Musical Vision:
{musical_vision}

Musical Examples:
{musical_examples}

Creative Enhancements:
{enhancements}

Please create a {length} {target_instrument} part that demonstrates classical craftsmanship while expressing the musical vision.
""",
            "rock": """
You are a rock musician creating a {target_instrument} part for a {genre} piece.

Musical Context:
- Key: {key_signature}
- Tempo: {tempo} BPM
- Style: {genre}
- Mood: {mood}

Musical Vision:
{musical_vision}

Musical Examples:
{musical_examples}

Creative Enhancements:
{enhancements}

Please create a {length} {target_instrument} part that rocks while capturing the musical vision.
""",
            "default": """
You are a skilled musician creating a {target_instrument} part for a musical piece.

Musical Context:
- Key: {key_signature}
- Tempo: {tempo} BPM
- Style: {genre}
- Mood: {mood}

Musical Vision:
{musical_vision}

Musical Examples:
{musical_examples}

Creative Enhancements:
{enhancements}

Please create a {length} {target_instrument} part that captures the musical vision.
"""
        }
    
    def generate_prompt(
        self, 
        intent_collection: IntentCollection,
        enhancements: List[Dict[str, Any]] = None,
        length: str = "4-bar",
        musical_focus: str = "all elements"
    ) -> str:
        """
        Generate a rich, contextual prompt for LLM generation.
        
        Args:
            intent_collection: The discovered musical intents
            enhancements: Optional creative enhancements
            length: Length of the generated part
            musical_focus: Focus area for generation
            
        Returns:
            Formatted prompt string
        """
        context = intent_collection.context
        
        # Get the appropriate template
        template = self.prompt_templates.get(
            context.genre.lower() if context.genre else "default",
            self.prompt_templates["default"]
        )
        
        # Build musical vision from intents
        musical_vision = self._build_musical_vision(intent_collection)
        
        # Build musical examples
        musical_examples = self._build_musical_examples(intent_collection)
        
        # Build enhancements text
        enhancements_text = self._build_enhancements_text(enhancements or [])
        
        # Format the prompt
        prompt = template.format(
            target_instrument=context.target_instrument or "piano",
            genre=context.genre or "musical",
            key_signature=context.key_signature or "C Major",
            tempo=context.tempo or 120,
            mood=context.mood or "expressive",
            musical_vision=musical_vision,
            musical_examples=musical_examples,
            enhancements=enhancements_text,
            length=length,
            musical_focus=musical_focus
        )
        
        return prompt
    
    def _build_musical_vision(self, intent_collection: IntentCollection) -> str:
        """Build a musical vision description from discovered intents."""
        vision_parts = []
        
        # Group intents by type
        intent_groups = {}
        for intent in intent_collection.intents:
            if intent.intent_type not in intent_groups:
                intent_groups[intent.intent_type] = []
            intent_groups[intent.intent_type].append(intent)
        
        # Build vision for each element type
        for intent_type, intents in intent_groups.items():
            if intent_type == IntentType.RHYTHMIC:
                concepts = [intent.concept for intent in intents]
                vision_parts.append(f"Rhythm: {', '.join(concepts)}")
            elif intent_type == IntentType.HARMONIC:
                concepts = [intent.concept for intent in intents]
                vision_parts.append(f"Harmony: {', '.join(concepts)}")
            elif intent_type == IntentType.MELODIC:
                concepts = [intent.concept for intent in intents]
                vision_parts.append(f"Melody: {', '.join(concepts)}")
            elif intent_type == IntentType.EMOTIONAL:
                concepts = [intent.concept for intent in intents]
                vision_parts.append(f"Emotion: {', '.join(concepts)}")
            elif intent_type == IntentType.TIMBRAL:
                concepts = [intent.concept for intent in intents]
                vision_parts.append(f"Timbre: {', '.join(concepts)}")
        
        return "\n".join(vision_parts) if vision_parts else "Express the musical character"
    
    def _build_musical_examples(self, intent_collection: IntentCollection) -> str:
        """Build musical examples from the conversation context."""
        examples = []
        
        # Get examples from conversation history
        if intent_collection.context.conversation_history:
            for entry in intent_collection.context.conversation_history:
                if "like" in entry.lower() or "similar to" in entry.lower():
                    examples.append(entry)
        
        if examples:
            return "\n".join(f"- {example}" for example in examples[:3])
        else:
            return "No specific examples referenced"
    
    def _build_enhancements_text(self, enhancements: List[Dict[str, Any]]) -> str:
        """Build enhancements text for the prompt."""
        if not enhancements:
            return "No specific enhancements suggested"
        
        enhancement_texts = []
        for enhancement in enhancements:
            text = f"- {enhancement['enhancement']} ({enhancement['reasoning']})"
            enhancement_texts.append(text)
        
        return "\n".join(enhancement_texts)


# Convenience functions
def suggest_musical_enhancements(
    intent_collection: IntentCollection,
    enhancement_level: str = "medium"
) -> List[Dict[str, Any]]:
    """Suggest creative enhancements for a musical intent collection."""
    engine = MusicalCreativityEngine()
    return engine.suggest_creative_enhancements(intent_collection, enhancement_level)


def generate_musical_prompt(
    intent_collection: IntentCollection,
    enhancements: List[Dict[str, Any]] = None,
    length: str = "4-bar",
    musical_focus: str = "all elements"
) -> str:
    """Generate a rich, contextual prompt for musical generation."""
    generator = ContextualPromptGenerator()
    return generator.generate_prompt(intent_collection, enhancements, length, musical_focus)


def demo_creative_enhancement():
    """Demonstrate the creative enhancement system."""
    print("Creative Enhancement System Demo")
    print("=" * 50)
    
    # Create a sample intent collection
    from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence
    
    context = MusicalContext(
        genre="Jazz",
        tempo=120,
        key_signature="G Minor",
        target_instrument="bass",
        mood="mysterious"
    )
    
    intents = [
        MusicalIntent(
            intent_type=IntentType.RHYTHMIC,
            concept="swung eighths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.HARMONIC,
            concept="jazz sevenths",
            source="conversation",
            confidence=IntentConfidence.HIGH
        ),
        MusicalIntent(
            intent_type=IntentType.EMOTIONAL,
            concept="mysterious and dark",
            source="conversation",
            confidence=IntentConfidence.HIGH
        )
    ]
    
    collection = IntentCollection(
        generation_id="demo",
        context=context
    )
    
    for intent in intents:
        collection.add_intent(intent)
    
    # Test creative enhancements
    print("=== Creative Enhancements ===")
    enhancements = suggest_musical_enhancements(collection, "medium")
    
    for i, enhancement in enumerate(enhancements, 1):
        print(f"{i}. {enhancement['enhancement']}")
        print(f"   Type: {enhancement['type']}, Category: {enhancement['category']}")
        print(f"   Reasoning: {enhancement['reasoning']}")
        print()
    
    # Test prompt generation
    print("=== Generated Prompt ===")
    prompt = generate_musical_prompt(collection, enhancements, "4-bar", "rhythm and harmony")
    print(prompt)


if __name__ == "__main__":
    demo_creative_enhancement()
