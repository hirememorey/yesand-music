"""
Conversation-Driven Intent Discovery Agent

This module provides a holistic, conversation-driven approach to discovering
musical intent through natural dialogue rather than rigid schema filling.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re

from schemas import MusicalContext, MusicalIntent, IntentType, IntentConfidence, IntentCollection
from intent_parser import ConversationalIntentParser
from question_generator import (
    MusicalQuestionGenerator, ConversationalQuestionFlow,
    MusicalQuestion, QuestionType, QuestionPriority
)


class MusicalIntentDiscoveryAgent:
    """
    A conversation-driven agent that discovers musical intent through natural dialogue,
    letting musical understanding emerge organically rather than forcing it into rigid schemas.
    """
    
    def __init__(self, initial_context: Optional[MusicalContext] = None):
        self.intent_parser = ConversationalIntentParser()
        self.question_flow = ConversationalQuestionFlow()
        self.current_context = initial_context or MusicalContext()
        self.discovered_intents: List[MusicalIntent] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.musical_examples: Dict[str, List[str]] = {}
        self.discovery_complete = False
        
        # Initialize conversation
        self.intent_parser.start_conversation(self.current_context)
    
    def start_discovery_session(self, user_initial_input: str = None) -> Dict[str, Any]:
        """
        Start a musical intent discovery session with optional initial user input.
        
        Args:
            user_initial_input: Optional initial description from the user
            
        Returns:
            Dictionary containing welcome message and first question
        """
        welcome_message = self._generate_welcome_message()
        
        if user_initial_input:
            # Process the initial input
            intents, response = self.intent_parser.process_user_input(user_initial_input)
            self.discovered_intents.extend(intents)
            self.current_context = self.intent_parser.current_context
            
            # Record the interaction
            self.conversation_history.append({
                "type": "user_input",
                "content": user_initial_input,
                "intents": [intent.dict() for intent in intents],
                "timestamp": datetime.now()
            })
            
            # Generate follow-up question
            next_question = self.question_flow.get_next_question(self.current_context, intents)
            
            return {
                "welcome": welcome_message,
                "response": response,
                "intents_discovered": len(intents),
                "next_question": self._format_question(next_question) if next_question else None,
                "discovery_stage": self._assess_discovery_stage()
            }
        else:
            # Generate initial question
            next_question = self.question_flow.get_next_question(self.current_context, [])
            
            return {
                "welcome": welcome_message,
                "response": None,
                "intents_discovered": 0,
                "next_question": self._format_question(next_question) if next_question else None,
                "discovery_stage": self._assess_discovery_stage()
            }
    
    def process_musical_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input and continue the discovery conversation.
        
        Args:
            user_input: User's musical description or response
            
        Returns:
            Dictionary containing response, discovered intents, and next steps
        """
        # Check for musical examples or references
        examples = self._extract_musical_examples(user_input)
        if examples:
            self._record_musical_examples(examples)
        
        # Process intents from the input
        intents, response = self.intent_parser.process_user_input(user_input)
        self.discovered_intents.extend(intents)
        self.current_context = self.intent_parser.current_context
        
        # Record the interaction
        self.conversation_history.append({
            "type": "user_input",
            "content": user_input,
            "intents": [intent.dict() for intent in intents],
            "examples": examples,
            "timestamp": datetime.now()
        })
        
        # Generate next question or discovery step
        next_question = self.question_flow.get_next_question(self.current_context, intents)
        
        # Assess if discovery is complete
        discovery_complete = self._assess_discovery_completeness()
        
        # Generate insights about the musical vision
        insights = self._generate_musical_insights()
        
        return {
            "response": response,
            "intents_discovered": len(intents),
            "total_intents": len(self.discovered_intents),
            "next_question": self._format_question(next_question) if next_question else None,
            "discovery_stage": self._assess_discovery_stage(),
            "discovery_complete": discovery_complete,
            "musical_insights": insights,
            "examples_referenced": examples
        }
    
    def _generate_welcome_message(self) -> str:
        """Generate a welcoming message that sets the tone for musical discovery."""
        return (
            "🎵 Welcome to your musical discovery session! I'm here to help you explore "
            "and clarify your musical vision. Think of me as your musical conversation partner - "
            "I'll ask questions, listen to your ideas, and help you discover what you're "
            "really trying to create. There are no wrong answers, just musical exploration!"
        )
    
    def _extract_musical_examples(self, text: str) -> List[str]:
        """Extract musical examples, references, or metaphors from user input."""
        examples = []
        
        # Look for common musical reference patterns
        patterns = [
            r"like\s+([^,\.]+)",  # "like Miles Davis"
            r"similar\s+to\s+([^,\.]+)",  # "similar to that song"
            r"in\s+the\s+style\s+of\s+([^,\.]+)",  # "in the style of John Coltrane"
            r"reminds\s+me\s+of\s+([^,\.]+)",  # "reminds me of that one song"
            r"think\s+([^,\.]+)",  # "think Herbie Hancock"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            examples.extend(matches)
        
        return [example.strip() for example in examples if example.strip()]
    
    def _record_musical_examples(self, examples: List[str]) -> None:
        """Record musical examples for context building."""
        for example in examples:
            if example not in self.musical_examples:
                self.musical_examples[example] = []
            self.musical_examples[example].append(datetime.now().isoformat())
    
    def _format_question(self, question: MusicalQuestion) -> Dict[str, Any]:
        """Format a question for presentation to the user."""
        if not question:
            return None
        
        return {
            "question": question.question,
            "type": question.question_type,
            "musical_focus": question.musical_focus,
            "suggested_follow_ups": question.suggested_follow_ups,
            "priority": question.priority
        }
    
    def _assess_discovery_stage(self) -> str:
        """Assess the current stage of musical discovery."""
        if len(self.discovered_intents) < 2:
            return "exploration"
        elif len(self.discovered_intents) < 5:
            return "building"
        elif len(self.discovered_intents) < 8:
            return "refining"
        else:
            return "complete"
    
    def _assess_discovery_completeness(self) -> bool:
        """Assess if the musical discovery is complete enough to proceed."""
        # Check for essential musical elements
        intent_types = {intent.intent_type for intent in self.discovered_intents}
        essential_elements = {IntentType.RHYTHMIC, IntentType.HARMONIC, IntentType.MELODIC}
        
        has_essential = len(intent_types.intersection(essential_elements)) >= 2
        
        # Check for context
        has_context = (
            self.current_context.tempo is not None and
            self.current_context.target_instrument is not None
        )
        
        # Check for sufficient detail
        has_sufficient_detail = len(self.discovered_intents) >= 5
        
        return has_essential and has_context and has_sufficient_detail
    
    def _generate_musical_insights(self) -> List[str]:
        """Generate insights about the discovered musical vision."""
        insights = []
        
        if not self.discovered_intents:
            return insights
        
        # Analyze intent types
        intent_types = {intent.intent_type for intent in self.discovered_intents}
        
        if IntentType.RHYTHMIC in intent_types:
            insights.append("You have a clear rhythmic vision")
        
        if IntentType.HARMONIC in intent_types:
            insights.append("Harmonic elements are well-defined")
        
        if IntentType.MELODIC in intent_types:
            insights.append("Melodic character is established")
        
        if IntentType.EMOTIONAL in intent_types:
            insights.append("Emotional character is clear")
        
        # Analyze confidence levels
        high_confidence = [intent for intent in self.discovered_intents if intent.confidence == IntentConfidence.HIGH]
        if len(high_confidence) > len(self.discovered_intents) * 0.7:
            insights.append("You have a strong, clear musical vision")
        
        # Analyze examples
        if self.musical_examples:
            insights.append(f"You're drawing inspiration from {len(self.musical_examples)} musical references")
        
        return insights
    
    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the discovery session."""
        if not self.discovered_intents:
            return {"error": "No musical intent discovered yet"}
        
        # Group intents by type
        intent_groups = {}
        for intent in self.discovered_intents:
            if intent.intent_type not in intent_groups:
                intent_groups[intent.intent_type] = []
            intent_groups[intent.intent_type].append(intent)
        
        # Calculate discovery metrics
        discovery_metrics = {
            "total_intents": len(self.discovered_intents),
            "intent_types_discovered": len(intent_groups),
            "conversation_turns": len(self.conversation_history),
            "musical_examples_referenced": len(self.musical_examples),
            "discovery_stage": self._assess_discovery_stage(),
            "completeness_score": self._calculate_completeness_score()
        }
        
        return {
            "discovery_metrics": discovery_metrics,
            "musical_context": self.current_context.dict() if self.current_context else None,
            "intent_groups": {
                intent_type: [intent.concept for intent in intents]
                for intent_type, intents in intent_groups.items()
            },
            "musical_examples": list(self.musical_examples.keys()),
            "conversation_highlights": self._get_conversation_highlights(),
            "musical_insights": self._generate_musical_insights()
        }
    
    def _calculate_completeness_score(self) -> float:
        """Calculate a completeness score for the discovery (0.0 to 1.0)."""
        score = 0.0
        
        # Basic context (40% of score)
        if self.current_context.tempo:
            score += 0.1
        if self.current_context.key_signature:
            score += 0.1
        if self.current_context.target_instrument:
            score += 0.1
        if self.current_context.genre:
            score += 0.1
        
        # Musical elements (40% of score)
        intent_types = {intent.intent_type for intent in self.discovered_intents}
        essential_elements = {IntentType.RHYTHMIC, IntentType.HARMONIC, IntentType.MELODIC}
        element_score = len(intent_types.intersection(essential_elements)) / len(essential_elements)
        score += element_score * 0.4
        
        # Detail level (20% of score)
        detail_score = min(len(self.discovered_intents) / 8, 1.0)
        score += detail_score * 0.2
        
        return min(score, 1.0)
    
    def _get_conversation_highlights(self) -> List[str]:
        """Get highlights from the conversation history."""
        highlights = []
        
        for entry in self.conversation_history:
            if entry["type"] == "user_input":
                content = entry["content"]
                if len(content) > 20:  # Only include substantial inputs
                    highlights.append(content[:100] + "..." if len(content) > 100 else content)
        
        return highlights[-5:]  # Return last 5 highlights
    
    def export_for_generation(self) -> Dict[str, Any]:
        """Export the discovered musical intent for MIDI generation."""
        if not self.discovered_intents:
            return {"error": "No musical intent discovered yet"}
        
        # Create intent collection
        collection = IntentCollection(
            generation_id=f"discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            context=self.current_context
        )
        
        for intent in self.discovered_intents:
            collection.add_intent(intent)
        
        return {
            "intent_collection": collection.dict(),
            "generation_ready": self.discovery_complete,
            "completeness_score": self._calculate_completeness_score(),
            "musical_context": collection.to_conversation_context()
        }


def start_musical_discovery(initial_context: Optional[MusicalContext] = None) -> MusicalIntentDiscoveryAgent:
    """Start a new musical intent discovery session."""
    return MusicalIntentDiscoveryAgent(initial_context)


def demo_musical_discovery():
    """Demonstrate the musical intent discovery process."""
    print("Musical Intent Discovery Demo")
    print("=" * 50)
    
    # Start discovery session
    agent = start_musical_discovery()
    
    # Start with initial input
    result = agent.start_discovery_session("I'm working on a jazz piece")
    
    print(f"Welcome: {result['welcome']}")
    print(f"Response: {result['response']}")
    print(f"Next Question: {result['next_question']['question'] if result['next_question'] else 'None'}")
    print(f"Discovery Stage: {result['discovery_stage']}")
    
    # Simulate conversation
    conversation_steps = [
        "It's in G minor at 120 BPM",
        "I want a mysterious, dark sound like Miles Davis",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony",
        "A sparse, ascending melody that builds tension"
    ]
    
    for step in conversation_steps:
        print(f"\n{'='*30}")
        print(f"User: {step}")
        
        result = agent.process_musical_input(step)
        
        print(f"Response: {result['response']}")
        print(f"Intents Discovered: {result['intents_discovered']}")
        print(f"Total Intents: {result['total_intents']}")
        
        if result['next_question']:
            print(f"Next Question: {result['next_question']['question']}")
        
        if result['musical_insights']:
            print(f"Insights: {', '.join(result['musical_insights'])}")
        
        print(f"Discovery Stage: {result['discovery_stage']}")
        print(f"Complete: {result['discovery_complete']}")
    
    # Get final summary
    print(f"\n{'='*50}")
    print("=== Discovery Summary ===")
    summary = agent.get_discovery_summary()
    
    print(f"Discovery Metrics: {summary['discovery_metrics']}")
    print(f"Musical Context: {summary['musical_context']}")
    print(f"Intent Groups: {summary['intent_groups']}")
    print(f"Musical Examples: {summary['musical_examples']}")
    print(f"Musical Insights: {summary['musical_insights']}")


if __name__ == "__main__":
    demo_musical_discovery()
