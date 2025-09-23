"""
Musical Conversation Engine

This module provides a conversational interface for musical collaboration,
allowing users to engage in natural musical dialogue rather than rigid commands.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicalResponseType(Enum):
    """Types of musical responses"""
    CONVERSATION = "conversation"
    MUSICAL_ACTION = "musical_action"
    CLARIFICATION = "clarification"
    REFERENCE = "reference"
    FEEDBACK_REQUEST = "feedback_request"

@dataclass
class MusicalContext:
    """Current musical context and state"""
    key: str = "C"
    tempo: int = 120
    time_signature: str = "4/4"
    style: str = "unknown"
    recent_patterns: List[str] = None
    current_track: str = "unknown"
    project_name: str = "untitled"
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.recent_patterns is None:
            self.recent_patterns = []
        if self.user_preferences is None:
            self.user_preferences = {}

@dataclass
class MusicalReference:
    """Musical reference for context and examples"""
    name: str
    type: str  # "artist", "song", "style", "technique"
    description: str
    examples: List[str]
    musical_elements: Dict[str, Any]

@dataclass
class MusicalResponse:
    """Response from the musical conversation engine"""
    response_type: MusicalResponseType
    message: str
    musical_action: Optional[Dict[str, Any]] = None
    references: List[MusicalReference] = None
    follow_up_questions: List[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.references is None:
            self.references = []
        if self.follow_up_questions is None:
            self.follow_up_questions = []

class MusicalReferenceLibrary:
    """Library of musical references and examples"""
    
    def __init__(self):
        self.references = {
            "funky": [
                MusicalReference(
                    name="Bootsy Collins",
                    type="artist",
                    description="Funk bass legend known for syncopated, percussive bass lines",
                    examples=["One Nation Under a Groove", "Flash Light"],
                    musical_elements={"rhythm": "syncopated", "technique": "slap", "feel": "groove"}
                ),
                MusicalReference(
                    name="James Brown",
                    type="artist", 
                    description="Godfather of Soul, master of the one beat",
                    examples=["Get Up (I Feel Like Being a) Sex Machine", "Super Bad"],
                    musical_elements={"rhythm": "on-beat", "technique": "muted", "feel": "driving"}
                )
            ],
            "groove": [
                MusicalReference(
                    name="Stevie Wonder",
                    type="artist",
                    description="Master of musical groove and feel",
                    examples=["Superstition", "Higher Ground"],
                    musical_elements={"rhythm": "syncopated", "harmony": "complex", "feel": "smooth"}
                ),
                MusicalReference(
                    name="Earth Wind & Fire",
                    type="artist",
                    description="Funk and R&B with complex arrangements",
                    examples=["September", "Boogie Wonderland"],
                    musical_elements={"rhythm": "polyrhythmic", "harmony": "jazz-influenced", "feel": "uplifting"}
                )
            ],
            "bright": [
                MusicalReference(
                    name="Major 7th chords",
                    type="technique",
                    description="Chords that add brightness and openness",
                    examples=["Cmaj7", "Fmaj7", "Gmaj7"],
                    musical_elements={"harmony": "major_7th", "feel": "bright", "color": "open"}
                ),
                MusicalReference(
                    name="Higher register voicings",
                    type="technique",
                    description="Playing chords in higher octaves for brightness",
                    examples=["Drop 2 voicings", "Spread voicings"],
                    musical_elements={"register": "high", "feel": "bright", "technique": "voicing"}
                )
            ],
            "jazz": [
                MusicalReference(
                    name="Miles Davis",
                    type="artist",
                    description="Jazz trumpet legend, master of space and phrasing",
                    examples=["Kind of Blue", "So What"],
                    musical_elements={"rhythm": "swing", "harmony": "modal", "feel": "cool"}
                ),
                MusicalReference(
                    name="Swing feel",
                    type="technique",
                    description="Rhythmic feel where off-beats are delayed",
                    examples=["8th note swing", "16th note swing"],
                    musical_elements={"rhythm": "swing", "feel": "groove", "technique": "timing"}
                )
            ]
        }
    
    def get_relevant_references(self, user_input: str) -> List[MusicalReference]:
        """Find musical references relevant to the user's input"""
        relevant_refs = []
        user_lower = user_input.lower()
        
        for category, refs in self.references.items():
            if category in user_lower:
                relevant_refs.extend(refs)
            else:
                # Check for keyword matches
                for ref in refs:
                    if any(keyword in user_lower for keyword in [ref.name.lower(), ref.type.lower()]):
                        relevant_refs.append(ref)
        
        return relevant_refs[:3]  # Limit to top 3 references

class MusicalContextManager:
    """Manages musical context and state"""
    
    def __init__(self):
        self.current_context = MusicalContext()
        self.conversation_history = []
    
    def get_current_context(self) -> MusicalContext:
        """Get the current musical context"""
        return self.current_context
    
    def update_context(self, key: str = None, tempo: int = None, style: str = None, 
                      track: str = None, project: str = None):
        """Update the musical context"""
        if key:
            self.current_context.key = key
        if tempo:
            self.current_context.tempo = tempo
        if style:
            self.current_context.style = style
        if track:
            self.current_context.current_track = track
        if project:
            self.current_context.project_name = project
    
    def add_pattern(self, pattern: str):
        """Add a recent pattern to context"""
        self.current_context.recent_patterns.append(pattern)
        # Keep only last 5 patterns
        if len(self.current_context.recent_patterns) > 5:
            self.current_context.recent_patterns = self.current_context.recent_patterns[-5:]
    
    def add_to_history(self, user_input: str, response: MusicalResponse):
        """Add to conversation history"""
        self.conversation_history.append({
            "user": user_input,
            "response": response,
            "timestamp": __import__("time").time()
        })
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

class MusicalConversationEngine:
    """Core engine for musical conversation and collaboration"""
    
    def __init__(self, api_key: str = None):
        """Initialize the musical conversation engine"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.context_manager = MusicalContextManager()
        self.reference_library = MusicalReferenceLibrary()
        
        # Musical conversation prompts
        self.conversation_prompts = {
            "system": """You are a musical collaborator and expert. You help musicians create, improve, and understand music through natural conversation.

Your role:
- Speak like a musician would - with references, feelings, and musical intuition
- Ask clarifying questions to understand musical intent
- Provide musical examples and references
- Suggest alternatives and variations
- Explain musical concepts in accessible terms
- Be encouraging and supportive

You understand:
- All musical genres and styles
- Musical terminology and slang
- The creative process and musical workflow
- How musicians think and communicate
- The importance of feel, groove, and musical expression

Respond naturally and musically, not like a technical manual.""",
            
            "conversation": """The user said: "{user_input}"

Current musical context:
- Key: {key}
- Tempo: {tempo} BPM
- Time signature: {time_signature}
- Style: {style}
- Current track: {current_track}
- Project: {project_name}
- Recent patterns: {recent_patterns}

Relevant musical references:
{references}

Respond as a musical collaborator. Be conversational, ask questions, provide examples, and suggest musical ideas. If you need to take a musical action, explain what you're doing and why.""",
            
            "action": """Based on the conversation, determine what musical action to take.

Available actions:
- generate_pattern: Create musical patterns (bass, melody, harmony, rhythm)
- improve_music: Enhance existing musical content
- analyze_music: Analyze musical elements
- control_daw: Interact with DAW (Ardour, etc.)
- explain_concept: Explain musical concepts

Return JSON with:
{{
    "action": "action_name",
    "parameters": {{}},
    "explanation": "Why this action and what it will do",
    "confidence": 0.0-1.0
}}"""
        }
    
    def engage(self, user_input: str) -> MusicalResponse:
        """Engage in musical conversation with the user"""
        try:
            # Get current context
            context = self.context_manager.get_current_context()
            
            # Get relevant references
            references = self.reference_library.get_relevant_references(user_input)
            
            # Format references for prompt
            ref_text = "\n".join([
                f"- {ref.name} ({ref.type}): {ref.description}"
                for ref in references
            ]) if references else "None"
            
            # Build conversation prompt
            prompt = self.conversation_prompts["conversation"].format(
                user_input=user_input,
                key=context.key,
                tempo=context.tempo,
                time_signature=context.time_signature,
                style=context.style,
                current_track=context.current_track,
                project_name=context.project_name,
                recent_patterns=", ".join(context.recent_patterns) if context.recent_patterns else "None",
                references=ref_text
            )
            
            # Get LLM response
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.conversation_prompts["system"]},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            message = response.choices[0].message.content
            
            # Determine if this needs a musical action
            action_response = self._determine_musical_action(user_input, message)
            
            # Create musical response
            musical_response = MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message=message,
                musical_action=action_response.get("action_data") if action_response else None,
                references=references,
                confidence=action_response.get("confidence", 0.0) if action_response else 0.0
            )
            
            # Add to conversation history
            self.context_manager.add_to_history(user_input, musical_response)
            
            return musical_response
            
        except Exception as e:
            logger.error(f"Error in musical conversation: {e}")
            return MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message="I'm having trouble understanding that. Could you try rephrasing it?",
                confidence=0.0
            )
    
    def _determine_musical_action(self, user_input: str, llm_response: str) -> Optional[Dict[str, Any]]:
        """Determine if a musical action is needed based on the conversation"""
        try:
            # Check if the response suggests a musical action
            action_keywords = [
                "generate", "create", "make", "build", "compose",
                "improve", "enhance", "fix", "adjust", "modify",
                "analyze", "examine", "look at", "check",
                "play", "record", "export", "import"
            ]
            
            if any(keyword in llm_response.lower() for keyword in action_keywords):
                # Ask LLM to determine the specific action
                action_prompt = self.conversation_prompts["action"]
                
                action_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"User: {user_input}\nLLM Response: {llm_response}\n\n{action_prompt}"}
                    ],
                    temperature=0.3,
                    max_tokens=200
                )
                
                action_text = action_response.choices[0].message.content
                
                # Try to parse JSON response
                try:
                    action_data = json.loads(action_text)
                    return action_data
                except json.JSONDecodeError:
                    # Fallback to simple action detection
                    return {
                        "action": "generate_pattern",
                        "parameters": {"type": "bass", "style": "funky"},
                        "explanation": "Generating a musical pattern based on your request",
                        "confidence": 0.7
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error determining musical action: {e}")
            return None
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history"""
        return self.context_manager.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.context_manager.conversation_history = []

# Example usage and testing
if __name__ == "__main__":
    # Test the musical conversation engine
    engine = MusicalConversationEngine()
    
    # Test conversations
    test_inputs = [
        "I need a funky bass line for my song",
        "This chorus sounds flat, how can I brighten it up?",
        "Make it groove like that Stevie Wonder track",
        "I want something jazzy but not too complex"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = engine.engage(user_input)
        print(f"Response: {response.message}")
        if response.musical_action:
            print(f"Action: {response.musical_action}")
        print("-" * 50)
