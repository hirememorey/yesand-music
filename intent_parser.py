"""
Conversational Intent Parser

This module provides conversational parsing of musical intent, integrating
with the existing musical conversation system to capture and structure
musical ideas from natural language.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re
import json

from schemas import (
    MusicalIntent, IntentCollection, MusicalContext, IntentType, 
    IntentConfidence, IntentParser, parse_musical_description
)


class ConversationalIntentParser:
    """
    Advanced conversational parser that understands musical context
    and can extract structured intent from natural language conversations.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_context: Optional[MusicalContext] = None
        self.intent_relationships: Dict[str, List[str]] = {}
        
    def start_conversation(self, initial_context: Optional[MusicalContext] = None) -> str:
        """Start a new musical conversation session."""
        self.conversation_history = []
        self.current_context = initial_context or MusicalContext()
        self.intent_relationships = {}
        
        session_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add initial context to history
        self.conversation_history.append({
            "type": "context_established",
            "timestamp": datetime.now(),
            "context": self.current_context.dict()
        })
        
        return session_id
    
    def process_user_input(self, user_input: str) -> Tuple[List[MusicalIntent], str]:
        """
        Process user input and extract musical intents.
        
        Returns:
            Tuple of (extracted_intents, response_suggestion)
        """
        # Add user input to conversation history
        self.conversation_history.append({
            "type": "user_input",
            "timestamp": datetime.now(),
            "content": user_input
        })
        
        # Parse intents from the input
        parser = IntentParser(self.current_context)
        intents = parser.parse_intent(user_input, "conversation")
        
        # Update context based on new intents
        self._update_context_from_intents(intents)
        
        # Generate response suggestion
        response = self._generate_response_suggestion(user_input, intents)
        
        # Add response to history
        self.conversation_history.append({
            "type": "system_response",
            "timestamp": datetime.now(),
            "content": response,
            "intents_extracted": [intent.dict() for intent in intents]
        })
        
        return intents, response
    
    def _update_context_from_intents(self, intents: List[MusicalIntent]) -> None:
        """Update the current context based on extracted intents."""
        for intent in intents:
            # Update context based on intent type
            if intent.intent_type == IntentType.RHYTHMIC:
                if "tempo" in intent.concept.lower():
                    tempo_match = re.search(r'(\d+)', intent.concept)
                    if tempo_match:
                        self.current_context.tempo = int(tempo_match.group(1))
                elif "feel" in intent.concept.lower() or "groove" in intent.concept.lower():
                    self.current_context.mood = intent.concept
            
            elif intent.intent_type == IntentType.HARMONIC:
                if "key" in intent.concept.lower():
                    # Extract key signature
                    key_match = re.search(r'([A-G][#b]?\s*(?:major|minor))', intent.concept, re.IGNORECASE)
                    if key_match:
                        self.current_context.key_signature = key_match.group(1)
            
            elif intent.intent_type == IntentType.STYLISTIC:
                if any(genre in intent.concept.lower() for genre in ['jazz', 'rock', 'funk', 'blues', 'classical']):
                    self.current_context.genre = intent.concept
            
            elif intent.intent_type == IntentType.EMOTIONAL:
                self.current_context.mood = intent.concept
            
            # Update conversation history
            self.current_context.conversation_history.append(intent.concept)
    
    def _generate_response_suggestion(self, user_input: str, intents: List[MusicalIntent]) -> str:
        """Generate a helpful response suggestion based on extracted intents."""
        if not intents:
            return "I'd love to help with your musical ideas! Could you tell me more about what you're trying to create?"
        
        # Group intents by type
        intent_groups = {}
        for intent in intents:
            if intent.intent_type not in intent_groups:
                intent_groups[intent.intent_type] = []
            intent_groups[intent.intent_type].append(intent)
        
        response_parts = []
        
        # Acknowledge what we understood
        if len(intents) == 1:
            intent = intents[0]
            response_parts.append(f"I understand you're working on {intent.concept} for {intent.intent_type}.")
        else:
            response_parts.append("I picked up several musical ideas from what you said:")
            for intent_type, type_intents in intent_groups.items():
                concepts = [intent.concept for intent in type_intents]
                response_parts.append(f"- {intent_type.title()}: {', '.join(concepts)}")
        
        # Ask clarifying questions
        clarifying_questions = self._generate_clarifying_questions(intents)
        if clarifying_questions:
            response_parts.append("\nTo help you better, I have a few questions:")
            for i, question in enumerate(clarifying_questions, 1):
                response_parts.append(f"{i}. {question}")
        
        # Suggest next steps
        next_steps = self._suggest_next_steps(intents)
        if next_steps:
            response_parts.append(f"\n{next_steps}")
        
        return "\n".join(response_parts)
    
    def _generate_clarifying_questions(self, intents: List[MusicalIntent]) -> List[str]:
        """Generate clarifying questions based on extracted intents."""
        questions = []
        
        # Check for missing context
        if not self.current_context.tempo:
            questions.append("What tempo are you thinking for this piece?")
        
        if not self.current_context.key_signature:
            questions.append("What key signature are you working in?")
        
        if not self.current_context.target_instrument:
            questions.append("What instrument are you generating this for?")
        
        # Check for ambiguous intents
        for intent in intents:
            if intent.confidence == IntentConfidence.LOW:
                questions.append(f"Could you clarify what you mean by '{intent.concept}'?")
            elif intent.intent_type == IntentType.CUSTOM:
                questions.append(f"Tell me more about '{intent.concept}' - what musical aspect are you focusing on?")
        
        return questions[:3]  # Limit to 3 questions to avoid overwhelming
    
    def _suggest_next_steps(self, intents: List[MusicalIntent]) -> str:
        """Suggest next steps based on current intents."""
        if len(intents) >= 3:
            return "You've given me a good foundation! Would you like me to generate some MIDI sketches based on these ideas?"
        elif len(intents) == 2:
            return "Great start! A few more details would help me create something that really fits your vision."
        else:
            return "Let's build on this idea. What other musical elements are you considering?"
    
    def get_current_intent_collection(self) -> IntentCollection:
        """Get the current collection of all intents from this conversation."""
        all_intents = []
        
        for entry in self.conversation_history:
            if entry["type"] == "system_response" and "intents_extracted" in entry:
                for intent_data in entry["intents_extracted"]:
                    intent = MusicalIntent(**intent_data)
                    all_intents.append(intent)
        
        collection = IntentCollection(
            generation_id=f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            context=self.current_context
        )
        
        for intent in all_intents:
            collection.add_intent(intent)
        
        return collection
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export the complete conversation for analysis or storage."""
        return {
            "conversation_history": self.conversation_history,
            "current_context": self.current_context.dict() if self.current_context else None,
            "intent_relationships": self.intent_relationships,
            "exported_at": datetime.now().isoformat()
        }


class IntentAnalyzer:
    """
    Analyzes captured intents to provide insights and suggestions.
    """
    
    @staticmethod
    def analyze_intent_collection(collection: IntentCollection) -> Dict[str, Any]:
        """Analyze an intent collection and provide insights."""
        analysis = {
            "total_intents": len(collection.intents),
            "intent_types": {},
            "confidence_distribution": {},
            "temporal_analysis": {},
            "relationship_analysis": {},
            "suggestions": []
        }
        
        # Count intents by type
        for intent in collection.intents:
            intent_type = intent.intent_type
            if intent_type not in analysis["intent_types"]:
                analysis["intent_types"][intent_type] = 0
            analysis["intent_types"][intent_type] += 1
        
        # Count confidence levels
        for intent in collection.intents:
            confidence = intent.confidence
            if confidence not in analysis["confidence_distribution"]:
                analysis["confidence_distribution"][confidence] = 0
            analysis["confidence_distribution"][confidence] += 1
        
        # Analyze relationships
        analysis["relationship_analysis"] = {
            "total_relationships": len(collection.intent_graph),
            "most_connected": max(collection.intent_graph.items(), key=lambda x: len(x[1])) if collection.intent_graph else None
        }
        
        # Generate suggestions
        analysis["suggestions"] = IntentAnalyzer._generate_suggestions(collection)
        
        return analysis
    
    @staticmethod
    def _generate_suggestions(collection: IntentCollection) -> List[str]:
        """Generate suggestions based on the intent collection."""
        suggestions = []
        
        # Check for missing elements
        intent_types = {intent.intent_type for intent in collection.intents}
        
        if IntentType.RHYTHMIC not in intent_types:
            suggestions.append("Consider adding rhythmic elements to define the groove")
        
        if IntentType.HARMONIC not in intent_types:
            suggestions.append("Harmonic elements would help establish the musical foundation")
        
        if IntentType.MELODIC not in intent_types:
            suggestions.append("Melodic ideas would add character and memorability")
        
        # Check for low confidence intents
        low_confidence_intents = [intent for intent in collection.intents if intent.confidence == IntentConfidence.LOW]
        if low_confidence_intents:
            suggestions.append(f"Clarify {len(low_confidence_intents)} musical concepts for better results")
        
        # Check for isolated intents
        if len(collection.intent_graph) < len(collection.intents) * 0.5:
            suggestions.append("Consider how different musical elements relate to each other")
        
        return suggestions


# Convenience functions
def start_musical_conversation(initial_context: Optional[MusicalContext] = None) -> ConversationalIntentParser:
    """Start a new musical conversation with intent parsing."""
    parser = ConversationalIntentParser()
    parser.start_conversation(initial_context)
    return parser


def analyze_musical_intent(collection: IntentCollection) -> Dict[str, Any]:
    """Analyze a collection of musical intents."""
    return IntentAnalyzer.analyze_intent_collection(collection)
