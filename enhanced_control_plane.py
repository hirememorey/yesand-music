"""
Enhanced Control Plane with Musical Conversation Engine

This module extends the existing control plane with conversational AI capabilities,
allowing users to engage in natural musical dialogue rather than rigid commands.
"""

import logging
from typing import Optional, Dict, Any, Tuple
import time
import os

from commands.control_plane import ControlPlane
from musical_conversation_engine import MusicalConversationEngine, MusicalResponse, MusicalResponseType
from iterative_musical_workflow import IterativeMusicalWorkflow, WorkflowState
from commands.types import Command, CommandType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedControlPlane(ControlPlane):
    """Enhanced control plane with conversational AI capabilities"""
    
    def __init__(self, midi_port_name: str = None, session_file: str = "session.json", 
                 openai_api_key: str = None) -> None:
        """Initialize the enhanced control plane.
        
        Args:
            midi_port_name: Name of the MIDI output port
            session_file: Path to the session state file
            openai_api_key: OpenAI API key for LLM integration
        """
        # Initialize base control plane
        super().__init__(midi_port_name, session_file)
        
        # Initialize musical conversation engine
        self.conversation_engine = MusicalConversationEngine(openai_api_key)
        
        # Initialize iterative workflow
        self.workflow = IterativeMusicalWorkflow(self.conversation_engine, self)
        
        # Conversation state
        self.conversation_mode = False
        self.current_project = None
        
        logger.info("Enhanced Control Plane initialized with conversational AI")
    
    def execute(self, command_text: str) -> str:
        """Execute a command with conversational AI fallback.
        
        Args:
            command_text: The command text to execute
            
        Returns:
            Response message indicating success or failure
        """
        # First, try to parse as a traditional command
        command = self.parser.parse(command_text)
        
        if command is not None:
            # Handle traditional commands normally
            return super().execute(command_text)
        
        # If not a traditional command, try conversational AI
        return self._handle_conversational_command(command_text)
    
    def _handle_conversational_command(self, user_input: str) -> str:
        """Handle conversational commands using the musical conversation engine.
        
        Args:
            user_input: The user's natural language input
            
        Returns:
            Response message from the conversation engine
        """
        try:
            # Check for conversation mode commands
            if user_input.lower().strip() in ["start conversation", "conversation mode", "chat mode"]:
                return self._start_conversation_mode()
            
            if user_input.lower().strip() in ["stop conversation", "exit conversation", "command mode"]:
                return self._stop_conversation_mode()
            
            if user_input.lower().strip() in ["project status", "show project", "current project"]:
                return self._show_project_status()
            
            if user_input.lower().strip() in ["clear project", "new project", "reset project"]:
                return self._clear_project()
            
            # Process the conversational input
            response, generated_content = self.workflow.process_user_input(user_input)
            
            # Format the response
            response_text = response.message
            
            # Add information about generated content
            if generated_content:
                response_text += f"\n\n🎵 Generated: {generated_content.get('explanation', 'Musical content created')}"
                
                # If it's a pattern, offer to play it
                if generated_content.get('type') == 'pattern' and generated_content.get('filename'):
                    response_text += f"\n\nTo play this pattern, use: play file {generated_content['filename']}"
            
            # Add follow-up suggestions
            if response.follow_up_questions:
                response_text += "\n\n💭 You can also ask:"
                for question in response.follow_up_questions[:3]:  # Limit to 3 suggestions
                    response_text += f"\n- {question}"
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error in conversational command: {e}")
            return f"I'm having trouble understanding that. Could you try rephrasing it? Error: {str(e)}"
    
    def _start_conversation_mode(self) -> str:
        """Start conversation mode for extended musical dialogue."""
        self.conversation_mode = True
        self.current_project = self.workflow.start_new_project("Conversation Project")
        
        return """🎵 Conversation mode started! 

I'm now your musical collaborator. You can:
- Ask me to generate musical patterns and ideas
- Describe what you want musically in your own words
- Give me feedback on what I create
- Ask me to explain musical concepts
- Have a natural musical conversation

Try saying something like:
- "I need a funky bass line for my song"
- "This chorus sounds flat, can you help?"
- "Make it groove like that Stevie Wonder track"
- "I want something jazzy but not too complex"

Type 'stop conversation' to return to command mode."""
    
    def _stop_conversation_mode(self) -> str:
        """Stop conversation mode and return to command mode."""
        self.conversation_mode = False
        project_summary = self.workflow.get_project_summary()
        
        return f"""🎵 Conversation mode stopped.

Project Summary:
- Iterations: {project_summary.get('iterations', 0)}
- Generated files: {len(project_summary.get('generated_files', []))}
- Current state: {project_summary.get('state', 'unknown')}

You're now back in command mode. Type 'help' for available commands."""
    
    def _show_project_status(self) -> str:
        """Show the current project status."""
        if not self.current_project:
            return "No active project. Start a conversation to begin a new project."
        
        summary = self.workflow.get_project_summary()
        
        status_text = f"""🎵 Current Project: {summary.get('name', 'Unknown')}

Context:
- Key: {summary['context']['key']}
- Tempo: {summary['context']['tempo']} BPM
- Style: {summary['context']['style']}

Progress:
- Iterations: {summary.get('iterations', 0)}
- Generated files: {len(summary.get('generated_files', []))}
- Current state: {summary.get('state', 'unknown')}

Generated Files:"""
        
        for i, filename in enumerate(summary.get('generated_files', []), 1):
            status_text += f"\n{i}. {filename}"
        
        return status_text
    
    def _clear_project(self) -> str:
        """Clear the current project and start fresh."""
        self.current_project = None
        self.workflow.current_project = None
        self.conversation_engine.context_manager.conversation_history = []
        
        return "🎵 Project cleared. Ready for a fresh start!"
    
    def process_feedback(self, feedback: str) -> str:
        """Process user feedback on generated content.
        
        Args:
            feedback: User feedback on the current musical content
            
        Returns:
            Response message with refined content
        """
        try:
            if not self.current_project:
                return "No active project to provide feedback on. Start a conversation first!"
            
            response, refined_content = self.workflow.process_feedback(feedback)
            
            # Format the response
            response_text = response.message
            
            # Add information about refined content
            if refined_content:
                response_text += f"\n\n🎵 Refined: {refined_content.get('explanation', 'Musical content refined')}"
                
                # If it's a pattern, offer to play it
                if refined_content.get('type') == 'pattern' and refined_content.get('filename'):
                    response_text += f"\n\nTo play this refined pattern, use: play file {refined_content['filename']}"
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            return f"I'm having trouble processing that feedback. Could you try rephrasing it? Error: {str(e)}"
    
    def get_conversation_history(self) -> list:
        """Get the conversation history."""
        return self.conversation_engine.get_conversation_history()
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_engine.clear_history()
        self.workflow.current_project = None
        self.current_project = None
    
    def get_enhanced_help(self) -> str:
        """Get enhanced help text including conversational features."""
        base_help = self.parser.get_help_text()
        
        enhanced_help = f"""{base_help}

🎵 CONVERSATIONAL AI FEATURES:

Start a musical conversation:
- "start conversation" - Begin conversational mode
- "I need a funky bass line" - Generate musical patterns
- "This sounds flat, make it brighter" - Provide feedback
- "Make it groove like Stevie Wonder" - Use musical references
- "Explain what you just did" - Learn about music

Project management:
- "project status" - Show current project
- "clear project" - Start fresh
- "stop conversation" - Return to command mode

Examples of natural musical language:
- "Generate a funky intro bass beat"
- "This chorus is landing flat, brighten it up"
- "Make it swing like that jazz track"
- "I want something more complex"
- "Can you make it simpler?"
- "What key would work better for this?"

The AI understands musical references, feelings, and context!
"""
        
        return enhanced_help

# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced control plane
    print("Testing Enhanced Control Plane...")
    
    try:
        # Initialize enhanced control plane
        enhanced_cp = EnhancedControlPlane()
        
        # Test traditional commands
        print("\n=== Testing Traditional Commands ===")
        print(enhanced_cp.execute("status"))
        print(enhanced_cp.execute("play scale C major"))
        
        # Test conversational commands
        print("\n=== Testing Conversational Commands ===")
        print(enhanced_cp.execute("start conversation"))
        print(enhanced_cp.execute("I need a funky bass line"))
        print(enhanced_cp.execute("Make it more complex"))
        print(enhanced_cp.execute("project status"))
        print(enhanced_cp.execute("stop conversation"))
        
        # Test enhanced help
        print("\n=== Enhanced Help ===")
        print(enhanced_cp.get_enhanced_help())
        
    except Exception as e:
        print(f"Error testing enhanced control plane: {e}")
        print("Make sure you have the OpenAI API key set in your environment variables.")
