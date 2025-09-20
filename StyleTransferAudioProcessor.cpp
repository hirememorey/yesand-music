#include "StyleTransferAudioProcessor.h"
#include "StyleTransferAudioProcessorEditor.h"

// ============================================================================
// CONSTRUCTOR AND DESTRUCTOR
// ============================================================================

StyleTransferAudioProcessor::StyleTransferAudioProcessor()
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

StyleTransferAudioProcessor::~StyleTransferAudioProcessor()
{
    // OSC cleanup will be added in next step
}

// ============================================================================
// AUDIO PROCESSOR OVERRIDES
// ============================================================================

void StyleTransferAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    // Initialize the style engine
    styleEngine.prepareToPlay(sampleRate, samplesPerBlock);
    
    // OSC initialization will be added in next step
}

void StyleTransferAudioProcessor::releaseResources()
{
    styleEngine.releaseResources();
    // OSC cleanup will be added in next step
}

void StyleTransferAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    // CRITICAL: Process OSC messages in non-real-time thread
    // This is safe because we're not in the audio thread yet
    processOSCMessages();
    
    // Get current parameters (thread-safe)
    StyleParameters currentStyle;
    currentStyle.swingRatio = *parameters.getRawParameterValue(SWING_RATIO_ID);
    currentStyle.accentAmount = *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
    
    // Update the style engine
    styleEngine.setStyleParameters(currentStyle);
    
    // Process MIDI through the style engine
    // CRITICAL: This is real-time safe - no allocation, locking, or blocking
    styleEngine.processBlock(buffer, midiMessages);
}

const juce::String StyleTransferAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool StyleTransferAudioProcessor::acceptsMidi() const
{
    return true;
}

bool StyleTransferAudioProcessor::producesMidi() const
{
    return true;
}

bool StyleTransferAudioProcessor::isMidiEffect() const
{
    return true;
}

double StyleTransferAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int StyleTransferAudioProcessor::getNumPrograms()
{
    return 1;
}

int StyleTransferAudioProcessor::getCurrentProgram()
{
    return 0;
}

void StyleTransferAudioProcessor::setCurrentProgram(int index)
{
    juce::ignoreUnused(index);
}

const juce::String StyleTransferAudioProcessor::getProgramName(int index)
{
    juce::ignoreUnused(index);
    return "Default";
}

void StyleTransferAudioProcessor::changeProgramName(int index, const juce::String& newName)
{
    juce::ignoreUnused(index, newName);
}

void StyleTransferAudioProcessor::getStateInformation(juce::MemoryBlock& destData)
{
    auto state = parameters.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void StyleTransferAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
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

juce::AudioProcessorEditor* StyleTransferAudioProcessor::createEditor()
{
    return new StyleTransferAudioProcessorEditor(*this);
}

bool StyleTransferAudioProcessor::hasEditor() const
{
    return true;
}

// ============================================================================
// OSC CONTROL INTERFACE
// ============================================================================

void StyleTransferAudioProcessor::setOSCEnabled(bool enabled)
{
    oscEnabled = enabled;
    *parameters.getRawParameterValue(OSC_ENABLED_ID) = enabled;
}

bool StyleTransferAudioProcessor::isOSCEnabled() const
{
    return oscEnabled;
}

void StyleTransferAudioProcessor::setOSCPort(int port)
{
    oscPort = port;
    *parameters.getRawParameterValue(OSC_PORT_ID) = static_cast<float>(port);
}

int StyleTransferAudioProcessor::getOSCPort() const
{
    return oscPort;
}

void StyleTransferAudioProcessor::setSwingRatio(float ratio)
{
    *parameters.getRawParameterValue(SWING_RATIO_ID) = ratio;
}

void StyleTransferAudioProcessor::setAccentAmount(float amount)
{
    *parameters.getRawParameterValue(ACCENT_AMOUNT_ID) = amount;
}

float StyleTransferAudioProcessor::getSwingRatio() const
{
    return *parameters.getRawParameterValue(SWING_RATIO_ID);
}

float StyleTransferAudioProcessor::getAccentAmount() const
{
    return *parameters.getRawParameterValue(ACCENT_AMOUNT_ID);
}

// ============================================================================
// OSC PROCESSING (NON-REAL-TIME)
// ============================================================================

void StyleTransferAudioProcessor::processOSCMessages()
{
    // CRITICAL: This runs in the non-real-time thread
    // Process all pending OSC messages from the FIFO queue
    
    int numMessages = oscMessageFifo.getNumReady();
    for (int i = 0; i < numMessages; ++i)
    {
        int index = oscMessageFifo.read(1);
        if (index >= 0 && index < oscAddresses.size())
        {
            handleOSCMessage(oscAddresses[index], oscValues[index]);
        }
    }
}

void StyleTransferAudioProcessor::handleOSCMessage(const juce::String& address, const juce::var& value)
{
    // CRITICAL: This runs in the non-real-time thread
    // Handle different OSC message types
    
    if (address == "/style/swing")
    {
        if (value.isDouble())
        {
            float swingRatio = static_cast<float>(value);
            setSwingRatio(swingRatio);
        }
    }
    else if (address == "/style/accent")
    {
        if (value.isDouble())
        {
            float accentAmount = static_cast<float>(value);
            setAccentAmount(accentAmount);
        }
    }
    else if (address == "/style/enable")
    {
        if (value.isBool())
        {
            bool enabled = value;
            setOSCEnabled(enabled);
        }
    }
    // Add more OSC message handlers as needed
}
