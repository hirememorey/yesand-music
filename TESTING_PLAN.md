# YesAnd Music - Testing Plan

## Overview

This document provides step-by-step instructions for testing the YesAnd Music system, including both the command-line MIDI editor and the invisible intelligence interface (Phase 3). The test plan covers the complete workflow from DAW export to transformation to DAW import, as well as invisible intelligence testing.

## Prerequisites

- Python 3.7+ installed
- YesAnd Music project dependencies installed (`pip install mido python-rtmidi`)
- A DAW (Digital Audio Workstation) such as:
  - GarageBand (macOS)
  - Logic Pro (macOS)
  - Ardour (cross-platform)
  - Reaper (cross-platform)
  - Any other DAW that supports MIDI import/export

## Test Plan: Command-Line MIDI Editor (Phase 1)

### Step 1: Create Test MIDI Content in DAW

1. **Open your DAW** and create a new project
2. **Create a MIDI track** with a simple 8th note pattern:
   - Use a simple instrument (piano, synth, etc.)
   - Create a pattern with both on-beat and off-beat notes
   - Example pattern (1 beat = 1 second):
     - Beat 1: Note on 0.0s, Note off 0.5s
     - Beat 1.5: Note on 0.5s, Note off 1.0s
     - Beat 2: Note on 1.0s, Note off 1.5s
     - Beat 2.5: Note on 1.5s, Note off 2.0s
3. **Record or program** the pattern (4-8 notes total)
4. **Play back** to verify the pattern sounds correct

### Step 2: Export MIDI from DAW

1. **Select the MIDI track** containing your test pattern
2. **Export as MIDI file**:
   - In GarageBand: File → Export → Export Song to Disk → Format: MIDI
   - In Logic Pro: File → Export → Selection as MIDI File
   - In Ardour: File → Export → Export Session → Format: MIDI
   - In Reaper: File → Render → Format: MIDI
3. **Save the file** as `test_pattern.mid` in an easily accessible location
4. **Verify the export** by checking the file size (should be > 0 bytes)

### Step 3: Test the Semantic MIDI Editor

1. **Open terminal/command prompt** and navigate to the YesAnd Music project directory
2. **Run the swing transformation**:
   ```bash
   python edit.py --input test_pattern.mid --output test_pattern_swung.mid --command "apply_swing"
   ```
3. **Verify the output**:
   - You should see status messages:
     ```
     YesAnd Music - Semantic MIDI Editor
     ========================================
     Input file:  test_pattern.mid
     Output file: test_pattern_swung.mid
     Command:     apply_swing
     ========================================
     Loading MIDI file...
     File loaded: X notes found
     Applying transformation: Swing
     Sorting notes by start time...
     Resolving overlaps...
     Saving MIDI file...
     File saved successfully
     ```
   - Check that `test_pattern_swung.mid` was created
   - Verify the file size is reasonable (> 0 bytes)

### Step 4: Import Back into DAW

1. **Open a new project** in your DAW (or create a new track in the same project)
2. **Import the transformed MIDI file**:
   - In GarageBand: File → Import → Choose `test_pattern_swung.mid`
   - In Logic Pro: File → Import → MIDI File → Choose `test_pattern_swung.mid`
   - In Ardour: File → Import → Choose `test_pattern_swung.mid`
   - In Reaper: File → Import → Choose `test_pattern_swung.mid`
3. **Load the same instrument** as the original pattern
4. **Play back** the transformed pattern

### Step 5: Verify the Transformation

1. **Compare the original and transformed patterns**:
   - Play the original pattern
   - Play the transformed pattern
   - Listen for the swing feel - off-beat notes should sound slightly delayed
2. **Check the timing visually** (if your DAW shows MIDI notes):
   - Off-beat notes should appear slightly later in the timeline
   - The overall pattern should maintain its musical structure
3. **Verify no audio issues**:
   - No clicks, pops, or dropouts
   - Notes should play cleanly
   - No missing or extra notes

## Expected Results

### ✅ Success Criteria
- The script runs without errors
- Both input and output MIDI files are created
- The transformed pattern has a noticeable swing feel
- Off-beat notes are delayed compared to the original
- No audio artifacts or missing notes
- The transformation preserves the musical structure

### ❌ Failure Indicators
- Script errors or crashes
- Missing output files
- No audible difference between original and transformed
- Audio artifacts (clicks, pops, dropouts)
- Missing or extra notes
- MIDI import errors in DAW

## Troubleshooting

### Common Issues

#### "File not found" Error
- **Problem**: Input MIDI file doesn't exist
- **Solution**: Verify the file path and ensure the MIDI file was exported correctly

#### "Unknown command" Error
- **Problem**: Incorrect command syntax
- **Solution**: Use exactly `apply_swing` (case-sensitive, with underscore)

#### "message time must be non-negative" Error
- **Problem**: MIDI format constraint violation
- **Solution**: This should be resolved in the current version with overlap resolution

#### No Audible Difference
- **Problem**: Pattern might not have off-beat notes
- **Solution**: Create a pattern with clear on-beat and off-beat notes (8th note pattern)

#### DAW Import Issues
- **Problem**: DAW can't import the transformed file
- **Solution**: Check file format and try re-exporting from the original DAW

### Debug Commands

If you encounter issues, try these debug commands:

```bash
# Check if the input file exists and is valid
python -c "from midi_io import parse_midi_file; notes = parse_midi_file('test_pattern.mid'); print(f'Loaded {len(notes)} notes')"

# Test the swing transformation directly
python -c "
from midi_io import parse_midi_file
from analysis import apply_swing
notes = parse_midi_file('test_pattern.mid')
swung = apply_swing(notes)
print('Original:', [f\"{n['pitch']}@{n['start_time_seconds']:.3f}\" for n in notes])
print('Swung:', [f\"{n['pitch']}@{n['start_time_seconds']:.3f}\" for n in swung])
"

# Verify the output file
python -c "from midi_io import parse_midi_file; notes = parse_midi_file('test_pattern_swung.mid'); print(f'Output has {len(notes)} notes')"
```

## Test Variations

### Test 1: Simple 8th Note Pattern
- Create a basic 8th note pattern (on-beat, off-beat, on-beat, off-beat)
- Expected: Clear swing feel on off-beat notes

### Test 2: Mixed Note Values
- Create a pattern with quarter notes and 8th notes
- Expected: Only 8th notes get swing treatment

### Test 3: Dense Pattern
- Create a pattern with many notes close together
- Expected: Overlap resolution prevents MIDI format errors

### Test 4: Single Note
- Create a pattern with just one note
- Expected: No transformation (no off-beat notes to swing)

## Success Metrics

- [ ] Script runs without errors
- [ ] Input file loads successfully
- [ ] Swing transformation applies correctly
- [ ] Output file saves successfully
- [ ] DAW can import the transformed file
- [ ] Audible swing feel is present
- [ ] No audio artifacts
- [ ] Musical structure is preserved

## Next Steps

Once this test plan passes successfully, the Phase 1 MVP is validated and ready for:
- Adding more transformation commands
- Implementing more sophisticated musical analysis
- Building the Phase 2 musical analysis engine
- Developing the semantic command parser

## Support

If you encounter issues not covered in this test plan:
1. Check the project documentation in `docs/`
2. Review the error messages carefully
3. Try the debug commands above
4. Verify your DAW's MIDI export/import settings
5. Ensure you're using the correct command syntax

---

**Note**: This test plan validates the core "Brain vs. Hands" architecture by testing the Python intelligence (swing transformation) working with simple MIDI file I/O, without requiring any DAW integration.

## Test Plan: Invisible Intelligence Interface (Phase 3)

### Prerequisites for Invisible Intelligence Testing
- Invisible intelligence implementation (Phase 3A, 3B, 3C)
- DAW with background analysis support
- Test MIDI files with various musical patterns

### Phase 3A: Background Intelligence Foundation Testing

#### Test 1: Background Pattern Recognition
1. **Load MIDI file** in DAW with invisible intelligence enabled
2. **Verify background analysis**:
   - Bass lines detected in background
   - Melodies detected in background
   - Chord progressions detected in background
   - Rhythmic patterns detected in background
   - Drums detected in background
3. **Test real-time updates** as MIDI data changes
4. **Verify performance** - no audio dropouts during background analysis

#### Test 2: Contextual MIDI Assistance
1. **Natural language commands** for musical modifications
2. **Verify immediate audio feedback** during assistance
3. **Test undo/redo** functionality
4. **Verify background state preservation** through operations

#### Test 3: DAW Integration
1. **Verify seamless background operation** within DAW workflow
2. **Test contextual menus** on right-click
3. **Verify familiar DAW tools** still work
4. **Test keyboard shortcuts** integration

### Phase 3B: Smart Invisible Assistance Testing

#### Test 1: Suggestion Display
1. **Load complex MIDI pattern**
2. **Verify suggestion indicators** appear through natural language
3. **Test suggestion types**:
   - Harmonic suggestions
   - Rhythmic suggestions
   - Melodic suggestions
   - Dynamic suggestions
4. **Verify natural language clarity** of suggestion indicators

#### Test 2: Natural Language Application
1. **Use natural language commands** to apply suggestions
2. **Verify immediate audio feedback**
3. **Test batch application** of multiple suggestions
4. **Verify undo/redo** for applied suggestions

#### Test 3: Musical Intelligence Display
1. **Ask for explanations** through natural language
2. **Verify musical theory** explanations are clear
3. **Test educational content** for learning
4. **Verify A/B comparison** through audio preview

### Phase 3C: Advanced Invisible Intelligence Features Testing

#### Test 1: Advanced Background Analysis
1. **Test harmonic analysis** without visual interference
2. **Test rhythmic analysis** with groove patterns
3. **Test melodic analysis** with contour detection
4. **Test dynamic analysis** with velocity analysis

#### Test 2: Multi-DAW Support
1. **Test in Logic Pro**
2. **Test in Pro Tools**
3. **Test in Cubase**
4. **Verify consistent experience** across DAWs

#### Test 3: Advanced Interaction Features
1. **Test voice commands** (if available)
2. **Test keyboard shortcuts**
3. **Test contextual menus**
4. **Test natural language interaction**

### Invisible Intelligence Success Criteria
- [ ] Background analysis works in real-time without audio dropouts
- [ ] Natural language assistance provides immediate feedback
- [ ] Smart suggestions improve musical quality
- [ ] DAW integration preserves familiar workflows
- [ ] Educational content helps users learn musical concepts
- [ ] Performance meets professional standards
