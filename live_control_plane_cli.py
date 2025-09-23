#!/usr/bin/env python3
"""
Live Control Plane CLI for Real-Time MIDI Streaming

This CLI provides an interactive interface for live musical conversation
with real-time MIDI streaming to Ardour DAW.
"""

import argparse
import sys
import os
import time
import threading
from typing import Optional, Dict, Any

from live_conversation_workflow import LiveConversationWorkflow, LiveWorkflowState

class LiveControlPlaneCLI:
    """Interactive CLI for live musical conversation"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the live control plane CLI"""
        self.workflow = LiveConversationWorkflow(openai_api_key)
        self.running = False
        self.current_session = None
        
    def start_interactive_mode(self):
        """Start interactive mode"""
        print("🎵 YesAnd Music - Live MIDI Streaming")
        print("=" * 50)
        print("Starting live conversation workflow...")
        
        # Start a conversation session
        session_id = self.workflow.start_conversation("Live Track")
        if not session_id:
            print("❌ Failed to start conversation session")
            print("Make sure Ardour is running and IAC Driver is enabled")
            return
        
        self.current_session = session_id
        self.running = True
        
        print(f"✅ Started session: {session_id}")
        print("🎹 Connected to Ardour - ready for live MIDI streaming!")
        print()
        print("Try these examples:")
        print("  'Give me a funky bassline'")
        print("  'Make it more complex'")
        print("  'Add some swing to it'")
        print("  'Make it brighter'")
        print("  'Stop' to end the session")
        print()
        
        # Start the interactive loop
        self._interactive_loop()
    
    def _interactive_loop(self):
        """Main interactive loop"""
        while self.running:
            try:
                # Get user input
                user_input = input("🎵 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    self._handle_stop()
                    break
                elif user_input.lower() in ['status', 'info']:
                    self._handle_status()
                    continue
                elif user_input.lower() in ['help', '?']:
                    self._handle_help()
                    continue
                elif user_input.lower() in ['clear', 'reset']:
                    self._handle_clear()
                    continue
                
                # Process the conversation
                print("🤖 AI: ", end="", flush=True)
                response = self.workflow.process_conversation(user_input)
                
                # Print response with typing effect
                self._print_with_typing(response.message)
                
                # Show additional info if there's a musical action
                if response.musical_action:
                    print(f"🎼 Action: {response.musical_action.get('action', 'unknown')}")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for assistance")
    
    def _print_with_typing(self, text: str, delay: float = 0.03):
        """Print text with a typing effect"""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()  # Newline at the end
    
    def _handle_stop(self):
        """Handle stop command"""
        print("🛑 Stopping live MIDI streaming...")
        self.workflow.end_conversation(self.current_session)
        self.running = False
        print("✅ Session ended")
    
    def _handle_status(self):
        """Handle status command"""
        status = self.workflow.get_session_status()
        print("\n📊 Session Status:")
        print(f"  Session ID: {status.get('session_id', 'None')}")
        print(f"  Track ID: {status.get('track_id', 'None')}")
        print(f"  State: {status.get('state', 'unknown')}")
        print(f"  Generated Content: {status.get('generated_content_count', 0)}")
        print(f"  Edits: {status.get('edit_count', 0)}")
        print(f"  Duration: {status.get('session_duration', 0):.1f}s")
        print()
    
    def _handle_help(self):
        """Handle help command"""
        print("\n🎵 YesAnd Music - Live MIDI Streaming Help")
        print("=" * 50)
        print("Musical Commands:")
        print("  'Give me a [style] [instrument]' - Generate musical content")
        print("    Examples: 'Give me a funky bassline', 'Create a jazz melody'")
        print()
        print("  'Make it [modification]' - Modify current content")
        print("    Examples: 'Make it more complex', 'Add some swing'")
        print("    Modifications: complex, simple, swing, accent, human, bright, dark")
        print()
        print("  'Change the [element]' - Modify specific elements")
        print("    Examples: 'Change the rhythm', 'Make the bass higher'")
        print()
        print("System Commands:")
        print("  'status' - Show current session status")
        print("  'clear' - Clear conversation history")
        print("  'stop' - End the session")
        print("  'help' - Show this help")
        print()
        print("Musical Styles: funky, jazz, blues, rock, classical, electronic")
        print("Instruments: bass, melody, harmony, drums, piano, guitar")
        print()
    
    def _handle_clear(self):
        """Handle clear command"""
        print("🧹 Clearing conversation history...")
        # Clear conversation history in the workflow
        if hasattr(self.workflow.conversation_engine, 'clear_history'):
            self.workflow.conversation_engine.clear_history()
        print("✅ History cleared")
    
    def run_single_command(self, command: str) -> str:
        """Run a single command and return the result"""
        if not self.current_session:
            # Start a session for single command
            session_id = self.workflow.start_conversation("Command Track")
            if not session_id:
                return "❌ Failed to start session"
            self.current_session = session_id
        
        # Process the command
        response = self.workflow.process_conversation(command)
        
        result = f"🤖 {response.message}"
        if response.musical_action:
            result += f"\n🎼 Action: {response.musical_action.get('action', 'unknown')}"
        
        return result
    
    def cleanup(self):
        """Cleanup resources"""
        if self.current_session:
            self.workflow.end_conversation(self.current_session)
        self.workflow.cleanup()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="YesAnd Music - Live MIDI Streaming Control Plane",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python live_control_plane_cli.py
  python live_control_plane_cli.py --interactive
  python live_control_plane_cli.py --command "Give me a funky bassline"
  python live_control_plane_cli.py --openai-key "sk-your-key-here"
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode (default)"
    )
    
    parser.add_argument(
        "--command", "-c",
        type=str,
        help="Run a single command"
    )
    
    parser.add_argument(
        "--openai-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    
    parser.add_argument(
        "--track-name",
        type=str,
        default="YesAnd Live Track",
        help="Name for the MIDI track (default: 'YesAnd Live Track')"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Get OpenAI API key
    api_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key required")
        print("Set OPENAI_API_KEY environment variable or use --openai-key")
        sys.exit(1)
    
    # Create CLI instance
    cli = LiveControlPlaneCLI(api_key)
    
    try:
        if args.command:
            # Run single command
            result = cli.run_single_command(args.command)
            print(result)
        else:
            # Start interactive mode
            cli.start_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        cli.cleanup()

if __name__ == "__main__":
    main()
