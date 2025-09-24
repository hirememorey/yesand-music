#!/usr/bin/env python3
"""
Secure Enhancement CLI - Main Interface

This module provides a command-line interface for the security-first
real-time Ardour enhancement system.
"""

import argparse
import sys
import time
import json
from typing import Dict, Any, Optional

from secure_enhancement_system import (
    FailFastEnhancer, EnhancementMode, EnhancementRequest, EnhancementResult
)
from security_first_architecture import SecurityLevel

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🔒 SECURE ENHANCEMENT SYSTEM - Security-First Architecture")
    print("=" * 60)
    print("Real-Time Ardour Enhancement with Built-in Security")
    print("=" * 60)

def print_status(enhancer: FailFastEnhancer):
    """Print system status"""
    status = enhancer.get_system_status()
    
    print("\n📊 SYSTEM STATUS")
    print("-" * 30)
    print(f"Mode: {status['mode']}")
    print(f"Healthy: {'✅' if status['healthy'] else '❌'}")
    
    # OSC Status
    osc_status = status.get('osc_status', {})
    if osc_status:
        print(f"\n🎵 OSC Status:")
        for name, client_status in osc_status.items():
            healthy = "✅" if client_status['healthy'] else "❌"
            print(f"  {name}: {healthy}")
    
    # File Status
    file_status = status.get('file_status', {})
    if file_status:
        print(f"\n📁 File Status:")
        for name, client_status in file_status.items():
            healthy = "✅" if client_status['healthy'] else "❌"
            print(f"  {name}: {healthy}")
    
    # LLM Status
    llm_status = status.get('llm_status', {})
    if llm_status:
        print(f"\n🤖 LLM Status:")
        for name, client_status in llm_status.items():
            healthy = "✅" if client_status['healthy'] else "❌"
            print(f"  {name}: {healthy}")

def print_enhancement_result(result: EnhancementResult):
    """Print enhancement result"""
    print(f"\n🎵 ENHANCEMENT RESULT")
    print("-" * 30)
    print(f"Success: {'✅' if result.success else '❌'}")
    print(f"Message: {result.message}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print(f"Security Level: {result.security_level.value}")
    
    if result.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.metadata:
        print(f"\n📋 Metadata:")
        for key, value in result.metadata.items():
            print(f"  {key}: {value}")

def interactive_mode(enhancer: FailFastEnhancer):
    """Interactive mode for real-time enhancement"""
    print("\n🎮 INTERACTIVE MODE")
    print("Type 'help' for commands, 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            command = input("\n🔒 secure-enhance> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if command.lower() == 'help':
                print_help()
                continue
            
            if command.lower() == 'status':
                print_status(enhancer)
                continue
            
            if command.lower().startswith('enhance '):
                user_request = command[8:].strip()
                if not user_request:
                    print("❌ Please provide an enhancement request")
                    continue
                
                # Parse enhancement type
                enhancement_type = "general"
                if "bass" in user_request.lower():
                    enhancement_type = "bass"
                elif "drum" in user_request.lower():
                    enhancement_type = "drums"
                elif "melody" in user_request.lower():
                    enhancement_type = "melody"
                elif "harmony" in user_request.lower():
                    enhancement_type = "harmony"
                
                # Create enhancement request
                request = EnhancementRequest(
                    user_request=user_request,
                    enhancement_type=enhancement_type,
                    security_level=SecurityLevel.MEDIUM,
                    user_id="interactive_user",
                    session_id="interactive_session"
                )
                
                # Process enhancement
                print(f"\n🔄 Processing: {user_request}")
                result = enhancer.enhance(request)
                print_enhancement_result(result)
                continue
            
            print(f"❌ Unknown command: {command}")
            print("Type 'help' for available commands")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def print_help():
    """Print help information"""
    print("\n📖 AVAILABLE COMMANDS")
    print("-" * 30)
    print("enhance <request>  - Enhance music with AI")
    print("  Examples:")
    print("    enhance create a funky bassline")
    print("    enhance add drums to this track")
    print("    enhance make the melody more jazz-like")
    print("    enhance improve the harmony")
    print()
    print("status            - Show system status")
    print("help              - Show this help")
    print("quit/exit/q       - Exit the program")

def single_command_mode(enhancer: FailFastEnhancer, args):
    """Single command mode"""
    request = EnhancementRequest(
        user_request=args.request,
        enhancement_type=args.type or "general",
        track_id=args.track_id,
        security_level=SecurityLevel[args.security_level.upper()],
        user_id=args.user_id,
        session_id=args.session_id
    )
    
    print(f"\n🔄 Processing: {args.request}")
    result = enhancer.enhance(request)
    print_enhancement_result(result)
    
    # Return appropriate exit code
    return 0 if result.success else 1

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Security-First Real-Time Ardour Enhancement System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python secure_enhancement_cli.py --interactive
  
  # Single command
  python secure_enhancement_cli.py --request "create a funky bassline"
  
  # With specific parameters
  python secure_enhancement_cli.py --request "add drums" --type drums --track-id "2"
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=False)
    mode_group.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start in interactive mode'
    )
    mode_group.add_argument(
        '--request', '-r',
        type=str,
        help='Enhancement request (single command mode)'
    )
    
    # Enhancement parameters
    parser.add_argument(
        '--type', '-t',
        type=str,
        choices=['bass', 'drums', 'melody', 'harmony', 'general'],
        default='general',
        help='Enhancement type'
    )
    parser.add_argument(
        '--track-id',
        type=str,
        help='Target track ID'
    )
    parser.add_argument(
        '--security-level',
        type=str,
        choices=['low', 'medium', 'high', 'critical'],
        default='medium',
        help='Security level'
    )
    parser.add_argument(
        '--user-id',
        type=str,
        default='cli_user',
        help='User ID'
    )
    parser.add_argument(
        '--session-id',
        type=str,
        default='cli_session',
        help='Session ID'
    )
    
    # System options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Initialize enhancement system
    try:
        enhancer = FailFastEnhancer()
        print("✅ Enhancement system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize enhancement system: {str(e)}")
        return 1
    
    # Handle status command
    if args.status:
        print_status(enhancer)
        enhancer.shutdown()
        return 0
    
    try:
        # Handle different modes
        if args.status:
            print_status(enhancer)
            return 0
        elif args.interactive:
            interactive_mode(enhancer)
        elif args.request:
            return single_command_mode(enhancer, args)
        else:
            print("❌ No mode specified. Use --interactive, --request, or --status")
            return 1
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    finally:
        # Cleanup
        try:
            enhancer.shutdown()
        except:
            pass

if __name__ == "__main__":
    sys.exit(main())
