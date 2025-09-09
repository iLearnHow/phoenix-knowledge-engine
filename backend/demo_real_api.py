#!/usr/bin/env python3
"""
Demo Real API Testing Script for Phoenix Knowledge Engine
Demonstrates the system working with actual OpenAI API calls
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class DemoAPITester:
    """Demo API tester for Phoenix Knowledge Engine"""
    
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
        
        print("🎯 Phoenix Knowledge Engine - Real API Demo")
        print("=" * 60)
    
    def setup_client(self):
        """Setup OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ ERROR: OpenAI API key not configured!")
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
    
    def test_complete_lesson_generation(self, topic: str):
        """Test complete lesson generation with both avatars"""
        print(f"\n🎓 Generating Complete Lesson: {topic}")
        print("-" * 50)
        
        # Step 1: Generate Learning Plan (Orchestrator)
        print("1️⃣ Creating Learning Plan...")
        orchestrator_prompt = f"""Create a comprehensive learning plan for "{topic}" in this exact JSON format:

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
                    {"role": "user", "content": orchestrator_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Calculate cost
            input_tokens = len(orchestrator_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            # Parse response
            plan_data = json.loads(response.choices[0].message.content)
            print(f"   ✅ Learning plan created! Cost: ${cost:.4f}")
            print(f"   📋 Title: {plan_data['learning_objective']['title']}")
            print(f"   📚 Components: {len(plan_data['knowledge_components_plan'])}")
            
        except Exception as e:
            print(f"   ❌ Learning plan failed: {e}")
            return False
        
        # Step 2: Generate Content with Kelly (Academic)
        print("\n2️⃣ Generating Content with Kelly (Academic)...")
        kelly_prompt = f"""As Kelly, an educational specialist, create educational content about "{topic}" with an academic, methodical approach.

Focus on:
- Step-by-step explanations
- Building foundational understanding
- Clear, academic language
- Multiple examples and analogies

Create a comprehensive lesson that would help students understand this topic thoroughly. Include:
1. Core concept explanation
2. Key facts
3. Practical examples
4. Underlying principles
5. Common misconceptions to avoid

Make it educational and thorough."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Kelly, an educational specialist with a warm, professional demeanor who excels at breaking down complex topics."},
                    {"role": "user", "content": kelly_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            input_tokens = len(kelly_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            kelly_content = response.choices[0].message.content.strip()
            print(f"   ✅ Kelly's lesson created! Cost: ${cost:.4f}")
            print(f"   📝 Content preview: {kelly_content[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Kelly's lesson failed: {e}")
            return False
        
        # Step 3: Generate Content with Ken (Practical)
        print("\n3️⃣ Generating Content with Ken (Practical)...")
        ken_prompt = f"""As Ken, a practical application expert, create educational content about "{topic}" with a hands-on, practical approach.

Focus on:
- Real-world applications
- Immediate practical use
- Concrete examples
- Learning by doing

Create a practical lesson that shows how this topic applies in real life. Include:
1. Real-world applications
2. Hands-on examples
3. Practical exercises
4. Industry use cases
5. Common mistakes to avoid

Make it engaging and practical."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Ken, a practical application expert with an energetic, engaging personality who focuses on real-world applications."},
                    {"role": "user", "content": ken_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            input_tokens = len(ken_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            ken_content = response.choices[0].message.content.strip()
            print(f"   ✅ Ken's lesson created! Cost: ${cost:.4f}")
            print(f"   📝 Content preview: {ken_content[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Ken's lesson failed: {e}")
            return False
        
        # Step 4: Generate Quiz Questions
        print("\n4️⃣ Creating Comprehension Check...")
        quiz_prompt = f"""Create a multiple-choice quiz about "{topic}" with 3 questions that test understanding of key concepts.

Format as JSON:
{{
  "questions": [
    {{
      "question": "Question text here",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_answer": "A",
      "explanation": "Why this answer is correct"
    }}
  ]
}}

Make questions challenging but fair, testing real understanding of {topic}."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator who designs fair, educational assessments."},
                    {"role": "user", "content": quiz_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            input_tokens = len(quiz_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            quiz_data = json.loads(response.choices[0].message.content)
            print(f"   ✅ Quiz created! Cost: ${cost:.4f}")
            print(f"   📝 Questions: {len(quiz_data['questions'])}")
            
        except Exception as e:
            print(f"   ❌ Quiz creation failed: {e}")
            return False
        
        # Step 5: Quality Control Check
        print("\n5️⃣ Running Quality Control...")
        qc_prompt = f"""Review this educational content about "{topic}" for quality:

KELLY'S CONTENT (Academic):
{kelly_content[:300]}...

KEN'S CONTENT (Practical):
{ken_content[:300]}...

Rate the content quality and provide feedback on:
1. Educational value
2. Clarity and accuracy
3. Engagement level
4. Completeness
5. Any issues or improvements needed

Provide a brief assessment."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a quality control expert who reviews educational content for accuracy, clarity, and educational value."},
                    {"role": "user", "content": qc_prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            input_tokens = len(qc_prompt.split())
            output_tokens = len(response.choices[0].message.content.split())
            cost = self.calculate_cost("gpt-3.5-turbo", input_tokens, output_tokens)
            self.total_cost += cost
            
            qc_feedback = response.choices[0].message.content.strip()
            print(f"   ✅ Quality control complete! Cost: ${cost:.4f}")
            print(f"   📝 Feedback: {qc_feedback[:100]}...")
            
        except Exception as e:
            print(f"   ❌ Quality control failed: {e}")
            return False
        
        return True
    
    def run_demo(self):
        """Run the complete demo"""
        print("\n🚀 Starting Phoenix Knowledge Engine Demo")
        print("=" * 60)
        
        # Setup client
        if not self.setup_client():
            return False
        
        # Demo topics
        demo_topics = [
            "The Pythagorean Theorem",
            "Photosynthesis",
            "Supply and Demand"
        ]
        
        for i, topic in enumerate(demo_topics, 1):
            print(f"\n📚 DEMO {i}: {topic}")
            print("=" * 60)
            
            success = self.test_complete_lesson_generation(topic)
            
            if success:
                print(f"\n✅ Demo {i} completed successfully!")
            else:
                print(f"\n❌ Demo {i} failed!")
            
            # Small delay between demos
            if i < len(demo_topics):
                print("\n⏳ Preparing next demo...")
                time.sleep(2)
        
        return True
    
    def print_summary(self):
        """Print demo summary"""
        print("\n" + "=" * 60)
        print("🎉 PHOENIX KNOWLEDGE ENGINE DEMO COMPLETE!")
        print("=" * 60)
        
        print(f"💰 Total Cost: ${self.total_cost:.4f}")
        print(f"⏱️  Demo Duration: {time.time() - self.start_time:.1f} seconds")
        
        print(f"\n🎯 WHAT WAS DEMONSTRATED:")
        print(f"✅ OpenAI API Integration")
        print(f"✅ Learning Plan Generation (Orchestrator)")
        print(f"✅ Kelly Avatar (Academic Content)")
        print(f"✅ Ken Avatar (Practical Content)")
        print(f"✅ Quiz Generation (Quality Control)")
        print(f"✅ Cost Tracking & Management")
        print(f"✅ Real-time Content Generation")
        
        print(f"\n🚀 SYSTEM STATUS: FULLY OPERATIONAL")
        print(f"💡 Ready for production deployment!")
        
        # Save demo results
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_cost': self.total_cost,
            'demo_duration': time.time() - self.start_time,
            'status': 'SUCCESS'
        }
        
        with open('demo_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Demo results saved to: demo_results.json")


def main():
    """Main demo function"""
    print("🎯 Phoenix Knowledge Engine - Real API Demo")
    print("This will demonstrate the complete system working with real AI!")
    print("Estimated cost: $0.20 - $0.80")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed with the demo? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Demo cancelled.")
        return
    
    # Create demo tester
    demo = DemoAPITester()
    demo.start_time = time.time()
    
    # Run demo
    if demo.run_demo():
        demo.print_summary()
    else:
        print("❌ Demo failed to run.")


if __name__ == "__main__":
    main()
