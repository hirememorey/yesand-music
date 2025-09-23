#!/usr/bin/env python3
"""
Test: Musical Conversation System

This script tests the musical conversation system to ensure it's working correctly.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestMusicalConversationEngine(unittest.TestCase):
    """Test the musical conversation engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock OpenAI API key
        os.environ['OPENAI_API_KEY'] = 'test-key'
        
        # Mock the OpenAI client
        with patch('musical_conversation_engine.openai.OpenAI') as mock_openai:
            self.mock_client = Mock()
            mock_openai.return_value = self.mock_client
            
            from musical_conversation_engine import MusicalConversationEngine
            self.engine = MusicalConversationEngine()
    
    def test_initialization(self):
        """Test that the engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.context_manager)
        self.assertIsNotNone(self.engine.reference_library)
    
    def test_reference_library(self):
        """Test the musical reference library"""
        refs = self.engine.reference_library.get_relevant_references("funky bass")
        self.assertGreater(len(refs), 0)
        self.assertTrue(any("Bootsy" in ref.name for ref in refs))
    
    def test_context_management(self):
        """Test musical context management"""
        context = self.engine.context_manager.get_current_context()
        self.assertIsNotNone(context)
        self.assertEqual(context.key, "C")
        self.assertEqual(context.tempo, 120)
    
    @patch('musical_conversation_engine.openai.OpenAI')
    def test_conversation_engagement(self, mock_openai):
        """Test conversation engagement"""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "I'll help you create a funky bass line!"
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create engine with mocked client
        from musical_conversation_engine import MusicalConversationEngine
        engine = MusicalConversationEngine()
        
        # Test conversation
        response = engine.engage("I need a funky bass line")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.message, "I'll help you create a funky bass line!")

class TestIterativeMusicalWorkflow(unittest.TestCase):
    """Test the iterative musical workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock dependencies
        with patch('iterative_musical_workflow.MusicalConversationEngine') as mock_conv_engine, \
             patch('iterative_musical_workflow.ControlPlane') as mock_control_plane:
            
            self.mock_conv_engine = Mock()
            self.mock_control_plane = Mock()
            
            from iterative_musical_workflow import IterativeMusicalWorkflow
            self.workflow = IterativeMusicalWorkflow(self.mock_conv_engine, self.mock_control_plane)
    
    def test_project_creation(self):
        """Test project creation"""
        project = self.workflow.start_new_project("Test Project")
        
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(len(project.iterations), 0)
    
    def test_feedback_classification(self):
        """Test feedback classification"""
        # Test different types of feedback
        test_cases = [
            ("Make it more complex", "too_simple"),
            ("This is too busy", "too_complex"),
            ("Make it jazzier", "wrong_style"),
            ("Make it faster", "wrong_tempo"),
            ("Make it brighter", "brighter"),
            ("Make it darker", "darker")
        ]
        
        for feedback, expected_type in test_cases:
            classified_type = self.workflow._classify_feedback(feedback)
            self.assertEqual(classified_type, expected_type)
    
    def test_pattern_generation(self):
        """Test pattern generation"""
        # Mock the workflow's current project
        self.workflow.current_project = Mock()
        self.workflow.current_project.context = Mock()
        self.workflow.current_project.context.key = "C"
        self.workflow.current_project.context.tempo = 120
        self.workflow.current_project.generated_files = []
        
        # Test bass pattern generation
        action = {
            "action": "generate_pattern",
            "parameters": {"type": "bass", "style": "funk"}
        }
        
        result = self.workflow._generate_musical_content(action)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "pattern")
        self.assertEqual(result["pattern_type"], "bass")
        self.assertEqual(result["style"], "funk")

class TestEnhancedControlPlane(unittest.TestCase):
    """Test the enhanced control plane"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock all dependencies
        with patch('enhanced_control_plane.ControlPlane.__init__') as mock_super_init, \
             patch('enhanced_control_plane.MusicalConversationEngine') as mock_conv_engine, \
             patch('enhanced_control_plane.IterativeMusicalWorkflow') as mock_workflow:
            
            mock_super_init.return_value = None
            self.mock_conv_engine = Mock()
            self.mock_workflow = Mock()
            
            from enhanced_control_plane import EnhancedControlPlane
            self.enhanced_cp = EnhancedControlPlane()
    
    def test_initialization(self):
        """Test enhanced control plane initialization"""
        self.assertIsNotNone(self.enhanced_cp)
        self.assertIsNotNone(self.enhanced_cp.conversation_engine)
        self.assertIsNotNone(self.enhanced_cp.workflow)
    
    def test_conversation_mode_commands(self):
        """Test conversation mode commands"""
        # Test start conversation
        response = self.enhanced_cp.execute("start conversation")
        self.assertIn("Conversation mode started", response)
        
        # Test stop conversation
        response = self.enhanced_cp.execute("stop conversation")
        self.assertIn("Conversation mode stopped", response)
        
        # Test project status
        response = self.enhanced_cp.execute("project status")
        self.assertIsNotNone(response)
    
    def test_enhanced_help(self):
        """Test enhanced help functionality"""
        help_text = self.enhanced_cp.get_enhanced_help()
        
        self.assertIn("CONVERSATIONAL AI FEATURES", help_text)
        self.assertIn("start conversation", help_text)
        self.assertIn("Musical references", help_text)

class TestIntegration(unittest.TestCase):
    """Test integration between components"""
    
    def test_imports(self):
        """Test that all modules can be imported"""
        try:
            from musical_conversation_engine import MusicalConversationEngine
            from iterative_musical_workflow import IterativeMusicalWorkflow
            from enhanced_control_plane import EnhancedControlPlane
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")
    
    def test_dependencies(self):
        """Test that required dependencies are available"""
        try:
            import openai
            self.assertTrue(True)
        except ImportError:
            self.fail("OpenAI library not installed. Run: pip install openai")
    
    def test_configuration(self):
        """Test configuration and environment setup"""
        # Test that we can create a conversation engine (with mocked API key)
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            try:
                from musical_conversation_engine import MusicalConversationEngine
                engine = MusicalConversationEngine()
                self.assertIsNotNone(engine)
            except Exception as e:
                self.fail(f"Failed to create conversation engine: {e}")

def run_tests():
    """Run all tests"""
    print("🧪 Running Musical Conversation System Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestMusicalConversationEngine))
    test_suite.addTest(unittest.makeSuite(TestIterativeMusicalWorkflow))
    test_suite.addTest(unittest.makeSuite(TestEnhancedControlPlane))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
