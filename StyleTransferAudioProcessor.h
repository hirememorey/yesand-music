#pragma once

#include <juce_audio_processors/juce_audio_processors.h>

// ============================================================================
// STYLE PARAMETERS STRUCTURE
// ============================================================================

struct StyleParameters
{
    float swingRatio = 0.5f;     // 0.5 = straight, > 0.5 = swing feel
    float accentAmount = 20.0f;  // Velocity to add to accented beats
};

// ============================================================================
// MAIN AUDIO PROCESSOR CLASS (JUCE Entry Point)
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
    // OSC CONTROL INTERFACE
    // ============================================================================
    
    void setOSCEnabled(bool enabled);
    bool isOSCEnabled() const;
    void setOSCPort(int port);
    int getOSCPort() const;
    
    // Style parameter control via OSC
    void setSwingRatio(float ratio);
    void setAccentAmount(float amount);
    float getSwingRatio() const;
    float getAccentAmount() const;

private:
    // ============================================================================
    // OSC PROCESSING (NON-REAL-TIME)
    // ============================================================================
    
    void processOSCMessages();
    void handleOSCMessage(const juce::String& address, const juce::var& value);
    
    // ============================================================================
    // REAL-TIME SAFE TRANSFORMATION METHODS
    // ============================================================================
    
    /**
     * Apply swing feel to a MIDI message
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     */
    juce::MidiMessage applySwing(const juce::MidiMessage& inputMessage, 
                                const StyleParameters& style, 
                                double beatsPerMinute, 
                                double sampleRate);
    
    /**
     * Apply accent emphasis to a MIDI message
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     */
    juce::MidiMessage applyAccent(const juce::MidiMessage& inputMessage, 
                                 const StyleParameters& style, 
                                 double beatsPerMinute, 
                                 double sampleRate);
    
    /**
     * Apply all style transformations to a MIDI buffer
     * REAL-TIME SAFE: No memory allocation, locking, or blocking calls
     */
    void applyStyle(juce::MidiBuffer& midiMessages, 
                   const StyleParameters& style, 
                   double beatsPerMinute, 
                   double sampleRate);
    
    // ============================================================================
    // PRIVATE MEMBER VARIABLES
    // ============================================================================
    
    // Current processing state
    double currentBPM = 120.0;
    double currentSampleRate = 44100.0;
    
    // Parameter management (thread-safe)
    juce::AudioProcessorValueTreeState parameters;
    
    // Make parameters accessible to editor
    friend class StyleTransferAudioProcessorEditor;
    
    // Parameter IDs
    static constexpr const char* SWING_RATIO_ID = "swingRatio";
    static constexpr const char* ACCENT_AMOUNT_ID = "accentAmount";
    static constexpr const char* OSC_ENABLED_ID = "oscEnabled";
    static constexpr const char* OSC_PORT_ID = "oscPort";
    
    // OSC state (non-real-time) - will be implemented in next phase
    bool oscEnabled = false;
    int oscPort = 3819;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferAudioProcessor)
};
