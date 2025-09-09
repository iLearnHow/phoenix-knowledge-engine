"""
Worker AI service for generating specific content components.
"""

import json
import logging
from typing import Dict, Any, List
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import (
    LearningObjective, KnowledgeComponent, ComprehensionCheck, 
    GenerationLog
)

logger = logging.getLogger('phoenix.worker')


class WorkerService:
    """
    Service for generating specific content components using AI.
    """
    
    def __init__(self):
        self.client = get_llm_service('worker')
    
    def generate_learning_objective_summary(self, learning_objective: LearningObjective) -> str:
        """
        Generate a summary for a learning objective.
        
        Args:
            learning_objective: The learning objective instance
            
        Returns:
            Generated summary
        """
        try:
            from worker.prompts import get_learning_objective_prompt
            
            prompt = get_learning_objective_prompt(
                learning_objective.title, 
                learning_objective.core_question
            )
            
            logger.info(f"Generating summary for learning objective: {learning_objective.id}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a world-class curriculum designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Update the learning objective
            learning_objective.summary = summary
            learning_objective.save()
            
            # Log the generation
            self._log_generation(learning_objective, prompt, summary, True)
            
            logger.info(f"Successfully generated summary for learning objective: {learning_objective.id}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary for learning objective {learning_objective.id}: {e}")
            self._log_generation(learning_objective, prompt, str(e), False, str(e))
            raise
    
    def generate_knowledge_component(self, learning_objective: LearningObjective, 
                                   component_type: str, purpose: str, sort_order: int) -> KnowledgeComponent:
        """
        Generate a knowledge component.
        
        Args:
            learning_objective: The learning objective instance
            component_type: Type of component to generate
            purpose: Purpose of this component
            sort_order: Order of this component
            
        Returns:
            Created KnowledgeComponent instance
        """
        try:
            from worker.prompts import get_knowledge_component_prompt, get_component_system_prompt
            
            prompt = get_knowledge_component_prompt(
                learning_objective.title, 
                component_type, 
                purpose
            )
            
            system_prompt = get_component_system_prompt(component_type)
            
            logger.info(f"Generating {component_type} component for learning objective: {learning_objective.id}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Create the knowledge component
            knowledge_component = KnowledgeComponent.objects.create(
                learning_objective=learning_objective,
                type=component_type,
                content=content,
                sort_order=sort_order,
                validation_status='PENDING'
            )
            
            # Log the generation
            self._log_generation(learning_objective, prompt, content, True)
            
            logger.info(f"Successfully generated {component_type} component: {knowledge_component.id}")
            return knowledge_component
            
        except Exception as e:
            logger.error(f"Error generating {component_type} component for learning objective {learning_objective.id}: {e}")
            self._log_generation(learning_objective, prompt, str(e), False, str(e))
            raise
    
    def generate_comprehension_check(self, learning_objective: LearningObjective) -> ComprehensionCheck:
        """
        Generate a comprehension check (quiz question).
        
        Args:
            learning_objective: The learning objective instance
            
        Returns:
            Created ComprehensionCheck instance
        """
        try:
            from worker.prompts import get_comprehension_check_prompt
            
            prompt = get_comprehension_check_prompt(learning_objective.title)
            
            logger.info(f"Generating comprehension check for learning objective: {learning_objective.id}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert assessment designer who creates fair, educational quiz questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the JSON response
            check_data = json.loads(response.choices[0].message.content)
            
            # Create the comprehension check
            comprehension_check = ComprehensionCheck.objects.create(
                learning_objective=learning_objective,
                question_text=check_data['question_text'],
                options=check_data['options'],
                correct_index=check_data['correct_index'],
                explanation=check_data['explanation'],
                validation_status='PENDING'
            )
            
            # Log the generation
            self._log_generation(learning_objective, prompt, response.choices[0].message.content, True)
            
            logger.info(f"Successfully generated comprehension check: {comprehension_check.id}")
            return comprehension_check
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for comprehension check: {e}")
            self._log_generation(learning_objective, prompt, str(e), False, str(e))
            raise ValueError(f"Invalid JSON response from AI: {e}")
            
        except Exception as e:
            logger.error(f"Error generating comprehension check for learning objective {learning_objective.id}: {e}")
            self._log_generation(learning_objective, prompt, str(e), False, str(e))
            raise
    
    def generate_all_components(self, learning_objective: LearningObjective, 
                              knowledge_components_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate all components for a learning objective.
        
        Args:
            learning_objective: The learning objective instance
            knowledge_components_plan: List of component plans from orchestrator
            
        Returns:
            Dictionary containing generation results
        """
        try:
            # Generate summary
            summary = self.generate_learning_objective_summary(learning_objective)
            
            # Generate knowledge components
            knowledge_components = []
            for component_plan in knowledge_components_plan:
                component = self.generate_knowledge_component(
                    learning_objective,
                    component_plan['type'],
                    component_plan['purpose'],
                    component_plan['sort_order']
                )
                knowledge_components.append(component)
            
            # Generate comprehension check
            comprehension_check = self.generate_comprehension_check(learning_objective)
            
            # Update learning objective status
            learning_objective.status = 'READY'
            learning_objective.save()
            
            logger.info(f"Successfully generated all components for learning objective: {learning_objective.id}")
            
            return {
                'learning_objective': learning_objective,
                'knowledge_components': knowledge_components,
                'comprehension_check': comprehension_check,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error generating all components for learning objective {learning_objective.id}: {e}")
            # Update learning objective status to failed
            learning_objective.status = 'FAILED'
            learning_objective.save()
            
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _log_generation(self, learning_objective: LearningObjective, prompt: str, 
                       response: str, success: bool, error_message: str = ""):
        """
        Log the AI generation attempt.
        
        Args:
            learning_objective: The learning objective being generated for
            prompt: The prompt sent to AI
            response: The response from AI
            success: Whether the generation was successful
            error_message: Error message if generation failed
        """
        try:
            GenerationLog.objects.create(
                learning_objective=learning_objective,
                prompt_used=prompt,
                ai_response=response,
                generation_time=0.0,  # Will be calculated in actual implementation
                tokens_used=len(prompt.split()) + len(response.split()),
                success=success,
                error_message=error_message
            )
        except Exception as e:
            logger.error(f"Failed to log generation: {e}")


def process_knowledge_components(learning_objective_id: str, knowledge_components_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process knowledge components generation for a learning objective.
    
    Args:
        learning_objective_id: ID of the learning objective
        knowledge_components_plan: List of component plans
        
    Returns:
        Dictionary containing processing results
    """
    try:
        learning_objective = LearningObjective.objects.get(id=learning_objective_id)
        service = WorkerService()
        
        return service.generate_all_components(learning_objective, knowledge_components_plan)
        
    except LearningObjective.DoesNotExist:
        logger.error(f"Learning objective not found: {learning_objective_id}")
        return {
            'status': 'error',
            'error': 'Learning objective not found'
        }
    except Exception as e:
        logger.error(f"Error processing knowledge components: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
