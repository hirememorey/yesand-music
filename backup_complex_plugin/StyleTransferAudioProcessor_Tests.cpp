// StyleTransferAudioProcessor_Tests.cpp
// Comprehensive test suite for modular MIDI transformation functions

#include "StyleTransferAudioProcessor_Refactored.h"
#include <gtest/gtest.h>

class StyleTransferAudioProcessorTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        processor = std::make_unique<StyleTransferAudioProcessor>();
        sampleRate = 44100.0;
        bpm = 120.0;
        
        // Test style parameters
        testStyle.swingRatio = 0.7f;  // Moderate swing
        testStyle.accentAmount = 15.0f;  // Moderate accent
    }
    
    void TearDown() override
    {
        processor.reset();
    }
    
    std::unique_ptr<StyleTransferAudioProcessor> processor;
    StyleParameters testStyle;
    double sampleRate;
    double bpm;
};

// ============================================================================
// VELOCITY PRESERVATION TESTS - CRITICAL SAFETY VALIDATION
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, VelocityPreservation_AccentModifiesNotOverwrites)
{
    // CRITICAL TEST: Ensure accent modifies original velocity, doesn't overwrite it
    
    // Create test message with specific velocity
    int originalVelocity = 80;
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, originalVelocity);
    inputMessage.setTimeStamp(0.0); // Down-beat position for accent
    
    // Apply accent transformation
    juce::MidiMessage result = processor->applyAccent(inputMessage, testStyle, bpm, sampleRate);
    
    // CRITICAL ASSERTION: Result velocity should be original + accent amount
    int expectedVelocity = originalVelocity + static_cast<int>(testStyle.accentAmount);
    EXPECT_EQ(result.getVelocity(), expectedVelocity);
    
    // CRITICAL ASSERTION: Result should NOT be just the accent amount
    EXPECT_NE(result.getVelocity(), static_cast<int>(testStyle.accentAmount));
}

TEST_F(StyleTransferAudioProcessorTest, VelocityPreservation_NoAccentPreservesOriginal)
{
    // Test that non-accented notes preserve original velocity exactly
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 90);
    inputMessage.setTimeStamp(0.5); // Off-beat position (no accent)
    
    juce::MidiMessage result = processor->applyAccent(inputMessage, testStyle, bpm, sampleRate);
    
    // Should preserve original velocity exactly
    EXPECT_EQ(result.getVelocity(), 90);
}

TEST_F(StyleTransferAudioProcessorTest, VelocityPreservation_VelocityClamping)
{
    // Test that velocity is properly clamped to 0-127 range
    
    // Test high velocity that would exceed 127
    juce::MidiMessage highVelMessage = juce::MidiMessage::noteOn(1, 60, 120);
    highVelMessage.setTimeStamp(0.0); // Down-beat for accent
    
    juce::MidiMessage result = processor->applyAccent(highVelMessage, testStyle, bpm, sampleRate);
    
    // Should be clamped to 127, not 120 + 15 = 135
    EXPECT_EQ(result.getVelocity(), 127);
}

TEST_F(StyleTransferAudioProcessorTest, VelocityPreservation_VelocityFloor)
{
    // Test that velocity doesn't go below 0
    
    StyleParameters extremeStyle = testStyle;
    extremeStyle.accentAmount = -200.0f; // Large negative accent
    
    juce::MidiMessage lowVelMessage = juce::MidiMessage::noteOn(1, 60, 10);
    lowVelMessage.setTimeStamp(0.0); // Down-beat for accent
    
    juce::MidiMessage result = processor->applyAccent(lowVelMessage, extremeStyle, bpm, sampleRate);
    
    // Should be clamped to 0, not 10 - 200 = -190
    EXPECT_EQ(result.getVelocity(), 0);
}

// ============================================================================
// SWING TRANSFORMATION TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, SwingTransformation_OffBeatNotesGetDelay)
{
    // Test that off-beat notes get swing delay applied
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat position (8th note)
    
    juce::MidiMessage result = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
    
    // Should have delayed timestamp
    EXPECT_GT(result.getTimeStamp(), inputMessage.getTimeStamp());
}

TEST_F(StyleTransferAudioProcessorTest, SwingTransformation_DownBeatNotesNoDelay)
{
    // Test that down-beat notes don't get swing delay
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0); // Down-beat position
    
    juce::MidiMessage result = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
    
    // Should have same timestamp
    EXPECT_DOUBLE_EQ(result.getTimeStamp(), inputMessage.getTimeStamp());
}

TEST_F(StyleTransferAudioProcessorTest, SwingTransformation_StraightRatioNoDelay)
{
    // Test that straight swing ratio (0.5) produces no delay
    
    StyleParameters straightStyle = testStyle;
    straightStyle.swingRatio = 0.5f; // Straight timing
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat position
    
    juce::MidiMessage result = processor->applySwing(inputMessage, straightStyle, bpm, sampleRate);
    
    // Should have same timestamp (no delay)
    EXPECT_DOUBLE_EQ(result.getTimeStamp(), inputMessage.getTimeStamp());
}

// ============================================================================
// MESSAGE PRESERVATION TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, MessagePreservation_NonNoteOnMessagesUnchanged)
{
    // Test that non-note-on messages pass through unchanged
    
    juce::MidiMessage noteOffMessage = juce::MidiMessage::noteOff(1, 60, 80);
    juce::MidiMessage ccMessage = juce::MidiMessage::controllerEvent(1, 74, 64);
    juce::MidiMessage pitchBendMessage = juce::MidiMessage::pitchWheel(1, 8192);
    
    // All should pass through unchanged
    EXPECT_EQ(processor->applySwing(noteOffMessage, testStyle, bpm, sampleRate), noteOffMessage);
    EXPECT_EQ(processor->applyAccent(noteOffMessage, testStyle, bpm, sampleRate), noteOffMessage);
    
    EXPECT_EQ(processor->applySwing(ccMessage, testStyle, bpm, sampleRate), ccMessage);
    EXPECT_EQ(processor->applyAccent(ccMessage, testStyle, bpm, sampleRate), ccMessage);
    
    EXPECT_EQ(processor->applySwing(pitchBendMessage, testStyle, bpm, sampleRate), pitchBendMessage);
    EXPECT_EQ(processor->applyAccent(pitchBendMessage, testStyle, bpm, sampleRate), pitchBendMessage);
}

TEST_F(StyleTransferAudioProcessorTest, MessagePreservation_ChannelAndNoteNumberPreserved)
{
    // Test that channel and note number are preserved through transformations
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(3, 72, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat for swing
    
    juce::MidiMessage swingResult = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
    juce::MidiMessage accentResult = processor->applyAccent(inputMessage, testStyle, bpm, sampleRate);
    
    // Channel and note number should be preserved
    EXPECT_EQ(swingResult.getChannel(), 3);
    EXPECT_EQ(swingResult.getNoteNumber(), 72);
    
    EXPECT_EQ(accentResult.getChannel(), 3);
    EXPECT_EQ(accentResult.getNoteNumber(), 72);
}

// ============================================================================
// TRANSFORMATION CHAIN TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, TransformationChain_OrderMatters)
{
    // Test that transformation order produces expected results
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat position (swing + accent)
    
    // Apply transformations in sequence
    juce::MidiMessage swingResult = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
    juce::MidiMessage finalResult = processor->applyAccent(swingResult, testStyle, bpm, sampleRate);
    
    // Should have both swing delay and accent applied
    EXPECT_GT(finalResult.getTimeStamp(), inputMessage.getTimeStamp()); // Swing applied
    EXPECT_GT(finalResult.getVelocity(), inputMessage.getVelocity());   // Accent applied
}

// ============================================================================
// REAL-TIME SAFETY VALIDATION
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, RealTimeSafety_NoMemoryAllocation)
{
    // This test would need to be run with memory profiling tools
    // to ensure no dynamic allocation occurs in the audio thread
    
    // For now, we verify the functions can be called repeatedly without issues
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5);
    
    // Call functions many times to check for stability
    for (int i = 0; i < 1000; ++i) {
        juce::MidiMessage swingResult = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
        juce::MidiMessage accentResult = processor->applyAccent(swingResult, testStyle, bpm, sampleRate);
        
        // Results should be consistent
        EXPECT_TRUE(swingResult.isNoteOn());
        EXPECT_TRUE(accentResult.isNoteOn());
    }
}

// ============================================================================
// EDGE CASE TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, EdgeCase_ZeroAccentAmount)
{
    // Test with zero accent amount
    
    StyleParameters zeroAccentStyle = testStyle;
    zeroAccentStyle.accentAmount = 0.0f;
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0); // Down-beat position
    
    juce::MidiMessage result = processor->applyAccent(inputMessage, zeroAccentStyle, bpm, sampleRate);
    
    // Should preserve original velocity exactly
    EXPECT_EQ(result.getVelocity(), inputMessage.getVelocity());
}

TEST_F(StyleTransferAudioProcessorTest, EdgeCase_ExtremeSwingRatio)
{
    // Test with extreme swing ratios
    
    StyleParameters extremeSwingStyle = testStyle;
    extremeSwingStyle.swingRatio = 1.0f; // Maximum swing
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat position
    
    juce::MidiMessage result = processor->applySwing(inputMessage, extremeSwingStyle, bpm, sampleRate);
    
    // Should have maximum delay
    EXPECT_GT(result.getTimeStamp(), inputMessage.getTimeStamp());
}

// ============================================================================
// PERFORMANCE TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorTest, Performance_LargeMidiBuffer)
{
    // Test performance with large MIDI buffer
    
    juce::MidiBuffer largeBuffer;
    
    // Create 1000 MIDI events
    for (int i = 0; i < 1000; ++i) {
        juce::MidiMessage message = juce::MidiMessage::noteOn(1, 60 + (i % 12), 80);
        message.setTimeStamp(i * 0.1); // Spread over time
        largeBuffer.addEvent(message, i * 100);
    }
    
    // Apply transformations - should complete quickly
    auto start = std::chrono::high_resolution_clock::now();
    processor->applyStyle(largeBuffer, testStyle, bpm, sampleRate);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // Should complete in reasonable time (less than 1ms for 1000 events)
    EXPECT_LT(duration.count(), 1000);
}
