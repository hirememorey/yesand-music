"""
Enhanced Musical Conversation Engine

This module provides a natural, conversational integration of the intent discovery,
creative enhancement, and prompt generation systems, preserving the musical
conversation flow and context we've built.
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import uuid

from schemas import MusicalContext, IntentCollection, IntentType
from intent_discovery_agent import MusicalIntentDiscoveryAgent
from creative_enhancement import (
    MusicalCreativityEngine, ContextualPromptGenerator,
    suggest_musical_enhancements, generate_musical_prompt
)


@dataclass
class MusicalSuggestion:
    """A musical suggestion with context and reasoning"""
    suggestion_id: str
    title: str
    description: str
    musical_reasoning: str
    implementation_notes: str
    confidence_score: float
    suggestion_type: str
    midi_sketch_available: bool = False
    enhancement_suggestions: List[Dict[str, Any]] = None


@dataclass
class ConversationContext:
    """Complete context for musical conversation"""
    discovery_agent: MusicalIntentDiscoveryAgent
    intent_collection: Optional[IntentCollection]
    conversation_history: List[Dict[str, Any]]
    current_problem: Optional[str]
    user_preferences: Dict[str, Any]
    session_id: str
    discovery_complete: bool = False
    creative_enhancements: List[Dict[str, Any]] = None


class EnhancedMusicalConversationEngine:
    """
    Enhanced conversation engine that naturally integrates intent discovery,
    creative enhancement, and prompt generation through musical conversation.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.conversation_context = None
        self.suggestion_history = []
        self.creativity_engine = MusicalCreativityEngine()
        self.prompt_generator = ContextualPromptGenerator()
        self.conversation_mode = "discovery"  # "discovery", "enhancement", "generation"
        
        # Musical knowledge base
        self.musical_styles = {
            'jazz': ['complex harmonies', 'syncopated rhythms', 'improvisation'],
            'rock': ['power chords', 'driving rhythms', 'distorted guitars'],
            'blues': ['12-bar progression', 'bent notes', 'call and response'],
            'classical': ['formal structure', 'orchestration', 'counterpoint'],
            'electronic': ['synthesizers', 'repetitive patterns', 'effects'],
            'funk': ['syncopated bass', 'rhythmic complexity', 'percussion'],
            'grunge': ['distorted guitars', 'alternative tunings', 'raw sound']
        }
    
    def start_conversation(self, project_path: Optional[str] = None, initial_input: str = None) -> str:
        """Start a new musical conversation with intent discovery"""
        session_id = str(uuid.uuid4())
        
        # Initialize discovery agent
        discovery_agent = MusicalIntentDiscoveryAgent()
        
        # Initialize conversation context
        self.conversation_context = ConversationContext(
            discovery_agent=discovery_agent,
            intent_collection=None,
            conversation_history=[],
            current_problem=None,
            user_preferences={},
            session_id=session_id,
            discovery_complete=False
        )
        
        # Start discovery session
        if initial_input:
            result = discovery_agent.start_discovery_session(initial_input)
        else:
            result = discovery_agent.start_discovery_session()
        
        # Get initial intent collection
        self.conversation_context.intent_collection = self._get_intent_collection_from_discovery_agent(discovery_agent)
        
        # Record the initial interaction
        self.conversation_context.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'system',
            'content': result['welcome']
        })
        
        if result['response']:
            self.conversation_context.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'system',
                'content': result['response']
            })
        
        return result['welcome'] + "\n\n" + (result['response'] or "")
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and provide appropriate response"""
        if not self.conversation_context:
            return "Please start a conversation first with start_conversation()"
        
        # Add to conversation history
        self.conversation_context.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'user',
            'content': user_input
        })
        
        # Process through discovery agent
        result = self.conversation_context.discovery_agent.process_musical_input(user_input)
        
        # Update intent collection
        self.conversation_context.intent_collection = self._get_intent_collection_from_discovery_agent(
            self.conversation_context.discovery_agent
        )
        
        # Record the response
        self.conversation_context.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'system',
            'content': result['response']
        })
        
        # Check if discovery is complete
        if result['discovery_complete'] and not self.conversation_context.discovery_complete:
            self.conversation_context.discovery_complete = True
            self.conversation_mode = "enhancement"
            
            # Generate creative enhancements
            enhancements = suggest_musical_enhancements(
                self.conversation_context.intent_collection, 
                "medium"
            )
            self.conversation_context.creative_enhancements = enhancements
            
            # Add enhancement suggestions to response
            enhancement_text = self._format_enhancement_suggestions(enhancements)
            result['response'] += f"\n\n🎨 **Creative Enhancement Suggestions:**\n{enhancement_text}"
        
        # Add next question if available
        if result['next_question']:
            next_question_text = f"\n\n**Next Question:** {result['next_question']['question']}"
            if result['next_question']['suggested_follow_ups']:
                follow_ups = ", ".join(result['next_question']['suggested_follow_ups'])
                next_question_text += f"\n*Suggestions: {follow_ups}*"
            result['response'] += next_question_text
        
        # Add musical insights if available
        if result['musical_insights']:
            insights_text = ", ".join(result['musical_insights'])
            result['response'] += f"\n\n💡 **Musical Insights:** {insights_text}"
        
        return result['response']
    
    def _format_enhancement_suggestions(self, enhancements: List[Dict[str, Any]]) -> str:
        """Format creative enhancement suggestions for display"""
        if not enhancements:
            return "No specific enhancements suggested at this time."
        
        enhancement_texts = []
        for i, enhancement in enumerate(enhancements[:5], 1):
            enhancement_texts.append(
                f"{i}. **{enhancement['enhancement']}** - {enhancement['reasoning']}"
            )
        
        return "\n".join(enhancement_texts)
    
    def _get_intent_collection_from_discovery_agent(self, discovery_agent) -> Optional[IntentCollection]:
        """Get intent collection from discovery agent"""
        if not discovery_agent.discovered_intents:
            return None
        
        # Create intent collection
        collection = IntentCollection(
            generation_id=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            context=discovery_agent.current_context
        )
        
        for intent in discovery_agent.discovered_intents:
            collection.add_intent(intent)
        
        return collection
    
    def get_musical_suggestions(self, user_input: str = None) -> List[MusicalSuggestion]:
        """Get musical suggestions based on discovered intent"""
        if not self.conversation_context or not self.conversation_context.intent_collection:
            return []
        
        suggestions = []
        intent_collection = self.conversation_context.intent_collection
        
        # Generate suggestions based on discovered intents
        if IntentType.RHYTHMIC in [intent.intent_type for intent in intent_collection.intents]:
            suggestions.extend(self._generate_rhythmic_suggestions(intent_collection))
        
        if IntentType.HARMONIC in [intent.intent_type for intent in intent_collection.intents]:
            suggestions.extend(self._generate_harmonic_suggestions(intent_collection))
        
        if IntentType.MELODIC in [intent.intent_type for intent in intent_collection.intents]:
            suggestions.extend(self._generate_melodic_suggestions(intent_collection))
        
        # Add creative enhancements to suggestions
        if self.conversation_context.creative_enhancements:
            for suggestion in suggestions:
                suggestion.enhancement_suggestions = self.conversation_context.creative_enhancements
        
        return suggestions
    
    def _generate_rhythmic_suggestions(self, intent_collection: IntentCollection) -> List[MusicalSuggestion]:
        """Generate rhythmic suggestions based on discovered intents"""
        suggestions = []
        
        # Find rhythmic intents
        rhythmic_intents = [intent for intent in intent_collection.intents if intent.intent_type == IntentType.RHYTHMIC]
        
        for intent in rhythmic_intents:
            if "swung" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Enhance Swung Feel",
                    description="Build on the swung rhythm with syncopation and rhythmic displacement",
                    musical_reasoning="Swung rhythms can be enhanced with additional syncopation and off-beat accents",
                    implementation_notes="Try adding anticipations and delayed attacks to enhance the swing feel",
                    confidence_score=0.8,
                    suggestion_type="rhythm"
                ))
            elif "syncopated" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Develop Syncopation",
                    description="Expand the syncopated patterns with polyrhythmic elements",
                    musical_reasoning="Syncopated rhythms can be developed with more complex rhythmic patterns",
                    implementation_notes="Try adding polyrhythmic elements or cross-rhythms",
                    confidence_score=0.7,
                    suggestion_type="rhythm"
                ))
        
        return suggestions
    
    def _generate_harmonic_suggestions(self, intent_collection: IntentCollection) -> List[MusicalSuggestion]:
        """Generate harmonic suggestions based on discovered intents"""
        suggestions = []
        
        # Find harmonic intents
        harmonic_intents = [intent for intent in intent_collection.intents if intent.intent_type == IntentType.HARMONIC]
        
        for intent in harmonic_intents:
            if "jazz" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Expand Jazz Harmony",
                    description="Add chord extensions and jazz harmony techniques",
                    musical_reasoning="Jazz harmony can be expanded with extensions, alterations, and substitutions",
                    implementation_notes="Try adding 9ths, 11ths, and 13ths to your chord progressions",
                    confidence_score=0.8,
                    suggestion_type="harmony"
                ))
            elif "seventh" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Develop Seventh Chords",
                    description="Build on the seventh chord foundation with secondary dominants",
                    musical_reasoning="Seventh chords can be developed with secondary dominants and extensions",
                    implementation_notes="Try adding secondary dominants before your seventh chords",
                    confidence_score=0.7,
                    suggestion_type="harmony"
                ))
        
        return suggestions
    
    def _generate_melodic_suggestions(self, intent_collection: IntentCollection) -> List[MusicalSuggestion]:
        """Generate melodic suggestions based on discovered intents"""
        suggestions = []
        
        # Find melodic intents
        melodic_intents = [intent for intent in intent_collection.intents if intent.intent_type == IntentType.MELODIC]
        
        for intent in melodic_intents:
            if "ascending" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Develop Ascending Melody",
                    description="Build on the ascending melodic idea with sequences and development",
                    musical_reasoning="Ascending melodies can be developed with sequences and motivic development",
                    implementation_notes="Try creating melodic sequences that build on the ascending pattern",
                    confidence_score=0.8,
                    suggestion_type="melody"
                ))
            elif "sparse" in intent.concept.lower():
                suggestions.append(MusicalSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    title="Add Melodic Detail",
                    description="Enhance the sparse melody with ornamentation and passing tones",
                    musical_reasoning="Sparse melodies can be enhanced with tasteful ornamentation",
                    implementation_notes="Try adding passing tones, neighbor tones, and melodic ornaments",
                    confidence_score=0.7,
                    suggestion_type="melody"
                ))
        
        return suggestions
    
    def generate_midi_prompt(self, length: str = "4-bar", focus: str = "all elements") -> str:
        """Generate a prompt for MIDI generation based on discovered intent"""
        if not self.conversation_context or not self.conversation_context.intent_collection:
            return "No musical intent discovered yet. Please continue the conversation to build your musical vision."
        
        # Generate creative enhancements if not already done
        if not self.conversation_context.creative_enhancements:
            self.conversation_context.creative_enhancements = suggest_musical_enhancements(
                self.conversation_context.intent_collection, 
                "medium"
            )
        
        # Generate the prompt
        prompt = generate_musical_prompt(
            self.conversation_context.intent_collection,
            self.conversation_context.creative_enhancements,
            length,
            focus
        )
        
        return prompt
    
    def get_context_summary(self) -> str:
        """Get a summary of the current conversation context"""
        if not self.conversation_context:
            return "No active conversation"
        
        summary_parts = []
        
        # Discovery summary
        if self.conversation_context.intent_collection:
            collection = self.conversation_context.intent_collection
            summary_parts.append(f"🎵 **Musical Vision Discovered:**")
            summary_parts.append(f"   {collection.to_conversation_context()}")
            
            if collection.context.tempo:
                summary_parts.append(f"🎼 **Tempo:** {collection.context.tempo} BPM")
            if collection.context.key_signature:
                summary_parts.append(f"🎼 **Key:** {collection.context.key_signature}")
            if collection.context.target_instrument:
                summary_parts.append(f"🎸 **Instrument:** {collection.context.target_instrument}")
        
        # Discovery status
        if self.conversation_context.discovery_complete:
            summary_parts.append("✅ **Discovery Complete** - Ready for generation")
        else:
            summary_parts.append("🔄 **Discovery in Progress** - Building musical vision")
        
        # Creative enhancements
        if self.conversation_context.creative_enhancements:
            summary_parts.append(f"🎨 **Creative Enhancements:** {len(self.conversation_context.creative_enhancements)} suggestions")
        
        return "\n".join(summary_parts)
    
    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the discovery session"""
        if not self.conversation_context or not self.conversation_context.discovery_agent:
            return {"error": "No active discovery session"}
        
        return self.conversation_context.discovery_agent.get_discovery_summary()
    
    def export_for_generation(self) -> Dict[str, Any]:
        """Export the discovered musical intent for MIDI generation"""
        if not self.conversation_context or not self.conversation_context.intent_collection:
            return {"error": "No musical intent discovered yet"}
        
        return self.conversation_context.discovery_agent.export_for_generation()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history"""
        if not self.conversation_context:
            return []
        return self.conversation_context.conversation_history
    
    def save_conversation(self, file_path: str) -> bool:
        """Save conversation to file"""
        if not self.conversation_context:
            return False
        
        try:
            conversation_data = {
                'session_id': self.conversation_context.session_id,
                'discovery_complete': self.conversation_context.discovery_complete,
                'conversation_history': self.conversation_context.conversation_history,
                'suggestion_history': [s.__dict__ for s in self.suggestion_history]
            }
            
            # Add intent collection if available
            if self.conversation_context.intent_collection:
                conversation_data['intent_collection'] = self.conversation_context.intent_collection.dict()
            
            # Add creative enhancements if available
            if self.conversation_context.creative_enhancements:
                conversation_data['creative_enhancements'] = self.conversation_context.creative_enhancements
            
            with open(file_path, 'w') as f:
                json.dump(conversation_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False


def demo_enhanced_conversation():
    """Demo the enhanced musical conversation engine"""
    engine = EnhancedMusicalConversationEngine()
    
    print(engine.start_conversation(initial_input="I'm working on a jazz piece"))
    
    # Simulate a conversation
    responses = [
        "It's in G minor at 120 BPM",
        "I want a mysterious, dark sound like Miles Davis",
        "Swung eighths for the rhythm",
        "Jazz sevenths for the harmony",
        "A sparse, ascending melody that builds tension"
    ]
    
    for response in responses:
        print(f"\nUser: {response}")
        print(f"AI: {engine.process_user_input(response)}")
    
    print("\n" + "="*50)
    print("🎵 CONTEXT SUMMARY")
    print("="*50)
    print(engine.get_context_summary())
    
    # Generate MIDI prompt
    print("\n" + "="*50)
    print("🎼 MIDI GENERATION PROMPT")
    print("="*50)
    prompt = engine.generate_midi_prompt("4-bar", "rhythm and harmony")
    print(prompt)


if __name__ == "__main__":
    demo_enhanced_conversation()
