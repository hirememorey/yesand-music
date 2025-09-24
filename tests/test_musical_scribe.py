"""
Test suite for Musical Scribe architecture.

Comprehensive tests for all Musical Scribe components including
project parsing, context analysis, prompt building, and integration.
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import Musical Scribe components
from musical_scribe import (
    ProjectStateParser, MusicalContextEngine, 
    ContextualPromptBuilder, MusicalScribeEngine
)
from musical_scribe.project_state_parser import ProjectState, ProjectInfo, TrackInfo
from musical_scribe.musical_context_engine import MusicalContext
from musical_scribe_integration import MusicalScribeIntegration


class TestProjectStateParser(unittest.TestCase):
    """Test ProjectStateParser functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = ProjectStateParser()
    
    def test_initialization(self):
        """Test parser initialization."""
        self.assertIsInstance(self.parser, ProjectStateParser)
        self.assertIn('ardour', self.parser.supported_daws)
    
    def test_detect_daw_type_ardour_file(self):
        """Test DAW type detection for Ardour file."""
        with tempfile.NamedTemporaryFile(suffix='.ardour', delete=False) as f:
            f.write(b'<ardour>test</ardour>')
            temp_path = f.name
        
        try:
            daw_type = self.parser._detect_daw_type(Path(temp_path))
            self.assertEqual(daw_type, 'ardour')
        finally:
            os.unlink(temp_path)
    
    def test_detect_daw_type_ardour_directory(self):
        """Test DAW type detection for Ardour project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_file = Path(temp_dir) / 'project.ardour'
            project_file.write_text('<ardour>test</ardour>')
            
            daw_type = self.parser._detect_daw_type(Path(temp_dir))
            self.assertEqual(daw_type, 'ardour')
    
    def test_extract_ardour_project_info(self):
        """Test Ardour project info extraction."""
        # Create mock XML element
        import xml.etree.ElementTree as ET
        root = ET.Element('ardour')
        root.set('name', 'Test Project')
        root.set('sample-rate', '48000')
        root.set('bit-depth', '24')
        
        # Add tempo element
        tempo_elem = ET.SubElement(root, 'tempo')
        tempo_elem.set('beats-per-minute', '120')
        
        # Add time signature element
        time_sig_elem = ET.SubElement(root, 'time-signature')
        time_sig_elem.set('numerator', '4')
        time_sig_elem.set('denominator', '4')
        
        project_info = self.parser._extract_ardour_project_info(root)
        
        self.assertEqual(project_info.name, 'Test Project')
        self.assertEqual(project_info.tempo, 120.0)
        self.assertEqual(project_info.time_signature, '4/4')
        self.assertEqual(project_info.sample_rate, 48000)
        self.assertEqual(project_info.bit_depth, 24)
    
    def test_analyze_track_musical_content(self):
        """Test track musical content analysis."""
        regions = [
            {
                'type': 'midi',
                'midi_data': {
                    'notes': [
                        {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
                        {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
                        {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}
                    ]
                },
                'length': 2.0
            }
        ]
        
        analysis = self.parser._analyze_track_musical_content(regions, 'midi')
        
        self.assertTrue(analysis['has_midi_content'])
        self.assertEqual(analysis['note_count'], 3)
        self.assertEqual(analysis['pitch_range']['min'], 60)
        self.assertEqual(analysis['pitch_range']['max'], 67)
        self.assertEqual(analysis['density'], 'medium')


class TestMusicalContextEngine(unittest.TestCase):
    """Test MusicalContextEngine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = MusicalContextEngine()
    
    def test_initialization(self):
        """Test context engine initialization."""
        self.assertIsInstance(self.engine, MusicalContextEngine)
        self.assertIn('jazz', self.engine.genre_indicators)
        self.assertIn('beginner', self.engine.complexity_indicators)
    
    def test_detect_key_signature(self):
        """Test key signature detection."""
        notes = [
            {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},  # C
            {'pitch': 64, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},  # E
            {'pitch': 67, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}   # G
        ]
        
        key = self.engine._detect_key_signature(notes)
        self.assertIsNotNone(key)
    
    def test_detect_chord_progression(self):
        """Test chord progression detection."""
        notes = [
            {'pitch': 60, 'start_time': 0.0, 'duration': 1.0},  # C
            {'pitch': 64, 'start_time': 0.0, 'duration': 1.0},  # E
            {'pitch': 67, 'start_time': 0.0, 'duration': 1.0},  # G
            {'pitch': 57, 'start_time': 1.0, 'duration': 1.0},  # A
            {'pitch': 60, 'start_time': 1.0, 'duration': 1.0},  # C
            {'pitch': 64, 'start_time': 1.0, 'duration': 1.0}   # E
        ]
        
        progression = self.engine._detect_chord_progression(notes)
        self.assertIsInstance(progression, list)
    
    def test_analyze_voice_leading(self):
        """Test voice leading analysis."""
        notes = [
            {'pitch': 60, 'velocity': 80, 'start_time': 0.0, 'duration': 0.5},
            {'pitch': 62, 'velocity': 75, 'start_time': 0.5, 'duration': 0.5},
            {'pitch': 64, 'velocity': 85, 'start_time': 1.0, 'duration': 0.5}
        ]
        
        quality = self.engine._analyze_voice_leading(notes)
        self.assertIn(quality, ['good', 'fair', 'poor'])
    
    def test_detect_primary_genre(self):
        """Test primary genre detection."""
        # Create mock project state
        project_state = Mock()
        project_state.tracks = [
            Mock(name='Jazz Piano'),
            Mock(name='Bass'),
            Mock(name='Drums')
        ]
        
        genre = self.engine._detect_primary_genre(project_state)
        self.assertIsInstance(genre, str)


class TestContextualPromptBuilder(unittest.TestCase):
    """Test ContextualPromptBuilder functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = ContextualPromptBuilder()
    
    def test_initialization(self):
        """Test prompt builder initialization."""
        self.assertIsInstance(self.builder, ContextualPromptBuilder)
        self.assertIn('bassist', self.builder.musical_roles)
        self.assertIn('bassist_enhancement', self.builder.prompt_templates)
    
    def test_determine_musical_role_bass(self):
        """Test musical role determination for bass requests."""
        # Create mock musical context
        musical_context = Mock()
        
        role = self.builder._determine_musical_role("add a funky bassline", musical_context)
        self.assertEqual(role.name, 'Expert Bassist')
    
    def test_determine_musical_role_drums(self):
        """Test musical role determination for drum requests."""
        musical_context = Mock()
        
        role = self.builder._determine_musical_role("add some drums", musical_context)
        self.assertEqual(role.name, 'Expert Drummer')
    
    def test_build_project_context(self):
        """Test project context building."""
        # Create mock project state
        project_state = Mock()
        project_state.project_info = Mock()
        project_state.project_info.name = 'Test Project'
        project_state.project_info.tempo = 120
        project_state.project_info.time_signature = '4/4'
        project_state.project_info.sample_rate = 48000
        project_state.tracks = []
        
        musical_context = Mock()
        musical_context.arrangement_analysis = Mock()
        musical_context.arrangement_analysis.instrumental_balance = {'midi': 0.5, 'audio': 0.5}
        
        context = self.builder._build_project_context(project_state, musical_context)
        
        self.assertIn('Test Project', context)
        self.assertIn('120 BPM', context)
        self.assertIn('4/4', context)
    
    def test_build_musical_analysis(self):
        """Test musical analysis building."""
        # Create mock musical context
        musical_context = Mock()
        musical_context.harmonic_analysis = Mock()
        musical_context.harmonic_analysis.key_signature = 'C major'
        musical_context.harmonic_analysis.harmonic_complexity = 'moderate'
        musical_context.harmonic_analysis.voice_leading_quality = 'good'
        musical_context.harmonic_analysis.dissonance_level = 'low'
        musical_context.harmonic_analysis.harmonic_rhythm = 'medium'
        musical_context.harmonic_analysis.chord_progression = ['C', 'Am', 'F', 'G']
        
        musical_context.rhythmic_analysis = Mock()
        musical_context.rhythmic_analysis.primary_time_signature = '4/4'
        musical_context.rhythmic_analysis.tempo_consistency = 'consistent'
        musical_context.rhythmic_analysis.swing_feel = 'straight'
        musical_context.rhythmic_analysis.syncopation_level = 'medium'
        musical_context.rhythmic_analysis.groove_quality = 'tight'
        musical_context.rhythmic_analysis.rhythmic_density = 'medium'
        
        musical_context.arrangement_analysis = Mock()
        musical_context.arrangement_analysis.overall_density = 'medium'
        musical_context.arrangement_analysis.dynamic_range = 'medium'
        musical_context.arrangement_analysis.frequency_balance = 'balanced'
        musical_context.arrangement_analysis.arrangement_complexity = 'moderate'
        musical_context.arrangement_analysis.section_transitions = 'smooth'
        
        musical_context.style_analysis = Mock()
        musical_context.style_analysis.primary_genre = 'jazz'
        musical_context.style_analysis.secondary_genres = []
        musical_context.style_analysis.production_style = 'live'
        musical_context.style_analysis.complexity_level = 'intermediate'
        musical_context.style_analysis.mood_characteristics = []
        
        musical_context.musical_coherence_score = 0.8
        
        analysis = self.builder._build_musical_analysis(musical_context)
        
        self.assertIn('C major', analysis)
        self.assertIn('moderate', analysis)
        self.assertIn('jazz', analysis)
        self.assertIn('0.8', analysis)


class TestMusicalScribeEngine(unittest.TestCase):
    """Test MusicalScribeEngine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = MusicalScribeEngine()
    
    def test_initialization(self):
        """Test engine initialization."""
        self.assertIsInstance(self.engine, MusicalScribeEngine)
        self.assertIsInstance(self.engine.project_parser, ProjectStateParser)
        self.assertIsInstance(self.engine.context_engine, MusicalContextEngine)
        self.assertIsInstance(self.engine.prompt_builder, ContextualPromptBuilder)
    
    def test_get_supported_daws(self):
        """Test supported DAWs retrieval."""
        daws = self.engine.get_supported_daws()
        self.assertIn('ardour', daws)
        self.assertIsInstance(daws, list)
    
    def test_is_llm_available(self):
        """Test LLM availability check."""
        available = self.engine.is_llm_available()
        self.assertIsInstance(available, bool)
    
    def test_create_basic_bass_pattern(self):
        """Test basic bass pattern creation."""
        pattern = self.engine._create_basic_bass_pattern()
        
        self.assertEqual(pattern.name, "Basic Bass Pattern")
        self.assertEqual(pattern.enhancement_type, "bass_line")
        self.assertGreater(pattern.confidence_score, 0.0)
        self.assertIsInstance(pattern.midi_data, list)
        self.assertGreater(len(pattern.midi_data), 0)
    
    def test_create_basic_drum_pattern(self):
        """Test basic drum pattern creation."""
        pattern = self.engine._create_basic_drum_pattern()
        
        self.assertEqual(pattern.name, "Basic Drum Pattern")
        self.assertEqual(pattern.enhancement_type, "drum_pattern")
        self.assertGreater(pattern.confidence_score, 0.0)
        self.assertIsInstance(pattern.midi_data, list)
        self.assertGreater(len(pattern.midi_data), 0)


class TestMusicalScribeIntegration(unittest.TestCase):
    """Test MusicalScribeIntegration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = MusicalScribeIntegration()
    
    def test_initialization(self):
        """Test integration initialization."""
        self.assertIsInstance(self.integration, MusicalScribeIntegration)
        self.assertIsInstance(self.integration.engine, MusicalScribeEngine)
        self.assertTrue(self.integration.fallback_enabled)
    
    def test_get_system_status(self):
        """Test system status retrieval."""
        status = self.integration.get_system_status()
        
        self.assertIn('musical_scribe_available', status)
        self.assertIn('llm_available', status)
        self.assertIn('supported_daws', status)
        self.assertIn('fallback_enabled', status)
        self.assertTrue(status['musical_scribe_available'])
    
    def test_enable_fallback(self):
        """Test fallback enable/disable."""
        self.integration.enable_fallback(False)
        self.assertFalse(self.integration.fallback_enabled)
        
        self.integration.enable_fallback(True)
        self.assertTrue(self.integration.fallback_enabled)
    
    def test_enable_debug_export(self):
        """Test debug export enable/disable."""
        self.integration.enable_debug_export(False)
        self.assertFalse(self.integration.export_debug_info)
        
        self.integration.enable_debug_export(True)
        self.assertTrue(self.integration.export_debug_info)
    
    def test_set_debug_output_dir(self):
        """Test debug output directory setting."""
        test_dir = "/tmp/test_debug"
        self.integration.set_debug_output_dir(test_dir)
        self.assertEqual(str(self.integration.debug_output_dir), test_dir)


class TestMusicalScribeCommands(unittest.TestCase):
    """Test Musical Scribe command integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        from commands.control_plane import ControlPlane
        self.control_plane = ControlPlane()
    
    def test_musical_scribe_enhance_command_parsing(self):
        """Test Musical Scribe enhance command parsing."""
        from commands.parser import CommandParser
        parser = CommandParser()
        
        command = parser.parse("musical scribe enhance add a funky bassline")
        self.assertIsNotNone(command)
        self.assertEqual(command.type.value, "musical_scribe_enhance")
        self.assertEqual(command.params["user_request"], "add a funky bassline")
    
    def test_musical_scribe_analyze_command_parsing(self):
        """Test Musical Scribe analyze command parsing."""
        from commands.parser import CommandParser
        parser = CommandParser()
        
        command = parser.parse("musical scribe analyze")
        self.assertIsNotNone(command)
        self.assertEqual(command.type.value, "musical_scribe_analyze")
    
    def test_musical_scribe_prompt_command_parsing(self):
        """Test Musical Scribe prompt command parsing."""
        from commands.parser import CommandParser
        parser = CommandParser()
        
        command = parser.parse("musical scribe prompt create a jazz melody")
        self.assertIsNotNone(command)
        self.assertEqual(command.type.value, "musical_scribe_prompt")
        self.assertEqual(command.params["user_request"], "create a jazz melody")
    
    def test_musical_scribe_status_command_parsing(self):
        """Test Musical Scribe status command parsing."""
        from commands.parser import CommandParser
        parser = CommandParser()
        
        command = parser.parse("musical scribe status")
        self.assertIsNotNone(command)
        self.assertEqual(command.type.value, "musical_scribe_status")
    
    def test_help_text_includes_musical_scribe(self):
        """Test that help text includes Musical Scribe commands."""
        from commands.parser import CommandParser
        parser = CommandParser()
        
        help_text = parser.get_help_text()
        self.assertIn("Musical Scribe", help_text)
        self.assertIn("musical scribe enhance", help_text)
        self.assertIn("musical scribe analyze", help_text)
        self.assertIn("musical scribe prompt", help_text)
        self.assertIn("musical scribe status", help_text)


class TestMusicalScribeEndToEnd(unittest.TestCase):
    """End-to-end tests for Musical Scribe functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = MusicalScribeIntegration()
    
    @patch('musical_scribe_integration.MusicalScribeEngine')
    def test_enhance_project_success(self, mock_engine_class):
        """Test successful project enhancement."""
        # Mock the engine and its methods
        mock_engine = Mock()
        mock_engine_class.return_value = mock_engine
        
        # Mock the enhance_music method
        mock_result = Mock()
        mock_result.success = True
        mock_result.patterns = [
            Mock(
                name="Test Pattern",
                description="Test description",
                midi_data=[],
                confidence_score=0.8,
                enhancement_type="bass_line",
                musical_justification="Test justification"
            )
        ]
        mock_result.project_context = "Test context"
        mock_result.musical_analysis = "Test analysis"
        mock_result.enhancement_opportunities = "Test opportunities"
        mock_result.confidence_score = 0.8
        mock_result.error_message = None
        
        mock_engine.enhance_music.return_value = mock_result
        
        # Test enhancement
        result = self.integration.enhance_project("test_project.ardour", "add a bassline")
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['patterns']), 1)
        self.assertEqual(result['patterns'][0]['name'], "Test Pattern")
        self.assertFalse(result.get('fallback_used', False))
    
    @patch('musical_scribe_integration.MusicalScribeEngine')
    def test_enhance_project_failure_with_fallback(self, mock_engine_class):
        """Test project enhancement failure with fallback."""
        # Mock the engine to raise an exception
        mock_engine = Mock()
        mock_engine_class.return_value = mock_engine
        mock_engine.enhance_music.side_effect = Exception("Test error")
        
        # Test enhancement with fallback
        result = self.integration.enhance_project("test_project.ardour", "add a bassline")
        
        # Should use fallback
        self.assertTrue(result.get('fallback_used', False))


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestProjectStateParser,
        TestMusicalContextEngine,
        TestContextualPromptBuilder,
        TestMusicalScribeEngine,
        TestMusicalScribeIntegration,
        TestMusicalScribeCommands,
        TestMusicalScribeEndToEnd
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Musical Scribe Test Results")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    print(f"{'='*50}")
