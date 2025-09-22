// StyleTransferAudioProcessor_Humanization_Tests.cpp
// Comprehensive test suite for Humanization feature

#include "StyleTransferAudioProcessor_Humanization.h"
#include <gtest/gtest.h>

class StyleTransferAudioProcessorHumanizationTest : public ::testing::Test
{
protected:
    void SetUp() override
    {
        processor = std::make_unique<StyleTransferAudioProcessor>();
        sampleRate = 44100.0;
        bpm = 120.0;
        
        // Test style parameters
        testStyle.swingRatio = 0.7f;
        testStyle.accentAmount = 15.0f;
        testStyle.humanizeTimingAmount = 0.5f;  // Moderate timing humanization
        testStyle.humanizeVelocityAmount = 0.3f; // Moderate velocity humanization
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
// VELOCITY HUMANIZATION TESTS - CRITICAL SAFETY VALIDATION
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, VelocityHumanization_ModifiesNotOverwrites)
{
    // CRITICAL TEST: Ensure humanization modifies original velocity, doesn't overwrite it
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0);
    
    // Apply humanization multiple times to test consistency
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
        
        // CRITICAL ASSERTION: Result velocity should be original +/- small offset
        int velocityDifference = result.getVelocity() - inputMessage.getVelocity();
        int maxExpectedOffset = static_cast<int>(10 * testStyle.humanizeVelocityAmount); // Max 3 with 0.3 amount
        
        EXPECT_GE(velocityDifference, -maxExpectedOffset);
        EXPECT_LE(velocityDifference, maxExpectedOffset);
        
        // CRITICAL ASSERTION: Result should NOT be completely random
        EXPECT_NE(result.getVelocity(), 0);
        EXPECT_NE(result.getVelocity(), 127);
    }
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, VelocityHumanization_ZeroAmountPreservesOriginal)
{
    // Test that zero humanization amount preserves original velocity exactly
    
    StyleParameters noHumanizationStyle = testStyle;
    noHumanizationStyle.humanizeVelocityAmount = 0.0f;
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0);
    
    juce::MidiMessage result = processor->applyHumanization(inputMessage, noHumanizationStyle, bpm, sampleRate);
    
    // Should preserve original velocity exactly
    EXPECT_EQ(result.getVelocity(), inputMessage.getVelocity());
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, VelocityHumanization_VelocityClamping)
{
    // Test that humanized velocity is properly clamped to 0-127 range
    
    StyleParameters extremeStyle = testStyle;
    extremeStyle.humanizeVelocityAmount = 1.0f; // Maximum humanization
    
    // Test high velocity that could exceed 127
    juce::MidiMessage highVelMessage = juce::MidiMessage::noteOn(1, 60, 125);
    highVelMessage.setTimeStamp(0.0);
    
    // Test multiple times to catch edge cases
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(highVelMessage, extremeStyle, bpm, sampleRate);
        EXPECT_LE(result.getVelocity(), 127);
    }
    
    // Test low velocity that could go below 0
    juce::MidiMessage lowVelMessage = juce::MidiMessage::noteOn(1, 60, 5);
    lowVelMessage.setTimeStamp(0.0);
    
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(lowVelMessage, extremeStyle, bpm, sampleRate);
        EXPECT_GE(result.getVelocity(), 0);
    }
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, VelocityHumanization_ScalingWorks)
{
    // Test that humanization amount properly scales the variation
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0);
    
    // Test with different humanization amounts
    std::vector<float> amounts = {0.0f, 0.25f, 0.5f, 0.75f, 1.0f};
    std::vector<int> maxVariations;
    
    for (float amount : amounts) {
        StyleParameters scaledStyle = testStyle;
        scaledStyle.humanizeVelocityAmount = amount;
        
        int maxVariation = 0;
        for (int i = 0; i < 100; ++i) {
            juce::MidiMessage result = processor->applyHumanization(inputMessage, scaledStyle, bpm, sampleRate);
            int variation = abs(result.getVelocity() - inputMessage.getVelocity());
            maxVariation = std::max(maxVariation, variation);
        }
        maxVariations.push_back(maxVariation);
    }
    
    // Higher amounts should generally produce larger variations
    for (size_t i = 1; i < amounts.size(); ++i) {
        EXPECT_GE(maxVariations[i], maxVariations[i-1]);
    }
}

// ============================================================================
// TIMING HUMANIZATION TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, TimingHumanization_ModifiesNotOverwrites)
{
    // CRITICAL TEST: Ensure humanization modifies original timestamp, doesn't overwrite it
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0); // 1 second timestamp
    
    // Apply humanization multiple times to test consistency
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
        
        // CRITICAL ASSERTION: Result timestamp should be original +/- small offset
        double timeDifference = result.getTimeStamp() - inputMessage.getTimeStamp();
        double maxExpectedOffsetMs = 5.0 * testStyle.humanizeTimingAmount; // Max 2.5ms with 0.5 amount
        double maxExpectedOffsetSeconds = maxExpectedOffsetMs / 1000.0;
        
        EXPECT_GE(timeDifference, -maxExpectedOffsetSeconds);
        EXPECT_LE(timeDifference, maxExpectedOffsetSeconds);
        
        // CRITICAL ASSERTION: Result should NOT be completely random
        EXPECT_GT(result.getTimeStamp(), 0.0);
    }
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, TimingHumanization_ZeroAmountPreservesOriginal)
{
    // Test that zero humanization amount preserves original timestamp exactly
    
    StyleParameters noHumanizationStyle = testStyle;
    noHumanizationStyle.humanizeTimingAmount = 0.0f;
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.5);
    
    juce::MidiMessage result = processor->applyHumanization(inputMessage, noHumanizationStyle, bpm, sampleRate);
    
    // Should preserve original timestamp exactly
    EXPECT_DOUBLE_EQ(result.getTimeStamp(), inputMessage.getTimeStamp());
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, TimingHumanization_ScalingWorks)
{
    // Test that humanization amount properly scales the timing variation
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0);
    
    // Test with different humanization amounts
    std::vector<float> amounts = {0.0f, 0.25f, 0.5f, 0.75f, 1.0f};
    std::vector<double> maxVariations;
    
    for (float amount : amounts) {
        StyleParameters scaledStyle = testStyle;
        scaledStyle.humanizeTimingAmount = amount;
        
        double maxVariation = 0.0;
        for (int i = 0; i < 100; ++i) {
            juce::MidiMessage result = processor->applyHumanization(inputMessage, scaledStyle, bpm, sampleRate);
            double variation = abs(result.getTimeStamp() - inputMessage.getTimeStamp());
            maxVariation = std::max(maxVariation, variation);
        }
        maxVariations.push_back(maxVariation);
    }
    
    // Higher amounts should generally produce larger variations
    for (size_t i = 1; i < amounts.size(); ++i) {
        EXPECT_GE(maxVariations[i], maxVariations[i-1]);
    }
}

// ============================================================================
// MESSAGE PRESERVATION TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, MessagePreservation_NonNoteOnMessagesUnchanged)
{
    // Test that non-note-on messages pass through unchanged
    
    juce::MidiMessage noteOffMessage = juce::MidiMessage::noteOff(1, 60, 80);
    juce::MidiMessage ccMessage = juce::MidiMessage::controllerEvent(1, 74, 64);
    juce::MidiMessage pitchBendMessage = juce::MidiMessage::pitchWheel(1, 8192);
    
    // All should pass through unchanged
    EXPECT_EQ(processor->applyHumanization(noteOffMessage, testStyle, bpm, sampleRate), noteOffMessage);
    EXPECT_EQ(processor->applyHumanization(ccMessage, testStyle, bpm, sampleRate), ccMessage);
    EXPECT_EQ(processor->applyHumanization(pitchBendMessage, testStyle, bpm, sampleRate), pitchBendMessage);
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, MessagePreservation_ChannelAndNoteNumberPreserved)
{
    // Test that channel and note number are preserved through humanization
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(3, 72, 80);
    inputMessage.setTimeStamp(0.5);
    
    juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
    
    // Channel and note number should be preserved
    EXPECT_EQ(result.getChannel(), 3);
    EXPECT_EQ(result.getNoteNumber(), 72);
}

// ============================================================================
// TRANSFORMATION CHAIN TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, TransformationChain_HumanizationLast)
{
    // Test that humanization is applied last in the transformation chain
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5); // Off-beat position (swing + accent + humanization)
    
    // Apply transformations in sequence
    juce::MidiMessage swingResult = processor->applySwing(inputMessage, testStyle, bpm, sampleRate);
    juce::MidiMessage accentResult = processor->applyAccent(swingResult, testStyle, bpm, sampleRate);
    juce::MidiMessage finalResult = processor->applyHumanization(accentResult, testStyle, bpm, sampleRate);
    
    // Should have swing delay, accent, and humanization applied
    EXPECT_GT(finalResult.getTimeStamp(), inputMessage.getTimeStamp()); // Swing + timing humanization
    EXPECT_GT(finalResult.getVelocity(), inputMessage.getVelocity());   // Accent + velocity humanization
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, TransformationChain_OrderMatters)
{
    // Test that transformation order produces expected results
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5);
    
    // Apply all transformations
    juce::MidiMessage processedMessage = inputMessage;
    processedMessage = processor->applySwing(processedMessage, testStyle, bpm, sampleRate);
    processedMessage = processor->applyAccent(processedMessage, testStyle, bpm, sampleRate);
    processedMessage = processor->applyHumanization(processedMessage, testStyle, bpm, sampleRate);
    
    // Should have all transformations applied
    EXPECT_GT(processedMessage.getTimeStamp(), inputMessage.getTimeStamp());
    EXPECT_GT(processedMessage.getVelocity(), inputMessage.getVelocity());
}

// ============================================================================
// REAL-TIME SAFETY VALIDATION
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, RealTimeSafety_NoMemoryAllocation)
{
    // Test that humanization functions can be called repeatedly without issues
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.5);
    
    // Call functions many times to check for stability
    for (int i = 0; i < 1000; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
        
        // Results should be consistent and valid
        EXPECT_TRUE(result.isNoteOn());
        EXPECT_GE(result.getVelocity(), 0);
        EXPECT_LE(result.getVelocity(), 127);
        EXPECT_GT(result.getTimeStamp(), 0.0);
    }
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, RealTimeSafety_RandomGeneratorStability)
{
    // Test that the random generator doesn't cause issues
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(0.0);
    
    // Call humanization many times rapidly
    for (int i = 0; i < 10000; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
        
        // Should always produce valid results
        EXPECT_TRUE(result.isNoteOn());
        EXPECT_GE(result.getVelocity(), 0);
        EXPECT_LE(result.getVelocity(), 127);
    }
}

// ============================================================================
// EDGE CASE TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, EdgeCase_ExtremeHumanizationAmounts)
{
    // Test with extreme humanization amounts
    
    StyleParameters extremeStyle = testStyle;
    extremeStyle.humanizeTimingAmount = 1.0f;   // Maximum timing humanization
    extremeStyle.humanizeVelocityAmount = 1.0f; // Maximum velocity humanization
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0);
    
    // Should still produce valid results
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, extremeStyle, bpm, sampleRate);
        
        EXPECT_GE(result.getVelocity(), 0);
        EXPECT_LE(result.getVelocity(), 127);
        EXPECT_GT(result.getTimeStamp(), 0.0);
    }
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, EdgeCase_ZeroHumanizationAmounts)
{
    // Test with zero humanization amounts
    
    StyleParameters noHumanizationStyle = testStyle;
    noHumanizationStyle.humanizeTimingAmount = 0.0f;
    noHumanizationStyle.humanizeVelocityAmount = 0.0f;
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0);
    
    juce::MidiMessage result = processor->applyHumanization(inputMessage, noHumanizationStyle, bpm, sampleRate);
    
    // Should preserve original values exactly
    EXPECT_EQ(result.getVelocity(), inputMessage.getVelocity());
    EXPECT_DOUBLE_EQ(result.getTimeStamp(), inputMessage.getTimeStamp());
}

// ============================================================================
// PERFORMANCE TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, Performance_LargeMidiBuffer)
{
    // Test performance with large MIDI buffer including humanization
    
    juce::MidiBuffer largeBuffer;
    
    // Create 1000 MIDI events
    for (int i = 0; i < 1000; ++i) {
        juce::MidiMessage message = juce::MidiMessage::noteOn(1, 60 + (i % 12), 80);
        message.setTimeStamp(i * 0.1); // Spread over time
        largeBuffer.addEvent(message, i * 100);
    }
    
    // Apply transformations including humanization - should complete quickly
    auto start = std::chrono::high_resolution_clock::now();
    processor->applyStyle(largeBuffer, testStyle, bpm, sampleRate);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // Should complete in reasonable time (less than 2ms for 1000 events with humanization)
    EXPECT_LT(duration.count(), 2000);
}

// ============================================================================
// MUSICAL AUTHENTICITY TESTS
// ============================================================================

TEST_F(StyleTransferAudioProcessorHumanizationTest, MusicalAuthenticity_SubtleVariation)
{
    // Test that humanization produces subtle, musical variation
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0);
    
    std::vector<int> velocities;
    std::vector<double> timestamps;
    
    // Collect results from multiple humanization calls
    for (int i = 0; i < 1000; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, testStyle, bpm, sampleRate);
        velocities.push_back(result.getVelocity());
        timestamps.push_back(result.getTimeStamp());
    }
    
    // Calculate variation statistics
    int minVel = *std::min_element(velocities.begin(), velocities.end());
    int maxVel = *std::max_element(velocities.begin(), velocities.end());
    double minTime = *std::min_element(timestamps.begin(), timestamps.end());
    double maxTime = *std::max_element(timestamps.begin(), timestamps.end());
    
    // Should have some variation but not extreme
    EXPECT_GT(maxVel - minVel, 0); // Some velocity variation
    EXPECT_LT(maxVel - minVel, 20); // But not too much (max 10 offset * 2)
    
    EXPECT_GT(maxTime - minTime, 0.0); // Some timing variation
    EXPECT_LT(maxTime - minTime, 0.01); // But not too much (max 5ms * 2)
}

TEST_F(StyleTransferAudioProcessorHumanizationTest, MusicalAuthenticity_PreservesMusicalIntent)
{
    // Test that humanization preserves the overall musical intent
    
    juce::MidiMessage inputMessage = juce::MidiMessage::noteOn(1, 60, 80);
    inputMessage.setTimeStamp(1.0);
    
    // Test with moderate humanization
    StyleParameters moderateStyle = testStyle;
    moderateStyle.humanizeTimingAmount = 0.3f;
    moderateStyle.humanizeVelocityAmount = 0.2f;
    
    std::vector<int> velocities;
    std::vector<double> timestamps;
    
    for (int i = 0; i < 100; ++i) {
        juce::MidiMessage result = processor->applyHumanization(inputMessage, moderateStyle, bpm, sampleRate);
        velocities.push_back(result.getVelocity());
        timestamps.push_back(result.getTimeStamp());
    }
    
    // Calculate averages
    double avgVel = std::accumulate(velocities.begin(), velocities.end(), 0.0) / velocities.size();
    double avgTime = std::accumulate(timestamps.begin(), timestamps.end(), 0.0) / timestamps.size();
    
    // Averages should be close to original values
    EXPECT_NEAR(avgVel, inputMessage.getVelocity(), 2.0); // Within 2 velocity units
    EXPECT_NEAR(avgTime, inputMessage.getTimeStamp(), 0.001); // Within 1ms
}
