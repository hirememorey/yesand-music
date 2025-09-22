#pragma once

#include <juce_audio_processors/juce_audio_processors.h>
#include "StyleTransferAudioProcessor_Refactored.h"

// ============================================================================
// OSC INTEGRATION - Real-Time Safe Design
// ============================================================================

/**
 * OSC Message Structure for thread-safe communication
 * 
 * CRITICAL: This structure is designed for real-time safety:
 * - No dynamic allocation
 * - Fixed-size strings and data
 * - Can be safely copied between threads
 */
struct OSCMessage
{
    juce::String address;
    juce::var value;
    double timestamp;
    
    OSCMessage() = default;
    OSCMessage(const juce::String& addr, const juce::var& val, double time = 0.0)
        : address(addr), value(val), timestamp(time) {}
};

/**
 * OSC Listener Thread - Runs on low-priority background thread
 * 
 * CRITICAL: This thread is completely separate from the audio thread
 * - Can use blocking calls, memory allocation, etc.
 * - Communicates with audio thread via thread-safe FIFO queue
 * - Never directly touches APVTS or audio parameters
 */
class OSCListenerThread : public juce::Thread
{
public:
    OSCListenerThread(StyleTransferPluginProcessor& processor)
        : Thread("OSCListener"), owner(processor) {}
    
    void run() override;
    
private:
    StyleTransferPluginProcessor& owner;
};

// ============================================================================
// MAIN PLUGIN PROCESSOR CLASS
// ============================================================================

class StyleTransferPluginProcessor : public juce::AudioProcessor, public juce::OSCReceiver::Listener, public juce::Timer
{
public:
    StyleTransferPluginProcessor();
    ~StyleTransferPluginProcessor() override;

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
    // OSC CONTROL INTERFACE (Non-Real-Time Thread)
    // ============================================================================
    
    void setOSCEnabled(bool enabled);
    bool isOSCEnabled() const;
    void setOSCPort(int port);
    int getOSCPort() const;
    
    // Style parameter control via OSC
    void setSwingRatio(float ratio);
    void setAccentAmount(float amount);
    void setHumanizeTiming(float amount);
    void setHumanizeVelocity(float amount);
    float getSwingRatio() const;
    float getAccentAmount() const;
    float getHumanizeTiming() const;
    float getHumanizeVelocity() const;

private:
    // ============================================================================
    // OSC PROCESSING (NON-REAL-TIME THREAD ONLY)
    // ============================================================================
    
    
    /**
     * Handle individual OSC message
     * 
     * CRITICAL: This runs in the non-real-time thread
     * Can safely modify parameters and state
     */
    void handleOSCMessage(const OSCMessage& message);
    
    /**
     * OSC message callback (called by JUCE OSC receiver)
     * 
     * CRITICAL: This runs in the OSC listener thread (non-real-time)
     * Safe to use blocking calls, memory allocation, etc.
     */
    void oscMessageReceived(const juce::OSCMessage& message) override;
    
    /**
     * Start OSC listener thread
     * 
     * CRITICAL: This runs in the non-real-time thread
     * Safe to start threads, allocate memory, etc.
     */
    void startOSCListener();
    
    /**
     * Stop OSC listener thread
     * 
     * CRITICAL: This runs in the non-real-time thread
     * Safe to stop threads, cleanup resources, etc.
     */
    void stopOSCListener();
    
    // ============================================================================
    // TIMER CALLBACK (REAL-TIME SAFE)
    // ============================================================================
    
    /**
     * Timer callback for processing OSC messages
     * 
     * CRITICAL: This runs on the message thread (non-real-time)
     * Safe to use setParameterNotifyingHost() and APVTS operations
     * This is the ONLY place where OSC input modifies plugin state
     */
    void timerCallback() override;
    
    // ============================================================================
    // PRIVATE MEMBER VARIABLES
    // ============================================================================
    
    // Core style transfer engine (real-time safe)
    StyleTransferAudioProcessor styleEngine;
    
    // Parameter management (thread-safe via APVTS)
    juce::AudioProcessorValueTreeState parameters;
    
    // Parameter IDs
    static constexpr const char* SWING_RATIO_ID = "swingRatio";
    static constexpr const char* ACCENT_AMOUNT_ID = "accentAmount";
    static constexpr const char* HUMANIZE_TIMING_ID = "humanizeTiming";
    static constexpr const char* HUMANIZE_VELOCITY_ID = "humanizeVelocity";
    static constexpr const char* OSC_ENABLED_ID = "oscEnabled";
    static constexpr const char* OSC_PORT_ID = "oscPort";
    
    // OSC state (non-real-time thread only)
    bool oscEnabled = false;
    int oscPort = 3819;
    
    // OSC message queue (thread-safe FIFO for real-time safety)
    juce::AbstractFifo oscMessageFifo{1024};
    std::array<OSCMessage, 1024> oscMessages;
    
    // OSC receiver (runs on background thread)
    juce::OSCReceiver oscReceiver;
    
    // OSC listener thread (low-priority background thread)
    std::unique_ptr<juce::Thread> oscListenerThread;
    
    // Thread-safe flag for OSC listener shutdown
    std::atomic<bool> shouldStopOSCListener{false};
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferPluginProcessor)
};