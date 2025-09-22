#include "PluginEditor.h"

// ============================================================================
// CONSTRUCTOR AND DESTRUCTOR
// ============================================================================

StyleTransferPluginEditor::StyleTransferPluginEditor(StyleTransferPluginProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p)
{
    // Set editor size - increased to accommodate 6 sliders
    setSize(500, 400);
    
    // ============================================================================
    // SWING RATIO SLIDER (0.0 - 1.0, 0.01 step)
    // ============================================================================
    swingRatioSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    swingRatioSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    swingRatioSlider.setRange(0.0, 1.0, 0.01);
    swingRatioSlider.setValue(0.5);
    addAndMakeVisible(swingRatioSlider);
    
    swingRatioLabel.setText("Swing Ratio", juce::dontSendNotification);
    swingRatioLabel.attachToComponent(&swingRatioSlider, false);
    addAndMakeVisible(swingRatioLabel);
    
    // ============================================================================
    // ACCENT AMOUNT SLIDER (0.0 - 50.0, 0.1 step)
    // ============================================================================
    accentAmountSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    accentAmountSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    accentAmountSlider.setRange(0.0, 50.0, 0.1);
    accentAmountSlider.setValue(20.0);
    addAndMakeVisible(accentAmountSlider);
    
    accentAmountLabel.setText("Accent Amount", juce::dontSendNotification);
    accentAmountLabel.attachToComponent(&accentAmountSlider, false);
    addAndMakeVisible(accentAmountLabel);
    
    // ============================================================================
    // HUMANIZE TIMING SLIDER (0.0 - 1.0, 0.01 step)
    // ============================================================================
    humanizeTimingSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    humanizeTimingSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    humanizeTimingSlider.setRange(0.0, 1.0, 0.01);
    humanizeTimingSlider.setValue(0.0);
    addAndMakeVisible(humanizeTimingSlider);
    
    humanizeTimingLabel.setText("Humanize Timing", juce::dontSendNotification);
    humanizeTimingLabel.attachToComponent(&humanizeTimingSlider, false);
    addAndMakeVisible(humanizeTimingLabel);
    
    // ============================================================================
    // HUMANIZE VELOCITY SLIDER (0.0 - 1.0, 0.01 step)
    // ============================================================================
    humanizeVelocitySlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    humanizeVelocitySlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    humanizeVelocitySlider.setRange(0.0, 1.0, 0.01);
    humanizeVelocitySlider.setValue(0.0);
    addAndMakeVisible(humanizeVelocitySlider);
    
    humanizeVelocityLabel.setText("Humanize Velocity", juce::dontSendNotification);
    humanizeVelocityLabel.attachToComponent(&humanizeVelocitySlider, false);
    addAndMakeVisible(humanizeVelocityLabel);
    
    // ============================================================================
    // OSC ENABLED SLIDER (0.0 = false, 1.0 = true)
    // ============================================================================
    oscEnabledSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    oscEnabledSlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 80, 20);
    oscEnabledSlider.setRange(0.0, 1.0, 1.0);  // Only 0.0 and 1.0 values
    oscEnabledSlider.setValue(0.0);
    addAndMakeVisible(oscEnabledSlider);
    
    oscEnabledLabel.setText("OSC Enabled", juce::dontSendNotification);
    oscEnabledLabel.attachToComponent(&oscEnabledSlider, false);
    addAndMakeVisible(oscEnabledLabel);
    
    // ============================================================================
    // OSC PORT SLIDER (1000 - 65535, 1 step)
    // ============================================================================
    oscPortSlider.setSliderStyle(juce::Slider::LinearHorizontal);
    oscPortSlider.setTextBoxStyle(juce::Slider::TextBoxRight, false, 80, 20);
    oscPortSlider.setRange(1000, 65535, 1);
    oscPortSlider.setValue(3819);
    addAndMakeVisible(oscPortSlider);
    
    oscPortLabel.setText("OSC Port", juce::dontSendNotification);
    oscPortLabel.attachToComponent(&oscPortSlider, false);
    addAndMakeVisible(oscPortLabel);
    
    // ============================================================================
    // PARAMETER ATTACHMENTS (THREAD-SAFE) - ALL using SliderAttachment
    // ============================================================================
    swingRatioAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "swingRatio", swingRatioSlider);
    accentAmountAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "accentAmount", accentAmountSlider);
    humanizeTimingAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "humanizeTiming", humanizeTimingSlider);
    humanizeVelocityAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "humanizeVelocity", humanizeVelocitySlider);
    oscEnabledAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.parameters, "oscEnabled", oscEnabledSlider);
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
    auto rotarySliderHeight = 80;
    auto linearSliderHeight = 40;
    auto titleHeight = 40;
    
    // Title area
    auto titleArea = bounds.removeFromTop(titleHeight);
    
    // ============================================================================
    // ROW 1: Swing Ratio and Accent Amount (rotary sliders)
    // ============================================================================
    auto row1 = bounds.removeFromTop(rotarySliderHeight);
    auto swingArea = row1.removeFromLeft(bounds.getWidth() / 2);
    auto accentArea = row1;
    
    swingRatioLabel.setBounds(swingArea.removeFromLeft(120));
    swingRatioSlider.setBounds(swingArea);
    
    accentAmountLabel.setBounds(accentArea.removeFromLeft(120));
    accentAmountSlider.setBounds(accentArea);
    
    // ============================================================================
    // ROW 2: Humanize Timing and Humanize Velocity (rotary sliders)
    // ============================================================================
    auto row2 = bounds.removeFromTop(rotarySliderHeight);
    auto humanizeTimingArea = row2.removeFromLeft(bounds.getWidth() / 2);
    auto humanizeVelocityArea = row2;
    
    humanizeTimingLabel.setBounds(humanizeTimingArea.removeFromLeft(120));
    humanizeTimingSlider.setBounds(humanizeTimingArea);
    
    humanizeVelocityLabel.setBounds(humanizeVelocityArea.removeFromLeft(120));
    humanizeVelocitySlider.setBounds(humanizeVelocityArea);
    
    // ============================================================================
    // ROW 3: OSC Enabled and OSC Port (linear sliders)
    // ============================================================================
    auto row3 = bounds.removeFromTop(linearSliderHeight);
    auto oscEnabledArea = row3.removeFromLeft(bounds.getWidth() / 2);
    auto oscPortArea = row3;
    
    oscEnabledLabel.setBounds(oscEnabledArea.removeFromLeft(120));
    oscEnabledSlider.setBounds(oscEnabledArea);
    
    oscPortLabel.setBounds(oscPortArea.removeFromLeft(120));
    oscPortSlider.setBounds(oscPortArea);
}