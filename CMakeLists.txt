cmake_minimum_required(VERSION 3.15)

project(StyleTransfer VERSION 1.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(PkgConfig REQUIRED)

# Find liblo (Lightweight OSC library) - real-time safe for audio applications
pkg_check_modules(LIBLO REQUIRED liblo)

# Add JUCE as a subdirectory (you'll need to have JUCE in your project)
# Alternative: use find_package if JUCE is installed system-wide
# find_package(JUCE REQUIRED)
add_subdirectory(JUCE)

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${LIBLO_INCLUDE_DIRS})

# Create the plugin target
juce_add_plugin(StyleTransfer
    COMPANY_NAME "Music Cursor"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT TRUE
    IS_MIDI_EFFECT TRUE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE Mcrs
    PLUGIN_CODE StTr
    FORMATS AU VST3
    PRODUCT_NAME "Style Transfer"
)

# Add source files
target_sources(StyleTransfer
    PRIVATE
        StyleTransferAudioProcessor.cpp
        StyleTransferAudioProcessor.h
        StyleTransferAudioProcessorEditor.cpp
        StyleTransferAudioProcessorEditor.h
        PluginProcessor.cpp
        PluginProcessor.h
        PluginEditor.cpp
        PluginEditor.h
)

# Link libraries
target_link_libraries(StyleTransfer
    PRIVATE
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_audio_devices
        juce::juce_audio_formats
        juce::juce_audio_basics
        juce::juce_core
        juce::juce_data_structures
        juce::juce_events
        juce::juce_graphics
        juce::juce_gui_basics
        juce::juce_gui_extra
        ${LIBLO_LIBRARIES}
)

# Compiler definitions
target_compile_definitions(StyleTransfer
    PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
        JucePlugin_Build_VST=0
        JucePlugin_Build_AU=1
        JucePlugin_Build_VST3=1
        JucePlugin_Build_Standalone=0
        JucePlugin_Build_Unity=0
)

# Compiler flags
target_compile_options(StyleTransfer
    PRIVATE
        ${LIBLO_CFLAGS_OTHER}
)

# Linker flags
target_link_options(StyleTransfer
    PRIVATE
        ${LIBLO_LDFLAGS_OTHER}
)

# macOS specific settings
if(APPLE)
    set_target_properties(StyleTransfer PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_BUNDLE_BUNDLE_NAME "Style Transfer"
        MACOSX_BUNDLE_BUNDLE_VERSION "1.0.0"
        MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0.0"
    )
endif()
