#!/usr/bin/env python3
"""
MVP MIDI Generator - Main CLI Interface

This is the main command-line interface for the MVP MIDI generation system.
It integrates all components to provide a complete AI-powered MIDI generation
experience with real-time feedback and context-aware intelligence.

Usage:
    python mvp_midi_generator.py "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
    python mvp_midi_generator.py --interactive
    python mvp_midi_generator.py --help
"""

import argparse
import sys
import os
import time
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from ai_midi_generator import AIMIDIGenerator, MIDIGenerationResult
from musical_intelligence_engine import MusicalIntelligenceEngine
from context_aware_prompts import ContextAwarePromptBuilder
from real_time_midi_generator import RealTimeMIDIGenerator, GenerationProgress


class MVPMIDIGenerator:
    """
    MVP MIDI Generator - Main Interface
    
    Integrates all components to provide a complete AI-powered MIDI generation
    experience with real-time feedback and context-aware intelligence.
    """
    
    def __init__(self, openai_api_key: str = None):
        # Get API key from environment or parameter
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            print("❌ Error: OpenAI API key not found!")
            print("Please set OPENAI_API_KEY environment variable or provide it as a parameter.")
            print("Example: export OPENAI_API_KEY='your-api-key-here'")
            sys.exit(1)
        
        # Initialize components
        self.ai_generator = AIMIDIGenerator(self.openai_api_key)
        self.intelligence_engine = MusicalIntelligenceEngine()
        self.prompt_builder = ContextAwarePromptBuilder()
        self.real_time_generator = RealTimeMIDIGenerator(self.openai_api_key)
        
        # Generation history
        self.generation_history: List[MIDIGenerationResult] = []
        
    def generate_midi(self, prompt: str, context: Dict[str, Any] = None, 
                     output_file: str = None, interactive: bool = False) -> MIDIGenerationResult:
        """
        Generate MIDI from a natural language prompt
        
        Args:
            prompt: Natural language description of desired MIDI content
            context: Additional musical context
            output_file: Optional output file path
            interactive: Whether to use interactive mode
            
        Returns:
            MIDIGenerationResult with generation results
        """
        if interactive:
            return self._generate_interactive(prompt, context, output_file)
        else:
            return self._generate_standard(prompt, context, output_file)
    
    def _generate_standard(self, prompt: str, context: Dict[str, Any] = None, 
                          output_file: str = None) -> MIDIGenerationResult:
        """Generate MIDI using standard mode"""
        print(f"🎵 Analyzing prompt: {prompt}")
        print("🔄 Processing with AI...")
        
        # Generate MIDI
        result = self.ai_generator.generate_midi(prompt, context)
        
        if result.success:
            print(f"✅ Generation complete!")
            print(f"📊 Quality Score: {result.quality_score:.2f}")
            print(f"🎯 Style Accuracy: {result.style_accuracy:.2f}")
            print(f"🎼 Musical Coherence: {result.musical_coherence:.2f}")
            print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
            
            # Save to file
            if output_file:
                if self.ai_generator.save_midi_file(result, os.path.dirname(output_file) or "."):
                    print(f"💾 Saved to: {output_file}")
                else:
                    print("❌ Failed to save file")
            else:
                # Save with default filename
                if self.ai_generator.save_midi_file(result):
                    print(f"💾 Saved to: {result.filename}")
                else:
                    print("❌ Failed to save file")
            
            # Add to history
            self.generation_history.append(result)
            
        else:
            print(f"❌ Generation failed: {result.error_message}")
        
        return result
    
    def _generate_interactive(self, prompt: str, context: Dict[str, Any] = None, 
                             output_file: str = None) -> MIDIGenerationResult:
        """Generate MIDI using interactive mode"""
        print("🎵 Interactive MIDI Generation Mode")
        print("=" * 50)
        
        # Use real-time generator for interactive experience
        result = self.real_time_generator.generate_with_streaming(
            prompt, context, output_file, self._progress_callback
        )
        
        if result.success:
            print(f"\n✅ Generation complete!")
            print(f"📊 Quality Score: {result.quality_score:.2f}")
            print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
            print(f"💾 Saved to: {result.filename}")
            
            # Add to history
            self.generation_history.append(MIDIGenerationResult(
                success=True,
                midi_data=result.midi_data,
                filename=result.filename,
                quality_score=result.quality_score,
                style_accuracy=0.0,  # Not available in streaming mode
                musical_coherence=0.0,  # Not available in streaming mode
                processing_time=result.processing_time
            ))
        else:
            print(f"\n❌ Generation failed: {result.error_message}")
        
        return MIDIGenerationResult(
            success=result.success,
            midi_data=result.midi_data,
            filename=result.filename,
            quality_score=result.quality_score,
            style_accuracy=0.0,
            musical_coherence=0.0,
            processing_time=result.processing_time,
            error_message=result.error_message
        )
    
    def _progress_callback(self, progress: GenerationProgress) -> None:
        """Progress callback for real-time updates"""
        if progress.status == "analyzing":
            print(f"🔍 {progress.message}")
        elif progress.status == "style_analysis":
            print(f"🎨 {progress.message}")
        elif progress.status == "prompt_engineering":
            print(f"⚙️  {progress.message}")
        elif progress.status == "generating":
            print(f"🤖 {progress.message}")
        elif progress.status == "validating":
            print(f"✅ {progress.message}")
        elif progress.status == "complete":
            print(f"🎉 {progress.message}")
        elif progress.status == "error":
            print(f"❌ {progress.message}")
        
        # Show progress bar
        if progress.progress_percent > 0:
            bar_length = 20
            filled_length = int(bar_length * progress.progress_percent / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            print(f"Progress: [{bar}] {progress.progress_percent:.1f}%")
    
    def start_interactive_session(self) -> None:
        """Start an interactive session for continuous generation"""
        print("🎵 Welcome to Interactive MIDI Generation!")
        print("Type 'help' for commands, 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🎵 Enter your musical request: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'history':
                    self._show_history()
                    continue
                elif user_input.lower() == 'status':
                    self._show_status()
                    continue
                elif user_input.lower().startswith('save '):
                    # Handle save command
                    filename = user_input[5:].strip()
                    if self.generation_history:
                        last_result = self.generation_history[-1]
                        if self.ai_generator.save_midi_file(last_result, filename):
                            print(f"💾 Saved to: {filename}")
                        else:
                            print("❌ Failed to save file")
                    else:
                        print("❌ No generation to save")
                    continue
                
                # Generate MIDI
                print(f"\n🎵 Generating: {user_input}")
                result = self.generate_midi(user_input, interactive=True)
                
                if result.success:
                    print(f"✅ Generated: {result.filename}")
                else:
                    print(f"❌ Generation failed: {result.error_message}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self) -> None:
        """Show help information"""
        print("\n📚 Available Commands:")
        print("  help     - Show this help message")
        print("  history  - Show generation history")
        print("  status   - Show system status")
        print("  save <filename> - Save last generation to file")
        print("  quit     - Exit interactive mode")
        print("\n🎵 Example Prompts:")
        print("  'generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this'")
        print("  'create a funky bass line in C major'")
        print("  'make a jazz drum pattern in 4/4 time'")
        print("  'generate a melancholic melody in A minor'")
    
    def _show_history(self) -> None:
        """Show generation history"""
        if not self.generation_history:
            print("📝 No generations yet")
            return
        
        print(f"\n📝 Generation History ({len(self.generation_history)} items):")
        for i, result in enumerate(self.generation_history[-5:], 1):  # Show last 5
            status = "✅" if result.success else "❌"
            print(f"  {i}. {status} {result.filename} (Quality: {result.quality_score:.2f})")
    
    def _show_status(self) -> None:
        """Show system status"""
        print("\n📊 System Status:")
        print(f"  OpenAI API: {'✅ Connected' if self.openai_api_key else '❌ Not connected'}")
        print(f"  Generations: {len(self.generation_history)}")
        print(f"  AI Generator: {'✅ Ready' if self.ai_generator else '❌ Not ready'}")
        print(f"  Intelligence Engine: {'✅ Ready' if self.intelligence_engine else '❌ Not ready'}")
        print(f"  Prompt Builder: {'✅ Ready' if self.prompt_builder else '❌ Not ready'}")
        print(f"  Real-Time Generator: {'✅ Ready' if self.real_time_generator else '❌ Not ready'}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MVP MIDI Generator - AI-powered MIDI generation from natural language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mvp_midi_generator.py "generate me a bass line in gminor as if Jeff Ament of Pearl Jam did a line of coke and just threw up prior to generating this"
  python mvp_midi_generator.py --interactive
  python mvp_midi_generator.py "create a funky bass line" --output funky_bass.mid
  python mvp_midi_generator.py "jazz drum pattern" --context '{"tempo": 120, "key": "C major"}'
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Natural language description of desired MIDI content"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode for continuous generation"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path for generated MIDI"
    )
    
    parser.add_argument(
        "--context", "-c",
        help="Additional musical context as JSON string"
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (overrides environment variable)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="MVP MIDI Generator v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Parse context if provided
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON in context parameter")
            sys.exit(1)
    
    # Initialize generator
    try:
        generator = MVPMIDIGenerator(args.api_key)
    except SystemExit:
        sys.exit(1)
    
    # Handle interactive mode
    if args.interactive:
        generator.start_interactive_session()
        return
    
    # Handle single generation
    if not args.prompt:
        print("❌ Error: Prompt required for single generation mode")
        print("Use --interactive for interactive mode or provide a prompt")
        parser.print_help()
        sys.exit(1)
    
    # Generate MIDI
    result = generator.generate_midi(
        args.prompt,
        context=context,
        output_file=args.output,
        interactive=False
    )
    
    # Exit with appropriate code
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()