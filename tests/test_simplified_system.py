"""
Test Suite for Simplified Phoenix Knowledge Engine
Comprehensive testing for the MVP system
"""

import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.conf import settings

from core.orchestrator.service import SimplifiedOrchestratorService
from core.worker.service import SimplifiedWorkerService
from core.quality_control.service import SimplifiedQualityControlService
from content.text.generator import TextContentGenerator
from avatars.service import avatar_service, AvatarType
from monitoring.cost_monitor import CostMonitor


class TestSimplifiedOrchestrator(TestCase):
    """Test the simplified orchestrator service"""
    
    def setUp(self):
        self.orchestrator = SimplifiedOrchestratorService()
    
    @patch('services.local_llm.get_llm_service')
    def test_generate_learning_plan(self, mock_get_llm):
        """Test learning plan generation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
          "learning_objective": {
            "title": "Test Topic",
            "core_question": "What is this about?",
            "summary": "A test topic for learning"
          },
          "knowledge_components_plan": [
            {"type": "CORE_CONCEPT", "purpose": "Define the concept", "sort_order": 1}
          ],
          "comprehension_check_plan": {
            "question_type": "multiple_choice",
            "purpose": "Test understanding"
          }
        }
        '''
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.orchestrator.generate_learning_plan("Test Topic")
        
        self.assertIn('learning_objective', result)
        self.assertIn('knowledge_components_plan', result)
        self.assertIn('comprehension_check_plan', result)
        self.assertEqual(result['learning_objective']['title'], 'Test Topic')


class TestSimplifiedWorker(TestCase):
    """Test the simplified worker service"""
    
    def setUp(self):
        self.worker = SimplifiedWorkerService()
    
    @patch('services.local_llm.get_llm_service')
    def test_generate_knowledge_component(self, mock_get_llm):
        """Test knowledge component generation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test concept explanation."
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.worker.generate_knowledge_component(
            "Test Topic", "CORE_CONCEPT", "Define the concept", 1
        )
        
        self.assertTrue(result['success'])
        self.assertIn('content', result)
        self.assertEqual(result['content'], "This is a test concept explanation.")
    
    @patch('services.local_llm.get_llm_service')
    def test_generate_comprehension_check(self, mock_get_llm):
        """Test comprehension check generation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
          "question_text": "What is the main concept?",
          "options": ["A", "B", "C", "D"],
          "correct_index": 0,
          "explanation": "A is correct because..."
        }
        '''
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.worker.generate_comprehension_check(
            "Test Topic", "Test understanding"
        )
        
        self.assertTrue(result['success'])
        self.assertIn('quiz_data', result)
        self.assertEqual(result['quiz_data']['question_text'], "What is the main concept?")


class TestSimplifiedQualityControl(TestCase):
    """Test the simplified quality control service"""
    
    def setUp(self):
        self.qc = SimplifiedQualityControlService()
    
    @patch('services.local_llm.get_llm_service')
    def test_validate_content(self, mock_get_llm):
        """Test content validation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "VALID"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.qc.validate_content(
            "This is test content", "CORE_CONCEPT", "Test Topic"
        )
        
        self.assertTrue(result['is_valid'])
        self.assertTrue(result['success'])
    
    @patch('services.local_llm.get_llm_service')
    def test_validate_content_invalid(self, mock_get_llm):
        """Test content validation with invalid content"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "INVALID: Contains errors"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.qc.validate_content(
            "This is invalid content", "CORE_CONCEPT", "Test Topic"
        )
        
        self.assertFalse(result['is_valid'])
        self.assertTrue(result['success'])


class TestAvatarService(TestCase):
    """Test the avatar service"""
    
    def test_get_avatar(self):
        """Test getting avatar by type"""
        kelly = avatar_service.get_avatar(AvatarType.KELLY)
        ken = avatar_service.get_avatar(AvatarType.KEN)
        
        self.assertIsNotNone(kelly)
        self.assertIsNotNone(ken)
        self.assertEqual(kelly.name, "Kelly")
        self.assertEqual(ken.name, "Ken")
    
    def test_select_avatar_for_topic(self):
        """Test avatar selection based on topic"""
        # Academic topic should select Kelly
        academic_topic = "mathematics"
        avatar = avatar_service.select_avatar_for_topic(academic_topic)
        self.assertEqual(avatar, AvatarType.KELLY)
        
        # Practical topic should select Ken
        practical_topic = "programming"
        avatar = avatar_service.select_avatar_for_topic(practical_topic)
        self.assertEqual(avatar, AvatarType.KEN)
        
        # Default topic should select Kelly
        default_topic = "general knowledge"
        avatar = avatar_service.select_avatar_for_topic(default_topic)
        self.assertEqual(avatar, AvatarType.KELLY)
    
    def test_get_avatar_response(self):
        """Test getting avatar response"""
        response = avatar_service.get_avatar_response(
            AvatarType.KELLY, "Test Topic", "CORE_CONCEPT"
        )
        
        self.assertIn('avatar_name', response)
        self.assertIn('system_prompt', response)
        self.assertIn('prompt_modifier', response)
        self.assertEqual(response['avatar_name'], 'Kelly')


class TestTextContentGenerator(TestCase):
    """Test the text content generator"""
    
    def setUp(self):
        self.generator = TextContentGenerator()
    
    @patch('services.local_llm.get_llm_service')
    def test_generate_learning_objective_summary(self, mock_get_llm):
        """Test learning objective summary generation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test summary."
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.generator.generate_learning_objective_summary(
            "Test Topic", AvatarType.KELLY
        )
        
        self.assertTrue(result['success'])
        self.assertIn('summary', result)
        self.assertEqual(result['avatar_used'], 'Kelly')
    
    @patch('services.local_llm.get_llm_service')
    def test_generate_knowledge_component(self, mock_get_llm):
        """Test knowledge component generation"""
        # Mock the LLM response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test component."
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_llm.return_value = mock_client
        
        result = self.generator.generate_knowledge_component(
            "Test Topic", "CORE_CONCEPT", "Define the concept", AvatarType.KELLY
        )
        
        self.assertTrue(result['success'])
        self.assertIn('content', result)
        self.assertEqual(result['component_type'], 'CORE_CONCEPT')


class TestCostMonitor(TestCase):
    """Test the cost monitoring system"""
    
    def setUp(self):
        self.monitor = CostMonitor()
    
    def test_track_api_call(self):
        """Test API call tracking"""
        result = self.monitor.track_api_call(
            "gpt-3.5-turbo", 1000, 500, "test_operation"
        )
        
        self.assertIn('cost', result)
        self.assertIn('budget_status', result)
        self.assertGreater(result['cost'], 0)
    
    def test_budget_status(self):
        """Test budget status checking"""
        # Track a call to generate some cost
        self.monitor.track_api_call("gpt-3.5-turbo", 1000, 500, "test")
        
        status = self.monitor._check_budget_status()
        
        self.assertIn('daily_cost', status)
        self.assertIn('monthly_cost', status)
        self.assertIn('daily_limit', status)
        self.assertIn('monthly_limit', status)
    
    def test_usage_summary(self):
        """Test usage summary generation"""
        # Track some calls
        self.monitor.track_api_call("gpt-3.5-turbo", 1000, 500, "test1")
        self.monitor.track_api_call("gpt-3.5-turbo", 2000, 1000, "test2")
        
        summary = self.monitor.get_usage_summary(7)
        
        self.assertIn('total_cost', summary)
        self.assertIn('total_calls', summary)
        self.assertIn('daily_breakdown', summary)
        self.assertGreater(summary['total_cost'], 0)
        self.assertGreater(summary['total_calls'], 0)


class TestIntegration(TestCase):
    """Integration tests for the complete system"""
    
    @patch('services.local_llm.get_llm_service')
    def test_complete_content_generation_flow(self, mock_get_llm):
        """Test the complete content generation flow"""
        # Mock the LLM responses
        mock_client = MagicMock()
        
        # Mock orchestrator response
        orchestrator_response = MagicMock()
        orchestrator_response.choices[0].message.content = '''
        {
          "learning_objective": {
            "title": "Integration Test Topic",
            "core_question": "What is this about?",
            "summary": "A test topic for integration testing"
          },
          "knowledge_components_plan": [
            {"type": "CORE_CONCEPT", "purpose": "Define the concept", "sort_order": 1}
          ],
          "comprehension_check_plan": {
            "question_type": "multiple_choice",
            "purpose": "Test understanding"
          }
        }
        '''
        
        # Mock worker responses
        worker_response = MagicMock()
        worker_response.choices[0].message.content = "This is test content."
        
        # Mock quality control response
        qc_response = MagicMock()
        qc_response.choices[0].message.content = "VALID"
        
        # Set up mock to return different responses based on call
        def mock_create(*args, **kwargs):
            messages = args[1]['messages']
            if 'orchestrator' in str(messages):
                return orchestrator_response
            elif 'quality control' in str(messages):
                return qc_response
            else:
                return worker_response
        
        mock_client.chat.completions.create.side_effect = mock_create
        mock_get_llm.return_value = mock_client
        
        # Test the complete flow
        from content.text.generator import generate_lesson_with_avatar
        
        result = generate_lesson_with_avatar("Integration Test Topic")
        
        self.assertTrue(result['success'])
        self.assertIn('summary', result)
        self.assertIn('components', result)
        self.assertIn('comprehension_check', result)


if __name__ == '__main__':
    unittest.main()
