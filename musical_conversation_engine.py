#!/usr/bin/env python3
"""
Musical Conversation Engine

This system combines project state analysis with user input to provide
contextual musical suggestions and problem-solving assistance.

Key Features:
- Dual context sources (project state + user input)
- Contextual musical suggestions
- Problem-solving assistance
- Musical reasoning and explanations
- Integration with AI for intelligent responses
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import uuid

from musical_context_interview import MusicalContext, MusicalContextInterview
from project_state_analyzer import ProjectState, ProjectStateAnalyzer


@dataclass
class MusicalSuggestion:
    """A musical suggestion with context and reasoning"""
    suggestion_id: str
    title: str
    description: str
    musical_reasoning: str
    implementation_notes: str
    confidence_score: float
    suggestion_type: str  # 'chord_progression', 'melody', 'rhythm', 'arrangement', etc.
    midi_sketch_available: bool = False


@dataclass
class ConversationContext:
    """Complete context for musical conversation"""
    user_context: MusicalContext
    project_state: Optional[ProjectState]
    conversation_history: List[Dict[str, Any]]
    current_problem: Optional[str]
    user_preferences: Dict[str, Any]
    session_id: str


class MusicalConversationEngine:
    """Enhanced conversation engine for musical problem-solving"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.context_interview = MusicalContextInterview()
        self.project_analyzer = ProjectStateAnalyzer()
        self.conversation_context = None
        self.suggestion_history = []
        self.conversation_mode = "initial"  # "initial", "interview", "conversation"
        
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
        
        self.musical_problems = {
            'bridge': 'A bridge typically provides contrast and leads back to the main material',
            'chorus': 'A chorus should be memorable and emotionally impactful',
            'verse': 'A verse tells the story and builds toward the chorus',
            'intro': 'An intro sets the mood and introduces key musical elements',
            'outro': 'An outro provides closure and can fade or build to a climax'
        }
    
    def start_conversation(self, project_path: Optional[str] = None) -> str:
        """Start a new musical conversation"""
        session_id = str(uuid.uuid4())
        
        # Initialize conversation context
        self.conversation_context = ConversationContext(
            user_context=MusicalContext(),
            project_state=None,
            conversation_history=[],
            current_problem=None,
            user_preferences={},
            session_id=session_id
        )
        
        # Analyze project if provided
        if project_path:
            try:
                self.conversation_context.project_state = self.project_analyzer.analyze_project(project_path)
            except Exception as e:
                print(f"Warning: Could not analyze project {project_path}: {e}")
        
        # Start interview immediately and take control
        self.context_interview.start_interview()
        self.conversation_mode = "interview"
        
        # Return interview's welcome message
        return self.context_interview.start_interview()
    
    def get_context_summary(self) -> str:
        """Get a summary of the current conversation context"""
        if not self.conversation_context:
            return "No active conversation"
        
        summary_parts = []
        
        # User context summary
        if self.conversation_context.user_context.song_concept:
            summary_parts.append(f"🎵 Song: {self.conversation_context.user_context.song_concept}")
        
        if self.conversation_context.user_context.key_signature and self.conversation_context.user_context.tempo:
            summary_parts.append(f"🎼 Key: {self.conversation_context.user_context.key_signature}, Tempo: {self.conversation_context.user_context.tempo} BPM")
        
        if self.conversation_context.user_context.musical_problem:
            summary_parts.append(f"❓ Problem: {self.conversation_context.user_context.musical_problem}")
        
        # Project state summary
        if self.conversation_context.project_state:
            if self.conversation_context.project_state.tempo:
                summary_parts.append(f"📁 Project Tempo: {self.conversation_context.project_state.tempo} BPM")
            
            if self.conversation_context.project_state.musical_parts:
                summary_parts.append(f"🎸 Project Parts: {', '.join(self.conversation_context.project_state.musical_parts)}")
        
        return "\n".join(summary_parts)
    
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
        
        # CRITICAL: Let interview system handle ALL input during interview phase
        if self.conversation_mode == "interview":
            return self._handle_interview_phase(user_input)
        else:
            return self._handle_conversation_phase(user_input)
    
    def _handle_interview_phase(self, user_input: str) -> str:
        """Handle user input during interview phase"""
        question = self.context_interview.get_next_question()
        
        # Process answer through interview system
        success, message = self.context_interview.answer_question(question.question_id, user_input)
        if not success:
            return f"❌ {message}\n\n{question.question_text}"
        
        # Check if all required questions are answered
        answered, total = self.context_interview.get_progress()
        if answered >= total:
            # All required questions answered - transition to conversation mode
            self.conversation_mode = "conversation"
            self.conversation_context.user_context = self.context_interview.current_context
            return "Great! Now I have enough context to help you. What specific musical challenge are you facing?"
        
        # More questions to answer
        return f"✅ {message}\n\n{self._get_next_question_prompt()}"
    
    def _handle_conversation_phase(self, user_input: str) -> str:
        """Handle user input during conversation phase"""
        # Determine response type
        response_type = self._determine_response_type(user_input)
        
        if response_type == "musical_suggestion":
            return self._handle_musical_suggestion(user_input)
        elif response_type == "problem_clarification":
            return self._handle_problem_clarification(user_input)
        elif response_type == "suggestion_refinement":
            return self._handle_suggestion_refinement(user_input)
        else:
            return self._handle_general_conversation(user_input)
    
    def _get_next_question_prompt(self) -> str:
        """Get the next question prompt"""
        question = self.context_interview.get_next_question()
        if question:
            return f"Next question: {question.question_text}"
        else:
            return "Great! Now I have enough context to help you. What specific musical challenge are you facing?"
    
    def _determine_response_type(self, user_input: str) -> str:
        """Determine the type of response needed based on user input"""
        user_input_lower = user_input.lower()
        
        # Check if user is answering interview questions
        if any(keyword in user_input_lower for keyword in ['my song is about', 'the key is', 'tempo is', 'i have']):
            return "context_interview"
        
        # Check if user is asking for musical suggestions
        if any(keyword in user_input_lower for keyword in ['suggest', 'help with', 'what should', 'how can i']):
            return "musical_suggestion"
        
        # Check if user is clarifying a problem
        if any(keyword in user_input_lower for keyword in ['the problem is', 'i need help', 'i can\'t figure out']):
            return "problem_clarification"
        
        # Check if user is refining suggestions
        if any(keyword in user_input_lower for keyword in ['make it', 'change it', 'instead of', 'what about']):
            return "suggestion_refinement"
        
        return "general_conversation"
    
    
    def _handle_musical_suggestion(self, user_input: str) -> str:
        """Handle requests for musical suggestions"""
        if not self.conversation_context.user_context.musical_problem:
            return "I'd love to help with musical suggestions! First, could you tell me what specific musical challenge you're facing?"
        
        # Generate contextual suggestions
        suggestions = self._generate_musical_suggestions(user_input)
        
        if not suggestions:
            return "I need a bit more context to provide good suggestions. Could you tell me more about your song and the specific problem you're facing?"
        
        # Format suggestions for display
        response_parts = ["🎵 Here are some musical suggestions based on your context:\n"]
        
        for i, suggestion in enumerate(suggestions, 1):
            response_parts.append(f"**{i}. {suggestion.title}**")
            response_parts.append(f"   {suggestion.description}")
            response_parts.append(f"   *Musical reasoning: {suggestion.musical_reasoning}*")
            response_parts.append(f"   *Confidence: {suggestion.confidence_score:.1%}*\n")
        
        return "\n".join(response_parts)
    
    def _handle_problem_clarification(self, user_input: str) -> str:
        """Handle problem clarification requests"""
        # Extract the problem from user input
        problem = self._extract_problem_from_input(user_input)
        
        if problem:
            self.conversation_context.current_problem = problem
            self.conversation_context.user_context.musical_problem = problem
            
            return f"""I understand your problem: {problem}

Let me provide some suggestions based on your musical context. Could you also tell me:
1. What key and tempo is your song in?
2. What instruments do you already have?
3. What musical style are you going for?

This will help me give you more targeted suggestions."""
        
        return "Could you tell me more about the specific musical challenge you're facing? The more details you provide, the better I can help."
    
    def _handle_suggestion_refinement(self, user_input: str) -> str:
        """Handle suggestion refinement requests"""
        if not self.suggestion_history:
            return "I don't have any previous suggestions to refine. Could you first ask me for some musical suggestions?"
        
        # This would refine previous suggestions based on user feedback
        return "I'd be happy to refine my suggestions! Could you tell me what specifically you'd like me to change about the previous suggestions?"
    
    def _handle_general_conversation(self, user_input: str) -> str:
        """Handle general conversation"""
        return """I'm here to help with your musical challenges! 

To give you the best suggestions, I need to understand:
1. What's your song about?
2. What musical problem are you facing?
3. What's the key, tempo, and style?
4. What instruments do you already have?

The more context you provide, the better I can help you solve your musical problems."""
    
    def _extract_problem_from_input(self, user_input: str) -> Optional[str]:
        """Extract the musical problem from user input"""
        # Simple extraction - in practice, you'd use more sophisticated NLP
        problem_indicators = [
            'i need help with',
            'i can\'t figure out',
            'the problem is',
            'i\'m struggling with',
            'help me with'
        ]
        
        user_input_lower = user_input.lower()
        for indicator in problem_indicators:
            if indicator in user_input_lower:
                # Extract the problem part
                start_idx = user_input_lower.find(indicator) + len(indicator)
                problem = user_input[start_idx:].strip()
                return problem
        
        return None
    
    def _generate_musical_suggestions(self, user_input: str) -> List[MusicalSuggestion]:
        """Generate contextual musical suggestions"""
        suggestions = []
        
        # Get context for suggestion generation
        context = self._get_suggestion_context()
        
        # Generate suggestions based on the musical problem
        # Use context from interview if available, otherwise fall back to conversation context
        if self.context_interview.is_complete():
            interview_context = self.context_interview.get_context_for_ai()
            problem = interview_context.get('musical_problem', '')
        else:
            problem = self.conversation_context.user_context.musical_problem
        
        if not problem:
            return suggestions
        
        # Simple suggestion generation based on problem type
        if 'bridge' in problem.lower():
            suggestions.extend(self._generate_bridge_suggestions(context))
        elif 'chorus' in problem.lower():
            suggestions.extend(self._generate_chorus_suggestions(context))
        elif 'verse' in problem.lower():
            suggestions.extend(self._generate_verse_suggestions(context))
        elif 'intro' in problem.lower():
            suggestions.extend(self._generate_intro_suggestions(context))
        else:
            suggestions.extend(self._generate_general_suggestions(context))
        
        return suggestions
    
    def _get_suggestion_context(self) -> Dict[str, Any]:
        """Get context for suggestion generation"""
        context = {
            'song_concept': self.conversation_context.user_context.song_concept,
            'key_signature': self.conversation_context.user_context.key_signature,
            'tempo': self.conversation_context.user_context.tempo,
            'existing_parts': self.conversation_context.user_context.existing_parts,
            'style_preferences': self.conversation_context.user_context.style_preferences,
            'emotional_intent': self.conversation_context.user_context.emotional_intent
        }
        
        # Add project state context if available
        if self.conversation_context.project_state:
            context['project_tempo'] = self.conversation_context.project_state.tempo
            context['project_parts'] = self.conversation_context.project_state.musical_parts
            context['chord_progression'] = self.conversation_context.project_state.chord_progression
        
        return context
    
    def _generate_bridge_suggestions(self, context: Dict[str, Any]) -> List[MusicalSuggestion]:
        """Generate suggestions for bridge sections"""
        suggestions = []
        
        key = context.get('key_signature', 'C major')
        tempo = context.get('tempo', 120)
        
        # Suggestion 1: Contrasting key
        suggestions.append(MusicalSuggestion(
            suggestion_id=str(uuid.uuid4()),
            title="Contrasting Key Bridge",
            description=f"Move to a contrasting key (like {self._get_relative_key(key)}) to create tension and contrast",
            musical_reasoning="Bridges often use contrasting keys to provide relief from the main key and create interest",
            implementation_notes=f"Start the bridge in {self._get_relative_key(key)}, then modulate back to {key} for the return",
            confidence_score=0.8,
            suggestion_type="key_change"
        ))
        
        # Suggestion 2: Rhythmic contrast
        suggestions.append(MusicalSuggestion(
            suggestion_id=str(uuid.uuid4()),
            title="Rhythmic Contrast Bridge",
            description="Change the rhythmic feel - if the song is straight, add swing; if it's complex, simplify",
            musical_reasoning="Rhythmic contrast provides variety and keeps the listener engaged",
            implementation_notes="Try changing from straight eighth notes to swung eighth notes, or vice versa",
            confidence_score=0.7,
            suggestion_type="rhythm_change"
        ))
        
        return suggestions
    
    def _generate_chorus_suggestions(self, context: Dict[str, Any]) -> List[MusicalSuggestion]:
        """Generate suggestions for chorus sections"""
        suggestions = []
        
        key = context.get('key_signature', 'C major')
        
        # Suggestion 1: Stronger chord progression
        suggestions.append(MusicalSuggestion(
            suggestion_id=str(uuid.uuid4()),
            title="Stronger Chord Progression",
            description=f"Use a more powerful chord progression in {key} with stronger harmonic movement",
            musical_reasoning="Choruses need strong harmonic support to feel impactful and memorable",
            implementation_notes=f"Try I-V-vi-IV or I-vi-IV-V progressions in {key}",
            confidence_score=0.8,
            suggestion_type="harmony"
        ))
        
        return suggestions
    
    def _generate_verse_suggestions(self, context: Dict[str, Any]) -> List[MusicalSuggestion]:
        """Generate suggestions for verse sections"""
        suggestions = []
        
        # Suggestion 1: Build tension
        suggestions.append(MusicalSuggestion(
            suggestion_id=str(uuid.uuid4()),
            title="Build Tension Toward Chorus",
            description="Use chord progressions that create tension and lead naturally to the chorus",
            musical_reasoning="Verses should build energy and anticipation for the chorus",
            implementation_notes="Try using ii-V progressions or suspended chords to create tension",
            confidence_score=0.7,
            suggestion_type="harmony"
        ))
        
        return suggestions
    
    def _generate_intro_suggestions(self, context: Dict[str, Any]) -> List[MusicalSuggestion]:
        """Generate suggestions for intro sections"""
        suggestions = []
        
        # Suggestion 1: Establish key and mood
        suggestions.append(MusicalSuggestion(
            suggestion_id=str(uuid.uuid4()),
            title="Establish Key and Mood",
            description="Create an intro that establishes the key, tempo, and emotional mood of the song",
            musical_reasoning="Intros set the stage for the entire song and should immediately communicate the song's character",
            implementation_notes="Use the main chord progression or a simplified version to establish the harmonic foundation",
            confidence_score=0.8,
            suggestion_type="arrangement"
        ))
        
        return suggestions
    
    def _generate_general_suggestions(self, context: Dict[str, Any]) -> List[MusicalSuggestion]:
        """Generate general musical suggestions"""
        suggestions = []
        
        # Suggestion 1: Analyze existing parts
        existing_parts = context.get('existing_parts', [])
        if existing_parts:
            suggestions.append(MusicalSuggestion(
                suggestion_id=str(uuid.uuid4()),
                title="Analyze Existing Parts",
                description=f"Look at your existing parts ({', '.join(existing_parts)}) and identify what's missing",
                musical_reasoning="Understanding what you have helps identify what you need",
                implementation_notes="Consider the musical roles: rhythm, harmony, melody, and bass",
                confidence_score=0.6,
                suggestion_type="analysis"
            ))
        
        return suggestions
    
    def _get_relative_key(self, key: str) -> str:
        """Get the relative key of a given key"""
        # Simple relative key mapping
        relative_keys = {
            'C major': 'A minor',
            'G major': 'E minor',
            'D major': 'B minor',
            'A major': 'F# minor',
            'E major': 'C# minor',
            'B major': 'G# minor',
            'F# major': 'D# minor',
            'F major': 'D minor',
            'Bb major': 'G minor',
            'Eb major': 'C minor',
            'Ab major': 'F minor',
            'Db major': 'Bb minor'
        }
        return relative_keys.get(key, 'A minor')
    
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
                'user_context': self.conversation_context.user_context.__dict__,
                'project_state': self.conversation_context.project_state.__dict__ if self.conversation_context.project_state else None,
                'conversation_history': self.conversation_context.conversation_history,
                'suggestion_history': [s.__dict__ for s in self.suggestion_history]
            }
            
            with open(file_path, 'w') as f:
                json.dump(conversation_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False


def demo_conversation():
    """Demo the musical conversation engine"""
    engine = MusicalConversationEngine()
    
    print(engine.start_conversation())
    
    # Simulate a conversation
    responses = [
        "My song is about leaders who shoot the messenger instead of fixing problems",
        "I need help with a bridge that makes sense",
        "The key is G minor and tempo is 120 BPM",
        "I have a DX7 bass line and fuzz guitar",
        "I'm going for a grungy, aggressive sound"
    ]
    
    for response in responses:
        print(f"\nUser: {response}")
        print(f"AI: {engine.process_user_input(response)}")
    
    print("\n" + "="*50)
    print("🎵 CONTEXT SUMMARY")
    print("="*50)
    print(engine.get_context_summary())


if __name__ == "__main__":
    demo_conversation()
