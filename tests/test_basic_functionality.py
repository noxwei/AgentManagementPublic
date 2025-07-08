#!/usr/bin/env python3
"""
🧪 Basic Functionality Tests
============================

Test suite for the Agent Management System.
Validates core functionality and hybrid personality storage.

Public release version - sanitized for open source distribution.
"""

import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project paths
sys.path.append("../core")
sys.path.append("../agents")

class TestHybridPersonalityLoader(unittest.TestCase):
    """Test the hybrid personality loader functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_personalities_dir = Path(self.temp_dir) / "personalities"
        self.test_personalities_dir.mkdir()
        
        # Create test personality file
        self.test_personality = {
            "detailed_traits": {
                "test_trait": 0.8,
                "another_trait": 0.6
            },
            "response_patterns": {
                "greeting": "Hello from {agent_name}!",
                "analysis": "Analyzing {context}: {findings}"
            },
            "learning_history": [],
            "contextual_memories": []
        }
        
        with open(self.test_personalities_dir / "test_agent_personality.json", 'w') as f:
            json.dump(self.test_personality, f)
    
    @patch('psycopg2.connect')
    def test_load_detailed_personality(self, mock_connect):
        """Test loading personality from JSON file"""
        from hybrid_personality_loader import HybridPersonalityLoader
        
        loader = HybridPersonalityLoader(json_dir=str(self.test_personalities_dir))
        personality = loader.load_detailed_personality("test_agent")
        
        self.assertEqual(personality["detailed_traits"]["test_trait"], 0.8)
        self.assertEqual(personality["response_patterns"]["greeting"], "Hello from {agent_name}!")
    
    @patch('psycopg2.connect')
    def test_load_nonexistent_personality(self, mock_connect):
        """Test loading personality that doesn't exist"""
        from hybrid_personality_loader import HybridPersonalityLoader
        
        loader = HybridPersonalityLoader(json_dir=str(self.test_personalities_dir))
        personality = loader.load_detailed_personality("nonexistent_agent")
        
        self.assertEqual(personality["detailed_traits"], {})
        self.assertEqual(personality["response_patterns"], {})
    
    @patch('psycopg2.connect')
    def test_update_detailed_personality(self, mock_connect):
        """Test updating personality data"""
        from hybrid_personality_loader import HybridPersonalityLoader
        
        loader = HybridPersonalityLoader(json_dir=str(self.test_personalities_dir))
        
        # Update personality
        new_data = {
            "detailed_traits": {
                "new_trait": 0.9
            }
        }
        
        success = loader.update_detailed_personality("test_agent", new_data)
        self.assertTrue(success)
        
        # Verify update
        updated_personality = loader.load_detailed_personality("test_agent")
        self.assertEqual(updated_personality["detailed_traits"]["new_trait"], 0.9)


class TestBaseAgent(unittest.TestCase):
    """Test the base agent functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_personalities_dir = Path(self.temp_dir) / "personalities"
        self.test_personalities_dir.mkdir()
    
    @patch('psycopg2.connect')
    def test_agent_creation(self, mock_connect):
        """Test basic agent creation"""
        # Mock database connection
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        from base_agent import BaseAgent
        
        # Patch the personalities directory
        with patch.object(BaseAgent, 'setup_logging'):
            agent = BaseAgent("test_agent")
            agent.personality_loader.json_dir = self.test_personalities_dir
            
            self.assertEqual(agent.agent_name, "test_agent")
            self.assertIsNotNone(agent.personality)
    
    @patch('psycopg2.connect')
    def test_response_generation(self, mock_connect):
        """Test agent response generation"""
        # Mock database connection
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        from base_agent import BaseAgent
        
        with patch.object(BaseAgent, 'setup_logging'):
            agent = BaseAgent("test_agent")
            agent.personality_loader.json_dir = self.test_personalities_dir
            
            # Test greeting
            greeting = agent.generate_response("Hello", "greeting")
            self.assertIn("test_agent", greeting)
            
            # Test analysis
            analysis = agent.generate_response("test context", "analysis")
            self.assertIn("test context", analysis)
    
    @patch('psycopg2.connect')
    def test_personality_traits(self, mock_connect):
        """Test personality trait access"""
        # Mock database connection
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        from base_agent import BaseAgent
        
        with patch.object(BaseAgent, 'setup_logging'):
            agent = BaseAgent("test_agent")
            agent.personality_loader.json_dir = self.test_personalities_dir
            
            # Test default traits
            helpfulness = agent.get_personality_trait("helpfulness", 0.0)
            self.assertIsInstance(helpfulness, (int, float))
            
            # Test missing trait with default
            missing_trait = agent.get_personality_trait("nonexistent", "default_value")
            self.assertEqual(missing_trait, "default_value")
    
    @patch('psycopg2.connect')
    def test_memory_tracking(self, mock_connect):
        """Test memory tracking functionality"""
        # Mock database connection
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        from base_agent import BaseAgent
        
        with patch.object(BaseAgent, 'setup_logging'):
            agent = BaseAgent("test_agent")
            agent.personality_loader.json_dir = self.test_personalities_dir
            
            # Generate some interactions
            agent.generate_response("test 1", "greeting")
            agent.generate_response("test 2", "analysis") 
            agent.generate_response("test 3", "completion")
            
            # Check memory log
            self.assertEqual(len(agent.memory_log), 3)
            self.assertEqual(agent.daily_interactions, 3)
            
            # Test memory summary
            summary = agent.get_memory_summary()
            self.assertEqual(summary["total_interactions"], 3)
            self.assertIn("greeting", summary["interaction_types"])
    
    @patch('psycopg2.connect')
    def test_human_readable_report(self, mock_connect):
        """Test human-readable memory report generation"""
        # Mock database connection
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        from base_agent import BaseAgent
        
        with patch.object(BaseAgent, 'setup_logging'):
            agent = BaseAgent("test_agent")
            agent.personality_loader.json_dir = self.test_personalities_dir
            
            # Generate report
            report = agent.generate_human_readable_report()
            
            # Verify report contains expected sections
            self.assertIn("test_agent", report)
            self.assertIn("Personality:", report)
            self.assertIn("Recent Activity", report)
            self.assertIn("Relationships:", report)


class TestDatabaseSchema(unittest.TestCase):
    """Test database schema validation"""
    
    def test_schema_file_exists(self):
        """Test that schema file exists and is readable"""
        schema_file = Path("../database/hybrid_personality_schema.sql")
        self.assertTrue(schema_file.exists())
        
        with open(schema_file, 'r') as f:
            content = f.read()
            
        # Check for key tables
        self.assertIn("CREATE TABLE", content)
        self.assertIn("agent_personalities", content)
        self.assertIn("agent_relationships", content)
        self.assertIn("agent_memory_summaries", content)
        
        # Check for views
        self.assertIn("CREATE OR REPLACE VIEW", content)
        self.assertIn("agent_personality_overview", content)
        self.assertIn("agent_relationship_network", content)


class TestPersonalityFiles(unittest.TestCase):
    """Test personality file structure"""
    
    def test_sample_personality_files(self):
        """Test that sample personality files are valid JSON"""
        personalities_dir = Path("../personalities")
        
        if personalities_dir.exists():
            for json_file in personalities_dir.glob("*.json"):
                with open(json_file, 'r') as f:
                    try:
                        personality = json.load(f)
                        
                        # Check required structure
                        self.assertIn("detailed_traits", personality)
                        self.assertIn("response_patterns", personality)
                        self.assertIsInstance(personality["detailed_traits"], dict)
                        self.assertIsInstance(personality["response_patterns"], dict)
                        
                    except json.JSONDecodeError:
                        self.fail(f"Invalid JSON in {json_file}")


class TestExampleFiles(unittest.TestCase):
    """Test example files are executable"""
    
    def test_basic_usage_file_exists(self):
        """Test that basic usage example exists"""
        example_file = Path("../examples/basic_usage.py")
        self.assertTrue(example_file.exists())
        
        with open(example_file, 'r') as f:
            content = f.read()
            
        # Check for key functions
        self.assertIn("def example_1_create_simple_agent", content)
        self.assertIn("def example_2_customize_personality", content)
        self.assertIn("def main", content)


def run_tests():
    """Run all tests with output"""
    print("🧪 Running Agent Management System Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestHybridPersonalityLoader,
        TestBaseAgent,
        TestDatabaseSchema,
        TestPersonalityFiles,
        TestExampleFiles
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)