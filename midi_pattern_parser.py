"""
MIDI Pattern Parser and Generator

Parses LLM responses and generates MIDI patterns for track enhancement.
Handles MIDI file generation and integration with Ardour.
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import mido
from mido import MidiFile, MidiTrack, Message

from llm_track_enhancer import MIDIPattern, EnhancementResult


@dataclass
class MIDIGenerationOptions:
    """Options for MIDI generation."""
    tempo: int = 120
    time_signature: Tuple[int, int] = (4, 4)
    sample_rate: int = 44100
    quantization: float = 0.25  # Quarter note quantization
    velocity_curve: str = "linear"  # "linear", "exponential", "logarithmic"
    humanization: bool = True
    humanization_amount: float = 0.1


class MIDIPatternParser:
    """
    Parses LLM responses and generates MIDI patterns.
    
    Converts LLM-generated patterns into MIDI files and provides
    integration with Ardour for track enhancement.
    """
    
    def __init__(self, generation_options: MIDIGenerationOptions = None):
        """
        Initialize MIDI pattern parser.
        
        Args:
            generation_options: Options for MIDI generation
        """
        self.generation_options = generation_options or MIDIGenerationOptions()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def parse_enhancement_result(self, result: EnhancementResult) -> List[Dict[str, Any]]:
        """
        Parse enhancement result and generate MIDI files.
        
        Args:
            result: Enhancement result from LLM
            
        Returns:
            List of generated MIDI file information
        """
        generated_files = []
        
        for i, pattern in enumerate(result.patterns):
            try:
                # Generate MIDI file
                midi_file_path = self._generate_midi_file(pattern, result, i)
                
                # Generate audio preview (optional)
                audio_preview_path = self._generate_audio_preview(pattern, result, i)
                
                file_info = {
                    "pattern_name": pattern.name,
                    "midi_file": midi_file_path,
                    "audio_preview": audio_preview_path,
                    "description": pattern.description,
                    "confidence": pattern.confidence_score,
                    "enhancement_type": pattern.enhancement_type,
                    "musical_justification": pattern.musical_justification
                }
                
                generated_files.append(file_info)
                
            except Exception as e:
                self.logger.error(f"Error generating MIDI for pattern {pattern.name}: {e}")
        
        return generated_files
    
    def _generate_midi_file(self, pattern: MIDIPattern, result: EnhancementResult, index: int) -> str:
        """Generate MIDI file from pattern."""
        # Create filename
        safe_name = "".join(c for c in pattern.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_name}_{index}_{int(time.time())}.mid"
        file_path = Path("generated_patterns") / filename
        file_path.parent.mkdir(exist_ok=True)
        
        # Create MIDI file
        midi_file = MidiFile()
        track = MidiTrack()
        midi_file.tracks.append(track)
        
        # Set tempo
        tempo = mido.bpm2tempo(pattern.tempo)
        track.append(Message('set_tempo', tempo=tempo))
        
        # Set time signature
        track.append(Message('time_signature', 
                           numerator=pattern.time_signature.split('/')[0],
                           denominator=pattern.time_signature.split('/')[1]))
        
        # Add MIDI data
        self._add_midi_data_to_track(track, pattern.midi_data)
        
        # Save file
        midi_file.save(str(file_path))
        
        self.logger.info(f"Generated MIDI file: {file_path}")
        return str(file_path)
    
    def _add_midi_data_to_track(self, track: MidiTrack, midi_data: List[Dict[str, Any]]):
        """Add MIDI data to track with proper timing."""
        # Sort by start time
        sorted_data = sorted(midi_data, key=lambda x: x.get('start_time_seconds', 0))
        
        # Convert to MIDI ticks
        ticks_per_beat = 480  # Standard MIDI resolution
        ticks_per_second = ticks_per_beat * (self.generation_options.tempo / 60)
        
        # Track active notes for note-off events
        active_notes = {}
        
        for note_data in sorted_data:
            start_time = note_data.get('start_time_seconds', 0)
            duration = note_data.get('duration_seconds', 0.5)
            pitch = note_data.get('pitch', 60)
            velocity = note_data.get('velocity', 80)
            track_index = note_data.get('track_index', 0)
            
            # Convert to ticks
            start_tick = int(start_time * ticks_per_second)
            duration_tick = int(duration * ticks_per_second)
            
            # Add note on
            track.append(Message('note_on', 
                               note=pitch, 
                               velocity=velocity, 
                               time=start_tick,
                               channel=track_index))
            
            # Schedule note off
            end_tick = start_tick + duration_tick
            active_notes[(pitch, track_index)] = end_tick
        
        # Add note off events
        for (pitch, channel), end_tick in active_notes.items():
            track.append(Message('note_off', 
                               note=pitch, 
                               velocity=0, 
                               time=end_tick,
                               channel=channel))
    
    def _generate_audio_preview(self, pattern: MIDIPattern, result: EnhancementResult, index: int) -> Optional[str]:
        """Generate audio preview of pattern (placeholder)."""
        # This would integrate with audio synthesis
        # For now, return None
        return None
    
    def create_ardour_import_script(self, generated_files: List[Dict[str, Any]], 
                                  project_path: str) -> str:
        """Create Lua script for importing patterns into Ardour."""
        script_content = f"""
-- Ardour import script for generated patterns
-- Generated at {time.strftime('%Y-%m-%d %H:%M:%S')}

local session = Session:get()
if not session then
    print("No active session")
    return false
end

-- Import patterns
local patterns = {json.dumps(generated_files, indent=2)}

for i, pattern in ipairs(patterns) do
    print("Importing pattern: " .. pattern.pattern_name)
    
    -- Create new MIDI track
    local track = session:new_midi_track(1, 1, pattern.pattern_name, 1)
    if track then
        -- Import MIDI file
        local midi_file = pattern.midi_file
        if midi_file and string.len(midi_file) > 0 then
            -- Import logic would go here
            print("  MIDI file: " .. midi_file)
            print("  Description: " .. pattern.description)
            print("  Confidence: " .. pattern.confidence)
        end
    end
end

print("Import completed")
return true
"""
        
        # Save script
        script_path = Path("ardour_scripts") / f"import_patterns_{int(time.time())}.lua"
        script_path.parent.mkdir(exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def create_enhancement_summary(self, result: EnhancementResult, 
                                 generated_files: List[Dict[str, Any]]) -> str:
        """Create summary of enhancement results."""
        summary_parts = []
        
        summary_parts.append(f"# Track Enhancement Summary")
        summary_parts.append(f"")
        summary_parts.append(f"**Enhancement Type:** {result.enhancement_type}")
        summary_parts.append(f"**Track ID:** {result.track_id}")
        summary_parts.append(f"**User Request:** {result.user_request}")
        summary_parts.append(f"**Confidence:** {result.confidence:.2f}")
        summary_parts.append(f"**Processing Time:** {result.processing_time:.2f}s")
        summary_parts.append(f"")
        
        summary_parts.append(f"## Generated Patterns")
        summary_parts.append(f"")
        
        for i, file_info in enumerate(generated_files, 1):
            summary_parts.append(f"### Pattern {i}: {file_info['pattern_name']}")
            summary_parts.append(f"")
            summary_parts.append(f"- **Description:** {file_info['description']}")
            summary_parts.append(f"- **Confidence:** {file_info['confidence']:.2f}")
            summary_parts.append(f"- **MIDI File:** {file_info['midi_file']}")
            summary_parts.append(f"- **Musical Justification:** {file_info['musical_justification']}")
            summary_parts.append(f"")
        
        summary_parts.append(f"## Musical Analysis")
        summary_parts.append(f"")
        summary_parts.append(result.musical_analysis)
        summary_parts.append(f"")
        
        summary_parts.append(f"## Suggestions")
        summary_parts.append(f"")
        for suggestion in result.suggestions:
            summary_parts.append(f"- {suggestion}")
        
        return "\n".join(summary_parts)
    
    def export_patterns_to_json(self, result: EnhancementResult, 
                              generated_files: List[Dict[str, Any]], 
                              output_path: str) -> bool:
        """Export patterns and metadata to JSON."""
        try:
            export_data = {
                "enhancement_result": {
                    "success": result.success,
                    "enhancement_type": result.enhancement_type,
                    "track_id": result.track_id,
                    "user_request": result.user_request,
                    "confidence": result.confidence,
                    "processing_time": result.processing_time,
                    "error_message": result.error_message
                },
                "patterns": [
                    {
                        "name": pattern.name,
                        "description": pattern.description,
                        "midi_data": pattern.midi_data,
                        "confidence_score": pattern.confidence_score,
                        "enhancement_type": pattern.enhancement_type,
                        "musical_justification": pattern.musical_justification,
                        "track_id": pattern.track_id,
                        "duration": pattern.duration,
                        "tempo": pattern.tempo,
                        "time_signature": pattern.time_signature
                    }
                    for pattern in result.patterns
                ],
                "generated_files": generated_files,
                "musical_analysis": result.musical_analysis,
                "suggestions": result.suggestions,
                "timestamp": time.time()
            }
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting patterns to JSON: {e}")
            return False
    
    def validate_midi_pattern(self, pattern: MIDIPattern) -> Tuple[bool, List[str]]:
        """Validate MIDI pattern for correctness."""
        errors = []
        
        # Check required fields
        if not pattern.name:
            errors.append("Pattern name is required")
        
        if not pattern.midi_data:
            errors.append("MIDI data is required")
        
        # Validate MIDI data
        for i, note in enumerate(pattern.midi_data):
            if not isinstance(note, dict):
                errors.append(f"Note {i} must be a dictionary")
                continue
            
            # Check required fields
            required_fields = ['pitch', 'velocity', 'start_time_seconds', 'duration_seconds']
            for field in required_fields:
                if field not in note:
                    errors.append(f"Note {i} missing required field: {field}")
            
            # Validate pitch range
            if 'pitch' in note:
                pitch = note['pitch']
                if not isinstance(pitch, int) or pitch < 0 or pitch > 127:
                    errors.append(f"Note {i} has invalid pitch: {pitch}")
            
            # Validate velocity range
            if 'velocity' in note:
                velocity = note['velocity']
                if not isinstance(velocity, int) or velocity < 0 or velocity > 127:
                    errors.append(f"Note {i} has invalid velocity: {velocity}")
            
            # Validate timing
            if 'start_time_seconds' in note:
                start_time = note['start_time_seconds']
                if not isinstance(start_time, (int, float)) or start_time < 0:
                    errors.append(f"Note {i} has invalid start time: {start_time}")
            
            if 'duration_seconds' in note:
                duration = note['duration_seconds']
                if not isinstance(duration, (int, float)) or duration <= 0:
                    errors.append(f"Note {i} has invalid duration: {duration}")
        
        # Validate confidence score
        if not isinstance(pattern.confidence_score, (int, float)) or pattern.confidence_score < 0 or pattern.confidence_score > 1:
            errors.append(f"Invalid confidence score: {pattern.confidence_score}")
        
        # Validate tempo
        if not isinstance(pattern.tempo, (int, float)) or pattern.tempo <= 0:
            errors.append(f"Invalid tempo: {pattern.tempo}")
        
        return len(errors) == 0, errors
    
    def optimize_pattern_for_ardour(self, pattern: MIDIPattern) -> MIDIPattern:
        """Optimize pattern for Ardour import."""
        # Create optimized copy
        optimized_data = []
        
        for note in pattern.midi_data:
            # Quantize timing
            start_time = note.get('start_time_seconds', 0)
            duration = note.get('duration_seconds', 0.5)
            
            # Quantize to quarter notes
            quantized_start = round(start_time / self.generation_options.quantization) * self.generation_options.quantization
            quantized_duration = round(duration / self.generation_options.quantization) * self.generation_options.quantization
            
            # Apply humanization if enabled
            if self.generation_options.humanization:
                humanization_amount = self.generation_options.humanization_amount
                start_offset = (hash(str(note)) % 100) / 100.0 * humanization_amount - humanization_amount / 2
                quantized_start += start_offset
            
            optimized_note = note.copy()
            optimized_note['start_time_seconds'] = max(0, quantized_start)
            optimized_note['duration_seconds'] = max(0.1, quantized_duration)
            
            optimized_data.append(optimized_note)
        
        # Create optimized pattern
        optimized_pattern = MIDIPattern(
            name=pattern.name + " (Optimized)",
            description=pattern.description + " - Optimized for Ardour",
            midi_data=optimized_data,
            confidence_score=pattern.confidence_score,
            enhancement_type=pattern.enhancement_type,
            musical_justification=pattern.musical_justification,
            track_id=pattern.track_id,
            duration=pattern.duration,
            tempo=pattern.tempo,
            time_signature=pattern.time_signature
        )
        
        return optimized_pattern
