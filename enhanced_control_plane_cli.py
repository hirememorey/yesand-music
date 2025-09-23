#!/usr/bin/env python3
"""
Enhanced Control Plane CLI with Musical Conversation

This CLI provides an interactive interface for the enhanced control plane
with conversational AI capabilities.
"""

import sys
import os
import argparse
import logging
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_control_plane import EnhancedControlPlane

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Enhanced Control Plane CLI with Musical Conversation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start interactive mode
  python enhanced_control_plane_cli.py

  # Execute a single command
  python enhanced_control_plane_cli.py "I need a funky bass line"

  # Start in conversation mode
  python enhanced_control_plane_cli.py --conversation

  # Show enhanced help
  python enhanced_control_plane_cli.py --help-enhanced
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute (if not provided, starts interactive mode)"
    )
    
    parser.add_argument(
        "--conversation",
        action="store_true",
        help="Start in conversation mode"
    )
    
    parser.add_argument(
        "--help-enhanced",
        action="store_true",
        help="Show enhanced help with conversational features"
    )
    
    parser.add_argument(
        "--midi-port",
        help="MIDI output port name (default: from config)"
    )
    
    parser.add_argument(
        "--session-file",
        default="session.json",
        help="Session state file (default: session.json)"
    )
    
    parser.add_argument(
        "--openai-key",
        help="OpenAI API key (default: from OPENAI_API_KEY environment variable)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize enhanced control plane
        enhanced_cp = EnhancedControlPlane(
            midi_port_name=args.midi_port,
            session_file=args.session_file,
            openai_api_key=args.openai_key
        )
        
        # Handle help command
        if args.help_enhanced:
            print(enhanced_cp.get_enhanced_help())
            return 0
        
        # Handle single command
        if args.command:
            if args.conversation:
                # Start conversation mode first
                print(enhanced_cp.execute("start conversation"))
                print()
            
            # Execute the command
            result = enhanced_cp.execute(args.command)
            print(result)
            return 0
        
        # Interactive mode
        run_interactive_mode(enhanced_cp, args.conversation)
        return 0
        
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def run_interactive_mode(enhanced_cp: EnhancedControlPlane, start_conversation: bool = False):
    """Run the interactive mode."""
    print("🎵 Enhanced Control Plane CLI")
    print("=" * 50)
    print("Type 'help' for commands, 'start conversation' for AI chat, or 'quit' to exit")
    print()
    
    if start_conversation:
        print(enhanced_cp.execute("start conversation"))
        print()
    
    while True:
        try:
            # Get user input
            user_input = input("🎵 > ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye! 👋")
                break
            
            if user_input.lower() in ["clear", "cls"]:
                os.system("clear" if os.name == "posix" else "cls")
                continue
            
            if user_input.lower() == "history":
                show_conversation_history(enhanced_cp)
                continue
            
            if user_input.lower() == "project":
                print(enhanced_cp.execute("project status"))
                continue
            
            # Execute the command
            result = enhanced_cp.execute(user_input)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except EOFError:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                import traceback
                traceback.print_exc()

def show_conversation_history(enhanced_cp: EnhancedControlPlane):
    """Show the conversation history."""
    history = enhanced_cp.get_conversation_history()
    
    if not history:
        print("No conversation history.")
        return
    
    print("\n📜 Conversation History:")
    print("-" * 40)
    
    for i, exchange in enumerate(history, 1):
        print(f"{i}. User: {exchange['user']}")
        print(f"   AI: {exchange['response'].message}")
        print()

def show_welcome_message():
    """Show the welcome message."""
    print("""
🎵 Welcome to YesAnd Music Enhanced Control Plane! 🎵

This is your AI-powered musical collaborator that understands natural language
and can help you create, improve, and understand music through conversation.

Quick Start:
1. Type 'start conversation' to begin chatting with your AI musical collaborator
2. Ask for musical patterns: "I need a funky bass line"
3. Give feedback: "Make it more complex"
4. Use musical references: "Make it groove like Stevie Wonder"
5. Learn about music: "Explain what you just did"

Traditional Commands:
- Type 'help' to see all available commands
- Type 'status' to see current state
- Type 'play scale C major' to play a scale

Examples:
- "Generate a funky intro bass beat"
- "This chorus is landing flat, brighten it up"
- "Make it swing like that jazz track"
- "I want something more complex"

Type 'quit' to exit.
""")

if __name__ == "__main__":
    # Show welcome message if no arguments
    if len(sys.argv) == 1:
        show_welcome_message()
    
    sys.exit(main())
