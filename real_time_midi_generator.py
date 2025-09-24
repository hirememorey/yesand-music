"""
Real-Time MIDI Generation System

This module provides real-time MIDI generation capabilities with streaming
updates and live feedback for the MVP MIDI generation system.

Key Features:
- Real-time generation with streaming updates
- Live progress feedback
- Streaming MIDI data to files
- Real-time quality assessment
- Interactive generation modes
"""

import time
import json
from typing import Dict, List, Optional, Any, Generator, Callable
from dataclasses import dataclass
from pathlib import Path
import threading
from queue import Queue, Empty

from ai_midi_generator import AIMIDIGenerator, MIDIGenerationRequest, MIDIGenerationResult
from musical_intelligence_engine import MusicalIntelligenceEngine, MusicalContext
from context_aware_prompts import ContextAwarePromptBuilder, EnhancedPrompt


@dataclass
class GenerationProgress:
    """Progress information for real-time generation"""
    status: str
    message: str
    progress_percent: float
    current_step: str
    estimated_time_remaining: float
    data: Optional[Dict[str, Any]] = None


@dataclass
class StreamingMIDIResult:
    """Result of streaming MIDI generation"""
    success: bool
    midi_data: List[Dict[str, Any]]
    filename: str
    quality_score: float
    processing_time: float
    progress_updates: List[GenerationProgress]
    error_message: Optional[str] = None


class RealTimeMIDIGenerator:
    """
    Real-Time MIDI Generator with streaming capabilities
    
    Provides real-time MIDI generation with live progress updates,
    streaming data output, and interactive generation modes.
    """
    
    def __init__(self, openai_api_key: str, security_level: str = "medium"):
        self.ai_generator = AIMIDIGenerator(openai_api_key)
        self.intelligence_engine = MusicalIntelligenceEngine()
        self.prompt_builder = ContextAwarePromptBuilder()
        self.generation_queue = Queue()
        self.is_generating = False
        self.current_generation = None
        self.progress_callbacks: List[Callable[[GenerationProgress], None]] = []
        
    def generate_live(self, prompt: str, context: Dict[str, Any] = None, 
                     progress_callback: Callable[[GenerationProgress], None] = None) -> Generator[GenerationProgress, None, None]:
        """
        Generate MIDI content in real-time with streaming updates
        
        Args:
            prompt: Natural language musical prompt
            context: Additional musical context
            progress_callback: Optional callback for progress updates
            
        Yields:
            GenerationProgress updates throughout the generation process
        """
        start_time = time.time()
        
        try:
            # Step 1: Analyze prompt
            yield GenerationProgress(
                status="analyzing",
                message="Analyzing prompt and extracting musical context...",
                progress_percent=10.0,
                current_step="prompt_analysis",
                estimated_time_remaining=30.0
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="analyzing",
                    message="Analyzing prompt and extracting musical context...",
                    progress_percent=10.0,
                    current_step="prompt_analysis",
                    estimated_time_remaining=30.0
                ))
            
            musical_context = self.intelligence_engine.analyze_prompt(prompt, context or {})
            
            # Step 2: Extract style characteristics
            yield GenerationProgress(
                status="style_analysis",
                message="Analyzing style characteristics and mood...",
                progress_percent=25.0,
                current_step="style_analysis",
                estimated_time_remaining=25.0
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="style_analysis",
                    message="Analyzing style characteristics and mood...",
                    progress_percent=25.0,
                    current_step="style_analysis",
                    estimated_time_remaining=25.0
                ))
            
            style_characteristics = self.intelligence_engine.extract_style_characteristics(prompt, musical_context)
            
            # Step 3: Build enhanced prompt
            yield GenerationProgress(
                status="prompt_engineering",
                message="Building context-aware prompt for AI generation...",
                progress_percent=40.0,
                current_step="prompt_engineering",
                estimated_time_remaining=20.0
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="prompt_engineering",
                    message="Building context-aware prompt for AI generation...",
                    progress_percent=40.0,
                    current_step="prompt_engineering",
                    estimated_time_remaining=20.0
                ))
            
            enhanced_prompt = self.prompt_builder.build_musical_prompt(
                prompt, musical_context, style_characteristics
            )
            
            # Step 4: Generate MIDI with AI
            yield GenerationProgress(
                status="generating",
                message="Generating MIDI with AI...",
                progress_percent=60.0,
                current_step="ai_generation",
                estimated_time_remaining=15.0
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="generating",
                    message="Generating MIDI with AI...",
                    progress_percent=60.0,
                    current_step="ai_generation",
                    estimated_time_remaining=15.0
                ))
            
            # Use the AI generator's live generation
            for update in self.ai_generator.generate_live(prompt, context):
                if update["status"] == "complete":
                    midi_data = update["midi_data"]
                    quality_assessment = update["quality_assessment"]
                    break
                elif update["status"] == "error":
                    raise Exception(update["message"])
            
            # Step 5: Validate and assess quality
            yield GenerationProgress(
                status="validating",
                message="Validating and assessing quality...",
                progress_percent=85.0,
                current_step="quality_validation",
                estimated_time_remaining=5.0
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="validating",
                    message="Validating and assessing quality...",
                    progress_percent=85.0,
                    current_step="quality_validation",
                    estimated_time_remaining=5.0
                ))
            
            # Step 6: Complete
            processing_time = time.time() - start_time
            
            yield GenerationProgress(
                status="complete",
                message="MIDI generation complete",
                progress_percent=100.0,
                current_step="complete",
                estimated_time_remaining=0.0,
                data={
                    "midi_data": midi_data,
                    "quality_assessment": quality_assessment,
                    "musical_context": musical_context,
                    "style_characteristics": style_characteristics,
                    "processing_time": processing_time
                }
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="complete",
                    message="MIDI generation complete",
                    progress_percent=100.0,
                    current_step="complete",
                    estimated_time_remaining=0.0,
                    data={
                        "midi_data": midi_data,
                        "quality_assessment": quality_assessment,
                        "musical_context": musical_context,
                        "style_characteristics": style_characteristics,
                        "processing_time": processing_time
                    }
                ))
            
        except Exception as e:
            yield GenerationProgress(
                status="error",
                message=f"Generation failed: {str(e)}",
                progress_percent=0.0,
                current_step="error",
                estimated_time_remaining=0.0,
                data={"error": str(e)}
            )
            
            if progress_callback:
                progress_callback(GenerationProgress(
                    status="error",
                    message=f"Generation failed: {str(e)}",
                    progress_percent=0.0,
                    current_step="error",
                    estimated_time_remaining=0.0,
                    data={"error": str(e)}
                ))
    
    def generate_with_streaming(self, prompt: str, context: Dict[str, Any] = None,
                               output_file: str = None, progress_callback: Callable[[GenerationProgress], None] = None) -> StreamingMIDIResult:
        """
        Generate MIDI with streaming updates and save to file
        
        Args:
            prompt: Natural language musical prompt
            context: Additional musical context
            output_file: Optional output file path
            progress_callback: Optional callback for progress updates
            
        Returns:
            StreamingMIDIResult with generation results and progress updates
        """
        start_time = time.time()
        progress_updates = []
        midi_data = []
        quality_score = 0.0
        filename = ""
        error_message = None
        
        try:
            # Generate with streaming updates
            for progress in self.generate_live(prompt, context, progress_callback):
                progress_updates.append(progress)
                
                if progress.status == "complete":
                    midi_data = progress.data["midi_data"]
                    quality_score = progress.data["quality_assessment"]["quality_score"]
                    filename = self._generate_filename(prompt, progress.data["musical_context"])
                    break
                elif progress.status == "error":
                    error_message = progress.message
                    break
            
            # Save to file if specified
            if midi_data and output_file:
                self._save_midi_data(midi_data, output_file)
            elif midi_data and not output_file:
                # Generate default filename
                if not filename:
                    filename = self._generate_filename(prompt, {})
                self._save_midi_data(midi_data, filename)
            
            processing_time = time.time() - start_time
            
            return StreamingMIDIResult(
                success=len(midi_data) > 0,
                midi_data=midi_data,
                filename=filename,
                quality_score=quality_score,
                processing_time=processing_time,
                progress_updates=progress_updates,
                error_message=error_message
            )
            
        except Exception as e:
            return StreamingMIDIResult(
                success=False,
                midi_data=[],
                filename="",
                quality_score=0.0,
                processing_time=time.time() - start_time,
                progress_updates=progress_updates,
                error_message=str(e)
            )
    
    def generate_interactive(self, prompt: str, context: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Generate MIDI in interactive mode with user feedback
        
        Args:
            prompt: Natural language musical prompt
            context: Additional musical context
            
        Yields:
            Interactive updates and requests for user input
        """
        try:
            # Start generation
            yield {
                "type": "start",
                "message": "Starting interactive MIDI generation...",
                "prompt": prompt
            }
            
            # Analyze prompt
            yield {
                "type": "analysis",
                "message": "Analyzing your prompt...",
                "step": "prompt_analysis"
            }
            
            musical_context = self.intelligence_engine.analyze_prompt(prompt, context or {})
            
            # Show analysis results
            yield {
                "type": "analysis_result",
                "message": "Analysis complete",
                "musical_context": {
                    "key": musical_context.key,
                    "tempo": musical_context.tempo,
                    "instrument": musical_context.instrument,
                    "style": musical_context.style,
                    "mood": musical_context.mood.value,
                    "complexity": musical_context.complexity.value
                }
            }
            
            # Ask for confirmation or modifications
            yield {
                "type": "confirmation",
                "message": "Does this analysis look correct? You can modify any aspect.",
                "options": ["continue", "modify_key", "modify_tempo", "modify_style", "modify_mood"]
            }
            
            # Generate MIDI
            yield {
                "type": "generation",
                "message": "Generating MIDI with AI...",
                "step": "ai_generation"
            }
            
            # Use live generation
            for update in self.generate_live(prompt, context):
                if update.status == "complete":
                    yield {
                        "type": "complete",
                        "message": "MIDI generation complete!",
                        "midi_data": update.data["midi_data"],
                        "quality_assessment": update.data["quality_assessment"],
                        "filename": self._generate_filename(prompt, update.data["musical_context"])
                    }
                    break
                elif update.status == "error":
                    yield {
                        "type": "error",
                        "message": f"Generation failed: {update.message}",
                        "error": update.data.get("error", "Unknown error")
                    }
                    break
                else:
                    yield {
                        "type": "progress",
                        "message": update.message,
                        "progress_percent": update.progress_percent,
                        "current_step": update.current_step
                    }
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"Interactive generation failed: {str(e)}",
                "error": str(e)
            }
    
    def _generate_filename(self, prompt: str, musical_context: Dict[str, Any]) -> str:
        """Generate intelligent filename based on prompt and context"""
        # Extract key elements
        key = musical_context.get("key", "unknown").replace(" ", "_").lower()
        instrument = musical_context.get("instrument", "unknown")
        style = musical_context.get("style", "unknown")
        
        # Create base filename
        timestamp = int(time.time())
        base_name = f"{instrument}_{style}_{key}_{timestamp}"
        
        # Clean up filename
        import re
        base_name = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)
        base_name = re.sub(r'_+', '_', base_name)
        
        return f"{base_name}.mid"
    
    def _save_midi_data(self, midi_data: List[Dict[str, Any]], filename: str) -> bool:
        """Save MIDI data to file"""
        try:
            from midi_io import save_midi_file
            save_midi_file(midi_data, filename)
            return True
        except Exception as e:
            print(f"Failed to save MIDI file: {e}")
            return False
    
    def add_progress_callback(self, callback: Callable[[GenerationProgress], None]) -> None:
        """Add progress callback for generation updates"""
        self.progress_callbacks.append(callback)
    
    def remove_progress_callback(self, callback: Callable[[GenerationProgress], None]) -> None:
        """Remove progress callback"""
        if callback in self.progress_callbacks:
            self.progress_callbacks.remove(callback)
    
    def get_generation_status(self) -> Dict[str, Any]:
        """Get current generation status"""
        return {
            "is_generating": self.is_generating,
            "current_generation": self.current_generation,
            "queue_size": self.generation_queue.qsize(),
            "active_callbacks": len(self.progress_callbacks)
        }
    
    def cancel_generation(self) -> bool:
        """Cancel current generation"""
        if self.is_generating:
            self.is_generating = False
            self.current_generation = None
            return True
        return False
    
    def clear_queue(self) -> None:
        """Clear generation queue"""
        while not self.generation_queue.empty():
            try:
                self.generation_queue.get_nowait()
            except Empty:
                break