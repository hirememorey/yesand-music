#!/usr/bin/env python3
"""
MVP User-Driven MIDI Generator with Musical Quality Gates

This is the core MVP system that allows users to type in any prompt
and get back a high-quality MIDI file, with built-in user evaluation
and feedback loops for continuous improvement.
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

class MusicalQualityGate:
    """Musical quality assessment engine with user feedback integration."""
    
    def __init__(self):
        self.quality_criteria = {
            'musical_coherence': 0.3,  # Does it make musical sense?
            'style_accuracy': 0.25,    # Does it match the requested style?
            'technical_quality': 0.2,  # Is it technically well-formed?
            'user_preference': 0.25    # Does it match user's taste?
        }
        
        # User feedback learning system
        self.user_feedback_db = {}
        self.quality_models = {}
        
    def assess_quality(self, midi_data: Dict, user_context: Dict, generation_id: str) -> Tuple[float, Dict]:
        """
        Assess musical quality of generated MIDI.
        
        Returns:
            Tuple of (quality_score, detailed_feedback)
        """
        feedback = {
            'musical_coherence': self._assess_musical_coherence(midi_data),
            'style_accuracy': self._assess_style_accuracy(midi_data, user_context),
            'technical_quality': self._assess_technical_quality(midi_data),
            'user_preference': self._assess_user_preference(midi_data, user_context, generation_id)
        }
        
        # Calculate weighted quality score
        quality_score = sum(
            feedback[criterion] * weight 
            for criterion, weight in self.quality_criteria.items()
        )
        
        return quality_score, feedback
    
    def _assess_musical_coherence(self, midi_data: Dict) -> float:
        """Assess if the music makes musical sense."""
        notes = midi_data.get('notes', [])
        if not notes:
            return 0.0
            
        # Check for basic musical coherence
        score = 0.5  # Base score
        
        # Check for reasonable note density
        note_density = len(notes) / max(midi_data.get('duration', 1), 1)
        if 0.5 <= note_density <= 4.0:  # Reasonable notes per second
            score += 0.2
            
        # Check for reasonable pitch range
        pitches = [note.get('pitch', 60) for note in notes]
        if pitches:
            pitch_range = max(pitches) - min(pitches)
            if 12 <= pitch_range <= 48:  # 1-4 octaves
                score += 0.2
                
        # Check for reasonable velocity range
        velocities = [note.get('velocity', 64) for note in notes]
        if velocities:
            velocity_range = max(velocities) - min(velocities)
            if velocity_range >= 20:  # Some dynamic variation
                score += 0.1
                
        return min(score, 1.0)
    
    def _assess_style_accuracy(self, midi_data: Dict, user_context: Dict) -> float:
        """Assess if the music matches the requested style."""
        requested_style = user_context.get('style', '').lower()
        if not requested_style:
            return 0.7  # Neutral score if no style specified
            
        # Basic style matching (can be expanded)
        style_indicators = {
            'jazz': ['swing', 'syncopation', 'complex harmony'],
            'rock': ['driving rhythm', 'power chords', 'aggressive'],
            'funk': ['syncopated', 'groove', 'bass heavy'],
            'classical': ['structured', 'melodic', 'harmonic'],
            'blues': ['pentatonic', 'bent notes', 'call and response']
        }
        
        # For now, return a base score - this would be enhanced with ML
        return 0.6
    
    def _assess_technical_quality(self, midi_data: Dict) -> float:
        """Assess technical quality of the MIDI."""
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
    
    def _assess_user_preference(self, midi_data: Dict, user_context: Dict, generation_id: str) -> float:
        """Assess based on user's historical preferences."""
        user_id = user_context.get('user_id', 'anonymous')
        
        # If we have feedback for this user, use it
        if user_id in self.user_feedback_db:
            user_preferences = self.user_feedback_db[user_id]
            # Simple preference matching (would be enhanced with ML)
            return 0.7
        else:
            # Default score for new users
            return 0.6
    
    def record_user_feedback(self, generation_id: str, user_rating: float, 
                           user_comments: str, user_id: str = 'anonymous'):
        """Record user feedback for learning and improvement."""
        if user_id not in self.user_feedback_db:
            self.user_feedback_db[user_id] = []
            
        feedback_entry = {
            'generation_id': generation_id,
            'rating': user_rating,
            'comments': user_comments,
            'timestamp': datetime.now().isoformat()
        }
        
        self.user_feedback_db[user_id].append(feedback_entry)
        
        # Update quality models based on feedback
        self._update_quality_models(user_id, feedback_entry)
    
    def _update_quality_models(self, user_id: str, feedback_entry: Dict):
        """Update quality models based on user feedback."""
        # This would implement machine learning to improve quality assessment
        # For now, just store the feedback
        pass


class MusicalContextExtractor:
    """Extract musical context from user prompts."""
    
    def __init__(self):
        self.key_patterns = [
            (r'\b([a-g][#b]?)\s+(major|minor|maj|min)\b', lambda m: f"{m.group(1).upper()} {m.group(2)}"),
            (r'\b([a-g][#b]?)\s+major\b', lambda m: f"{m.group(1).upper()} major"),
            (r'\b([a-g][#b]?)\s+minor\b', lambda m: f"{m.group(1).upper()} minor"),
            (r'\b([a-g][#b]?)\s+min\b', lambda m: f"{m.group(1).upper()} minor")
        ]
        
        self.tempo_patterns = {
            r'\b(\d+)\s*bpm\b': 'tempo',
            r'\b(\d+)\s*beats?\s+per\s+minute\b': 'tempo',
            r'\b(slow|fast|medium)\b': 'tempo_qualitative'
        }
        
        self.style_patterns = {
            r'\b(jazz|jazz\s+style)\b': 'jazz',
            r'\b(rock|rock\s+style)\b': 'rock',
            r'\b(funk|funky)\b': 'funk',
            r'\b(blues|bluesy)\b': 'blues',
            r'\b(classical|classic)\b': 'classical',
            r'\b(electronic|electronic\s+music)\b': 'electronic'
        }
        
        self.instrument_patterns = {
            r'\b(bass|bassline|bass\s+line)\b': 'bass',
            r'\b(drums|drum\s+pattern|beat)\b': 'drums',
            r'\b(piano|piano\s+part)\b': 'piano',
            r'\b(guitar|guitar\s+part)\b': 'guitar',
            r'\b(melody|melodic)\b': 'melody'
        }
        
        self.length_patterns = {
            r'\b(\d+)\s*(measures?|bars?)\b': 'measures',
            r'\b(\d+)\s*beats?\b': 'beats',
            r'\b(\d+)\s*seconds?\b': 'seconds'
        }
    
    def extract_context(self, prompt: str) -> Dict[str, Any]:
        """Extract musical context from user prompt."""
        context = {
            'original_prompt': prompt,
            'key': None,
            'tempo': None,
            'style': None,
            'instrument': None,
            'length': None,
            'mood': None,
            'complexity': None
        }
        
        prompt_lower = prompt.lower()
        
        # Extract key
        for pattern, formatter in self.key_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                context['key'] = formatter(match)
                break
        
        # Extract tempo
        for pattern, context_key in self.tempo_patterns.items():
            match = re.search(pattern, prompt_lower)
            if match:
                if context_key == 'tempo':
                    context['tempo'] = int(match.group(1))
                else:
                    tempo_map = {'slow': 80, 'medium': 120, 'fast': 160}
                    context['tempo'] = tempo_map.get(match.group(1), 120)
                break
        
        # Extract style
        for pattern, style in self.style_patterns.items():
            if re.search(pattern, prompt_lower):
                context['style'] = style
                break
        
        # Extract instrument
        for pattern, instrument in self.instrument_patterns.items():
            if re.search(pattern, prompt_lower):
                context['instrument'] = instrument
                break
        
        # Extract length
        for pattern, unit in self.length_patterns.items():
            match = re.search(pattern, prompt_lower)
            if match:
                context['length'] = {
                    'value': int(match.group(1)),
                    'unit': unit
                }
                break
        
        # Extract mood (simple keyword matching)
        mood_keywords = {
            'dark': ['dark', 'moody', 'brooding', 'ominous'],
            'bright': ['bright', 'happy', 'cheerful', 'upbeat'],
            'melancholic': ['melancholic', 'sad', 'sorrowful', 'mournful'],
            'energetic': ['energetic', 'exciting', 'intense', 'powerful']
        }
        
        for mood, keywords in mood_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                context['mood'] = mood
                break
        
        # Extract complexity
        complexity_keywords = {
            'simple': ['simple', 'basic', 'easy'],
            'complex': ['complex', 'intricate', 'sophisticated', 'advanced']
        }
        
        for complexity, keywords in complexity_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                context['complexity'] = complexity
                break
        
        return context


class MIDIGenerator:
    """Generate MIDI using OpenAI with quality validation."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.quality_gate = MusicalQualityGate()
        self.context_extractor = MusicalContextExtractor()
        
    def generate_midi(self, prompt: str, user_id: str = 'anonymous') -> Dict[str, Any]:
        """Generate MIDI with quality validation and user feedback integration."""
        generation_id = str(uuid.uuid4())
        
        # Extract musical context
        context = self.context_extractor.extract_context(prompt)
        context['user_id'] = user_id
        context['generation_id'] = generation_id
        
        # Generate with quality validation
        for attempt in range(3):  # Max 3 attempts
            try:
                midi_data = self._generate_with_openai(prompt, context)
                quality_score, feedback = self.quality_gate.assess_quality(midi_data, context, generation_id)
                
                if quality_score >= 0.7:  # High quality threshold
                    return {
                        'success': True,
                        'midi_data': midi_data,
                        'quality_score': quality_score,
                        'feedback': feedback,
                        'generation_id': generation_id,
                        'context': context,
                        'attempt': attempt + 1
                    }
                else:
                    # Refine prompt based on quality feedback
                    prompt = self._refine_prompt(prompt, feedback, attempt)
                    
            except Exception as e:
                print(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # Last attempt
                    return {
                        'success': False,
                        'error': str(e),
                        'generation_id': generation_id,
                        'context': context
                    }
        
        # If all attempts fail, return best attempt with warning
        return {
            'success': True,
            'midi_data': midi_data,
            'quality_score': quality_score,
            'feedback': feedback,
            'generation_id': generation_id,
            'context': context,
            'warning': 'Quality below threshold after 3 attempts',
            'attempt': 3
        }
    
    def _generate_with_openai(self, prompt: str, context: Dict) -> Dict:
        """Generate MIDI using OpenAI API."""
        # Build enhanced prompt with context
        enhanced_prompt = self._build_enhanced_prompt(prompt, context)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional music producer and composer. Generate high-quality MIDI data based on user requests. Always respond with valid JSON format."
                },
                {
                    "role": "user",
                    "content": enhanced_prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # Parse response
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = content
            
        midi_data = json.loads(json_str)
        
        # Ensure required fields
        if 'notes' not in midi_data:
            midi_data['notes'] = []
        if 'tempo' not in midi_data:
            midi_data['tempo'] = context.get('tempo', 120)
        if 'key' not in midi_data:
            midi_data['key'] = context.get('key', 'C major')
        if 'duration' not in midi_data:
            midi_data['duration'] = 8.0  # Default 8 seconds
            
        return midi_data
    
    def _build_enhanced_prompt(self, prompt: str, context: Dict) -> str:
        """Build enhanced prompt with musical context."""
        enhanced_prompt = f"""
Generate a MIDI pattern based on this request: "{prompt}"

Musical Context:
- Key: {context.get('key', 'C major')}
- Tempo: {context.get('tempo', 120)} BPM
- Style: {context.get('style', 'general')}
- Instrument: {context.get('instrument', 'piano')}
- Length: {context.get('length', {}).get('value', 4)} {context.get('length', {}).get('unit', 'measures')}
- Mood: {context.get('mood', 'neutral')}
- Complexity: {context.get('complexity', 'medium')}

Requirements:
- Generate professional-quality music that matches the context
- Use proper musical theory and harmony
- Create engaging and musical patterns
- Ensure technical correctness

Respond with JSON in this exact format:
{{
    "notes": [
        {{
            "pitch": 60,
            "velocity": 80,
            "start_time": 0.0,
            "duration": 0.5,
            "channel": 0
        }}
    ],
    "tempo": 120,
    "key": "C major",
    "time_signature": "4/4",
    "duration": 8.0
}}
"""
        return enhanced_prompt
    
    def _refine_prompt(self, original_prompt: str, feedback: Dict, attempt: int) -> str:
        """Refine prompt based on quality feedback."""
        refinements = []
        
        if feedback.get('musical_coherence', 0) < 0.6:
            refinements.append("Focus on creating musically coherent patterns with proper harmony and rhythm.")
            
        if feedback.get('style_accuracy', 0) < 0.6:
            refinements.append("Pay closer attention to the requested musical style and genre conventions.")
            
        if feedback.get('technical_quality', 0) < 0.6:
            refinements.append("Ensure all MIDI parameters are within valid ranges and technically correct.")
        
        if refinements:
            refined_prompt = f"{original_prompt}\n\nRefinement (attempt {attempt + 1}): {'. '.join(refinements)}"
        else:
            refined_prompt = f"{original_prompt}\n\nRefinement (attempt {attempt + 1}): Generate a more sophisticated and engaging musical pattern."
            
        return refined_prompt
    
    def record_user_feedback(self, generation_id: str, rating: float, comments: str, user_id: str = 'anonymous'):
        """Record user feedback for learning and improvement."""
        self.quality_gate.record_user_feedback(generation_id, rating, comments, user_id)


class MVPUserDrivenGenerator:
    """Main MVP system for user-driven MIDI generation."""
    
    def __init__(self, api_key: str):
        self.generator = MIDIGenerator(api_key)
        self.output_dir = Path("generated_midi")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_and_save(self, prompt: str, user_id: str = 'anonymous') -> Dict[str, Any]:
        """Generate MIDI and save to file with user feedback integration."""
        print(f"🎵 Generating MIDI for: '{prompt}'")
        print("=" * 50)
        
        # Generate MIDI
        result = self.generator.generate_midi(prompt, user_id)
        
        if not result['success']:
            print(f"❌ Generation failed: {result['error']}")
            return result
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = re.sub(r'[^\w\s-]', '', prompt)[:30]
        filename = f"{safe_prompt}_{timestamp}.mid"
        filepath = self.output_dir / filename
        
        # Convert to MIDI file
        try:
            self._save_midi_file(result['midi_data'], filepath)
            result['filepath'] = str(filepath)
            result['filename'] = filename
            
            # Display results
            print(f"✅ Generation successful!")
            print(f"📁 Saved to: {filepath}")
            print(f"🎯 Quality Score: {result['quality_score']:.2f}/1.0")
            print(f"🔄 Attempts: {result['attempt']}")
            
            if 'warning' in result:
                print(f"⚠️  Warning: {result['warning']}")
            
            # Show quality feedback
            print("\n📊 Quality Feedback:")
            for criterion, score in result['feedback'].items():
                print(f"  {criterion.replace('_', ' ').title()}: {score:.2f}")
            
            # Prompt for user feedback
            self._prompt_user_feedback(result['generation_id'], user_id)
            
        except Exception as e:
            print(f"❌ Failed to save MIDI file: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
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
                                    channel=note.get('channel', 0),
                                    note=note.get('pitch', 60),
                                    velocity=note.get('velocity', 80),
                                    time=int(note.get('start_time', 0) * 480)))
            
            # Note off
            track.append(mido.Message('note_off',
                                    channel=note.get('channel', 0),
                                    note=note.get('pitch', 60),
                                    velocity=0,
                                    time=int(note.get('duration', 0.5) * 480)))
        
        mid.save(str(filepath))
    
    def _prompt_user_feedback(self, generation_id: str, user_id: str):
        """Prompt user for feedback on generated music."""
        print("\n" + "=" * 50)
        print("📝 User Feedback (Optional)")
        print("=" * 50)
        
        try:
            rating = input("Rate this generation (1-5, or press Enter to skip): ").strip()
            if rating:
                rating = float(rating)
                if 1 <= rating <= 5:
                    comments = input("Any comments or suggestions (optional): ").strip()
                    self.generator.record_user_feedback(generation_id, rating, comments, user_id)
                    print("✅ Thank you for your feedback!")
                else:
                    print("⚠️  Rating must be between 1 and 5")
            else:
                print("⏭️  Skipping feedback")
        except (ValueError, KeyboardInterrupt):
            print("⏭️  Skipping feedback")
    
    def interactive_mode(self, user_id: str = 'anonymous'):
        """Interactive mode for continuous generation."""
        print("🎵 MVP User-Driven MIDI Generator - Interactive Mode")
        print("=" * 60)
        print("Type your musical prompts and get high-quality MIDI files!")
        print("Type 'quit' to exit, 'help' for commands")
        print("=" * 60)
        
        while True:
            try:
                prompt = input("\n🎵 Enter your musical prompt: ").strip()
                
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
        print("\n📖 Help - Available Commands:")
        print("  help     - Show this help message")
        print("  status   - Show system status")
        print("  quit     - Exit the program")
        print("\n💡 Example Prompts:")
        print("  'Create a funky bass line in C major'")
        print("  'Generate a jazz piano melody in G minor'")
        print("  'Make a rock drum pattern at 140 BPM'")
        print("  'Create a melancholic melody for 8 measures'")
    
    def _show_status(self):
        """Show system status."""
        print("\n📊 System Status:")
        print(f"  Output Directory: {self.output_dir}")
        print(f"  Generated Files: {len(list(self.output_dir.glob('*.mid')))}")
        print(f"  Quality Gate: Active")
        print(f"  User Feedback: Enabled")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="MVP User-Driven MIDI Generator")
    parser.add_argument("prompt", nargs="?", help="Musical prompt to generate MIDI from")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--output", "-o", help="Output filename (optional)")
    parser.add_argument("--user-id", "-u", default="anonymous", help="User ID for feedback tracking")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return 1
    
    # Initialize generator
    generator = MVPUserDrivenGenerator(api_key)
    
    if args.interactive:
        generator.interactive_mode(args.user_id)
    elif args.prompt:
        result = generator.generate_and_save(args.prompt, args.user_id)
        if not result['success']:
            return 1
    else:
        print("❌ Error: Please provide a prompt or use --interactive mode")
        print("Use --help for more information")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
