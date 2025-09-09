"""
Simplified Orchestrator AI service for generating structured learning plans.
Focuses on core functionality without complex model routing.
"""

import json
import logging
from typing import Dict, Any, List
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import LearningObjective, KnowledgeComponent, ComprehensionCheck, GenerationLog

logger = logging.getLogger('phoenix.orchestrator')


class SimplifiedOrchestratorService:
    """
    Simplified service for orchestrating content generation.
    Uses single model with optimized prompts for cost efficiency.
    """
    
    def __init__(self):
        self.client = get_llm_service('orchestrator')
        self.model = "gpt-3.5-turbo"  # Cost-effective model for MVP
    
    def generate_learning_plan(self, topic: str) -> Dict[str, Any]:
        """
        Generate a structured learning plan for a given topic.
        Optimized for cost and simplicity.
        """
        try:
            prompt = self._create_optimized_prompt(topic)
            
            logger.info(f"Generating learning plan for topic: {topic}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational architect. Create comprehensive learning plans in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500  # Reduced for cost efficiency
            )
            
            # Parse the JSON response
            plan_data = json.loads(response.choices[0].message.content)
            
            logger.info(f"Successfully generated learning plan for topic: {topic}")
            return plan_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for topic {topic}: {e}")
            raise ValueError(f"Invalid JSON response from AI: {e}")
            
        except Exception as e:
            logger.error(f"Error generating learning plan for topic {topic}: {e}")
            raise
    
    def _create_optimized_prompt(self, topic: str) -> str:
        """
        Create an optimized prompt that generates the required JSON structure
        while minimizing token usage.
        """
        return f"""Create a learning plan for "{topic}" in this exact JSON format:

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
    
    def create_learning_objective(self, plan_data: Dict[str, Any]) -> LearningObjective:
        """Create a LearningObjective from the plan data."""
        learning_obj_data = plan_data['learning_objective']
        
        learning_objective = LearningObjective.objects.create(
            title=learning_obj_data['title'],
            core_question=learning_obj_data['core_question'],
            summary=learning_obj_data['summary'],
            status='GENERATING'
        )
        
        logger.info(f"Created learning objective: {learning_objective.id}")
        return learning_objective
    
    def create_knowledge_components_plan(self, learning_objective: LearningObjective, plan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create the knowledge components plan from the orchestrator data."""
        components_plan = plan_data['knowledge_components_plan']
        
        knowledge_components_plan = []
        for component_plan in components_plan:
            knowledge_components_plan.append({
                'learning_objective_id': str(learning_objective.id),
                'type': component_plan['type'],
                'purpose': component_plan['purpose'],
                'sort_order': component_plan['sort_order']
            })
        
        logger.info(f"Created knowledge components plan with {len(knowledge_components_plan)} components")
        return knowledge_components_plan
    
    def create_comprehension_check_plan(self, learning_objective: LearningObjective, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create the comprehension check plan from the orchestrator data."""
        check_plan = plan_data['comprehension_check_plan']
        
        comprehension_check_plan = {
            'learning_objective_id': str(learning_objective.id),
            'question_type': check_plan['question_type'],
            'purpose': check_plan['purpose']
        }
        
        logger.info(f"Created comprehension check plan for learning objective: {learning_objective.id}")
        return comprehension_check_plan


def orchestrate_content_generation(topic: str) -> Dict[str, Any]:
    """
    Main function to orchestrate content generation for a topic.
    Simplified version for MVP.
    """
    service = SimplifiedOrchestratorService()
    
    try:
        # Generate the learning plan
        plan_data = service.generate_learning_plan(topic)
        
        # Create the learning objective
        learning_objective = service.create_learning_objective(plan_data)
        
        # Create the knowledge components plan
        knowledge_components_plan = service.create_knowledge_components_plan(learning_objective, plan_data)
        
        # Create the comprehension check plan
        comprehension_check_plan = service.create_comprehension_check_plan(learning_objective, plan_data)
        
        return {
            'learning_objective': learning_objective,
            'knowledge_components_plan': knowledge_components_plan,
            'comprehension_check_plan': comprehension_check_plan,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Orchestration failed for topic {topic}: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
