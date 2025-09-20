#pragma once

#include <JuceHeader.h>
#include "StyleTransferAudioProcessor_Refactored.h"

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
    // PRIVATE MEMBER VARIABLES
    // ============================================================================
    
    // Core style transfer engine
    StyleTransferAudioProcessor styleEngine;
    
    // Parameter management (thread-safe)
    juce::AudioProcessorValueTreeState parameters;
    
    // Parameter IDs
    static constexpr const char* SWING_RATIO_ID = "swingRatio";
    static constexpr const char* ACCENT_AMOUNT_ID = "accentAmount";
    static constexpr const char* OSC_ENABLED_ID = "oscEnabled";
    static constexpr const char* OSC_PORT_ID = "oscPort";
    
    // OSC state (non-real-time)
    bool oscEnabled = false;
    int oscPort = 3819;
    
    // OSC message queue (thread-safe FIFO)
    juce::AbstractFifo oscMessageFifo{1024};
    std::array<juce::String, 1024> oscAddresses;
    std::array<juce::var, 1024> oscValues;
    
    // OSC server (will be added in next step)
    // juce::OSCReceiver oscReceiver;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferAudioProcessor)
};
