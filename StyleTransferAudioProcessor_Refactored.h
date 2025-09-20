// StyleTransferAudioProcessor_Refactored.h
// Header file for refactored modular MIDI transformation functions

#pragma once

#include <JuceHeader.h>

// ============================================================================
// STYLE PARAMETERS STRUCTURE
// ============================================================================

struct StyleParameters
{
    float swingRatio = 0.5f;     // 0.5 = straight, > 0.5 = swing feel
    float accentAmount = 20.0f;  // Velocity to add to accented beats
};

// ============================================================================
// MAIN AUDIO PROCESSOR CLASS
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
     * Apply all style transformations to a MIDI buffer
     * 
     * @param midiMessages Input/output MIDI buffer
     * @param style Style parameters for transformations
     * @param beatsPerMinute Current tempo
     * @param sampleRate Current sample rate
     * 
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     * TRANSFORMATION ORDER: Swing first (rhythmic), then accent (dynamic)
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
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferAudioProcessor)
};
