#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

// ============================================================================
// PLUGIN EDITOR CLASS
// ============================================================================

class StyleTransferPluginEditor : public juce::AudioProcessorEditor
{
public:
    StyleTransferPluginEditor(StyleTransferPluginProcessor&);
    ~StyleTransferPluginEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    // ============================================================================
    // UI COMPONENTS
    // ============================================================================
    
    StyleTransferPluginProcessor& audioProcessor;
    
    // Parameter sliders - ALL 6 APVTS parameters as sliders
    juce::Slider swingRatioSlider;
    juce::Slider accentAmountSlider;
    juce::Slider humanizeTimingSlider;
    juce::Slider humanizeVelocitySlider;
    juce::Slider oscEnabledSlider;  // Bool as slider (0.0 = false, 1.0 = true)
    juce::Slider oscPortSlider;
    
    // Labels
    juce::Label swingRatioLabel;
    juce::Label accentAmountLabel;
    juce::Label humanizeTimingLabel;
    juce::Label humanizeVelocityLabel;
    juce::Label oscEnabledLabel;
    juce::Label oscPortLabel;
    
    // Parameter attachments (thread-safe) - ALL using SliderAttachment
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> swingRatioAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> accentAmountAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> humanizeTimingAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> humanizeVelocityAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> oscEnabledAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> oscPortAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(StyleTransferPluginEditor)
};