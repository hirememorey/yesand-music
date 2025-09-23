"""
Iterative Musical Workflow

This module handles the conversational music creation process,
allowing users to iteratively refine and improve their musical ideas.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time

from musical_conversation_engine import MusicalConversationEngine, MusicalResponse, MusicalContext
from commands.control_plane import ControlPlane
from commands.types import CommandType
from midi_io import parse_midi_file, save_midi_file
from analysis import apply_swing, filter_notes_by_pitch
from theory import generate_scale, generate_arpeggio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowState(Enum):
    """States of the iterative musical workflow"""
    CONVERSATION = "conversation"
    GENERATING = "generating"
    PRESENTING = "presenting"
    REFINING = "refining"
    COMPLETE = "complete"

@dataclass
class MusicalIteration:
    """A single iteration in the musical workflow"""
    iteration_id: str
    user_input: str
    conversation_response: MusicalResponse
    generated_content: Optional[Dict[str, Any]] = None
    feedback: Optional[str] = None
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()

@dataclass
class MusicalProject:
    """A musical project with iterations and context"""
    project_id: str
    name: str
    context: MusicalContext
    iterations: List[MusicalIteration]
    current_state: WorkflowState
    generated_files: List[str] = None
    
    def __post_init__(self):
        if self.generated_files is None:
            self.generated_files = []

class IterativeMusicalWorkflow:
    """Handles iterative musical creation and refinement"""
    
    def __init__(self, conversation_engine: MusicalConversationEngine, control_plane: ControlPlane):
        """Initialize the iterative musical workflow"""
        self.conversation_engine = conversation_engine
        self.control_plane = control_plane
        self.current_project: Optional[MusicalProject] = None
        self.feedback_handlers = {
            "too_simple": self._handle_too_simple_feedback,
            "too_complex": self._handle_too_complex_feedback,
            "wrong_style": self._handle_wrong_style_feedback,
            "wrong_tempo": self._handle_wrong_tempo_feedback,
            "wrong_key": self._handle_wrong_key_feedback,
            "more_groove": self._handle_more_groove_feedback,
            "brighter": self._handle_brighter_feedback,
            "darker": self._handle_darker_feedback
        }
    
    def start_new_project(self, project_name: str = "untitled") -> MusicalProject:
        """Start a new musical project"""
        project_id = f"project_{int(time.time())}"
        context = self.conversation_engine.context_manager.get_current_context()
        context.project_name = project_name
        
        self.current_project = MusicalProject(
            project_id=project_id,
            name=project_name,
            context=context,
            iterations=[],
            current_state=WorkflowState.CONVERSATION
        )
        
        logger.info(f"Started new musical project: {project_name}")
        return self.current_project
    
    def process_user_input(self, user_input: str) -> Tuple[MusicalResponse, Optional[Dict[str, Any]]]:
        """Process user input and return conversation response and generated content"""
        if not self.current_project:
            self.start_new_project()
        
        # Update project context
        self.conversation_engine.context_manager.current_context = self.current_project.context
        
        # Engage in musical conversation
        conversation_response = self.conversation_engine.engage(user_input)
        
        # Create iteration record
        iteration = MusicalIteration(
            iteration_id=f"iter_{int(time.time())}",
            user_input=user_input,
            conversation_response=conversation_response
        )
        
        # Generate musical content if needed
        generated_content = None
        if conversation_response.musical_action:
            generated_content = self._generate_musical_content(conversation_response.musical_action)
            iteration.generated_content = generated_content
            self.current_project.current_state = WorkflowState.PRESENTING
        else:
            self.current_project.current_state = WorkflowState.CONVERSATION
        
        # Add iteration to project
        self.current_project.iterations.append(iteration)
        
        # Update context with any new information
        self._update_context_from_conversation(conversation_response)
        
        return conversation_response, generated_content
    
    def process_feedback(self, feedback: str) -> Tuple[MusicalResponse, Optional[Dict[str, Any]]]:
        """Process user feedback and generate refined content"""
        if not self.current_project or not self.current_project.iterations:
            return MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message="No active project to provide feedback on. Start a new conversation!",
                confidence=0.0
            ), None
        
        # Get the last iteration
        last_iteration = self.current_project.iterations[-1]
        last_iteration.feedback = feedback
        
        # Determine feedback type and handle accordingly
        feedback_type = self._classify_feedback(feedback)
        refined_action = self._handle_feedback(feedback_type, feedback, last_iteration)
        
        # Generate refined content
        refined_content = None
        if refined_action:
            refined_content = self._generate_musical_content(refined_action)
            self.current_project.current_state = WorkflowState.PRESENTING
        else:
            self.current_project.current_state = WorkflowState.CONVERSATION
        
        # Create new iteration for the refinement
        refinement_iteration = MusicalIteration(
            iteration_id=f"iter_{int(time.time())}",
            user_input=f"Feedback: {feedback}",
            conversation_response=MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message=f"Based on your feedback, I've refined the musical content.",
                confidence=0.8
            ),
            generated_content=refined_content
        )
        
        self.current_project.iterations.append(refinement_iteration)
        
        return refinement_iteration.conversation_response, refined_content
    
    def _generate_musical_content(self, action: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate musical content based on the action"""
        try:
            action_type = action.get("action", "")
            parameters = action.get("parameters", {})
            
            if action_type == "generate_pattern":
                return self._generate_pattern(parameters)
            elif action_type == "improve_music":
                return self._improve_music(parameters)
            elif action_type == "analyze_music":
                return self._analyze_music(parameters)
            else:
                logger.warning(f"Unknown action type: {action_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating musical content: {e}")
            return None
    
    def _generate_pattern(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a musical pattern"""
        pattern_type = parameters.get("type", "bass")
        style = parameters.get("style", "funk")
        key = self.current_project.context.key
        tempo = self.current_project.context.tempo
        
        # Generate pattern based on type and style
        if pattern_type == "bass":
            pattern = self._generate_bass_pattern(style, key, tempo)
        elif pattern_type == "melody":
            pattern = self._generate_melody_pattern(style, key, tempo)
        elif pattern_type == "harmony":
            pattern = self._generate_harmony_pattern(style, key, tempo)
        else:
            pattern = self._generate_generic_pattern(pattern_type, style, key, tempo)
        
        # Save pattern to file
        filename = f"{self.current_project.project_id}_{pattern_type}_{int(time.time())}.mid"
        save_midi_file(pattern, filename)
        self.current_project.generated_files.append(filename)
        
        return {
            "type": "pattern",
            "pattern_type": pattern_type,
            "style": style,
            "filename": filename,
            "notes": pattern,
            "explanation": f"Generated a {style} {pattern_type} pattern in {key} at {tempo} BPM"
        }
    
    def _generate_bass_pattern(self, style: str, key: str, tempo: int) -> List[Dict[str, Any]]:
        """Generate a bass pattern based on style"""
        # This is a simplified example - in practice, you'd have more sophisticated pattern generation
        if style == "funk":
            # Funk bass pattern with syncopation
            pattern = [
                {"pitch": 36, "velocity": 100, "start_time_seconds": 0.0, "duration_seconds": 0.25, "track_index": 0},
                {"pitch": 36, "velocity": 80, "start_time_seconds": 0.5, "duration_seconds": 0.25, "track_index": 0},
                {"pitch": 38, "velocity": 90, "start_time_seconds": 0.75, "duration_seconds": 0.25, "track_index": 0},
                {"pitch": 36, "velocity": 100, "start_time_seconds": 1.0, "duration_seconds": 0.25, "track_index": 0},
            ]
        elif style == "jazz":
            # Jazz walking bass pattern
            pattern = [
                {"pitch": 36, "velocity": 90, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 38, "velocity": 85, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 40, "velocity": 90, "start_time_seconds": 1.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 36, "velocity": 85, "start_time_seconds": 1.5, "duration_seconds": 0.5, "track_index": 0},
            ]
        else:
            # Default pattern
            pattern = [
                {"pitch": 36, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
                {"pitch": 36, "velocity": 80, "start_time_seconds": 1.0, "duration_seconds": 0.5, "track_index": 0},
            ]
        
        return pattern
    
    def _generate_melody_pattern(self, style: str, key: str, tempo: int) -> List[Dict[str, Any]]:
        """Generate a melody pattern"""
        # Generate scale-based melody
        scale_notes = generate_scale(key, "major")
        pattern = []
        
        for i, note in enumerate(scale_notes[:8]):
            pattern.append({
                "pitch": note + 60,  # Middle C range
                "velocity": 80,
                "start_time_seconds": i * 0.5,
                "duration_seconds": 0.4,
                "track_index": 1
            })
        
        return pattern
    
    def _generate_harmony_pattern(self, style: str, key: str, tempo: int) -> List[Dict[str, Any]]:
        """Generate a harmony pattern"""
        # Generate chord progression
        chords = self._get_chord_progression(key, style)
        pattern = []
        
        for i, chord in enumerate(chords):
            for j, note in enumerate(chord):
                pattern.append({
                    "pitch": note + 60,
                    "velocity": 70,
                    "start_time_seconds": i * 1.0,
                    "duration_seconds": 0.9,
                    "track_index": 2
                })
        
        return pattern
    
    def _generate_generic_pattern(self, pattern_type: str, style: str, key: str, tempo: int) -> List[Dict[str, Any]]:
        """Generate a generic pattern"""
        # Fallback pattern generation
        return [
            {"pitch": 60, "velocity": 80, "start_time_seconds": 0.0, "duration_seconds": 0.5, "track_index": 0},
            {"pitch": 62, "velocity": 80, "start_time_seconds": 0.5, "duration_seconds": 0.5, "track_index": 0},
        ]
    
    def _get_chord_progression(self, key: str, style: str) -> List[List[int]]:
        """Get chord progression based on key and style"""
        # Simplified chord progressions
        progressions = {
            "funk": [[0, 4, 7], [2, 5, 9], [0, 4, 7], [2, 5, 9]],  # C-F-C-F
            "jazz": [[0, 4, 7, 11], [2, 5, 9, 12], [0, 4, 7, 11], [2, 5, 9, 12]],  # Cmaj7-Fmaj7
            "default": [[0, 4, 7], [2, 5, 9], [0, 4, 7], [2, 5, 9]]
        }
        
        return progressions.get(style, progressions["default"])
    
    def _improve_music(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Improve existing musical content"""
        # This would integrate with existing musical solvers
        filename = parameters.get("filename")
        improvement_type = parameters.get("improvement_type", "groove")
        
        if filename:
            # Load and improve the file
            notes = parse_midi_file(filename)
            
            if improvement_type == "groove":
                improved_notes = apply_swing(notes, swing_ratio=0.7)
            else:
                improved_notes = notes  # Placeholder
            
            # Save improved version
            improved_filename = f"improved_{filename}"
            save_midi_file(improved_notes, improved_filename)
            self.current_project.generated_files.append(improved_filename)
            
            return {
                "type": "improvement",
                "improvement_type": improvement_type,
                "original_filename": filename,
                "improved_filename": improved_filename,
                "explanation": f"Improved the {improvement_type} of the musical content"
            }
        
        return {"type": "improvement", "error": "No filename provided"}
    
    def _analyze_music(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze musical content"""
        filename = parameters.get("filename")
        
        if filename:
            notes = parse_midi_file(filename)
            
            # Basic analysis
            analysis = {
                "total_notes": len(notes),
                "pitch_range": {
                    "low": min(note["pitch"] for note in notes),
                    "high": max(note["pitch"] for note in notes)
                },
                "duration": max(note["start_time_seconds"] + note["duration_seconds"] for note in notes)
            }
            
            return {
                "type": "analysis",
                "filename": filename,
                "analysis": analysis,
                "explanation": f"Analyzed {filename} - found {analysis['total_notes']} notes"
            }
        
        return {"type": "analysis", "error": "No filename provided"}
    
    def _classify_feedback(self, feedback: str) -> str:
        """Classify the type of feedback"""
        feedback_lower = feedback.lower()
        
        if any(word in feedback_lower for word in ["simple", "basic", "boring"]):
            return "too_simple"
        elif any(word in feedback_lower for word in ["complex", "complicated", "busy"]):
            return "too_complex"
        elif any(word in feedback_lower for word in ["style", "genre", "feel"]):
            return "wrong_style"
        elif any(word in feedback_lower for word in ["tempo", "speed", "slow", "fast"]):
            return "wrong_tempo"
        elif any(word in feedback_lower for word in ["key", "pitch", "higher", "lower"]):
            return "wrong_key"
        elif any(word in feedback_lower for word in ["groove", "rhythm", "swing"]):
            return "more_groove"
        elif any(word in feedback_lower for word in ["bright", "brighter", "lighter"]):
            return "brighter"
        elif any(word in feedback_lower for word in ["dark", "darker", "moody"]):
            return "darker"
        else:
            return "general"
    
    def _handle_feedback(self, feedback_type: str, feedback: str, iteration: MusicalIteration) -> Optional[Dict[str, Any]]:
        """Handle specific types of feedback"""
        if feedback_type in self.feedback_handlers:
            return self.feedback_handlers[feedback_type](feedback, iteration)
        else:
            return self._handle_general_feedback(feedback, iteration)
    
    def _handle_too_simple_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback that the content is too simple"""
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": iteration.generated_content.get("style", "funk"),
                "complexity": "high"
            },
            "explanation": "Adding more complexity and variation to the pattern"
        }
    
    def _handle_too_complex_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback that the content is too complex"""
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": iteration.generated_content.get("style", "funk"),
                "complexity": "low"
            },
            "explanation": "Simplifying the pattern to make it more accessible"
        }
    
    def _handle_wrong_style_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback about wrong style"""
        # Extract new style from feedback
        new_style = "funk"  # Default fallback
        if "jazz" in feedback.lower():
            new_style = "jazz"
        elif "blues" in feedback.lower():
            new_style = "blues"
        elif "rock" in feedback.lower():
            new_style = "rock"
        
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": new_style
            },
            "explanation": f"Changing the style to {new_style}"
        }
    
    def _handle_wrong_tempo_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback about tempo"""
        # Extract tempo from feedback
        new_tempo = self.current_project.context.tempo
        if "slower" in feedback.lower() or "slow" in feedback.lower():
            new_tempo = max(60, new_tempo - 20)
        elif "faster" in feedback.lower() or "fast" in feedback.lower():
            new_tempo = min(200, new_tempo + 20)
        
        self.current_project.context.tempo = new_tempo
        
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": iteration.generated_content.get("style", "funk"),
                "tempo": new_tempo
            },
            "explanation": f"Adjusting tempo to {new_tempo} BPM"
        }
    
    def _handle_wrong_key_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback about key"""
        # Extract key from feedback
        new_key = self.current_project.context.key
        if "higher" in feedback.lower():
            # Move up a fifth
            keys = ["C", "G", "D", "A", "E", "B", "F#", "C#"]
            try:
                current_index = keys.index(new_key)
                new_key = keys[(current_index + 1) % len(keys)]
            except ValueError:
                new_key = "G"
        elif "lower" in feedback.lower():
            # Move down a fifth
            keys = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]
            try:
                current_index = keys.index(new_key)
                new_key = keys[(current_index + 1) % len(keys)]
            except ValueError:
                new_key = "F"
        
        self.current_project.context.key = new_key
        
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": iteration.generated_content.get("style", "funk"),
                "key": new_key
            },
            "explanation": f"Changing key to {new_key}"
        }
    
    def _handle_more_groove_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback asking for more groove"""
        return {
            "action": "improve_music",
            "parameters": {
                "filename": iteration.generated_content.get("filename"),
                "improvement_type": "groove"
            },
            "explanation": "Adding more groove and swing to the pattern"
        }
    
    def _handle_brighter_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback asking for brighter sound"""
        return {
            "action": "improve_music",
            "parameters": {
                "filename": iteration.generated_content.get("filename"),
                "improvement_type": "brightness"
            },
            "explanation": "Making the harmony brighter and more uplifting"
        }
    
    def _handle_darker_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle feedback asking for darker sound"""
        return {
            "action": "improve_music",
            "parameters": {
                "filename": iteration.generated_content.get("filename"),
                "improvement_type": "darkness"
            },
            "explanation": "Making the harmony darker and more moody"
        }
    
    def _handle_general_feedback(self, feedback: str, iteration: MusicalIteration) -> Dict[str, Any]:
        """Handle general feedback"""
        return {
            "action": "generate_pattern",
            "parameters": {
                "type": iteration.generated_content.get("pattern_type", "bass"),
                "style": iteration.generated_content.get("style", "funk")
            },
            "explanation": "Generating a new version based on your feedback"
        }
    
    def _update_context_from_conversation(self, response: MusicalResponse):
        """Update musical context based on conversation response"""
        # Extract musical information from the response
        if "key" in response.message.lower():
            # Try to extract key information
            pass
        if "tempo" in response.message.lower():
            # Try to extract tempo information
            pass
        if "style" in response.message.lower():
            # Try to extract style information
            pass
    
    def get_project_summary(self) -> Dict[str, Any]:
        """Get a summary of the current project"""
        if not self.current_project:
            return {"error": "No active project"}
        
        return {
            "project_id": self.current_project.project_id,
            "name": self.current_project.name,
            "state": self.current_project.current_state.value,
            "iterations": len(self.current_project.iterations),
            "generated_files": self.current_project.generated_files,
            "context": {
                "key": self.current_project.context.key,
                "tempo": self.current_project.context.tempo,
                "style": self.current_project.context.style
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Test the iterative musical workflow
    from musical_conversation_engine import MusicalConversationEngine
    from commands.control_plane import ControlPlane
    
    # Initialize components
    conversation_engine = MusicalConversationEngine()
    control_plane = ControlPlane()
    
    # Create workflow
    workflow = IterativeMusicalWorkflow(conversation_engine, control_plane)
    
    # Test workflow
    print("Starting musical conversation workflow...")
    
    # Start new project
    project = workflow.start_new_project("Test Project")
    print(f"Started project: {project.name}")
    
    # Process user input
    response, content = workflow.process_user_input("I need a funky bass line")
    print(f"Response: {response.message}")
    if content:
        print(f"Generated: {content['explanation']}")
    
    # Process feedback
    feedback_response, refined_content = workflow.process_feedback("Make it more complex")
    print(f"Feedback response: {feedback_response.message}")
    if refined_content:
        print(f"Refined: {refined_content['explanation']}")
    
    # Get project summary
    summary = workflow.get_project_summary()
    print(f"Project summary: {summary}")
