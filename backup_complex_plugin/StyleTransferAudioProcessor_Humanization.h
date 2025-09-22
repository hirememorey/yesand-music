// StyleTransferAudioProcessor_Humanization.h
// Header file with Humanization feature implementation

#pragma once

#include <JuceHeader.h>

// ============================================================================
// STYLE PARAMETERS STRUCTURE - Extended with Humanization
// ============================================================================

struct StyleParameters
{
    float swingRatio = 0.5f;     // 0.5 = straight, > 0.5 = swing feel
    float accentAmount = 20.0f;  // Velocity to add to accented beats
    
    // Humanization parameters
    float humanizeTimingAmount = 0.0f;   // 0.0 = no timing variation, 1.0 = maximum
    float humanizeVelocityAmount = 0.0f; // 0.0 = no velocity variation, 1.0 = maximum
};

// ============================================================================
// MAIN AUDIO PROCESSOR CLASS - Extended with Humanization
// ============================================================================

class StyleTransferAudioProcessor : public juce::AudioProcessor
{
public:
    StyleTransferAudioProcessor();
    ~StyleTransferAudioProcessor() override;

    // AudioProcessor overrides
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) override;

    // Plugin information
    const juce::String getName() const override;
    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    // Program management
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int index, const juce::String& newName) override;

    // State management
    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    // Editor
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    // ============================================================================
    // PUBLIC STYLE CONTROL INTERFACE
    // ============================================================================
    
    void setStyleParameters(const StyleParameters& newStyle);
    StyleParameters getStyleParameters() const;

private:
    // ============================================================================
    // PRIVATE HELPER FUNCTIONS - Pure, Real-Time Safe Transformations
    // ============================================================================
    
    /**
     * Apply swing feel to a MIDI message
     * 
     * @param inputMessage The original MIDI message
     * @param style Style parameters containing swing ratio
     * @param beatsPerMinute Current tempo
     * @param sampleRate Current sample rate
     * @return New MIDI message with swing applied to timing
     * 
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     * PRESERVES: All original message properties except timing
     */
    juce::MidiMessage applySwing(const juce::MidiMessage& inputMessage, 
                                const StyleParameters& style, 
                                double beatsPerMinute, 
                                double sampleRate);
    
    /**
     * Apply accent emphasis to a MIDI message
     * 
     * @param inputMessage The original MIDI message
     * @param style Style parameters containing accent amount
     * @param beatsPerMinute Current tempo
     * @param sampleRate Current sample rate
     * @return New MIDI message with accent applied to velocity
     * 
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     * PRESERVES: All original message properties except velocity
     * CRITICAL: Modifies original velocity, never overwrites it
     */
    juce::MidiMessage applyAccent(const juce::MidiMessage& inputMessage, 
                                 const StyleParameters& style, 
                                 double beatsPerMinute, 
                                 double sampleRate);
    
    /**
     * Apply humanization to a MIDI message
     * 
     * @param inputMessage The original MIDI message
     * @param style Style parameters containing humanization amounts
     * @param beatsPerMinute Current tempo
     * @param sampleRate Current sample rate
     * @return New MIDI message with subtle timing and velocity variations
     * 
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     * PRESERVES: All original message properties except timing and velocity
     * CRITICAL: Modifies original values, never overwrites them
     * MUSICAL: Adds subtle, controlled randomness for authentic feel
     */
    juce::MidiMessage applyHumanization(const juce::MidiMessage& inputMessage, 
                                       const StyleParameters& style, 
                                       double beatsPerMinute, 
                                       double sampleRate);
    
    /**
     * Apply all style transformations to a MIDI buffer
     * 
     * @param midiMessages Input/output MIDI buffer
     * @param style Style parameters for transformations
     * @param beatsPerMinute Current tempo
     * @param sampleRate Current sample rate
     * 
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     * TRANSFORMATION ORDER: Swing (rhythmic) → Accent (dynamic) → Humanization (variation)
     */
    void applyStyle(juce::MidiBuffer& midiMessages, 
                   const StyleParameters& style, 
                   double beatsPerMinute, 
                   double sampleRate);

    // ============================================================================
    // PRIVATE MEMBER VARIABLES
    // ============================================================================
    
    StyleParameters currentStyle;
    double currentBPM = 120.0;
    double currentSampleRate = 44100.0;
    
    // Parameter management (thread-safe)
    juce::AudioProcessorValueTreeState parameters;
    
    // Parameter IDs
    static constexpr const char* SWING_RATIO_ID = "swingRatio";
    static constexpr const char* ACCENT_AMOUNT_ID = "accentAmount";
    static constexpr const char* HUMANIZE_TIMING_ID = "humanizeTiming";
    static constexpr const char* HUMANIZE_VELOCITY_ID = "humanizeVelocity";
    
    // Random number generator for humanization (real-time safe)
    juce::Random humanizationRandom;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferAudioProcessor)
};
