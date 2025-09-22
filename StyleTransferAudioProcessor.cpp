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
    // Store sample rate for transformation calculations
    currentSampleRate = sampleRate;
    
    // OSC initialization will be added in next step
}

void StyleTransferAudioProcessor::releaseResources()
{
    // Cleanup resources if needed
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
    
    // Process MIDI through the real-time safe transformation algorithms
    // CRITICAL: This is real-time safe - no allocation, locking, or blocking
    applyStyle(midiMessages, currentStyle, currentBPM, currentSampleRate);
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
    // OSC processing will be implemented in next phase
    // For now, this is a placeholder
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

// ============================================================================
// REAL-TIME SAFE TRANSFORMATION METHODS
// ============================================================================

juce::MidiMessage StyleTransferAudioProcessor::applySwing(const juce::MidiMessage& inputMessage, 
                                                          const StyleParameters& style, 
                                                          double beatsPerMinute, 
                                                          double sampleRate)
{
    // CRITICAL: Only process note-on messages, preserve all others unchanged
    if (!inputMessage.isNoteOn()) {
        return inputMessage;
    }
    
    // Calculate position in beats from the message timestamp
    double positionInBeats = inputMessage.getTimeStamp() * (beatsPerMinute / 60.0);
    double beatFraction = positionInBeats - floor(positionInBeats);
    
    // Apply swing only to off-beat notes (8th note positions)
    // Swing ratio: 0.5 = straight, > 0.5 = swing feel
    double swingDelay = 0.0;
    if (beatFraction > 0.4 && beatFraction < 0.6) {
        // Calculate swing delay: (ratio - 0.5) * 0.25 beats
        swingDelay = (style.swingRatio - 0.5) * 0.25;
    }
    
    // Convert beat delay to sample offset
    int delayInSamples = static_cast<int>(swingDelay * sampleRate * 60.0 / beatsPerMinute);
    
    // Create new message with adjusted timestamp
    // CRITICAL: Preserve all original properties except timing
    juce::MidiMessage newMessage = juce::MidiMessage::noteOn(
        inputMessage.getChannel(),
        inputMessage.getNoteNumber(),
        inputMessage.getVelocity()
    );
    
    // Apply the swing delay to the timestamp
    newMessage.setTimeStamp(inputMessage.getTimeStamp() + delayInSamples / sampleRate);
    
    return newMessage;
}

juce::MidiMessage StyleTransferAudioProcessor::applyAccent(const juce::MidiMessage& inputMessage, 
                                                           const StyleParameters& style, 
                                                           double beatsPerMinute, 
                                                           double sampleRate)
{
    // CRITICAL: Only process note-on messages, preserve all others unchanged
    if (!inputMessage.isNoteOn()) {
        return inputMessage;
    }
    
    // Calculate position in beats from the message timestamp
    double positionInBeats = inputMessage.getTimeStamp() * (beatsPerMinute / 60.0);
    double beatFraction = positionInBeats - floor(positionInBeats);
    
    // CRITICAL: Start with original velocity - NEVER overwrite it
    int originalVelocity = inputMessage.getVelocity();
    int newVelocity = originalVelocity;
    
    // Apply accent to down-beat notes (close to integer beat positions)
    if (beatFraction < 0.1 || beatFraction > 0.9) {
        // CRITICAL: MODIFY, don't overwrite - preserve human expression
        newVelocity = originalVelocity + static_cast<int>(style.accentAmount);
    }
    
    // CRITICAL: Clamp to valid MIDI range (0-127)
    newVelocity = juce::jlimit(0, 127, newVelocity);
    
    // Create new message with modified velocity
    // CRITICAL: Preserve all other original properties
    juce::MidiMessage newMessage = juce::MidiMessage::noteOn(
        inputMessage.getChannel(),
        inputMessage.getNoteNumber(),
        static_cast<juce::uint8>(newVelocity)
    );
    
    // Preserve original timestamp
    newMessage.setTimeStamp(inputMessage.getTimeStamp());
    
    return newMessage;
}

void StyleTransferAudioProcessor::applyStyle(juce::MidiBuffer& midiMessages, 
                                           const StyleParameters& style, 
                                           double beatsPerMinute, 
                                           double sampleRate)
{
    juce::MidiBuffer processedBuffer;
    
    for (const auto metadata : midiMessages)
    {
        auto message = metadata.getMessage();
        auto samplePosition = metadata.samplePosition;
        
        // CRITICAL: Process each message through the transformation chain
        // Each function is pure - takes input, returns modified output
        juce::MidiMessage processedMessage = message;
        
        // Apply transformations in sequence
        // ORDER MATTERS: Swing first (rhythmic feel), then accent (dynamic emphasis)
        processedMessage = applySwing(processedMessage, style, beatsPerMinute, sampleRate);
        processedMessage = applyAccent(processedMessage, style, beatsPerMinute, sampleRate);
        
        // Add the processed message to the output buffer
        // Use the processed message's timestamp for proper timing
        processedBuffer.addEvent(processedMessage, 
                                static_cast<int>(processedMessage.getTimeStamp() * sampleRate));
    }
    
    // Replace original buffer with processed messages
    midiMessages.clear();
    midiMessages.addEvents(processedBuffer, 0, -1, 0);
}

// ============================================================================
// JUCE PLUGIN ENTRY POINT
// ============================================================================

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new StyleTransferAudioProcessor();
}
