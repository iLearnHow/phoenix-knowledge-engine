"""
Orchestrator AI prompts for generating structured learning plans.
Based on the technical architecture specifications.
"""

ORCHESTRATOR_PROMPT_TEMPLATE = """
You are the Chief Learning Architect for our educational platform. Your task is to decompose the learning objective "{topic}" into a complete set of atomic knowledge components strictly following our schema.

Generate a structured JSON output that defines the plan to populate these tables:
1. `learning_objectives`: Title, Core Question, Summary.
2. `knowledge_components`: A list of components with their `type` (CORE_CONCEPT, FACT, EXAMPLE, etc.), `content`, and `sort_order`.
3. `comprehension_checks`: At least one multiple-choice question.

Your output must be a valid JSON object that can be parsed by our system to generate subsequent, specific creation prompts. Be meticulous, logical, and ensure complete coverage of the topic.

The JSON structure should be:
{{
  "learning_objective": {{
    "title": "The topic title",
    "core_question": "The central question this addresses",
    "summary": "Brief summary of the learning objective"
  }},
  "knowledge_components_plan": [
    {{ "type": "CORE_CONCEPT", "purpose": "Define the main concept", "sort_order": 1 }},
    {{ "type": "FACT", "purpose": "State important facts", "sort_order": 2 }},
    {{ "type": "EXAMPLE", "purpose": "Provide concrete examples", "sort_order": 3 }},
    {{ "type": "PRINCIPLE", "purpose": "Explain key principles", "sort_order": 4 }},
    {{ "type": "ANALOGY", "purpose": "Create helpful analogies", "sort_order": 5 }},
    {{ "type": "WARNING", "purpose": "Highlight common mistakes", "sort_order": 6 }}
  ],
  "comprehension_check_plan": {{
    "question_type": "multiple_choice",
    "purpose": "Test understanding of the core concept"
  }}
}}

Ensure the plan covers the topic comprehensively and follows educational best practices.
"""

def get_orchestrator_prompt(topic: str) -> str:
    """
    Generate the orchestrator prompt for a given topic.
    
    Args:
        topic: The learning objective topic
        
    Returns:
        Formatted prompt string
    """
    return ORCHESTRATOR_PROMPT_TEMPLATE.format(topic=topic)
