#pragma once

#include <JuceHeader.h>
#include "StyleTransferAudioProcessor.h"

// ============================================================================
// PLUGIN EDITOR CLASS
// ============================================================================

class StyleTransferAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    StyleTransferAudioProcessorEditor(StyleTransferAudioProcessor&);
    ~StyleTransferAudioProcessorEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    // ============================================================================
    // UI COMPONENTS
    // ============================================================================
    
    StyleTransferAudioProcessor& audioProcessor;
    
    // Parameter sliders
    juce::Slider swingRatioSlider;
    juce::Slider accentAmountSlider;
    juce::ToggleButton oscEnabledButton;
    juce::Slider oscPortSlider;
    
    // Labels
    juce::Label swingRatioLabel;
    juce::Label accentAmountLabel;
    juce::Label oscEnabledLabel;
    juce::Label oscPortLabel;
    
    // Parameter attachments
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> swingRatioAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> accentAmountAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> oscEnabledAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> oscPortAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferAudioProcessorEditor)
};
