"""
Simplified Worker AI service for generating specific content components.
Uses single model with optimized prompts for cost efficiency.
"""

import logging
from typing import Dict, Any
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import KnowledgeComponent, ComprehensionCheck, GenerationLog

logger = logging.getLogger('phoenix.worker')


class SimplifiedWorkerService:
    """
    Simplified service for generating content components.
    Uses single model with different prompts for different content types.
    """
    
    def __init__(self):
        self.client = get_llm_service('worker')
        self.model = "gpt-3.5-turbo"  # Cost-effective model for MVP
    
    def generate_knowledge_component(self, 
                                   learning_objective_title: str,
                                   component_type: str,
                                   purpose: str,
                                   sort_order: int) -> Dict[str, Any]:
        """
        Generate a specific knowledge component.
        Optimized for cost and quality.
        """
        try:
            prompt = self._create_component_prompt(learning_objective_title, component_type, purpose)
            
            logger.info(f"Generating {component_type} component for: {learning_objective_title}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert educator creating {component_type.lower()} content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300  # Reduced for cost efficiency
            )
            
            content = response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated {component_type} component")
            return {
                'content': content,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating {component_type} component: {e}")
            return {
                'content': f"Error generating {component_type}: {str(e)}",
                'success': False
            }
    
    def generate_comprehension_check(self, 
                                   learning_objective_title: str,
                                   purpose: str) -> Dict[str, Any]:
        """
        Generate a comprehension check (quiz question).
        Optimized for cost and quality.
        """
        try:
            prompt = self._create_quiz_prompt(learning_objective_title, purpose)
            
            logger.info(f"Generating comprehension check for: {learning_objective_title}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert assessment designer creating educational quiz questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400  # Slightly more for quiz questions
            )
            
            # Parse the JSON response
            import json
            quiz_data = json.loads(response.choices[0].message.content)
            
            logger.info(f"Successfully generated comprehension check")
            return {
                'quiz_data': quiz_data,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehension check: {e}")
            return {
                'quiz_data': {
                    'question_text': f"Error generating quiz: {str(e)}",
                    'options': ["Error", "Error", "Error", "Error"],
                    'correct_index': 0,
                    'explanation': "There was an error generating this quiz question."
                },
                'success': False
            }
    
    def _create_component_prompt(self, title: str, component_type: str, purpose: str) -> str:
        """Create an optimized prompt for knowledge components."""
        prompts = {
            'CORE_CONCEPT': f"Explain the core concept of {title}. {purpose}. Keep it clear and educational (2-3 sentences).",
            'FACT': f"State an important fact about {title}. {purpose}. Be concise and accurate (1-2 sentences).",
            'EXAMPLE': f"Provide a clear, practical example of {title}. {purpose}. Make it easy to understand (2-3 sentences).",
            'PRINCIPLE': f"Explain the key principle behind {title}. {purpose}. Focus on the underlying concept (2-3 sentences).",
            'ANALOGY': f"Create a helpful analogy for {title}. {purpose}. Make it relatable and clear (2-3 sentences).",
            'WARNING': f"Identify a common misconception or warning about {title}. {purpose}. Be helpful and clear (1-2 sentences)."
        }
        
        return prompts.get(component_type, f"Create {component_type.lower()} content about {title}. {purpose}.")
    
    def _create_quiz_prompt(self, title: str, purpose: str) -> str:
        """Create an optimized prompt for quiz questions."""
        return f"""Create a multiple-choice quiz question about {title}. {purpose}.

Return your response in this exact JSON format:
{{
  "question_text": "Clear, specific question about {title}",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "explanation": "Brief explanation of why the correct answer is right"
}}

Make the question challenging but fair, and ensure all options are plausible."""
    
    def create_knowledge_component(self, 
                                 learning_objective,
                                 component_plan: Dict[str, Any]) -> KnowledgeComponent:
        """Create a KnowledgeComponent in the database."""
        result = self.generate_knowledge_component(
            learning_objective.title,
            component_plan['type'],
            component_plan['purpose'],
            component_plan['sort_order']
        )
        
        return KnowledgeComponent.objects.create(
            learning_objective=learning_objective,
            type=component_plan['type'],
            content=result['content'],
            sort_order=component_plan['sort_order'],
            validation_status='PENDING'
        )
    
    def create_comprehension_check(self, 
                                 learning_objective,
                                 check_plan: Dict[str, Any]) -> ComprehensionCheck:
        """Create a ComprehensionCheck in the database."""
        result = self.generate_comprehension_check(
            learning_objective.title,
            check_plan['purpose']
        )
        
        quiz_data = result['quiz_data']
        
        return ComprehensionCheck.objects.create(
            learning_objective=learning_objective,
            question_text=quiz_data['question_text'],
            options=quiz_data['options'],
            correct_index=quiz_data['correct_index'],
            explanation=quiz_data['explanation'],
            validation_status='PENDING'
        )


def process_knowledge_components(learning_objective, components_plan: list) -> list:
    """
    Process all knowledge components for a learning objective.
    Simplified version for MVP.
    """
    service = SimplifiedWorkerService()
    created_components = []
    
    for component_plan in components_plan:
        try:
            component = service.create_knowledge_component(learning_objective, component_plan)
            created_components.append(component)
            logger.info(f"Created {component.type} component: {component.id}")
        except Exception as e:
            logger.error(f"Failed to create component {component_plan['type']}: {e}")
    
    return created_components


def process_comprehension_check(learning_objective, check_plan: Dict[str, Any]) -> ComprehensionCheck:
    """
    Process comprehension check for a learning objective.
    Simplified version for MVP.
    """
    service = SimplifiedWorkerService()
    
    try:
        check = service.create_comprehension_check(learning_objective, check_plan)
        logger.info(f"Created comprehension check: {check.id}")
        return check
    except Exception as e:
        logger.error(f"Failed to create comprehension check: {e}")
        raise
