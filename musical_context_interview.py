#!/usr/bin/env python3
"""
Musical Context Interview System

This system guides users through describing their musical context step-by-step,
helping them articulate their musical vision in a way that AI can understand.

Key Features:
- Structured questions that build musical context gradually
- Examples and templates for effective musical descriptions
- Context validation to ensure understanding
- Progressive disclosure from simple to complex concepts
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class MusicalContextType(Enum):
    """Types of musical context we can gather"""
    SONG_CONCEPT = "song_concept"
    TECHNICAL_DETAILS = "technical_details"
    EXISTING_PARTS = "existing_parts"
    MUSICAL_PROBLEM = "musical_problem"
    STYLE_PREFERENCES = "style_preferences"
    EMOTIONAL_INTENT = "emotional_intent"


@dataclass
class MusicalContextQuestion:
    """A single question in the musical context interview"""
    question_id: str
    question_text: str
    context_type: MusicalContextType
    required: bool = True
    examples: Optional[List[str]] = None
    follow_up_questions: Optional[List[str]] = None
    validation_pattern: Optional[str] = None


@dataclass
class MusicalContext:
    """Complete musical context gathered from user"""
    song_concept: Optional[str] = None
    key_signature: Optional[str] = None
    tempo: Optional[int] = None
    time_signature: Optional[str] = None
    existing_parts: List[str] = None
    musical_problem: Optional[str] = None
    style_preferences: List[str] = None
    emotional_intent: Optional[str] = None
    additional_context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.existing_parts is None:
            self.existing_parts = []
        if self.style_preferences is None:
            self.style_preferences = []
        if self.additional_context is None:
            self.additional_context = {}


class MusicalContextInterview:
    """Guides users through describing their musical context"""
    
    def __init__(self):
        self.questions = self._build_question_bank()
        self.current_context = MusicalContext()
        self.interview_state = "initial"
        self.required_questions = [q for q in self.questions if q.required]
        self.optional_questions = [q for q in self.questions if not q.required]
    
    def _build_question_bank(self) -> List[MusicalContextQuestion]:
        """Build the bank of questions for the musical context interview"""
        return [
            # Song Concept - Most important for understanding the musical vision
            MusicalContextQuestion(
                question_id="song_concept",
                question_text="What's your song about? What's the concept or story?",
                context_type=MusicalContextType.SONG_CONCEPT,
                required=True,
                examples=[
                    "A song about leaders who shoot the messenger instead of fixing problems",
                    "A love song about long-distance relationships",
                    "A protest song about environmental destruction"
                ]
            ),
            
            # Technical Details - Basic musical information
            MusicalContextQuestion(
                question_id="key_signature",
                question_text="What key is your song in?",
                context_type=MusicalContextType.TECHNICAL_DETAILS,
                required=True,
                examples=["G minor", "C major", "F# minor", "Bb major"],
                validation_pattern=r"^[A-G][#b]?\s+(major|minor|maj|min)$"
            ),
            
            MusicalContextQuestion(
                question_id="tempo",
                question_text="What's the tempo (BPM)?",
                context_type=MusicalContextType.TECHNICAL_DETAILS,
                required=True,
                examples=["120", "140", "80", "160"],
                validation_pattern=r"^\d+$"
            ),
            
            MusicalContextQuestion(
                question_id="time_signature",
                question_text="What's the time signature?",
                context_type=MusicalContextType.TECHNICAL_DETAILS,
                required=False,
                examples=["4/4", "3/4", "6/8", "7/8"],
                validation_pattern=r"^\d+/\d+$"
            ),
            
            # Existing Parts - What's already in the song
            MusicalContextQuestion(
                question_id="existing_parts",
                question_text="What instruments or parts do you already have?",
                context_type=MusicalContextType.EXISTING_PARTS,
                required=True,
                examples=[
                    "DX7 bass line, Dexed whistle effect, fuzz guitar",
                    "Piano, vocals, drums",
                    "Acoustic guitar, strings, percussion"
                ]
            ),
            
            # Musical Problem - What they need help with
            MusicalContextQuestion(
                question_id="musical_problem",
                question_text="What specific musical challenge are you facing?",
                context_type=MusicalContextType.MUSICAL_PROBLEM,
                required=True,
                examples=[
                    "I need help with a bridge that makes sense",
                    "The chorus doesn't feel strong enough",
                    "I can't figure out the right chord progression",
                    "The arrangement feels too busy"
                ]
            ),
            
            # Style Preferences - Musical taste and direction
            MusicalContextQuestion(
                question_id="style_preferences",
                question_text="What musical styles or artists are you inspired by?",
                context_type=MusicalContextType.STYLE_PREFERENCES,
                required=False,
                examples=[
                    "Grunge, Alice in Chains, Soundgarden",
                    "Jazz, Miles Davis, Bill Evans",
                    "Electronic, Aphex Twin, Boards of Canada"
                ]
            ),
            
            # Emotional Intent - The feeling they want to create
            MusicalContextQuestion(
                question_id="emotional_intent",
                question_text="What mood or feeling are you trying to create?",
                context_type=MusicalContextType.EMOTIONAL_INTENT,
                required=False,
                examples=[
                    "Dark, aggressive, confrontational",
                    "Melancholic, introspective, vulnerable",
                    "Energetic, uplifting, triumphant"
                ]
            )
        ]
    
    def start_interview(self) -> str:
        """Start the musical context interview"""
        self.interview_state = "in_progress"
        self.current_context = MusicalContext()
        
        return """🎵 Welcome to the Musical Context Interview!

I'm here to help you describe your musical vision so I can give you the best possible suggestions. 
Let's start with the basics and build up to the specific challenge you're facing.

This will take about 2-3 minutes, and I'll ask you questions step by step.
"""
    
    def get_next_question(self) -> Optional[MusicalContextQuestion]:
        """Get the next question in the interview"""
        if self.interview_state != "in_progress":
            return None
        
        # Find the first unanswered required question
        for question in self.required_questions:
            if not self._is_question_answered(question):
                return question
        
        # If all required questions are answered, offer optional questions
        for question in self.optional_questions:
            if not self._is_question_answered(question):
                return question
        
        # All questions answered
        self.interview_state = "completed"
        return None
    
    def _is_question_answered(self, question: MusicalContextQuestion) -> bool:
        """Check if a question has been answered"""
        if question.question_id == "song_concept":
            return self.current_context.song_concept is not None
        elif question.question_id == "key_signature":
            return self.current_context.key_signature is not None
        elif question.question_id == "tempo":
            return self.current_context.tempo is not None
        elif question.question_id == "time_signature":
            return self.current_context.time_signature is not None
        elif question.question_id == "existing_parts":
            return len(self.current_context.existing_parts) > 0
        elif question.question_id == "musical_problem":
            return self.current_context.musical_problem is not None
        elif question.question_id == "style_preferences":
            return len(self.current_context.style_preferences) > 0
        elif question.question_id == "emotional_intent":
            return self.current_context.emotional_intent is not None
        
        return False
    
    def answer_question(self, question_id: str, answer: str) -> Tuple[bool, str]:
        """Answer a question in the interview"""
        if self.interview_state != "in_progress":
            return False, "Interview is not in progress"
        
        # Validate the answer
        question = self._get_question_by_id(question_id)
        if not question:
            return False, f"Question {question_id} not found"
        
        if question.validation_pattern:
            if not re.match(question.validation_pattern, answer.strip()):
                return False, f"Invalid format. Examples: {', '.join(question.examples or [])}"
        
        # Store the answer
        success = self._store_answer(question_id, answer)
        if not success:
            return False, "Failed to store answer"
        
        return True, "Answer recorded successfully"
    
    def _get_question_by_id(self, question_id: str) -> Optional[MusicalContextQuestion]:
        """Get a question by its ID"""
        for question in self.questions:
            if question.question_id == question_id:
                return question
        return None
    
    def _store_answer(self, question_id: str, answer: str) -> bool:
        """Store an answer in the current context"""
        try:
            if question_id == "song_concept":
                self.current_context.song_concept = answer.strip()
            elif question_id == "key_signature":
                self.current_context.key_signature = answer.strip()
            elif question_id == "tempo":
                self.current_context.tempo = int(answer.strip())
            elif question_id == "time_signature":
                self.current_context.time_signature = answer.strip()
            elif question_id == "existing_parts":
                # Split by comma and clean up
                parts = [part.strip() for part in answer.split(",")]
                self.current_context.existing_parts = parts
            elif question_id == "musical_problem":
                self.current_context.musical_problem = answer.strip()
            elif question_id == "style_preferences":
                # Split by comma and clean up
                styles = [style.strip() for style in answer.split(",")]
                self.current_context.style_preferences = styles
            elif question_id == "emotional_intent":
                self.current_context.emotional_intent = answer.strip()
            else:
                return False
            
            return True
        except (ValueError, AttributeError):
            return False
    
    def get_context_summary(self) -> str:
        """Get a summary of the gathered context"""
        if self.interview_state != "completed":
            return "Interview not completed yet"
        
        summary_parts = []
        
        if self.current_context.song_concept:
            summary_parts.append(f"🎵 Song Concept: {self.current_context.song_concept}")
        
        if self.current_context.key_signature and self.current_context.tempo:
            summary_parts.append(f"🎼 Key: {self.current_context.key_signature}, Tempo: {self.current_context.tempo} BPM")
        
        if self.current_context.time_signature:
            summary_parts.append(f"⏱️ Time Signature: {self.current_context.time_signature}")
        
        if self.current_context.existing_parts:
            summary_parts.append(f"🎸 Existing Parts: {', '.join(self.current_context.existing_parts)}")
        
        if self.current_context.musical_problem:
            summary_parts.append(f"❓ Musical Challenge: {self.current_context.musical_problem}")
        
        if self.current_context.style_preferences:
            summary_parts.append(f"🎨 Style Influences: {', '.join(self.current_context.style_preferences)}")
        
        if self.current_context.emotional_intent:
            summary_parts.append(f"💭 Emotional Intent: {self.current_context.emotional_intent}")
        
        return "\n".join(summary_parts)
    
    def get_context_for_ai(self) -> Dict[str, Any]:
        """Get the context in a format suitable for AI processing"""
        return {
            "song_concept": self.current_context.song_concept,
            "key_signature": self.current_context.key_signature,
            "tempo": self.current_context.tempo,
            "time_signature": self.current_context.time_signature,
            "existing_parts": self.current_context.existing_parts,
            "musical_problem": self.current_context.musical_problem,
            "style_preferences": self.current_context.style_preferences,
            "emotional_intent": self.current_context.emotional_intent,
            "additional_context": self.current_context.additional_context
        }
    
    def is_complete(self) -> bool:
        """Check if the interview is complete"""
        return self.interview_state == "completed"
    
    def get_progress(self) -> Tuple[int, int]:
        """Get interview progress (answered, total)"""
        answered = sum(1 for q in self.required_questions if self._is_question_answered(q))
        total = len(self.required_questions)
        return answered, total


def demo_interview():
    """Demo the musical context interview system"""
    interview = MusicalContextInterview()
    
    print(interview.start_interview())
    
    while not interview.is_complete():
        question = interview.get_next_question()
        if not question:
            break
        
        print(f"\n{question.question_text}")
        if question.examples:
            print(f"Examples: {', '.join(question.examples)}")
        
        answer = input("Your answer: ").strip()
        
        success, message = interview.answer_question(question.question_id, answer)
        if not success:
            print(f"❌ {message}")
            continue
        
        print(f"✅ {message}")
    
    print("\n" + "="*50)
    print("🎵 CONTEXT SUMMARY")
    print("="*50)
    print(interview.get_context_summary())
    
    print("\n" + "="*50)
    print("🤖 AI CONTEXT")
    print("="*50)
    print(json.dumps(interview.get_context_for_ai(), indent=2))


if __name__ == "__main__":
    demo_interview()
