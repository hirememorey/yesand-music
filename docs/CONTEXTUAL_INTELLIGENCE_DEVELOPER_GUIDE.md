# Contextual Intelligence Developer Guide

## Overview

This guide provides comprehensive documentation for the Contextual Intelligence system implemented in Phase 3A. The system provides on-demand visual feedback and musical analysis without interfering with existing DAW workflows.

## Architecture

### Core Components

```
Contextual Intelligence System
├── contextual_intelligence.py     # Core analysis engine
├── visual_feedback_display.py     # Visual feedback display
├── commands/control_plane.py      # Extended control plane
├── commands/parser.py             # Extended command parser
└── commands/types.py              # Extended command types
```

### Data Flow

```
MIDI File → Contextual Intelligence → Musical Analysis → Visual Feedback → Display
     ↓              ↓                      ↓                ↓
  Project      Background Analysis    Smart Suggestions   User Understanding
  Loading      (Silent)               (On-Demand)        (Visual)
```

## Core Classes

### ContextualIntelligence

The main orchestrator for musical analysis and visual feedback.

```python
from contextual_intelligence import ContextualIntelligence

# Initialize
ci = ContextualIntelligence(session_file="session.json")

# Load a MIDI project
success = ci.load_project("song.mid")

# Get visual feedback
feedback = ci.get_visual_feedback("analyze bass")

# Apply suggestions
ci.apply_suggestion({"suggestion": "add_swing"})
```

**Key Methods:**
- `load_project(midi_file_path: str) -> bool`: Load MIDI project for analysis
- `get_visual_feedback(command: str) -> List[VisualFeedback]`: Get visual feedback for command
- `apply_suggestion(suggestion_data: Dict[str, Any]) -> bool`: Apply musical suggestion
- `get_feedback_summary() -> str`: Get summary of all feedback
- `clear_feedback() -> None`: Clear all visual feedback

### MusicalAnalysis

Comprehensive musical analysis results.

```python
@dataclass
class MusicalAnalysis:
    bass_notes: List[Dict[str, Any]]        # Bass line notes
    melody_notes: List[Dict[str, Any]]      # Melody notes
    harmony_notes: List[Dict[str, Any]]     # Harmony notes
    rhythm_pattern: Dict[str, Any]          # Rhythm analysis
    key_signature: str                      # Detected key
    tempo: float                           # Detected tempo
    time_signature: str                    # Detected time signature
    style_classification: str              # Style (jazz, classical, etc.)
    confidence_scores: Dict[str, float]    # Analysis confidence
```

### VisualFeedback

Structured feedback for display.

```python
@dataclass
class VisualFeedback:
    type: VisualFeedbackType               # Type of feedback
    element: MusicalElement                # Musical element
    message: str                          # User message
    data: Dict[str, Any]                  # Additional data
    timestamp: float                      # Creation time
    duration: Optional[float] = None      # Display duration
```

## Musical Analysis

### Bass Line Detection

Identifies low-pitch notes (≤C4) as bass elements.

```python
# Filter notes by pitch
bass_notes = filter_notes_by_pitch(notes, max_pitch=60)  # C4 and below

# Analysis includes:
# - Note count and pitch range
# - Confidence scoring
# - Visual highlighting
```

### Melody Recognition

Finds highest-pitch notes in each time segment.

```python
# Group notes by time segments
time_segments = {}
for note in notes:
    start_time = note['start_time_seconds']
    segment = int(start_time * 4)  # Quarter note segments
    if segment not in time_segments:
        time_segments[segment] = []
    time_segments[segment].append(note)

# Find highest pitch in each segment
melody_notes = []
for segment_notes in time_segments.values():
    if segment_notes:
        highest_note = max(segment_notes, key=lambda n: n['pitch'])
        melody_notes.append(highest_note)
```

### Harmony Analysis

Identifies supporting chord tones.

```python
# Harmony = all notes that aren't bass or melody
bass_pitches = {note['pitch'] for note in bass_notes}
melody_pitches = {note['pitch'] for note in melody_notes}

harmony_notes = []
for note in notes:
    if note['pitch'] not in bass_pitches and note['pitch'] not in melody_pitches:
        harmony_notes.append(note)
```

### Rhythm Analysis

Calculates swing, syncopation, and complexity.

```python
# Calculate swing ratio
swing_ratio = calculate_swing_ratio(notes)

# Calculate syncopation
syncopation = calculate_syncopation(notes)

# Analyze complexity
complexity = min(1.0, note_density / 8.0)
```

## Visual Feedback System

### Color Coding

Musical elements are color-coded for easy identification:

```python
color_map = {
    MusicalElement.BASS: "#4A90E2",      # Blue
    MusicalElement.MELODY: "#7ED321",    # Green
    MusicalElement.HARMONY: "#9013FE",   # Purple
    MusicalElement.RHYTHM: "#F5A623",    # Orange
    MusicalElement.DRUMS: "#D0021B",     # Red
}
```

### Visual Feedback Types

```python
class VisualFeedbackType(Enum):
    HIGHLIGHT = "highlight"           # Color-coded highlighting
    DIFF = "diff"                     # Before/after changes
    EXPLANATION = "explanation"       # Educational content
    SUGGESTION = "suggestion"         # Improvement recommendations
    ANALYSIS = "analysis"             # Comprehensive analysis
```

### Display System

The visual feedback display runs in a separate thread to avoid blocking audio:

```python
from visual_feedback_display import start_visual_feedback, add_visual_feedback

# Start display
start_visual_feedback()

# Add feedback
add_visual_feedback(feedback)
```

## Command System

### New Command Types

The system adds 10 new command types for contextual intelligence:

```python
# Analysis commands
CommandType.ANALYZE_BASS = "analyze_bass"
CommandType.ANALYZE_MELODY = "analyze_melody"
CommandType.ANALYZE_HARMONY = "analyze_harmony"
CommandType.ANALYZE_RHYTHM = "analyze_rhythm"
CommandType.ANALYZE_ALL = "analyze_all"

# Suggestion commands
CommandType.GET_SUGGESTIONS = "get_suggestions"
CommandType.APPLY_SUGGESTION = "apply_suggestion"

# Feedback commands
CommandType.SHOW_FEEDBACK = "show_feedback"
CommandType.CLEAR_FEEDBACK = "clear_feedback"

# Project commands
CommandType.LOAD_PROJECT = "load_project"
```

### Natural Language Patterns

Commands support multiple natural language patterns:

```python
# Bass analysis patterns
r"analyze\s+bass"
r"show\s+bass"
r"what\s+is\s+the\s+bass\s+doing"
r"bass\s+analysis"
r"highlight\s+bass"

# Melody analysis patterns
r"analyze\s+melody"
r"show\s+melody"
r"what\s+is\s+the\s+melody\s+doing"
r"melody\s+analysis"
r"highlight\s+melody"
```

## Integration with Control Plane

### Extended Control Plane

The control plane is extended with contextual intelligence capabilities:

```python
class ControlPlane:
    def __init__(self, ...):
        # ... existing initialization ...
        self.contextual_intelligence = ContextualIntelligence(session_file)
    
    def _handle_contextual_intelligence_command(self, command: Command) -> str:
        """Handle contextual intelligence commands."""
        # ... implementation ...
    
    def _format_visual_feedback(self, feedback_list) -> str:
        """Format visual feedback for display."""
        # ... implementation ...
```

### Command Flow

```
User Command → Command Parser → Control Plane → Contextual Intelligence → Visual Feedback Display
```

## Usage Examples

### Basic Analysis

```python
# Load a MIDI project
python control_plane_cli.py "load song.mid"

# Analyze different elements
python control_plane_cli.py "analyze bass"
python control_plane_cli.py "analyze melody"
python control_plane_cli.py "analyze all"

# Get suggestions
python control_plane_cli.py "get suggestions"
```

### Programmatic Usage

```python
from contextual_intelligence import ContextualIntelligence
from visual_feedback_display import start_visual_feedback

# Initialize
ci = ContextualIntelligence()

# Load project
ci.load_project("song.mid")

# Start visual feedback
start_visual_feedback()

# Get analysis
feedback = ci.get_visual_feedback("analyze bass")
print(f"Found {len(feedback)} feedback items")

# Apply suggestions
ci.apply_suggestion({"suggestion": "add_swing"})
```

## Testing

### Test Suite

The system includes comprehensive tests:

```python
# Run tests
python test_contextual_intelligence.py

# Interactive demo
python demo_contextual_intelligence.py
```

### Test Coverage

- Direct contextual intelligence analysis
- Command parsing and execution
- Control plane integration
- MIDI I/O functionality
- Visual feedback display

## Development Guidelines

### Adding New Analysis Types

1. **Add to MusicalElement enum**:
```python
class MusicalElement(Enum):
    # ... existing elements ...
    DRUMS = "drums"
```

2. **Implement analysis method**:
```python
def _analyze_drums(self, notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze drum patterns."""
    # ... implementation ...
```

3. **Add to analysis pipeline**:
```python
def _analyze_project(self) -> None:
    # ... existing analysis ...
    drum_notes = self._analyze_drums(notes)
```

4. **Add visual feedback**:
```python
def _get_drums_feedback(self) -> List[VisualFeedback]:
    """Get visual feedback for drums analysis."""
    # ... implementation ...
```

### Adding New Command Types

1. **Add to CommandType enum**:
```python
class CommandType(Enum):
    # ... existing types ...
    ANALYZE_DRUMS = "analyze_drums"
```

2. **Add regex patterns**:
```python
CommandType.ANALYZE_DRUMS: [
    r"analyze\s+drums",
    r"show\s+drums",
    r"what\s+are\s+the\s+drums\s+doing",
    r"drums\s+analysis",
    r"highlight\s+drums",
],
```

3. **Add parameter extraction**:
```python
elif cmd_type == CommandType.ANALYZE_DRUMS:
    # No parameters needed
    pass
```

4. **Add command handling**:
```python
elif command.type == CommandType.ANALYZE_DRUMS:
    feedback = self.contextual_intelligence.get_visual_feedback("analyze drums")
    return self._format_visual_feedback(feedback)
```

### Adding New Visual Feedback Types

1. **Add to VisualFeedbackType enum**:
```python
class VisualFeedbackType(Enum):
    # ... existing types ...
    COMPARISON = "comparison"
```

2. **Implement feedback generation**:
```python
def _get_comparison_feedback(self) -> List[VisualFeedback]:
    """Get comparison feedback."""
    # ... implementation ...
```

3. **Add to display system**:
```python
def _display_feedback(self, feedback: VisualFeedback) -> None:
    # ... existing display logic ...
    if feedback.type == VisualFeedbackType.COMPARISON:
        # ... comparison-specific display ...
```

## Performance Considerations

### Real-Time Safety

- Visual feedback runs in separate thread
- No blocking operations in audio-critical paths
- Background analysis doesn't interfere with MIDI playback

### Memory Management

- Visual feedback queue has size limits
- Old feedback is automatically cleaned up
- Analysis results are cached to avoid recomputation

### Thread Safety

- All visual feedback operations are thread-safe
- MIDI I/O operations are isolated from visual feedback
- Control plane operations are synchronized

## Troubleshooting

### Common Issues

1. **Visual feedback not displaying**:
   - Check if display thread is running
   - Verify feedback queue is not empty
   - Check for threading issues

2. **Analysis not working**:
   - Verify MIDI file is loaded correctly
   - Check note format compatibility
   - Review analysis confidence scores

3. **Commands not parsing**:
   - Check regex patterns in parser
   - Verify command type enum values
   - Test with simple commands first

### Debug Mode

Enable debug output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug output
python control_plane_cli.py "analyze bass"
```

## Future Development

### Phase 3B: Advanced Visual Features

- Visual diff system showing before/after changes
- Interactive suggestions with click-to-apply
- Advanced educational content and explanations
- A/B comparison through audio preview

### Phase 3C: DAW Integration

- Multi-DAW support (Logic Pro, Pro Tools, Cubase)
- Contextual menus and keyboard shortcuts
- Voice integration for hands-free operation
- Advanced performance optimization

## Conclusion

The Contextual Intelligence system provides a powerful foundation for musical analysis and visual feedback. It's designed to be extensible, maintainable, and non-intrusive, allowing musicians to understand and learn from their music without disrupting their creative workflow.

For questions or contributions, refer to the main project documentation and test suite.
