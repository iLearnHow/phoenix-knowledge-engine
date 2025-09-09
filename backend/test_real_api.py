#!/usr/bin/env python3
"""
Real API Testing Script for Phoenix Knowledge Engine
Tests the system with actual OpenAI API calls
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phoenix.settings')
import django
django.setup()

from core.orchestrator.service import SimplifiedOrchestratorService
from core.worker.service import SimplifiedWorkerService
from core.quality_control.service import SimplifiedQualityControlService
from content.text.generator import TextContentGenerator, generate_lesson_with_avatar
from avatars.service import avatar_service, AvatarType
from monitoring.cost_monitor import cost_monitor


class RealAPITester:
    """Test the Phoenix Knowledge Engine with real API calls"""
    
    def __init__(self):
        self.test_results = []
        self.total_cost = 0.0
        self.start_time = time.time()
        
        # Test topics
        self.test_topics = [
            "The Pythagorean Theorem",
            "Photosynthesis",
            "Supply and Demand",
            "Machine Learning Basics",
            "Climate Change"
        ]
        
        print("🧪 Phoenix Knowledge Engine - Real API Testing")
        print("=" * 60)
    
    def check_environment(self):
        """Check if environment is properly configured"""
        print("🔍 Checking environment configuration...")
        
        # Check OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ ERROR: OpenAI API key not configured!")
            print("   Please set your OpenAI API key in the .env file:")
            print("   OPENAI_API_KEY=sk-your-actual-key-here")
            return False
        
        print(f"✅ OpenAI API key configured: {api_key[:10]}...")
        
        # Check Django settings
        try:
            from django.conf import settings
            print(f"✅ Django settings loaded: {settings.DEBUG}")
        except Exception as e:
            print(f"❌ Django settings error: {e}")
            return False
        
        return True
    
    def test_orchestrator(self, topic: str):
        """Test the orchestrator service"""
        print(f"\n🎯 Testing Orchestrator: {topic}")
        
        try:
            orchestrator = SimplifiedOrchestratorService()
            result = orchestrator.generate_learning_plan(topic)
            
            print(f"✅ Orchestrator success!")
            print(f"   Title: {result['learning_objective']['title']}")
            print(f"   Components: {len(result['knowledge_components_plan'])}")
            
            return {
                'service': 'orchestrator',
                'topic': topic,
                'success': True,
                'result': result
            }
            
        except Exception as e:
            print(f"❌ Orchestrator failed: {e}")
            return {
                'service': 'orchestrator',
                'topic': topic,
                'success': False,
                'error': str(e)
            }
    
    def test_worker(self, topic: str, component_type: str):
        """Test the worker service"""
        print(f"\n🔧 Testing Worker: {component_type} for {topic}")
        
        try:
            worker = SimplifiedWorkerService()
            result = worker.generate_knowledge_component(
                topic, component_type, f"Test {component_type}", 1
            )
            
            if result['success']:
                print(f"✅ Worker success!")
                print(f"   Content: {result['content'][:100]}...")
            else:
                print(f"❌ Worker failed: {result.get('content', 'Unknown error')}")
            
            return {
                'service': 'worker',
                'topic': topic,
                'component_type': component_type,
                'success': result['success'],
                'result': result
            }
            
        except Exception as e:
            print(f"❌ Worker failed: {e}")
            return {
                'service': 'worker',
                'topic': topic,
                'component_type': component_type,
                'success': False,
                'error': str(e)
            }
    
    def test_quality_control(self, content: str, content_type: str, topic: str):
        """Test the quality control service"""
        print(f"\n🛡️ Testing Quality Control: {content_type}")
        
        try:
            qc = SimplifiedQualityControlService()
            result = qc.validate_content(content, content_type, topic)
            
            status = "PASSED" if result['is_valid'] else "FAILED"
            print(f"✅ Quality Control {status}!")
            print(f"   Notes: {result['validation_notes'][:100]}...")
            
            return {
                'service': 'quality_control',
                'content_type': content_type,
                'success': result['success'],
                'is_valid': result['is_valid'],
                'result': result
            }
            
        except Exception as e:
            print(f"❌ Quality Control failed: {e}")
            return {
                'service': 'quality_control',
                'content_type': content_type,
                'success': False,
                'error': str(e)
            }
    
    def test_avatar_system(self, topic: str):
        """Test the avatar system"""
        print(f"\n🎭 Testing Avatar System: {topic}")
        
        try:
            # Test avatar selection
            recommended_avatar = avatar_service.select_avatar_for_topic(topic)
            print(f"   Recommended avatar: {recommended_avatar.value}")
            
            # Test Kelly avatar
            kelly_response = avatar_service.get_avatar_response(
                AvatarType.KELLY, topic, "CORE_CONCEPT"
            )
            print(f"   Kelly system prompt: {len(kelly_response['system_prompt'])} chars")
            
            # Test Ken avatar
            ken_response = avatar_service.get_avatar_response(
                AvatarType.KEN, topic, "CORE_CONCEPT"
            )
            print(f"   Ken system prompt: {len(ken_response['system_prompt'])} chars")
            
            return {
                'service': 'avatar_system',
                'topic': topic,
                'success': True,
                'recommended_avatar': recommended_avatar.value,
                'kelly_response': kelly_response,
                'ken_response': ken_response
            }
            
        except Exception as e:
            print(f"❌ Avatar system failed: {e}")
            return {
                'service': 'avatar_system',
                'topic': topic,
                'success': False,
                'error': str(e)
            }
    
    def test_complete_lesson_generation(self, topic: str, avatar_preference: str = None):
        """Test complete lesson generation"""
        print(f"\n🎓 Testing Complete Lesson Generation: {topic}")
        
        try:
            result = generate_lesson_with_avatar(topic, avatar_preference)
            
            if result['success']:
                print(f"✅ Complete lesson generated!")
                print(f"   Avatar used: {result['avatar_used']}")
                print(f"   Summary: {result['summary']['summary'][:100]}...")
                print(f"   Components: {len(result['components'])}")
                print(f"   Quiz: {'Yes' if result['comprehension_check']['success'] else 'No'}")
            else:
                print(f"❌ Complete lesson failed: {result.get('error', 'Unknown error')}")
            
            return {
                'service': 'complete_lesson',
                'topic': topic,
                'avatar_preference': avatar_preference,
                'success': result['success'],
                'result': result
            }
            
        except Exception as e:
            print(f"❌ Complete lesson failed: {e}")
            return {
                'service': 'complete_lesson',
                'topic': topic,
                'avatar_preference': avatar_preference,
                'success': False,
                'error': str(e)
            }
    
    def test_cost_monitoring(self):
        """Test cost monitoring system"""
        print(f"\n💰 Testing Cost Monitoring System")
        
        try:
            # Track a test API call
            cost_result = cost_monitor.track_api_call(
                "gpt-3.5-turbo", 1000, 500, "test_operation"
            )
            
            print(f"✅ Cost monitoring working!")
            print(f"   Test cost: ${cost_result['cost']:.4f}")
            print(f"   Daily remaining: ${cost_result['daily_remaining']:.2f}")
            print(f"   Monthly remaining: ${cost_result['monthly_remaining']:.2f}")
            
            # Get usage summary
            summary = cost_monitor.get_usage_summary(7)
            print(f"   Total cost (7 days): ${summary['total_cost']:.4f}")
            print(f"   Total calls: {summary['total_calls']}")
            
            return {
                'service': 'cost_monitoring',
                'success': True,
                'cost_result': cost_result,
                'summary': summary
            }
            
        except Exception as e:
            print(f"❌ Cost monitoring failed: {e}")
            return {
                'service': 'cost_monitoring',
                'success': False,
                'error': str(e)
            }
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("\n🚀 Starting Comprehensive Test Suite")
        print("=" * 60)
        
        # Check environment first
        if not self.check_environment():
            print("\n❌ Environment check failed. Please fix configuration and try again.")
            return False
        
        # Test cost monitoring
        self.test_results.append(self.test_cost_monitoring())
        
        # Test with first topic
        test_topic = self.test_topics[0]
        
        # Test orchestrator
        self.test_results.append(self.test_orchestrator(test_topic))
        
        # Test worker with different component types
        component_types = ['CORE_CONCEPT', 'FACT', 'EXAMPLE']
        for component_type in component_types:
            self.test_results.append(self.test_worker(test_topic, component_type))
        
        # Test quality control
        test_content = "This is a test concept about photosynthesis."
        self.test_results.append(self.test_quality_control(test_content, 'CORE_CONCEPT', test_topic))
        
        # Test avatar system
        self.test_results.append(self.test_avatar_system(test_topic))
        
        # Test complete lesson generation
        self.test_results.append(self.test_complete_lesson_generation(test_topic, 'kelly'))
        
        # Test with different avatar
        self.test_results.append(self.test_complete_lesson_generation(test_topic, 'ken'))
        
        return True
    
    def generate_sample_lessons(self, num_lessons: int = 3):
        """Generate sample lessons for demonstration"""
        print(f"\n📚 Generating {num_lessons} Sample Lessons")
        print("=" * 60)
        
        for i, topic in enumerate(self.test_topics[:num_lessons]):
            print(f"\n📖 Lesson {i+1}: {topic}")
            
            # Generate with Kelly
            kelly_result = self.test_complete_lesson_generation(topic, 'kelly')
            self.test_results.append(kelly_result)
            
            # Generate with Ken
            ken_result = self.test_complete_lesson_generation(topic, 'ken')
            self.test_results.append(ken_result)
            
            # Small delay to avoid rate limiting
            time.sleep(2)
    
    def print_summary(self):
        """Print test summary and results"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        # Count results
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result.get('success', False))
        failed_tests = total_tests - successful_tests
        
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🧪 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Cost summary
        summary = cost_monitor.get_usage_summary(1)
        print(f"💰 Total Cost: ${summary['total_cost']:.4f}")
        print(f"📞 API Calls: {summary['total_calls']}")
        
        # Budget status
        budget_status = cost_monitor._check_budget_status()
        print(f"📊 Daily Budget: ${budget_status['daily_cost']:.2f} / ${budget_status['daily_limit']:.2f}")
        print(f"📊 Monthly Budget: ${budget_status['monthly_cost']:.2f} / ${budget_status['monthly_limit']:.2f}")
        
        # Failed tests
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"   - {result['service']}: {result.get('error', 'Unknown error')}")
        
        print("\n🎉 Testing Complete!")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        results_file = "test_results.json"
        
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'duration': time.time() - self.start_time,
            'total_tests': len(self.test_results),
            'successful_tests': sum(1 for r in self.test_results if r.get('success', False)),
            'cost_summary': cost_monitor.get_usage_summary(1),
            'budget_status': cost_monitor._check_budget_status(),
            'test_results': self.test_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")


def main():
    """Main test function"""
    print("🎯 Phoenix Knowledge Engine - Real API Testing")
    print("This will make real API calls and cost money!")
    print("Make sure you have set your OpenAI API key in .env")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Test cancelled.")
        return
    
    # Create tester
    tester = RealAPITester()
    
    # Run tests
    if tester.run_comprehensive_test():
        # Generate sample lessons
        tester.generate_sample_lessons(2)  # Generate 2 lessons to keep costs low
        
        # Print summary
        tester.print_summary()
    else:
        print("❌ Test suite failed to run.")


if __name__ == "__main__":
    main()
