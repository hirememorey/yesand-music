#!/usr/bin/env python3
"""
MVP Musical Quality First Generator

This implementation follows the post-mortem insights:
1. Trust the AI's musical judgment
2. Focus on musical quality over technical precision
3. Use duration as enhancement, not constraint
4. Let AI generate what it thinks is musically complete

Key Changes from Original MVP:
- Removed complex parsing that was choking on creative language
- Let AI generate naturally complete pieces
- Duration is a soft guideline, not hard requirement
- Focus on musical quality as primary metric
- User feedback focuses on musical satisfaction, not duration
"""

import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import uuid

import mido
from openai import OpenAI

# Import context support
from musical_notation_converter import convert_midi_to_json, extract_project_context_from_midi_file


class MusicalQualityFirstGate:
    """Musical quality assessment focused on musical satisfaction, not technical precision."""
    
    def __init__(self):
        self.quality_criteria = {
            'musical_completeness': 0.4,  # Does it sound complete and satisfying?
            'musical_interest': 0.3,      # Is it engaging and interesting?
            'style_authenticity': 0.2,    # Does it match the requested style?
            'technical_quality': 0.1      # Is it technically well-formed?
        }
        
        # User feedback learning system
        self.user_feedback_db = {}
        self.quality_models = {}
        
    def assess_quality(self, midi_data: Dict, user_context: Dict, generation_id: str) -> Tuple[float, Dict]:
        """
        Assess musical quality focusing on musical satisfaction.
        
        Returns:
            Tuple of (quality_score, detailed_feedback)
        """
        feedback = {
            'musical_completeness': self._assess_musical_completeness(midi_data),
            'musical_interest': self._assess_musical_interest(midi_data),
            'style_authenticity': self._assess_style_authenticity(midi_data, user_context),
            'technical_quality': self._assess_technical_quality(midi_data)
        }
        
        # Calculate weighted quality score
        quality_score = sum(
            feedback[criterion] * weight 
            for criterion, weight in self.quality_criteria.items()
        )
        
        return quality_score, feedback
    
    def _assess_musical_completeness(self, midi_data: Dict) -> float:
        """Assess if the music sounds complete and satisfying."""
        notes = midi_data.get('notes', [])
        if not notes:
            return 0.0
            
        # Check for musical completeness indicators
        score = 0.5  # Base score
        
        # Check for reasonable musical development
        note_count = len(notes)
        duration = midi_data.get('duration', 1.0)
        
        # Musical completeness is about feeling complete, not specific length
        if note_count >= 4:  # At least some musical content
            score += 0.2
            
        # Check for musical variety (not just repetition)
        unique_pitches = len(set(note.get('pitch', 60) for note in notes))
        if unique_pitches >= 3:  # Some harmonic variety
            score += 0.2
            
        # Check for rhythmic variety
        unique_velocities = len(set(note.get('velocity', 64) for note in notes))
        if unique_velocities >= 2:  # Some dynamic variety
            score += 0.1
            
        return min(score, 1.0)
    
    def _assess_musical_interest(self, midi_data: Dict) -> float:
        """Assess if the music is engaging and interesting."""
        notes = midi_data.get('notes', [])
        if not notes:
            return 0.0
            
        score = 0.5  # Base score
        
        # Check for rhythmic interest
        start_times = [note.get('start_time', 0) for note in notes]
        if len(set(start_times)) > len(notes) * 0.5:  # Not all on the same beat
            score += 0.2
            
        # Check for pitch range (musical interest)
        pitches = [note.get('pitch', 60) for note in notes]
        if pitches:
            pitch_range = max(pitches) - min(pitches)
            if pitch_range >= 12:  # At least an octave
                score += 0.2
                
        # Check for velocity variety (dynamic interest)
        velocities = [note.get('velocity', 64) for note in notes]
        if velocities:
            velocity_range = max(velocities) - min(velocities)
            if velocity_range >= 30:  # Good dynamic range
                score += 0.1
                
        return min(score, 1.0)
    
    def _assess_style_authenticity(self, midi_data: Dict, user_context: Dict) -> float:
        """Assess if the music matches the requested style."""
        requested_style = user_context.get('style', '').lower()
        if not requested_style:
            return 0.7  # Neutral score if no style specified
            
        # For now, return a base score - this would be enhanced with ML
        # The key insight is that we trust the AI to understand style
        return 0.7
    
    def _assess_technical_quality(self, midi_data: Dict) -> float:
        """Assess basic technical quality."""
        notes = midi_data.get('notes', [])
        if not notes:
            return 0.0
            
        score = 0.5  # Base score
        
        # Check for valid MIDI note numbers
        valid_notes = all(0 <= note.get('pitch', 0) <= 127 for note in notes)
        if valid_notes:
            score += 0.3
            
        # Check for valid velocities
        valid_velocities = all(0 <= note.get('velocity', 0) <= 127 for note in notes)
        if valid_velocities:
            score += 0.2
            
        return min(score, 1.0)
    
    def record_user_feedback(self, generation_id: str, user_rating: float, 
                           user_comments: str, user_id: str = 'anonymous'):
        """Record user feedback focused on musical satisfaction."""
        if user_id not in self.user_feedback_db:
            self.user_feedback_db[user_id] = []
            
        feedback_entry = {
            'generation_id': generation_id,
            'rating': user_rating,
            'comments': user_comments,
            'timestamp': datetime.now().isoformat(),
            'focus': 'musical_satisfaction'  # Focus on musical quality, not duration
        }
        
        self.user_feedback_db[user_id].append(feedback_entry)
        
        # Update quality models based on feedback
        self._update_quality_models(user_id, feedback_entry)
    
    def _update_quality_models(self, user_id: str, feedback_entry: Dict):
        """Update quality models based on user feedback."""
        # This would implement machine learning to improve quality assessment
        # For now, just store the feedback
        pass


class SimplePromptProcessor:
    """Simple prompt processor that trusts the AI to understand natural language."""
    
    def __init__(self):
        # Minimal extraction - only what's absolutely necessary
        self.basic_patterns = {
            'key': r'\b([a-g][#b]?\s+(?:major|minor|maj|min))\b',
            'tempo': r'\b(\d+)\s*bpm\b',
            'instrument': r'\b(bass|drums|melody|piano|guitar)\b'
        }
    
    def extract_basic_context(self, prompt: str) -> Dict[str, Any]:
        """Extract only the most basic context, let AI handle the rest."""
        context = {
            'original_prompt': prompt,
            'key': 'C major',  # Default
            'tempo': 120,      # Default
            'instrument': 'bass'  # Default
        }
        
        prompt_lower = prompt.lower()
        
        # Extract key (only if clearly specified)
        key_match = re.search(self.basic_patterns['key'], prompt_lower)
        if key_match:
            context['key'] = key_match.group(1)
        
        # Extract tempo (only if clearly specified)
        tempo_match = re.search(self.basic_patterns['tempo'], prompt_lower)
        if tempo_match:
            context['tempo'] = int(tempo_match.group(1))
        
        # Extract instrument (only if clearly specified)
        for instrument in ['bass', 'drums', 'melody', 'piano', 'guitar']:
            if instrument in prompt_lower:
                context['instrument'] = instrument
                break
        
        return context


class MusicalQualityFirstGenerator:
    """MIDI generator that prioritizes musical quality over technical precision."""
    
    def __init__(self, api_key: str, temperature: float = 0.9, quality_threshold: float = 0.4):
        self.client = OpenAI(api_key=api_key)
        self.quality_gate = MusicalQualityFirstGate()
        self.prompt_processor = SimplePromptProcessor()
        self.temperature = temperature
        self.quality_threshold = quality_threshold
        
    def generate_midi(self, prompt: str, user_id: str = 'anonymous', context_json: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate MIDI focusing on musical quality, not technical precision."""
        generation_id = str(uuid.uuid4())
        
        # Extract minimal context - let AI handle the complexity
        context = self.prompt_processor.extract_basic_context(prompt)
        context['user_id'] = user_id
        context['generation_id'] = generation_id
        
        # Add project context if provided (optional enhancement)
        if context_json:
            context['project_context'] = context_json
        
        # Generate with focus on musical quality
        for attempt in range(2):  # Reduced attempts - trust the AI
            try:
                midi_data = self._generate_with_ai(prompt, context)
                quality_score, feedback = self.quality_gate.assess_quality(midi_data, context, generation_id)
                
                # Use user-defined threshold - focus on musical satisfaction
                if quality_score >= self.quality_threshold:
                    return {
                        'success': True,
                        'midi_data': midi_data,
                        'quality_score': quality_score,
                        'feedback': feedback,
                        'generation_id': generation_id,
                        'context': context,
                        'attempt': attempt + 1,
                        'musical_approach': 'quality_first'
                    }
                else:
                    # Simple refinement - just ask for better quality
                    prompt = f"{prompt}\n\nPlease make this more musically interesting and complete."
                    
            except Exception as e:
                print(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt == 1:  # Last attempt
                    return {
                        'success': False,
                        'error': str(e),
                        'generation_id': generation_id,
                        'context': context
                    }
        
        # If all attempts fail, return best attempt
        return {
            'success': True,
            'midi_data': midi_data,
            'quality_score': quality_score,
            'feedback': feedback,
            'generation_id': generation_id,
            'context': context,
            'warning': 'Quality below ideal threshold',
            'attempt': 2,
            'musical_approach': 'quality_first'
        }
    
    def _generate_with_ai(self, prompt: str, context: Dict) -> Dict:
        """Generate MIDI using AI with minimal interference."""
        
        # Build simple, direct prompt - trust the AI
        enhanced_prompt = f"""You are a professional musician. Generate a {context['instrument']} part based on this request:

"{prompt}"

Musical Context:
- Key: {context['key']}
- Tempo: {context['tempo']} BPM
- Instrument: {context['instrument']}"""
        
        # Add project context if available (optional enhancement)
        if 'project_context' in context:
            project_context = context['project_context']
            enhanced_prompt += f"""

Project Context (for reference only - use as inspiration, not constraint):
- Project Key: {project_context.get('key', 'Unknown')}
- Project Tempo: {project_context.get('tempo', 'Unknown')} BPM
- Existing Tracks: {len(project_context.get('tracks', []))} tracks
- Use this context to create something that fits well with the existing music, but don't let it constrain your creativity."""

        enhanced_prompt += f"""

CRITICAL REQUIREMENTS FOR MUSICAL QUALITY:
1. RHYTHMIC COMPLEXITY: Use varied note lengths - eighth notes, sixteenth notes, syncopation, rests
2. MELODIC INTEREST: Create melodic phrases with direction, tension, and resolution
3. DYNAMIC VARIATION: Use different velocities (60-127) to create musical expression
4. PROFESSIONAL LEVEL: This must sound like something a professional musician would play
5. MUSICAL DEPTH: Include passing tones, chord tones, and musical development
6. DURATION: Create at least 8-16 measures of substantial musical content
7. STYLE AUTHENTICITY: Match the requested style with appropriate musical vocabulary

AVOID:
- Only quarter notes or simple patterns
- Repetitive, boring sequences
- Amateur-level simplicity
- Lack of musical development

Return ONLY a JSON object with this exact structure:
{{
    "notes": [
        {{
            "pitch": 36,
            "velocity": 80,
            "start_time": 0.0,
            "duration": 0.5,
            "track_index": 0
        }}
    ],
    "tempo": {context['tempo']},
    "key": "{context['key']}",
    "time_signature": "4/4",
    "duration": 8.0,
    "musical_description": "Brief description of the musical character"
}}

Generate the {context['instrument']} part now:"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class professional musician and composer with decades of experience. Generate sophisticated, musically complex MIDI data that demonstrates professional-level musicality. Your output must include rhythmic complexity, melodic development, dynamic variation, and musical depth. Avoid simple, amateur-level patterns. Create music that would impress other professional musicians. Always respond with valid JSON format."
                },
                {
                    "role": "user",
                    "content": enhanced_prompt
                }
            ],
            max_tokens=3000,  # Increased for longer pieces
            temperature=self.temperature   # User-controlled creativity
        )
        
        # Parse response
        content = response.choices[0].message.content.strip()
        
        # Debug: Print the response to see what we're getting
        print(f"🔍 AI Response (first 500 chars): {content[:500]}...")
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            print(f"🔍 Extracted JSON (first 200 chars): {json_str[:200]}...")
        else:
            json_str = content
            print(f"🔍 Using full content as JSON: {json_str[:200]}...")
            
        try:
            midi_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"📝 Full response content: {content}")
            raise
        
        # Ensure required fields with sensible defaults
        if 'notes' not in midi_data:
            midi_data['notes'] = []
        if 'tempo' not in midi_data:
            midi_data['tempo'] = context.get('tempo', 120)
        if 'key' not in midi_data:
            midi_data['key'] = context.get('key', 'C major')
        if 'duration' not in midi_data:
            # Let AI determine duration - don't force it
            midi_data['duration'] = 8.0
            
        return midi_data
    
    def record_user_feedback(self, generation_id: str, rating: float, comments: str, user_id: str = 'anonymous'):
        """Record user feedback focused on musical satisfaction."""
        self.quality_gate.record_user_feedback(generation_id, rating, comments, user_id)
    
    def display_generation_feedback(self, result: Dict[str, Any]) -> None:
        """Display detailed feedback about the generation."""
        if not result['success']:
            print(f"❌ Generation failed: {result['error']}")
            return
        
        print(f"\n📊 Generation Results:")
        print(f"  Quality Score: {result['quality_score']:.2f}/1.0")
        print(f"  Attempt: {result['attempt']}/2")
        print(f"  Musical Approach: {result['musical_approach']}")
        
        if 'feedback' in result:
            feedback = result['feedback']
            print(f"\n🎵 Musical Analysis:")
            print(f"  Musical Completeness: {feedback.get('musical_completeness', 0):.2f}/1.0")
            print(f"  Musical Interest: {feedback.get('musical_interest', 0):.2f}/1.0")
            print(f"  Style Authenticity: {feedback.get('style_authenticity', 0):.2f}/1.0")
            print(f"  Technical Quality: {feedback.get('technical_quality', 0):.2f}/1.0")
            
            if 'musical_description' in result['midi_data']:
                print(f"\n🎼 Musical Description: {result['midi_data']['musical_description']}")
        
        if 'warning' in result:
            print(f"\n⚠️  Warning: {result['warning']}")
        
        print(f"\n💡 Tips:")
        if result['quality_score'] < 0.7:
            print(f"  - Try adjusting temperature (--temperature) for different creativity levels")
            print(f"  - Try lowering quality threshold (--quality-threshold) for more experimental results")
        print(f"  - Use --regenerate to try again with different parameters")
        print(f"  - Use --show-feedback to see detailed analysis")


class MVPMusicalQualityFirstGenerator:
    """Main MVP system focused on musical quality first."""
    
    def __init__(self, api_key: str, temperature: float = 0.9, quality_threshold: float = 0.4):
        self.generator = MusicalQualityFirstGenerator(api_key, temperature, quality_threshold)
        self.output_dir = Path("generated_midi")
        self.output_dir.mkdir(exist_ok=True)
        self.temperature = temperature
        self.quality_threshold = quality_threshold
        
    def generate_and_save(self, prompt: str, user_id: str = 'anonymous', context_json: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate MIDI and save to file with focus on musical quality."""
        print(f"🎵 Generating musically complete {self._extract_instrument(prompt)} part...")
        print(f"📝 Prompt: '{prompt}'")
        print("=" * 60)
        
        # Generate MIDI
        result = self.generator.generate_midi(prompt, user_id, context_json)
        
        if not result['success']:
            print(f"❌ Generation failed: {result['error']}")
            return result
        
        # Show generation parameters
        print(f"🎛️  Generation Settings:")
        print(f"  Temperature: {self.temperature} (creativity level)")
        print(f"  Quality Threshold: {self.quality_threshold} (acceptance level)")
        print("=" * 60)
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = re.sub(r'[^\w\s-]', '', prompt)[:40]
        filename = f"{safe_prompt}_{timestamp}.mid"
        filepath = self.output_dir / filename
        
        # Convert to MIDI file
        try:
            self._save_midi_file(result['midi_data'], filepath)
            result['filepath'] = str(filepath)
            result['filename'] = filename
            
            # Display results
            print(f"✅ Musical generation successful!")
            print(f"📁 Saved to: {filepath}")
            print(f"🎯 Musical Quality Score: {result['quality_score']:.2f}/1.0")
            print(f"🎵 Approach: {result.get('musical_approach', 'quality_first')}")
            print(f"🔄 Attempts: {result['attempt']}")
            
            if 'warning' in result:
                print(f"⚠️  Note: {result['warning']}")
            
            # Show quality feedback focused on musical aspects
            print("\n📊 Musical Quality Assessment:")
            for criterion, score in result['feedback'].items():
                criterion_name = criterion.replace('_', ' ').title()
                print(f"  {criterion_name}: {score:.2f}")
            
            # Show musical description if available
            if 'musical_description' in result['midi_data']:
                print(f"\n🎼 Musical Character: {result['midi_data']['musical_description']}")
            
            # Prompt for user feedback focused on musical satisfaction
            self._prompt_user_feedback(result['generation_id'], user_id)
            
        except Exception as e:
            print(f"❌ Failed to save MIDI file: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
    def regenerate_with_different_params(self, prompt: str, user_id: str = 'anonymous', 
                                       temperature: float = None, quality_threshold: float = None) -> Dict[str, Any]:
        """Regenerate with different parameters."""
        if temperature is not None:
            self.temperature = temperature
            self.generator.temperature = temperature
        if quality_threshold is not None:
            self.quality_threshold = quality_threshold
            self.generator.quality_threshold = quality_threshold
        
        print(f"🔄 Regenerating with different parameters...")
        print(f"  New Temperature: {self.temperature}")
        print(f"  New Quality Threshold: {self.quality_threshold}")
        print("=" * 60)
        
        return self.generate_and_save(prompt, user_id)
    
    def extract_context_from_midi_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Extract project context from a MIDI file."""
        return extract_project_context_from_midi_file(filepath)
    
    def generate_with_context(self, prompt: str, context_file: str, user_id: str = 'anonymous') -> Dict[str, Any]:
        """Generate with context from a MIDI file."""
        context = self.extract_context_from_midi_file(context_file)
        if context:
            print(f"📁 Using context from: {context_file}")
            print(f"  Project Key: {context.get('key', 'Unknown')}")
            print(f"  Project Tempo: {context.get('tempo', 'Unknown')} BPM")
            print(f"  Existing Tracks: {len(context.get('tracks', []))}")
        else:
            print(f"⚠️  Could not extract context from {context_file}, generating without context")
        
        return self.generate_and_save(prompt, user_id, context)
    
    def _extract_instrument(self, prompt: str) -> str:
        """Extract instrument from prompt for display."""
        prompt_lower = prompt.lower()
        for instrument in ['bass', 'drums', 'melody', 'piano', 'guitar']:
            if instrument in prompt_lower:
                return instrument
        return 'musical'
    
    def _save_midi_file(self, midi_data: Dict, filepath: Path):
        """Save MIDI data to file."""
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo
        tempo = mido.bpm2tempo(midi_data.get('tempo', 120))
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))
        
        # Set time signature
        track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
        
        # Add notes
        for note in midi_data.get('notes', []):
            # Note on
            track.append(mido.Message('note_on', 
                                    channel=note.get('track_index', 0),
                                    note=note.get('pitch', 60),
                                    velocity=note.get('velocity', 80),
                                    time=int(note.get('start_time', 0) * 480)))
            
            # Note off
            track.append(mido.Message('note_off',
                                    channel=note.get('track_index', 0),
                                    note=note.get('pitch', 60),
                                    velocity=0,
                                    time=int(note.get('duration', 0.5) * 480)))
        
        mid.save(str(filepath))
    
    def _prompt_user_feedback(self, generation_id: str, user_id: str):
        """Prompt user for feedback focused on musical satisfaction."""
        # Only prompt for feedback in interactive mode
        if hasattr(self, '_interactive_mode') and self._interactive_mode:
            print("\n" + "=" * 60)
            print("📝 Musical Quality Feedback (Optional)")
            print("=" * 60)
            print("Rate this based on musical satisfaction, not technical precision:")
            print("1 = Not musically satisfying")
            print("5 = Very musically satisfying")
            
            try:
                rating = input("\nRate musical satisfaction (1-5, or press Enter to skip): ").strip()
                if rating:
                    rating = float(rating)
                    if 1 <= rating <= 5:
                        comments = input("What did you like or dislike about the musical character? (optional): ").strip()
                        self.generator.record_user_feedback(generation_id, rating, comments, user_id)
                        print("✅ Thank you for your musical feedback!")
                    else:
                        print("⚠️  Rating must be between 1 and 5")
                else:
                    print("⏭️  Skipping feedback")
            except (ValueError, KeyboardInterrupt):
                print("⏭️  Skipping feedback")
        else:
            print("\n💡 Use --interactive mode to provide feedback on musical quality")
    
    def interactive_mode(self, user_id: str = 'anonymous'):
        """Interactive mode focused on musical quality."""
        self._interactive_mode = True  # Set flag for feedback prompting
        print("🎵 MVP Musical Quality First Generator - Interactive Mode")
        print("=" * 70)
        print("Generate musically complete and satisfying MIDI parts!")
        print("Focus on musical quality over technical precision.")
        print("Type 'quit' to exit, 'help' for commands")
        print("=" * 70)
        
        while True:
            try:
                prompt = input("\n🎵 Enter your musical request: ").strip()
                
                if not prompt:
                    continue
                    
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                if prompt.lower() == 'help':
                    self._show_help()
                    continue
                
                if prompt.lower() == 'status':
                    self._show_status()
                    continue
                
                # Generate MIDI
                result = self.generate_and_save(prompt, user_id)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show help information."""
        print("\n📖 Help - Musical Quality First Approach:")
        print("  help     - Show this help message")
        print("  status   - Show system status")
        print("  quit     - Exit the program")
        print("\n🎛️  User Controls:")
        print("  --temperature X.X     - Set creativity level (0.1-1.0, default: 0.8)")
        print("  --quality-threshold X.X - Set quality threshold (0.1-1.0, default: 0.5)")
        print("  --show-feedback       - Show detailed generation analysis")
        print("  --regenerate          - Try again with different parameters")
        print("\n📁 Context Support (Optional):")
        print("  --context-file FILE   - Use MIDI file as context for generation")
        print("  --extract-context FILE - Extract context from MIDI file to JSON")
        print("\n💡 Example Prompts (be creative!):")
        print("  'I want 16 measures of an anthemic bass line as if Flea and Jeff Ament had a baby'")
        print("  'Create a funky bass line that makes me want to dance'")
        print("  'Generate a melancholic melody that tells a story'")
        print("  'Make a drum pattern that sounds like thunder'")
        print("\n🎯 Focus on musical quality, not technical precision!")
        print("\n🔧 Tips for Better Results:")
        print("  - Higher temperature (0.8-1.0) = more creative/experimental")
        print("  - Lower temperature (0.1-0.5) = more consistent/predictable")
        print("  - Higher quality threshold (0.7-0.9) = more selective")
        print("  - Lower quality threshold (0.3-0.5) = more experimental")
    
    def _show_status(self):
        """Show system status."""
        print("\n📊 System Status:")
        print(f"  Output Directory: {self.output_dir}")
        print(f"  Generated Files: {len(list(self.output_dir.glob('*.mid')))}")
        print(f"  Musical Quality Gate: Active")
        print(f"  User Feedback: Musical Satisfaction Focus")
        print(f"  Approach: Quality First, Duration Second")
        print(f"\n🎛️  Current Settings:")
        print(f"  Temperature: {self.temperature} (creativity level)")
        print(f"  Quality Threshold: {self.quality_threshold} (acceptance level)")
        print(f"\n💡 Use 'help' to see available commands and tips")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="MVP Musical Quality First Generator")
    parser.add_argument("prompt", nargs="?", help="Musical prompt to generate MIDI from")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--output", "-o", help="Output filename (optional)")
    parser.add_argument("--user-id", "-u", default="anonymous", help="User ID for feedback tracking")
    parser.add_argument("--temperature", "-t", type=float, default=0.9, 
                       help="Creativity level (0.1-1.0, default: 0.9)")
    parser.add_argument("--quality-threshold", "-q", type=float, default=0.4,
                       help="Quality threshold (0.1-1.0, default: 0.4)")
    parser.add_argument("--show-feedback", "-f", action="store_true",
                       help="Show detailed generation analysis")
    parser.add_argument("--regenerate", "-r", action="store_true",
                       help="Regenerate with different parameters")
    parser.add_argument("--context-file", "-c", help="MIDI file to use as context")
    parser.add_argument("--extract-context", "-e", help="Extract context from MIDI file and save to JSON")
    
    args = parser.parse_args()
    
    # Handle context extraction (doesn't need API key)
    if args.extract_context:
        from musical_notation_converter import extract_project_context_from_midi_file, save_context_to_file
        context = extract_project_context_from_midi_file(args.extract_context)
        if context:
            context_file = f"context_{Path(args.extract_context).stem}.json"
            if save_context_to_file(context, context_file):
                print(f"✅ Context extracted and saved to: {context_file}")
                print(f"  Project Key: {context.get('key', 'Unknown')}")
                print(f"  Project Tempo: {context.get('tempo', 'Unknown')} BPM")
                print(f"  Existing Tracks: {len(context.get('tracks', []))}")
            else:
                print(f"❌ Failed to save context to: {context_file}")
        else:
            print(f"❌ Failed to extract context from: {args.extract_context}")
        return 0
    
    # Check for API key (only needed for generation)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return 1
    
    # Initialize generator with user parameters
    generator = MVPMusicalQualityFirstGenerator(api_key, args.temperature, args.quality_threshold)
    
    if args.interactive:
        generator.interactive_mode(args.user_id)
    elif args.prompt:
        # Generate with or without context
        if args.context_file:
            result = generator.generate_with_context(args.prompt, args.context_file, args.user_id)
        else:
            result = generator.generate_and_save(args.prompt, args.user_id)
        
        # Show detailed feedback if requested
        if args.show_feedback:
            generator.generator.display_generation_feedback(result)
        
        # Handle regeneration
        if args.regenerate:
            print("\n🔄 Regenerating with different parameters...")
            # Try different temperature and quality threshold
            new_temp = 1.0 - args.temperature  # Flip temperature
            new_quality = max(0.3, args.quality_threshold - 0.2)  # Lower quality threshold
            result = generator.regenerate_with_different_params(
                args.prompt, args.user_id, new_temp, new_quality
            )
            if args.show_feedback:
                generator.generator.display_generation_feedback(result)
        
        if not result['success']:
            return 1
    else:
        print("❌ Error: Please provide a prompt or use --interactive mode")
        print("Use --help for more information")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
