#!/usr/bin/env python3
"""
Command-line interface for the control plane.

This module provides a CLI that can be called from chat or used interactively
for testing the control plane functionality.
"""

from __future__ import annotations

import sys
from typing import Optional

from commands.control_plane import ControlPlane


def main() -> None:
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print("Usage: python control_plane_cli.py <command>")
        print("       python control_plane_cli.py --interactive")
        print("       python control_plane_cli.py --help")
        sys.exit(1)
    
    if sys.argv[1] == "--help":
        print_help()
        sys.exit(0)
    
    if sys.argv[1] == "--interactive":
        run_interactive()
    else:
        # Execute single command
        command = " ".join(sys.argv[1:])
        execute_command(command)


def print_help() -> None:
    """Print help information."""
    print("Control Plane CLI")
    print("================")
    print()
    print("Usage:")
    print("  python control_plane_cli.py <command>     - Execute a single command")
    print("  python control_plane_cli.py --interactive - Start interactive mode")
    print("  python control_plane_cli.py --help        - Show this help")
    print()
    print("Examples:")
    print("  python control_plane_cli.py 'play scale C major'")
    print("  python control_plane_cli.py 'set tempo to 140'")
    print("  python control_plane_cli.py 'play random 8'")
    print("  python control_plane_cli.py 'status'")
    print()


def execute_command(command: str) -> None:
    """Execute a single command and print the result.
    
    Args:
        command: The command to execute
    """
    try:
        with ControlPlane() as control_plane:
            result = control_plane.execute(command)
            print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def run_interactive() -> None:
    """Run the interactive mode."""
    print("Control Plane Interactive Mode")
    print("=============================")
    print("Type commands or 'help' for available commands. Type 'quit' to exit.")
    print()
    
    try:
        with ControlPlane() as control_plane:
            while True:
                try:
                    command = input("> ").strip()
                    if not command:
                        continue
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    result = control_plane.execute(command)
                    print(result)
                    print()
                
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except EOFError:
                    print("\nExiting...")
                    break
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
