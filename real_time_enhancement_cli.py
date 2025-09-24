#!/usr/bin/env python3
"""
Real-Time Enhancement CLI

Command-line interface for real-time track enhancement in Ardour.
Provides interactive and command-line access to LLM-powered track enhancement.
"""

import argparse
import logging
import sys
import time
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from real_time_ardour_enhancer import RealTimeArdourEnhancer
from llm_track_enhancer import EnhancementResult


class RealTimeEnhancementCLI:
    """CLI interface for real-time track enhancement."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize CLI."""
        self.enhancer = RealTimeArdourEnhancer(openai_api_key)
        self.session_id = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('enhancement.log')
            ]
        )
    
    def start_session(self, session_id: str = None) -> bool:
        """Start enhancement session."""
        try:
            self.session_id = self.enhancer.start_enhancement_session(session_id)
            if self.session_id:
                print(f"✅ Started enhancement session: {self.session_id}")
                return True
            else:
                print("❌ Failed to start enhancement session")
                return False
        except Exception as e:
            print(f"❌ Error starting session: {e}")
            return False
    
    def stop_session(self):
        """Stop enhancement session."""
        try:
            self.enhancer.stop_enhancement_session()
            print("✅ Stopped enhancement session")
        except Exception as e:
            print(f"❌ Error stopping session: {e}")
    
    def enhance_track(self, user_request: str, track_id: str = None, 
                     enhancement_type: str = "general") -> EnhancementResult:
        """Enhance a track."""
        print(f"🎵 Enhancing track: {user_request}")
        
        result = self.enhancer.enhance_track(user_request, track_id, enhancement_type)
        
        if result.success:
            print(f"✅ Enhancement completed in {result.processing_time:.2f}s")
            print(f"📊 Confidence: {result.confidence:.2f}")
            print(f"🎼 Generated {len(result.patterns)} patterns")
            
            # Display patterns
            for i, pattern in enumerate(result.patterns, 1):
                print(f"  {i}. {pattern.name} (Confidence: {pattern.confidence_score:.2f})")
                print(f"     {pattern.description}")
            
            # Display suggestions
            if result.suggestions:
                print(f"💡 Suggestions:")
                for suggestion in result.suggestions:
                    print(f"  - {suggestion}")
        else:
            print(f"❌ Enhancement failed: {result.error_message}")
        
        return result
    
    def get_suggestions(self, track_id: str = None) -> List[str]:
        """Get enhancement suggestions."""
        suggestions = self.enhancer.get_enhancement_suggestions(track_id)
        
        if suggestions:
            print(f"💡 Enhancement suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("No suggestions available")
        
        return suggestions
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status."""
        project_state = self.enhancer.get_current_project_state()
        project_context = self.enhancer.get_current_project_context()
        
        status = {
            "session_id": self.session_id,
            "project_name": project_state.project_name if project_state else "Unknown",
            "tempo": project_state.tempo if project_state else 0,
            "time_signature": project_state.time_signature if project_state else "Unknown",
            "tracks": len(project_state.tracks) if project_state else 0,
            "regions": len(project_state.regions) if project_state else 0,
            "enhancement_opportunities": len(project_context.enhancement_opportunities) if project_context else 0
        }
        
        return status
    
    def display_status(self):
        """Display current project status."""
        status = self.get_project_status()
        
        print(f"📊 Project Status:")
        print(f"  Session: {status['session_id']}")
        print(f"  Project: {status['project_name']}")
        print(f"  Tempo: {status['tempo']} BPM")
        print(f"  Time Signature: {status['time_signature']}")
        print(f"  Tracks: {status['tracks']}")
        print(f"  Regions: {status['regions']}")
        print(f"  Enhancement Opportunities: {status['enhancement_opportunities']}")
    
    def interactive_mode(self):
        """Start interactive mode."""
        print("🎵 Real-Time Ardour Enhancement - Interactive Mode")
        print("Type 'help' for commands, 'quit' to exit")
        print()
        
        # Start session
        if not self.start_session():
            return
        
        try:
            while True:
                try:
                    command = input("enhance> ").strip()
                    
                    if not command:
                        continue
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    elif command.lower() == 'help':
                        self.show_help()
                    elif command.lower() == 'status':
                        self.display_status()
                    elif command.lower() == 'suggestions':
                        self.get_suggestions()
                    elif command.startswith('enhance '):
                        request = command[8:].strip()
                        if request:
                            self.enhance_track(request)
                        else:
                            print("Please provide an enhancement request")
                    elif command.startswith('enhance track '):
                        parts = command[14:].strip().split(' ', 1)
                        if len(parts) >= 2:
                            track_id, request = parts
                            self.enhance_track(request, track_id)
                        else:
                            print("Usage: enhance track <track_id> <request>")
                    elif command.startswith('enhance bass'):
                        request = command[13:].strip() or "make the bassline groovier"
                        self.enhance_track(request, enhancement_type="bass")
                    elif command.startswith('enhance drums'):
                        request = command[14:].strip() or "add a drum pattern"
                        self.enhance_track(request, enhancement_type="drums")
                    elif command.startswith('enhance melody'):
                        request = command[15:].strip() or "add a melody"
                        self.enhance_track(request, enhancement_type="melody")
                    elif command.startswith('enhance harmony'):
                        request = command[16:].strip() or "add harmony"
                        self.enhance_track(request, enhancement_type="harmony")
                    else:
                        print(f"Unknown command: {command}")
                        print("Type 'help' for available commands")
                
                except KeyboardInterrupt:
                    print("\nUse 'quit' to exit")
                except Exception as e:
                    print(f"Error: {e}")
        
        finally:
            self.stop_session()
    
    def show_help(self):
        """Show help information."""
        print("Available commands:")
        print("  help                    - Show this help")
        print("  status                  - Show project status")
        print("  suggestions             - Show enhancement suggestions")
        print("  enhance <request>       - Enhance any track")
        print("  enhance track <id> <request> - Enhance specific track")
        print("  enhance bass [request]  - Enhance bass line")
        print("  enhance drums [request] - Enhance drum pattern")
        print("  enhance melody [request] - Enhance melody")
        print("  enhance harmony [request] - Enhance harmony")
        print("  quit                    - Exit interactive mode")
        print()
        print("Examples:")
        print("  enhance make the bassline groovier")
        print("  enhance track 1 add more complexity")
        print("  enhance bass add walking bass line")
        print("  enhance drums add ghost notes")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Real-Time Ardour Enhancement CLI")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--session-id", help="Session ID")
    parser.add_argument("--command", help="Command to execute")
    parser.add_argument("--request", help="Enhancement request")
    parser.add_argument("--track-id", help="Track ID")
    parser.add_argument("--enhancement-type", default="general", 
                       choices=["general", "bass", "drums", "melody", "harmony"],
                       help="Enhancement type")
    parser.add_argument("--interactive", action="store_true", 
                       help="Start interactive mode")
    parser.add_argument("--status", action="store_true", 
                       help="Show project status")
    parser.add_argument("--suggestions", action="store_true", 
                       help="Show enhancement suggestions")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize CLI
    cli = RealTimeEnhancementCLI(args.api_key)
    
    try:
        if args.interactive:
            # Interactive mode
            cli.interactive_mode()
        elif args.status:
            # Show status
            if cli.start_session(args.session_id):
                cli.display_status()
                cli.stop_session()
        elif args.suggestions:
            # Show suggestions
            if cli.start_session(args.session_id):
                cli.get_suggestions(args.track_id)
                cli.stop_session()
        elif args.command == "enhance" and args.request:
            # Single enhancement command
            if cli.start_session(args.session_id):
                cli.enhance_track(args.request, args.track_id, args.enhancement_type)
                cli.stop_session()
        else:
            # Default to interactive mode
            cli.interactive_mode()
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
