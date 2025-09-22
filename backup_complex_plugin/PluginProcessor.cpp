#include "PluginProcessor.h"
#include "PluginEditor.h"

// ============================================================================
// CONSTRUCTOR AND DESTRUCTOR
// ============================================================================

StyleTransferPluginProcessor::StyleTransferPluginProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true))
    , parameters(*this, nullptr, "StyleTransferParameters",
        {
            std::make_unique<juce::AudioParameterFloat>(
                SWING_RATIO_ID, "Swing Ratio", 
                juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f), 0.5f),
            std::make_unique<juce::AudioParameterFloat>(
                ACCENT_AMOUNT_ID, "Accent Amount",
                juce::NormalisableRange<float>(0.0f, 50.0f, 0.1f), 20.0f),
            std::make_unique<juce::AudioParameterFloat>(
                HUMANIZE_TIMING_ID, "Humanize Timing",
                juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f), 0.0f),
            std::make_unique<juce::AudioParameterFloat>(
                HUMANIZE_VELOCITY_ID, "Humanize Velocity",
                juce::NormalisableRange<float>(0.0f, 1.0f, 0.01f), 0.0f),
            std::make_unique<juce::AudioParameterBool>(
                OSC_ENABLED_ID, "OSC Enabled", false),
            std::make_unique<juce::AudioParameterInt>(
                OSC_PORT_ID, "OSC Port",
                1000, 65535, 3819)
        })
{
    // Initialize OSC state from parameters
    oscEnabled = *parameters.getRawParameterValue(OSC_ENABLED_ID);
    oscPort = static_cast<int>(*parameters.getRawParameterValue(OSC_PORT_ID));
    
    // Start OSC listener thread if enabled
    if (oscEnabled)
    {
        startOSCListener();
    }
    
    // Start timer for OSC message processing (30 Hz)
    startTimer(33); // 33ms = ~30 Hz
}

StyleTransferPluginProcessor::~StyleTransferPluginProcessor()
{
    // Stop timer first
    stopTimer();
    
    // Stop OSC listener thread
    stopOSCListener();
}

// ============================================================================
// AUDIO PROCESSOR OVERRIDES
// ============================================================================

void StyleTransferPluginProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    // Initialize the style engine
    styleEngine.prepareToPlay(sampleRate, samplesPerBlock);
    
    // OSC initialization will be added in next step
}

void StyleTransferPluginProcessor::releaseResources()
{
    styleEngine.releaseResources();
    // OSC cleanup will be added in next step
}

void StyleTransferPluginProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    // CRITICAL: OSC processing is now handled by timerCallback()
    // This keeps the audio thread completely real-time safe
    
    // Get current parameters (thread-safe via APVTS)
    StyleParameters currentStyle;
    currentStyle.swingRatio = *parameters.getRawParameterValue(SWING_RATIO_ID);
    currentStyle.accentAmount = *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
    currentStyle.humanizeTimingAmount = *parameters.getRawParameterValue(HUMANIZE_TIMING_ID);
    currentStyle.humanizeVelocityAmount = *parameters.getRawParameterValue(HUMANIZE_VELOCITY_ID);
    
    // Update the style engine
    styleEngine.setStyleParameters(currentStyle);
    
    // Process MIDI through the style engine
    // CRITICAL: This is real-time safe - no allocation, locking, or blocking
    styleEngine.processBlock(buffer, midiMessages);
}

const juce::String StyleTransferPluginProcessor::getName() const
{
    return JucePlugin_Name;
}

bool StyleTransferPluginProcessor::acceptsMidi() const
{
    return true;
}

bool StyleTransferPluginProcessor::producesMidi() const
{
    return true;
}

bool StyleTransferPluginProcessor::isMidiEffect() const
{
    return true;
}

double StyleTransferPluginProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int StyleTransferPluginProcessor::getNumPrograms()
{
    return 1;
}

int StyleTransferPluginProcessor::getCurrentProgram()
{
    return 0;
}

void StyleTransferPluginProcessor::setCurrentProgram(int index)
{
    juce::ignoreUnused(index);
}

const juce::String StyleTransferPluginProcessor::getProgramName(int index)
{
    juce::ignoreUnused(index);
    return "Default";
}

void StyleTransferPluginProcessor::changeProgramName(int index, const juce::String& newName)
{
    juce::ignoreUnused(index, newName);
}

void StyleTransferPluginProcessor::getStateInformation(juce::MemoryBlock& destData)
{
    auto state = parameters.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void StyleTransferPluginProcessor::setStateInformation(const void* data, int sizeInBytes)
{
    std::unique_ptr<juce::XmlElement> xmlState(getXmlFromBinary(data, sizeInBytes));
    if (xmlState.get() != nullptr)
    {
        if (xmlState->hasTagName(parameters.state.getType()))
        {
            parameters.replaceState(juce::ValueTree::fromXml(*xmlState));
        }
    }
}

juce::AudioProcessorEditor* StyleTransferPluginProcessor::createEditor()
{
    return new StyleTransferPluginEditor(*this);
}

bool StyleTransferPluginProcessor::hasEditor() const
{
    return true;
}

// ============================================================================
// OSC CONTROL INTERFACE (Non-Real-Time Thread)
// ============================================================================

void StyleTransferPluginProcessor::setOSCEnabled(bool enabled)
{
    oscEnabled = enabled;
    *parameters.getRawParameterValue(OSC_ENABLED_ID) = enabled;
}

bool StyleTransferPluginProcessor::isOSCEnabled() const
{
    return oscEnabled;
}

void StyleTransferPluginProcessor::setOSCPort(int port)
{
    oscPort = port;
    *parameters.getRawParameterValue(OSC_PORT_ID) = static_cast<float>(port);
}

int StyleTransferPluginProcessor::getOSCPort() const
{
    return oscPort;
}

void StyleTransferPluginProcessor::setSwingRatio(float ratio)
{
    *parameters.getRawParameterValue(SWING_RATIO_ID) = ratio;
}

void StyleTransferPluginProcessor::setAccentAmount(float amount)
{
    *parameters.getRawParameterValue(ACCENT_AMOUNT_ID) = amount;
}

float StyleTransferPluginProcessor::getSwingRatio() const
{
    return *parameters.getRawParameterValue(SWING_RATIO_ID);
}

float StyleTransferPluginProcessor::getAccentAmount() const
{
    return *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
}

void StyleTransferPluginProcessor::setHumanizeTiming(float amount)
{
    *parameters.getRawParameterValue(HUMANIZE_TIMING_ID) = amount;
}

void StyleTransferPluginProcessor::setHumanizeVelocity(float amount)
{
    *parameters.getRawParameterValue(HUMANIZE_VELOCITY_ID) = amount;
}

float StyleTransferPluginProcessor::getHumanizeTiming() const
{
    return *parameters.getRawParameterValue(HUMANIZE_TIMING_ID);
}

float StyleTransferPluginProcessor::getHumanizeVelocity() const
{
    return *parameters.getRawParameterValue(HUMANIZE_VELOCITY_ID);
}

// ============================================================================
// OSC PROCESSING (NON-REAL-TIME THREAD ONLY)
// ============================================================================


void StyleTransferPluginProcessor::handleOSCMessage(const OSCMessage& message)
{
    // CRITICAL: This runs in the non-real-time thread
    // Handle different OSC message types
    
    if (message.address == "/style/swing")
    {
        if (message.value.isDouble())
        {
            float swingRatio = static_cast<float>(message.value);
            setSwingRatio(swingRatio);
        }
    }
    else if (message.address == "/style/accent")
    {
        if (message.value.isDouble())
        {
            float accentAmount = static_cast<float>(message.value);
            setAccentAmount(accentAmount);
        }
    }
    else if (message.address == "/style/enable")
    {
        if (message.value.isBool())
        {
            bool enabled = message.value;
            setOSCEnabled(enabled);
        }
    }
    else if (message.address == "/style/humanizeTiming")
    {
        if (message.value.isDouble())
        {
            float humanizeTiming = static_cast<float>(message.value);
            setHumanizeTiming(humanizeTiming);
        }
    }
    else if (message.address == "/style/humanizeVelocity")
    {
        if (message.value.isDouble())
        {
            float humanizeVelocity = static_cast<float>(message.value);
            setHumanizeVelocity(humanizeVelocity);
        }
    }
}

// ============================================================================
// OSC LISTENER THREAD IMPLEMENTATION
// ============================================================================

void OSCListenerThread::run()
{
    // CRITICAL: This runs on a low-priority background thread
    // Safe to use blocking calls, memory allocation, etc.
    
    while (!threadShouldExit())
    {
        // Check if OSC is enabled
        if (!owner.oscEnabled)
        {
            wait(100); // Wait 100ms before checking again
            continue;
        }
        
        // Try to connect to OSC port
        if (!owner.oscReceiver.isConnected())
        {
            if (owner.oscReceiver.connect(owner.oscPort))
            {
                DBG("OSC Receiver connected to port " << owner.oscPort);
            }
            else
            {
                wait(1000); // Wait 1 second before retrying
                continue;
            }
        }
        
        // Process incoming OSC messages
        owner.oscReceiver.addListener(this);
        
        // Wait for messages with a timeout
        wait(10); // 10ms timeout
    }
    
    // Cleanup
    owner.oscReceiver.removeListener(this);
    if (owner.oscReceiver.isConnected())
    {
        owner.oscReceiver.disconnect();
    }
}

void StyleTransferPluginProcessor::oscMessageReceived(const juce::OSCMessage& message)
{
    // CRITICAL: This runs on the OSC listener thread (non-real-time)
    // Safe to use blocking calls, memory allocation, etc.
    
    // Convert OSC message to our internal format
    OSCMessage internalMessage;
    internalMessage.address = message.getAddressPattern().toString();
    internalMessage.timestamp = juce::Time::getMillisecondCounterHiRes() / 1000.0;
    
    // Extract the first argument (we expect single float arguments)
    if (message.size() > 0)
    {
        if (message[0].isFloat32())
        {
            internalMessage.value = message[0].getFloat32();
        }
        else if (message[0].isInt32())
        {
            internalMessage.value = static_cast<float>(message[0].getInt32());
        }
        else if (message[0].isBool())
        {
            internalMessage.value = message[0].getBool();
        }
    }
    
    // Push message to FIFO queue (thread-safe)
    int index = oscMessageFifo.write(1);
    if (index >= 0 && index < oscMessages.size())
    {
        oscMessages[index] = internalMessage;
    }
}

void StyleTransferPluginProcessor::startOSCListener()
{
    // CRITICAL: This runs on the non-real-time thread
    // Safe to start threads, allocate memory, etc.
    
    if (oscListenerThread == nullptr)
    {
        oscListenerThread = std::make_unique<OSCListenerThread>(*this);
        oscListenerThread->startThread();
        DBG("OSC Listener thread started");
    }
}

void StyleTransferPluginProcessor::stopOSCListener()
{
    // CRITICAL: This runs on the non-real-time thread
    // Safe to stop threads, cleanup resources, etc.
    
    if (oscListenerThread != nullptr)
    {
        oscListenerThread->stopThread(1000); // Wait up to 1 second
        oscListenerThread.reset();
        DBG("OSC Listener thread stopped");
    }
    
    if (oscReceiver.isConnected())
    {
        oscReceiver.disconnect();
    }
}

// ============================================================================
// TIMER CALLBACK (REAL-TIME SAFE)
// ============================================================================

void StyleTransferPluginProcessor::timerCallback()
{
    // CRITICAL: This runs on the message thread (non-real-time)
    // Safe to use setParameterNotifyingHost() and APVTS operations
    // This is the ONLY place where OSC input modifies plugin state
    
    // Process all pending OSC messages from the FIFO queue
    int numMessages = oscMessageFifo.getNumReady();
    for (int i = 0; i < numMessages; ++i)
    {
        int index = oscMessageFifo.read(1);
        if (index >= 0 && index < oscMessages.size())
        {
            const OSCMessage& message = oscMessages[index];
            
            // Update parameters using APVTS (thread-safe)
            if (message.address == "/style/swing")
            {
                if (message.value.isDouble())
                {
                    float swingRatio = static_cast<float>(message.value);
                    // Clamp to valid range
                    swingRatio = juce::jlimit(0.0f, 1.0f, swingRatio);
                    // Use setParameterNotifyingHost to ensure DAW and UI are updated
                    parameters.getParameter(SWING_RATIO_ID)->setValueNotifyingHost(
                        parameters.getParameterRange(SWING_RATIO_ID).convertTo0to1(swingRatio));
                }
            }
            else if (message.address == "/style/accent")
            {
                if (message.value.isDouble())
                {
                    float accentAmount = static_cast<float>(message.value);
                    // Clamp to valid range
                    accentAmount = juce::jlimit(0.0f, 50.0f, accentAmount);
                    // Use setParameterNotifyingHost to ensure DAW and UI are updated
                    parameters.getParameter(ACCENT_AMOUNT_ID)->setValueNotifyingHost(
                        parameters.getParameterRange(ACCENT_AMOUNT_ID).convertTo0to1(accentAmount));
                }
            }
            else if (message.address == "/style/humanizeTiming")
            {
                if (message.value.isDouble())
                {
                    float humanizeTiming = static_cast<float>(message.value);
                    // Clamp to valid range
                    humanizeTiming = juce::jlimit(0.0f, 1.0f, humanizeTiming);
                    // Use setParameterNotifyingHost to ensure DAW and UI are updated
                    parameters.getParameter(HUMANIZE_TIMING_ID)->setValueNotifyingHost(
                        parameters.getParameterRange(HUMANIZE_TIMING_ID).convertTo0to1(humanizeTiming));
                }
            }
            else if (message.address == "/style/humanizeVelocity")
            {
                if (message.value.isDouble())
                {
                    float humanizeVelocity = static_cast<float>(message.value);
                    // Clamp to valid range
                    humanizeVelocity = juce::jlimit(0.0f, 1.0f, humanizeVelocity);
                    // Use setParameterNotifyingHost to ensure DAW and UI are updated
                    parameters.getParameter(HUMANIZE_VELOCITY_ID)->setValueNotifyingHost(
                        parameters.getParameterRange(HUMANIZE_VELOCITY_ID).convertTo0to1(humanizeVelocity));
                }
            }
            else if (message.address == "/style/enable")
            {
                if (message.value.isBool())
                {
                    bool enabled = message.value;
                    // Use setParameterNotifyingHost to ensure DAW and UI are updated
                    parameters.getParameter(OSC_ENABLED_ID)->setValueNotifyingHost(enabled ? 1.0f : 0.0f);
                }
            }
        }
    }
}