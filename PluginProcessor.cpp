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
}

StyleTransferPluginProcessor::~StyleTransferPluginProcessor()
{
    // OSC cleanup will be added in next step
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
    // CRITICAL: Process OSC messages in non-real-time thread
    // This is safe because we're not in the audio thread yet
    processOSCMessages();
    
    // Get current parameters (thread-safe via APVTS)
    StyleParameters currentStyle;
    currentStyle.swingRatio = *parameters.getRawParameterValue(SWING_RATIO_ID);
    currentStyle.accentAmount = *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
    
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

// ============================================================================
// OSC PROCESSING (NON-REAL-TIME THREAD ONLY)
// ============================================================================

void StyleTransferPluginProcessor::processOSCMessages()
{
    // CRITICAL: This runs in the non-real-time thread
    // Process all pending OSC messages from the FIFO queue
    
    int numMessages = oscMessageFifo.getNumReady();
    for (int i = 0; i < numMessages; ++i)
    {
        int index = oscMessageFifo.read(1);
        if (index >= 0 && index < oscMessages.size())
        {
            handleOSCMessage(oscMessages[index]);
        }
    }
}

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
    // Add more OSC message handlers as needed
}