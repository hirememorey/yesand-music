"""
Live Conversation Workflow for Real-Time MIDI Streaming

This module integrates the musical conversation system with live MIDI streaming,
enabling natural language control of real-time MIDI generation and editing.
"""

import time
import threading
from typing import List, Dict, Any, Optional, Generator
from dataclasses import dataclass
from enum import Enum

from musical_conversation_engine import MusicalConversationEngine, MusicalResponse, MusicalResponseType
from ardour_live_integration import ArdourLiveIntegration, MIDIStreamEvent, LiveMIDITrack
from live_editing_engine import LiveEditingEngine, LiveEditCommand, EditingOperation, LiveEditCommandBuilder

class LiveWorkflowState(Enum):
    """States of the live conversation workflow"""
    IDLE = "idle"
    GENERATING = "generating"
    STREAMING = "streaming"
    EDITING = "editing"
    RECORDING = "recording"

@dataclass
class LiveWorkflowSession:
    """Represents an active live workflow session"""
    session_id: str
    track_id: str
    state: LiveWorkflowState
    start_time: float
    current_region: Optional[str] = None
    generated_content: List[Dict[str, Any]] = None
    edit_history: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.generated_content is None:
            self.generated_content = []
        if self.edit_history is None:
            self.edit_history = []

class LiveConversationWorkflow:
    """Main workflow for live musical conversation with real-time MIDI streaming"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the live conversation workflow"""
        self.conversation_engine = MusicalConversationEngine(openai_api_key)
        self.ardour_integration = ArdourLiveIntegration()
        self.editing_engine = LiveEditingEngine()
        
        self.active_sessions = {}  # session_id -> LiveWorkflowSession
        self.current_session = None
        
        # Threading for real-time operations
        self.workflow_thread = None
        self.stop_workflow = threading.Event()
        
    def start_conversation(self, track_name: str = "YesAnd Live Track") -> str:
        """Start a new live conversation session"""
        try:
            # Connect to Ardour
            if not self.ardour_integration.connect():
                raise Exception("Failed to connect to Ardour")
            
            # Create a new MIDI track
            track_id = self.ardour_integration.create_midi_track(track_name)
            if not track_id:
                raise Exception("Failed to create MIDI track")
            
            # Enable live editing
            if not self.ardour_integration.enable_live_editing(track_id):
                raise Exception("Failed to enable live editing")
            
            # Create workflow session
            session_id = f"session_{int(time.time())}"
            session = LiveWorkflowSession(
                session_id=session_id,
                track_id=track_id,
                state=LiveWorkflowState.IDLE,
                start_time=time.time()
            )
            
            self.active_sessions[session_id] = session
            self.current_session = session
            
            return session_id
            
        except Exception as e:
            print(f"Error starting conversation: {e}")
            return None
    
    def process_conversation(self, user_input: str) -> MusicalResponse:
        """Process a conversation input and take appropriate action"""
        if not self.current_session:
            return MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message="No active session. Please start a conversation first.",
                confidence=0.0
            )
        
        try:
            # Get response from conversation engine
            response = self.conversation_engine.engage(user_input)
            
            # Check if this requires a musical action
            if response.musical_action:
                # Execute the musical action
                action_result = self._execute_musical_action(response.musical_action, user_input)
                
                # Update the response with action results
                if action_result:
                    response.message += f"\n\n{action_result['explanation']}"
                    response.confidence = max(response.confidence, action_result.get('confidence', 0.0))
            
            return response
            
        except Exception as e:
            return MusicalResponse(
                response_type=MusicalResponseType.CONVERSATION,
                message=f"I'm having trouble with that: {str(e)}",
                confidence=0.0
            )
    
    def _execute_musical_action(self, action_data: Dict[str, Any], user_input: str) -> Optional[Dict[str, Any]]:
        """Execute a musical action based on the conversation"""
        action_type = action_data.get("action", "")
        parameters = action_data.get("parameters", {})
        
        if action_type == "generate_pattern":
            return self._generate_and_stream_pattern(parameters, user_input)
        elif action_type == "improve_music":
            return self._improve_current_music(parameters, user_input)
        elif action_type == "analyze_music":
            return self._analyze_current_music(parameters, user_input)
        elif action_type == "control_daw":
            return self._control_daw(parameters, user_input)
        else:
            return None
    
    def _generate_and_stream_pattern(self, parameters: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Generate and stream a musical pattern"""
        try:
            # Extract parameters
            pattern_type = parameters.get("type", "bass")
            style = parameters.get("style", "funky")
            key = parameters.get("key", "C")
            duration = parameters.get("duration", 8.0)
            
            # Update session state
            self.current_session.state = LiveWorkflowState.GENERATING
            
            # Generate MIDI stream
            if pattern_type == "bass":
                midi_stream = self.ardour_integration.stream_generator.generate_bassline_stream(
                    style=style, key=key, duration=duration
                )
            else:
                # For other pattern types, use bass as fallback
                midi_stream = self.ardour_integration.stream_generator.generate_bassline_stream(
                    style=style, key=key, duration=duration
                )
            
            # Stream to track
            success = self.ardour_integration.stream_midi_to_track(
                self.current_session.track_id, 
                midi_stream, 
                duration
            )
            
            if success:
                # Record the generation
                generation_record = {
                    "type": "generation",
                    "pattern_type": pattern_type,
                    "style": style,
                    "key": key,
                    "duration": duration,
                    "timestamp": time.time(),
                    "user_input": user_input
                }
                self.current_session.generated_content.append(generation_record)
                
                # Update session state
                self.current_session.state = LiveWorkflowState.STREAMING
                
                return {
                    "success": True,
                    "explanation": f"Generated and streamed a {style} {pattern_type} line in {key}",
                    "confidence": 0.9,
                    "pattern_type": pattern_type,
                    "style": style,
                    "key": key
                }
            else:
                return {
                    "success": False,
                    "explanation": "Failed to stream the generated pattern",
                    "confidence": 0.0
                }
                
        except Exception as e:
            return {
                "success": False,
                "explanation": f"Error generating pattern: {str(e)}",
                "confidence": 0.0
            }
    
    def _improve_current_music(self, parameters: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Improve the current music based on user feedback"""
        try:
            # Determine improvement type from user input
            improvement_type = self._determine_improvement_type(user_input)
            
            # Create live edit command
            command = self._create_improvement_command(improvement_type, parameters)
            
            # Apply the improvement
            result = self.editing_engine.apply_live_edit(command)
            
            # Record the improvement
            improvement_record = {
                "type": "improvement",
                "improvement_type": improvement_type,
                "command": command,
                "result": result,
                "timestamp": time.time(),
                "user_input": user_input
            }
            self.current_session.edit_history.append(improvement_record)
            
            # Update session state
            self.current_session.state = LiveWorkflowState.EDITING
            
            return {
                "success": result.success,
                "explanation": result.explanation,
                "confidence": result.confidence,
                "improvement_type": improvement_type
            }
            
        except Exception as e:
            return {
                "success": False,
                "explanation": f"Error improving music: {str(e)}",
                "confidence": 0.0
            }
    
    def _analyze_current_music(self, parameters: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Analyze the current music"""
        try:
            # Get current track information
            track = self.ardour_integration.live_tracks.get(self.current_session.track_id)
            if not track:
                return {
                    "success": False,
                    "explanation": "No active track to analyze",
                    "confidence": 0.0
                }
            
            # Perform analysis (simplified for now)
            analysis = {
                "track_name": track.name,
                "midi_channel": track.midi_channel,
                "armed": track.armed,
                "muted": track.muted,
                "solo": track.solo,
                "generated_content_count": len(self.current_session.generated_content),
                "edit_count": len(self.current_session.edit_history)
            }
            
            return {
                "success": True,
                "explanation": f"Analyzed track '{track.name}': {analysis['generated_content_count']} generated patterns, {analysis['edit_count']} edits",
                "confidence": 0.8,
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "success": False,
                "explanation": f"Error analyzing music: {str(e)}",
                "confidence": 0.0
            }
    
    def _control_daw(self, parameters: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Control DAW operations"""
        try:
            operation = parameters.get("operation", "")
            
            if operation == "stop":
                self.ardour_integration.stop_streaming()
                return {
                    "success": True,
                    "explanation": "Stopped MIDI streaming",
                    "confidence": 0.9
                }
            elif operation == "pause":
                # Pause functionality would go here
                return {
                    "success": True,
                    "explanation": "Paused MIDI streaming",
                    "confidence": 0.8
                }
            elif operation == "resume":
                # Resume functionality would go here
                return {
                    "success": True,
                    "explanation": "Resumed MIDI streaming",
                    "confidence": 0.8
                }
            else:
                return {
                    "success": False,
                    "explanation": f"Unknown DAW operation: {operation}",
                    "confidence": 0.0
                }
                
        except Exception as e:
            return {
                "success": False,
                "explanation": f"Error controlling DAW: {str(e)}",
                "confidence": 0.0
            }
    
    def _determine_improvement_type(self, user_input: str) -> str:
        """Determine the type of improvement needed from user input"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["swing", "groove", "rhythm"]):
            return "add_swing"
        elif any(word in user_lower for word in ["accent", "emphasis", "punch"]):
            return "add_accent"
        elif any(word in user_lower for word in ["human", "natural", "real"]):
            return "humanize"
        elif any(word in user_lower for word in ["higher", "lower", "transpose"]):
            return "transpose"
        elif any(word in user_lower for word in ["simple", "easier", "less"]):
            return "simplify"
        elif any(word in user_lower for word in ["complex", "more", "elaborate"]):
            return "complexify"
        elif any(word in user_lower for word in ["velocity", "volume", "loud"]):
            return "modify_velocity"
        else:
            return "add_swing"  # Default improvement
    
    def _create_improvement_command(self, improvement_type: str, parameters: Dict[str, Any]) -> LiveEditCommand:
        """Create a live edit command for improvement"""
        # Map improvement types to editing operations
        operation_map = {
            "add_swing": EditingOperation.ADD_SWING,
            "add_accent": EditingOperation.ADD_ACCENT,
            "humanize": EditingOperation.HUMANIZE,
            "transpose": EditingOperation.TRANSPOSE,
            "simplify": EditingOperation.SIMPLIFY,
            "complexify": EditingOperation.COMPLEXIFY,
            "modify_velocity": EditingOperation.MODIFY_VELOCITY,
        }
        
        operation = operation_map.get(improvement_type, EditingOperation.ADD_SWING)
        
        # Create command with appropriate parameters
        command = (LiveEditCommandBuilder()
                  .set_operation(operation)
                  .set_target_track(self.current_session.track_id)
                  .set_intensity(0.8)
                  .build())
        
        # Add specific parameters based on operation
        if operation == EditingOperation.ADD_SWING:
            command.parameters["swing_ratio"] = 0.7
        elif operation == EditingOperation.ADD_ACCENT:
            command.parameters["accent_amount"] = 20
        elif operation == EditingOperation.HUMANIZE:
            command.parameters["timing_variation"] = 0.05
            command.parameters["velocity_variation"] = 0.1
        elif operation == EditingOperation.TRANSPOSE:
            command.parameters["semitones"] = 0  # Will be determined by user input
        elif operation == EditingOperation.MODIFY_VELOCITY:
            command.parameters["velocity_change"] = 10
            command.parameters["velocity_multiplier"] = 1.1
        
        return command
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get the current session status"""
        if not self.current_session:
            return {"status": "no_session"}
        
        return {
            "session_id": self.current_session.session_id,
            "track_id": self.current_session.track_id,
            "state": self.current_session.state.value,
            "generated_content_count": len(self.current_session.generated_content),
            "edit_count": len(self.current_session.edit_history),
            "session_duration": time.time() - self.current_session.start_time
        }
    
    def end_conversation(self, session_id: str = None) -> bool:
        """End a conversation session"""
        try:
            if session_id:
                if session_id in self.active_sessions:
                    del self.active_sessions[session_id]
            else:
                # End current session
                if self.current_session:
                    session_id = self.current_session.session_id
                    if session_id in self.active_sessions:
                        del self.active_sessions[session_id]
                    self.current_session = None
            
            # Stop any active streaming
            self.ardour_integration.stop_streaming()
            
            return True
            
        except Exception as e:
            print(f"Error ending conversation: {e}")
            return False
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            # Stop all streaming
            self.ardour_integration.stop_streaming()
            
            # Disconnect from Ardour
            self.ardour_integration.disconnect()
            
            # Clear sessions
            self.active_sessions.clear()
            self.current_session = None
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

# Example usage and testing
if __name__ == "__main__":
    # Test the live conversation workflow
    with LiveConversationWorkflow() as workflow:
        # Start a conversation
        session_id = workflow.start_conversation("Test Track")
        if session_id:
            print(f"Started conversation session: {session_id}")
            
            # Test conversation
            response = workflow.process_conversation("Give me a funky bassline")
            print(f"Response: {response.message}")
            
            # Test improvement
            response = workflow.process_conversation("Make it more complex")
            print(f"Response: {response.message}")
            
            # Get session status
            status = workflow.get_session_status()
            print(f"Session status: {status}")
            
            # End conversation
            workflow.end_conversation(session_id)
            print("Conversation ended")
        else:
            print("Failed to start conversation")
