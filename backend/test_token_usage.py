#!/usr/bin/env python3
"""
Token Usage Testing Script
Tests our system without spending money on OpenAI API calls
"""

import json
import re
from typing import Dict, List, Tuple

def count_tokens_roughly(text: str) -> int:
    """
    Rough token estimation (1 token ≈ 4 characters for English)
    This is an approximation - actual tokenization varies
    """
    return len(text) // 4

def analyze_prompts() -> Dict[str, int]:
    """Analyze our prompts to estimate token usage"""
    
    # Orchestrator prompt
    orchestrator_prompt = """
You are the Chief Learning Architect for our educational platform. Your task is to decompose the learning objective "{topic}" into a complete set of atomic knowledge components strictly following our schema.

Generate a structured JSON output that defines the plan to populate these tables:
1. `learning_objectives`: Title, Core Question, Summary.
2. `knowledge_components`: A list of components with their `type` (CORE_CONCEPT, FACT, EXAMPLE, etc.), `content`, and `sort_order`.
3. `comprehension_checks`: At least one multiple-choice question.

Your output must be a valid JSON object that can be parsed by our system to generate subsequent, specific creation prompts. Be meticulous, logical, and ensure complete coverage of the topic.

The JSON structure should be:
{
  "learning_objective": {
    "title": "The topic title",
    "core_question": "The central question this addresses",
    "summary": "Brief summary of the learning objective"
  },
  "knowledge_components_plan": [
    { "type": "CORE_CONCEPT", "purpose": "Define the main concept", "sort_order": 1 },
    { "type": "FACT", "purpose": "State important facts", "sort_order": 2 },
    { "type": "EXAMPLE", "purpose": "Provide concrete examples", "sort_order": 3 },
    { "type": "PRINCIPLE", "purpose": "Explain key principles", "sort_order": 4 },
    { "type": "ANALOGY", "purpose": "Create helpful analogies", "sort_order": 5 },
    { "type": "WARNING", "purpose": "Highlight common mistakes", "sort_order": 6 }
  ],
  "comprehension_check_plan": {
    "question_type": "multiple_choice",
    "purpose": "Test understanding of the core concept"
  }
}

Ensure the plan covers the topic comprehensively and follows educational best practices.
"""
    
    # Worker prompts
    summary_prompt = """You are a world-class curriculum designer. Write a concise and engaging summary for a learning objective. Do not add any other commentary.

TOPIC: {topic}
CORE_QUESTION: {core_question}

SUMMARY:"""
    
    component_prompt = """You are an expert educator specializing in {component_type}. Create exactly one {component_type} for the following topic.

TOPIC: {topic}
COMPONENT_TYPE: {component_type}
PURPOSE: {purpose}

YOUR OUTPUT (ONLY THE {component_type} ITSELF):"""
    
    quiz_prompt = """You are an assessment designer. Create one multiple-choice question to test understanding of {topic}.

- Generate 1 question with 4 plausible options.
- Indicate the correct answer and provide a one-sentence explanation of why it is correct.
- Format your output as a JSON object with the following keys: `question_text`, `options` (array), `correct_index` (integer), `explanation`.

TOPIC: {topic}"""
    
    # Estimate token usage
    estimates = {
        "orchestrator_input": count_tokens_roughly(orchestrator_prompt),
        "orchestrator_output": 300,  # Estimated JSON response
        "summary_input": count_tokens_roughly(summary_prompt),
        "summary_output": 150,  # Estimated summary length
        "component_input": count_tokens_roughly(component_prompt),
        "component_output": 200,  # Average component length
        "quiz_input": count_tokens_roughly(quiz_prompt),
        "quiz_output": 200,  # Estimated quiz JSON
        "quality_control_input": 200,  # Fact-checking prompt
        "quality_control_output": 50,  # Short approval/rejection
    }
    
    return estimates

def calculate_costs(estimates: Dict[str, int]) -> Dict[str, float]:
    """Calculate costs for different OpenAI models"""
    
    # Per learning objective token usage
    orchestrator_tokens = estimates["orchestrator_input"] + estimates["orchestrator_output"]
    summary_tokens = estimates["summary_input"] + estimates["summary_output"]
    component_tokens = (estimates["component_input"] + estimates["component_output"]) * 6  # 6 components
    quiz_tokens = estimates["quiz_input"] + estimates["quiz_output"]
    qc_tokens = (estimates["quality_control_input"] + estimates["quality_control_output"]) * 3  # 3 QC checks
    
    total_input = estimates["orchestrator_input"] + estimates["summary_input"] + (estimates["component_input"] * 6) + estimates["quiz_input"] + (estimates["quality_control_input"] * 3)
    total_output = estimates["orchestrator_output"] + estimates["summary_output"] + (estimates["component_output"] * 6) + estimates["quiz_output"] + (estimates["quality_control_output"] * 3)
    
    costs = {
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_tokens": total_input + total_output,
        "gpt4_input_cost": total_input * 0.03 / 1000,
        "gpt4_output_cost": total_output * 0.06 / 1000,
        "gpt4_total_cost": (total_input * 0.03 + total_output * 0.06) / 1000,
        "gpt4_turbo_input_cost": total_input * 0.01 / 1000,
        "gpt4_turbo_output_cost": total_output * 0.03 / 1000,
        "gpt4_turbo_total_cost": (total_input * 0.01 + total_output * 0.03) / 1000,
        "gpt35_input_cost": total_input * 0.001 / 1000,
        "gpt35_output_cost": total_output * 0.002 / 1000,
        "gpt35_total_cost": (total_input * 0.001 + total_output * 0.002) / 1000,
    }
    
    return costs

def generate_test_plan() -> Dict[str, any]:
    """Generate a comprehensive testing plan"""
    
    test_topics = [
        "The Pythagorean Theorem",
        "Photosynthesis Process", 
        "World War II Causes",
        "Newton's Laws of Motion",
        "The Water Cycle"
    ]
    
    test_plan = {
        "phase_1_free_tier": {
            "budget": "$5 (free tier)",
            "lessons": 5,
            "topics": test_topics[:2],
            "models": ["gpt-3.5-turbo"],
            "purpose": "Basic functionality testing"
        },
        "phase_2_small_budget": {
            "budget": "$20",
            "lessons": 50,
            "topics": test_topics,
            "models": ["gpt-3.5-turbo", "gpt-4-turbo"],
            "purpose": "Quality comparison and optimization"
        },
        "phase_3_development": {
            "budget": "$50/month",
            "lessons": 500,
            "topics": "Various educational topics",
            "models": ["gpt-3.5-turbo", "gpt-4-turbo"],
            "purpose": "Real-world usage patterns"
        }
    }
    
    return test_plan

def main():
    """Main testing function"""
    print("🧪 OpenAI Token Usage Analysis")
    print("=" * 50)
    
    # Analyze prompts
    estimates = analyze_prompts()
    costs = calculate_costs(estimates)
    
    print(f"\n📊 Token Usage Estimates:")
    print(f"Input tokens per lesson: {costs['total_input_tokens']:,}")
    print(f"Output tokens per lesson: {costs['total_output_tokens']:,}")
    print(f"Total tokens per lesson: {costs['total_tokens']:,}")
    
    print(f"\n💰 Cost Per Lesson:")
    print(f"GPT-4: ${costs['gpt4_total_cost']:.4f}")
    print(f"GPT-4 Turbo: ${costs['gpt4_turbo_total_cost']:.4f}")
    print(f"GPT-3.5 Turbo: ${costs['gpt35_total_cost']:.4f}")
    
    print(f"\n📈 Monthly Cost Projections (100 lessons):")
    print(f"GPT-4: ${costs['gpt4_total_cost'] * 100:.2f}")
    print(f"GPT-4 Turbo: ${costs['gpt4_turbo_total_cost'] * 100:.2f}")
    print(f"GPT-3.5 Turbo: ${costs['gpt35_total_cost'] * 100:.2f}")
    
    # Generate test plan
    test_plan = generate_test_plan()
    
    print(f"\n🎯 Recommended Testing Plan:")
    for phase, details in test_plan.items():
        print(f"\n{phase.replace('_', ' ').title()}:")
        print(f"  Budget: {details['budget']}")
        print(f"  Lessons: {details['lessons']}")
        print(f"  Purpose: {details['purpose']}")
    
    print(f"\n⚠️  Important Notes:")
    print(f"- These are estimates based on prompt analysis")
    print(f"- Actual usage may vary by 20-50%")
    print(f"- Start with free tier ($5) for initial testing")
    print(f"- Monitor actual usage in OpenAI dashboard")
    print(f"- Set budget alerts to prevent overspending")
    
    return costs, test_plan

if __name__ == "__main__":
    costs, test_plan = main()
