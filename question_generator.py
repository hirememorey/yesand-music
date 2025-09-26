"""
Dynamic Musical Question Generator

This module provides context-aware question generation for musical conversations,
replacing rigid field-path question banks with adaptive, conversational questioning.
"""

from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence


class QuestionType(str, Enum):
    """Types of questions that can be generated."""
    CLARIFYING = "clarifying"
    EXPLORATORY = "exploratory"
    CONTEXTUAL = "contextual"
    TECHNICAL = "technical"
    EMOTIONAL = "emotional"
    STYLISTIC = "stylistic"


class QuestionPriority(str, Enum):
    """Priority levels for questions."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class MusicalQuestion:
    """A dynamically generated musical question."""
    question: str
    question_type: QuestionType
    priority: QuestionPriority
    context: Dict[str, Any]
    suggested_follow_ups: List[str]
    musical_focus: str  # What musical aspect this question explores
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "question": self.question,
            "type": self.question_type,
            "priority": self.priority,
            "context": self.context,
            "suggested_follow_ups": self.suggested_follow_ups,
            "musical_focus": self.musical_focus
        }


class MusicalQuestionGenerator:
    """
    Generates context-aware musical questions that adapt to the conversation
    and musical context, rather than using rigid field-path mappings.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.question_patterns = self._build_question_patterns()
        self.musical_language_patterns = self._build_musical_language_patterns()
    
    def _build_question_patterns(self) -> Dict[QuestionType, List[str]]:
        """Build patterns for different types of musical questions."""
        return {
            QuestionType.CLARIFYING: [
                "Could you tell me more about {concept}?",
                "What do you mean by {concept}?",
                "I want to make sure I understand - when you say {concept}, are you thinking...?",
                "Let me clarify - {concept} in what way?"
            ],
            QuestionType.EXPLORATORY: [
                "What kind of {musical_element} are you imagining?",
                "How do you want the {musical_element} to feel?",
                "What's the character of the {musical_element}?",
                "What mood should the {musical_element} convey?"
            ],
            QuestionType.CONTEXTUAL: [
                "Given that you're working in {style}, how should the {musical_element} sound?",
                "Since this is {genre}, what {musical_element} approach fits best?",
                "With a {tempo} tempo, what {musical_element} works?",
                "In {key}, what {musical_element} would you like?"
            ],
            QuestionType.TECHNICAL: [
                "What {technical_aspect} are you thinking?",
                "How complex should the {technical_aspect} be?",
                "What {technical_aspect} techniques do you want to use?",
                "What {technical_aspect} approach fits your vision?"
            ],
            QuestionType.EMOTIONAL: [
                "What feeling should this convey?",
                "What's the emotional character you're going for?",
                "How should this make the listener feel?",
                "What atmosphere are you creating?"
            ],
            QuestionType.STYLISTIC: [
                "What style or genre are you working in?",
                "What musical tradition does this draw from?",
                "What era or period influences this?",
                "What cultural context shapes this?"
            ]
        }
    
    def _build_musical_language_patterns(self) -> Dict[str, List[str]]:
        """Build musical language patterns for natural conversation."""
        return {
            "rhythmic_elements": [
                "groove", "feel", "rhythm", "beat", "timing", "pulse",
                "syncopation", "swing", "straight", "complex", "simple"
            ],
            "harmonic_elements": [
                "harmony", "chords", "progression", "key", "tonality",
                "dissonance", "consonance", "tension", "resolution"
            ],
            "melodic_elements": [
                "melody", "line", "phrase", "motion", "contour",
                "intervals", "leaps", "steps", "ornamentation"
            ],
            "timbral_elements": [
                "sound", "tone", "timbre", "texture", "color",
                "articulation", "attack", "decay", "sustain"
            ],
            "structural_elements": [
                "form", "section", "arrangement", "development",
                "verse", "chorus", "bridge", "intro", "outro"
            ],
            "emotional_descriptors": [
                "mysterious", "dark", "bright", "aggressive", "gentle",
                "energetic", "calm", "tense", "relaxed", "dramatic"
            ],
            "style_descriptors": [
                "jazz", "classical", "rock", "funk", "blues",
                "fusion", "experimental", "traditional", "modern"
            ]
        }
    
    def generate_questions(
        self, 
        current_context: MusicalContext,
        recent_intents: List[MusicalIntent],
        conversation_stage: str = "early"
    ) -> List[MusicalQuestion]:
        """
        Generate contextually appropriate questions based on the current state.
        
        Args:
            current_context: Current musical context
            recent_intents: Recently captured intents
            conversation_stage: Stage of conversation (early, building, refining, complete)
            
        Returns:
            List of generated questions, ordered by priority
        """
        questions = []
        
        # Generate questions based on conversation stage
        if conversation_stage == "early":
            questions.extend(self._generate_early_questions(current_context))
        elif conversation_stage == "building":
            questions.extend(self._generate_building_questions(current_context, recent_intents))
        elif conversation_stage == "refining":
            questions.extend(self._generate_refining_questions(current_context, recent_intents))
        
        # Generate questions based on missing context
        questions.extend(self._generate_context_questions(current_context))
        
        # Generate questions based on recent intents
        questions.extend(self._generate_intent_questions(recent_intents))
        
        # Sort by priority and return
        questions.sort(key=lambda q: self._get_priority_score(q.priority), reverse=True)
        return questions[:5]  # Return top 5 questions
    
    def _generate_early_questions(self, context: MusicalContext) -> List[MusicalQuestion]:
        """Generate questions for early conversation stage."""
        questions = []
        
        if not context.genre:
            questions.append(MusicalQuestion(
                question="What kind of musical style are you working in?",
                question_type=QuestionType.STYLISTIC,
                priority=QuestionPriority.HIGH,
                context={"missing": "genre"},
                suggested_follow_ups=["jazz", "rock", "classical", "electronic", "other"],
                musical_focus="style"
            ))
        
        if not context.tempo:
            questions.append(MusicalQuestion(
                question="What tempo are you thinking for this piece?",
                question_type=QuestionType.TECHNICAL,
                priority=QuestionPriority.HIGH,
                context={"missing": "tempo"},
                suggested_follow_ups=["slow (60-80)", "medium (100-120)", "fast (140+)"],
                musical_focus="rhythm"
            ))
        
        if not context.target_instrument:
            questions.append(MusicalQuestion(
                question="What instrument are you generating this for?",
                question_type=QuestionType.TECHNICAL,
                priority=QuestionPriority.HIGH,
                context={"missing": "instrument"},
                suggested_follow_ups=["piano", "guitar", "bass", "drums", "strings", "other"],
                musical_focus="instrumentation"
            ))
        
        return questions
    
    def _generate_building_questions(self, context: MusicalContext, intents: List[MusicalIntent]) -> List[MusicalQuestion]:
        """Generate questions for building musical ideas."""
        questions = []
        
        # Check what musical elements are missing
        present_types = {intent.intent_type for intent in intents}
        
        if IntentType.RHYTHMIC not in present_types:
            questions.append(MusicalQuestion(
                question="What kind of rhythmic feel are you going for?",
                question_type=QuestionType.EXPLORATORY,
                priority=QuestionPriority.MEDIUM,
                context={"missing": "rhythm"},
                suggested_follow_ups=["straight", "swung", "syncopated", "complex", "simple"],
                musical_focus="rhythm"
            ))
        
        if IntentType.HARMONIC not in present_types:
            questions.append(MusicalQuestion(
                question="What harmonic approach fits your vision?",
                question_type=QuestionType.EXPLORATORY,
                priority=QuestionPriority.MEDIUM,
                context={"missing": "harmony"},
                suggested_follow_ups=["simple triads", "jazz chords", "modal", "atonal"],
                musical_focus="harmony"
            ))
        
        if IntentType.MELODIC not in present_types:
            questions.append(MusicalQuestion(
                question="What kind of melodic character do you want?",
                question_type=QuestionType.EXPLORATORY,
                priority=QuestionPriority.MEDIUM,
                context={"missing": "melody"},
                suggested_follow_ups=["sparse", "busy", "ascending", "descending", "angular"],
                musical_focus="melody"
            ))
        
        return questions
    
    def _generate_refining_questions(self, context: MusicalContext, intents: List[MusicalIntent]) -> List[MusicalQuestion]:
        """Generate questions for refining musical ideas."""
        questions = []
        
        # Look for low-confidence intents that need clarification
        for intent in intents:
            if intent.confidence == IntentConfidence.LOW:
                questions.append(MusicalQuestion(
                    question=f"Could you tell me more about what you mean by '{intent.concept}'?",
                    question_type=QuestionType.CLARIFYING,
                    priority=QuestionPriority.HIGH,
                    context={"intent": intent.concept, "confidence": "low"},
                    suggested_follow_ups=["Give me an example", "What style is this?", "How should it sound?"],
                    musical_focus=intent.intent_type
                ))
        
        # Look for custom intents that need exploration
        for intent in intents:
            if intent.intent_type == IntentType.CUSTOM:
                questions.append(MusicalQuestion(
                    question=f"Tell me more about '{intent.concept}' - what musical aspect are you focusing on?",
                    question_type=QuestionType.EXPLORATORY,
                    priority=QuestionPriority.MEDIUM,
                    context={"intent": intent.concept, "type": "custom"},
                    suggested_follow_ups=["rhythm", "harmony", "melody", "timbre", "structure"],
                    musical_focus="general"
                ))
        
        return questions
    
    def _generate_context_questions(self, context: MusicalContext) -> List[MusicalQuestion]:
        """Generate questions based on missing context."""
        questions = []
        
        if not context.key_signature:
            questions.append(MusicalQuestion(
                question="What key signature are you working in?",
                question_type=QuestionType.TECHNICAL,
                priority=QuestionPriority.MEDIUM,
                context={"missing": "key"},
                suggested_follow_ups=["C Major", "G Minor", "F# Major", "other"],
                musical_focus="harmony"
            ))
        
        if not context.mood:
            questions.append(MusicalQuestion(
                question="What mood or feeling should this convey?",
                question_type=QuestionType.EMOTIONAL,
                priority=QuestionPriority.MEDIUM,
                context={"missing": "mood"},
                suggested_follow_ups=["mysterious", "bright", "aggressive", "gentle", "dramatic"],
                musical_focus="emotional"
            ))
        
        return questions
    
    def _generate_intent_questions(self, intents: List[MusicalIntent]) -> List[MusicalQuestion]:
        """Generate questions based on recent intents."""
        questions = []
        
        # Look for intents that could be expanded
        for intent in intents:
            if intent.intent_type == IntentType.RHYTHMIC:
                questions.append(MusicalQuestion(
                    question=f"How complex should the rhythm be?",
                    question_type=QuestionType.TECHNICAL,
                    priority=QuestionPriority.LOW,
                    context={"intent": intent.concept},
                    suggested_follow_ups=["simple", "moderate", "complex", "very complex"],
                    musical_focus="rhythm"
                ))
            
            elif intent.intent_type == IntentType.HARMONIC:
                questions.append(MusicalQuestion(
                    question=f"What harmonic techniques should we use?",
                    question_type=QuestionType.TECHNICAL,
                    priority=QuestionPriority.LOW,
                    context={"intent": intent.concept},
                    suggested_follow_ups=["basic triads", "jazz chords", "modal harmony", "extended chords"],
                    musical_focus="harmony"
                ))
        
        return questions
    
    def _get_priority_score(self, priority: QuestionPriority) -> int:
        """Get numeric score for priority sorting."""
        return {
            QuestionPriority.HIGH: 3,
            QuestionPriority.MEDIUM: 2,
            QuestionPriority.LOW: 1
        }[priority]
    
    def generate_follow_up_question(
        self, 
        user_response: str, 
        original_question: MusicalQuestion,
        context: MusicalContext
    ) -> Optional[MusicalQuestion]:
        """Generate a follow-up question based on user response."""
        # Simple follow-up logic - in a real implementation, this would be more sophisticated
        if "not sure" in user_response.lower() or "don't know" in user_response.lower():
            return MusicalQuestion(
                question="Let me help you explore this - what musical examples inspire you?",
                question_type=QuestionType.EXPLORATORY,
                priority=QuestionPriority.MEDIUM,
                context={"follow_up": "uncertainty"},
                suggested_follow_ups=["jazz artists", "classical composers", "rock bands", "other genres"],
                musical_focus=original_question.musical_focus
            )
        
        return None


class ConversationalQuestionFlow:
    """
    Manages the flow of questions in a musical conversation,
    ensuring questions build naturally on each other.
    """
    
    def __init__(self):
        self.question_generator = MusicalQuestionGenerator()
        self.conversation_stage = "early"
        self.asked_questions: List[str] = []
        self.user_responses: List[Dict[str, Any]] = []
    
    def get_next_question(
        self, 
        context: MusicalContext, 
        recent_intents: List[MusicalIntent]
    ) -> Optional[MusicalQuestion]:
        """Get the next question in the conversation flow."""
        # Update conversation stage based on context
        self._update_conversation_stage(context, recent_intents)
        
        # Generate questions
        questions = self.question_generator.generate_questions(
            context, recent_intents, self.conversation_stage
        )
        
        # Filter out already asked questions
        available_questions = [
            q for q in questions 
            if q.question not in self.asked_questions
        ]
        
        if not available_questions:
            return None
        
        # Return the highest priority question
        next_question = available_questions[0]
        self.asked_questions.append(next_question.question)
        
        return next_question
    
    def _update_conversation_stage(self, context: MusicalContext, intents: List[MusicalIntent]) -> None:
        """Update the conversation stage based on current state."""
        if not context.tempo or not context.target_instrument:
            self.conversation_stage = "early"
        elif len(intents) < 3:
            self.conversation_stage = "building"
        elif len(intents) >= 3:
            self.conversation_stage = "refining"
        else:
            self.conversation_stage = "complete"
    
    def record_response(self, question: MusicalQuestion, response: str) -> None:
        """Record a user response to a question."""
        self.user_responses.append({
            "question": question.question,
            "response": response,
            "timestamp": datetime.now(),
            "musical_focus": question.musical_focus
        })


# Convenience functions
def generate_musical_questions(
    context: MusicalContext, 
    intents: List[MusicalIntent],
    stage: str = "early"
) -> List[MusicalQuestion]:
    """Generate musical questions for a given context."""
    generator = MusicalQuestionGenerator()
    return generator.generate_questions(context, intents, stage)


def start_question_flow() -> ConversationalQuestionFlow:
    """Start a new conversational question flow."""
    return ConversationalQuestionFlow()
