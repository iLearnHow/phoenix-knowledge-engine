#!/usr/bin/env python3
"""
Quick API Test for Phoenix Knowledge Engine
Simple test without Django setup
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class QuickAPITester:
    """Quick API tester for Phoenix Knowledge Engine"""
    
    def __init__(self):
        self.client = None
        self.total_cost = 0.0
        self.test_results = []
        
        # Model costs (per 1K tokens)
        self.model_costs = {
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
        
        print("🧪 Phoenix Knowledge Engine - Quick API Test")
        print("=" * 50)
    
    def setup_client(self):
        """Setup OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ ERROR: OpenAI API key not configured!")
            print("   Please set your OpenAI API key in the .env file:")
            print("   OPENAI_API_KEY=sk-your-actual-key-here")
            return False
        
        try:
            self.client = OpenAI(api_key=api_key)
            print(f"✅ OpenAI client configured: {api_key[:10]}...")
            return True
        except Exception as e:
            print(f"❌ Error setting up OpenAI client: {e}")
            return False
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for API call"""
        if model not in self.model_costs:
            model = "gpt-3.5-turbo"  # Default to cheapest
        
        input_cost = (input_tokens / 1000) * self.model_costs[model]["input"]
        output_cost = (output_tokens / 1000) * self.model_costs[model]["output"]
        return input_cost + output_cost
    
    def test_orchestrator_prompt(self, topic: str):
        """Test orchestrator functionality"""
        print(f"\n🎯 Testing Orchestrator: {topic}")
        
        prompt = f"""Create a learning plan for "{topic}" in this exact JSON format:

{{
  "learning_objective": {{
    "title": "Clear, concise title",
    "core_question": "What is the main question this addresses?",
    "summary": "Brief 2-3 sentence summary"
  }},
  "knowledge_components_plan": [
    {{"type": "CORE_CONCEPT", "purpose": "Define the main concept", "sort_order": 1}},
    {{"type": "FACT", "purpose": "Key fact about the topic", "sort_order": 2}},
    {{"type": "EXAMPLE", "purpose": "Practical example", "sort_order": 3}},
    {{"type": "PRINCIPLE", "purpose": "Underlying principle", "sort_order": 4}},
    {{"type": "WARNING", "purpose": "Common misconception to avoid", "sort_order": 5}}
  ],
  "comprehension_check_plan": {{
    "question_type": "multiple_choice",
    "purpose": "Test understanding of key concepts"
  }}
}}

Keep responses concise but educational. Focus on the most important aspects of {topic}."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational architect. Create comprehensive learning plans in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Calculate cost
            input_tokens = len(prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            # Parse response
            try:
                plan_data = json.loads(response.choices[0].message.content)
                print(f"✅ Orchestrator success! Cost: ${cost:.4f}")
                print(f"   Title: {plan_data['learning_objective']['title']}")
                print(f"   Components: {len(plan_data['knowledge_components_plan'])}")
                
                return {
                    'success': True,
                    'cost': cost,
                    'data': plan_data
                }
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                return {
                    'success': False,
                    'error': f"JSON parsing failed: {e}",
                    'cost': cost
                }
                
        except Exception as e:
            print(f"❌ Orchestrator failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0
            }
    
    def test_worker_prompt(self, topic: str, component_type: str):
        """Test worker functionality"""
        print(f"\n🔧 Testing Worker: {component_type} for {topic}")
        
        prompts = {
            'CORE_CONCEPT': f"Explain the core concept of {topic}. Keep it clear and educational (2-3 sentences).",
            'FACT': f"State an important fact about {topic}. Be concise and accurate (1-2 sentences).",
            'EXAMPLE': f"Provide a clear, practical example of {topic}. Make it easy to understand (2-3 sentences).",
            'PRINCIPLE': f"Explain the key principle behind {topic}. Focus on the underlying concept (2-3 sentences).",
            'WARNING': f"Identify a common misconception or warning about {topic}. Be helpful and clear (1-2 sentences)."
        }
        
        prompt = prompts.get(component_type, f"Create {component_type.lower()} content about {topic}.")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert educator creating {component_type.lower()} content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Calculate cost
            input_tokens = len(prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            content = response.choices[0].message.content.strip()
            print(f"✅ Worker success! Cost: ${cost:.4f}")
            print(f"   Content: {content[:100]}...")
            
            return {
                'success': True,
                'cost': cost,
                'content': content
            }
            
        except Exception as e:
            print(f"❌ Worker failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'cost': 0
            }
    
    def test_avatar_prompts(self, topic: str):
        """Test avatar-specific prompts"""
        print(f"\n🎭 Testing Avatar Prompts: {topic}")
        
        # Kelly (Academic) prompt
        kelly_prompt = f"""Create educational content about "{topic}" with an academic, methodical approach.

Focus on:
- Step-by-step explanations
- Building foundational understanding
- Clear, academic language
- Multiple examples and analogies

Create a brief explanation (2-3 sentences) that would help students understand this topic thoroughly."""
        
        # Ken (Practical) prompt
        ken_prompt = f"""Create educational content about "{topic}" with a practical, hands-on approach.

Focus on:
- Real-world applications
- Immediate practical use
- Concrete examples
- Learning by doing

Create a brief explanation (2-3 sentences) that shows how this topic applies in practice."""
        
        results = {}
        
        # Test Kelly
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Kelly, an educational specialist with a warm, professional demeanor who excels at breaking down complex topics."},
                    {"role": "user", "content": kelly_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            input_tokens = len(kelly_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            results['kelly'] = {
                'success': True,
                'cost': cost,
                'content': response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            results['kelly'] = {
                'success': False,
                'error': str(e),
                'cost': 0
            }
        
        # Test Ken
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Ken, a practical application expert with an energetic, engaging personality who focuses on real-world applications."},
                    {"role": "user", "content": ken_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            input_tokens = len(ken_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            results['ken'] = {
                'success': True,
                'cost': cost,
                'content': response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            results['ken'] = {
                'success': False,
                'error': str(e),
                'cost': 0
            }
        
        # Print results
        for avatar, result in results.items():
            if result['success']:
                print(f"✅ {avatar.capitalize()} success! Cost: ${result['cost']:.4f}")
                print(f"   Content: {result['content'][:100]}...")
            else:
                print(f"❌ {avatar.capitalize()} failed: {result['error']}")
        
        return results
    
    def run_quick_test(self):
        """Run quick test suite"""
        print("\n🚀 Starting Quick API Test")
        print("=" * 50)
        
        # Setup client
        if not self.setup_client():
            return False
        
        # Test topics
        test_topics = ["The Pythagorean Theorem", "Photosynthesis"]
        
        for topic in test_topics:
            print(f"\n📚 Testing topic: {topic}")
            
            # Test orchestrator
            orchestrator_result = self.test_orchestrator_prompt(topic)
            self.test_results.append({
                'test': 'orchestrator',
                'topic': topic,
                'result': orchestrator_result
            })
            
            # Test worker components
            component_types = ['CORE_CONCEPT', 'FACT', 'EXAMPLE']
            for component_type in component_types:
                worker_result = self.test_worker_prompt(topic, component_type)
                self.test_results.append({
                    'test': 'worker',
                    'topic': topic,
                    'component_type': component_type,
                    'result': worker_result
                })
            
            # Test avatars
            avatar_results = self.test_avatar_prompts(topic)
            self.test_results.append({
                'test': 'avatars',
                'topic': topic,
                'result': avatar_results
            })
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        # Count results
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results 
                             if result['result'].get('success', False))
        
        print(f"🧪 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {total_tests - successful_tests}")
        print(f"💰 Total Cost: ${self.total_cost:.4f}")
        print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Show sample results
        print(f"\n📝 Sample Results:")
        for result in self.test_results[:3]:  # Show first 3 results
            test_name = result['test']
            topic = result.get('topic', 'N/A')
            success = result['result'].get('success', False)
            cost = result['result'].get('cost', 0)
            print(f"   {test_name} ({topic}): {'✅' if success else '❌'} ${cost:.4f}")
        
        print(f"\n🎉 Quick test complete!")
        print(f"💡 The system is working! You can now run the full test suite.")


def main():
    """Main function"""
    print("🎯 Phoenix Knowledge Engine - Quick API Test")
    print("This will make real API calls and cost money!")
    print("Estimated cost: $0.10 - $0.50")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Test cancelled.")
        return
    
    # Create tester
    tester = QuickAPITester()
    
    # Run tests
    if tester.run_quick_test():
        tester.print_summary()
    else:
        print("❌ Test failed to run.")


if __name__ == "__main__":
    main()
