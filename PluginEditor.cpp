#include "PluginEditor.h"

// ============================================================================
// CONSTRUCTOR AND DESTRUCTOR
// ============================================================================

StyleTransferPluginEditor::StyleTransferPluginEditor(StyleTransferPluginProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p)
{
    // Set editor size
    setSize(400, 300);
    
    // Configure swing ratio slider
    swingRatioSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    swingRatioSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    swingRatioSlider.setRange(0.0, 1.0, 0.01);
    swingRatioSlider.setValue(0.5);
    addAndMakeVisible(swingRatioSlider);
    
    swingRatioLabel.setText("Swing Ratio", juce::dontSendNotification);
    swingRatioLabel.attachToComponent(&swingRatioSlider, false);
    addAndMakeVisible(swingRatioLabel);
    
    // Configure accent amount slider
    accentAmountSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    accentAmountSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    accentAmountSlider.setRange(0.0, 50.0, 0.1);
    accentAmountSlider.setValue(20.0);
    addAndMakeVisible(accentAmountSlider);
    
    accentAmountLabel.setText("Accent Amount", juce::dontSendNotification);
    accentAmountLabel.attachToComponent(&accentAmountSlider, false);
    addAndMakeVisible(accentAmountLabel);
    
    // Configure OSC enabled button
    oscEnabledButton.setButtonText("OSC Enabled");
    addAndMakeVisible(oscEnabledButton);
    
    oscEnabledLabel.setText("OSC Control", juce::dontSendNotification);
    oscEnabledLabel.attachToComponent(&oscEnabledButton, false);
    addAndMakeVisible(oscEnabledLabel);
    
    // Configure OSC port slider
    oscPortSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    oscPortSlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 80, 20);
    oscPortSlider.setRange(1000, 65535, 1);
    oscPortSlider.setValue(3819);
    addAndMakeVisible(oscPortSlider);
    
    oscPortLabel.setText("OSC Port", juce::dontSendNotification);
    oscPortLabel.attachToComponent(&oscPortSlider, false);
    addAndMakeVisible(oscPortLabel);
    
    // Create parameter attachments (thread-safe)
    swingRatioAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "swingRatio", swingRatioSlider);
    accentAmountAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "accentAmount", accentAmountSlider);
    oscEnabledAttachment = std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(
        audioProcessor.parameters, "oscEnabled", oscEnabledButton);
    oscPortAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "oscPort", oscPortSlider);
}

StyleTransferPluginEditor::~StyleTransferPluginEditor()
{
}

// ============================================================================
// PAINT AND RESIZE
// ============================================================================

void StyleTransferPluginEditor::paint(juce::Graphics& g)
{
    g.fillAll(getLookAndFeel().findColour(juce::ResizableWindow::backgroundColourId));
    
    g.setColour(juce::Colours::white);
    g.setFont(15.0f);
    g.drawFittedText("Style Transfer MIDI Effect", getLocalBounds(), juce::Justification::centredTop, 1);
}

void StyleTransferPluginEditor::resized()
{
    auto bounds = getLocalBounds();
    auto sliderHeight = 80;
    auto buttonHeight = 30;
    
    // Title area
    auto titleArea = bounds.removeFromTop(40);
    
    // Swing ratio controls
    auto swingArea = bounds.removeFromTop(sliderHeight);
    swingRatioLabel.setBounds(swingArea.removeFromLeft(100));
    swingRatioSlider.setBounds(swingArea);
    
    // Accent amount controls
    auto accentArea = bounds.removeFromTop(sliderHeight);
    accentAmountLabel.setBounds(accentArea.removeFromLeft(100));
    accentAmountSlider.setBounds(accentArea);
    
    // OSC controls
    auto oscArea = bounds.removeFromTop(buttonHeight + sliderHeight);
    
    // OSC enabled button
    auto oscButtonArea = oscArea.removeFromTop(buttonHeight);
    oscEnabledLabel.setBounds(oscButtonArea.removeFromLeft(100));
    oscEnabledButton.setBounds(oscButtonArea);
    
    // OSC port slider
    auto oscPortArea = oscArea;
    oscPortLabel.setBounds(oscPortArea.removeFromLeft(100));
    oscPortSlider.setBounds(oscPortArea);
}