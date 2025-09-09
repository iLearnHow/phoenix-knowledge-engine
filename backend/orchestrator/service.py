"""
Orchestrator AI service for generating structured learning plans.
"""

import json
import logging
from typing import Dict, Any, List
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import LearningObjective, KnowledgeComponent, ComprehensionCheck, GenerationLog

logger = logging.getLogger('phoenix.orchestrator')


class OrchestratorService:
    """
    Service for orchestrating the content generation process.
    """
    
    def __init__(self):
        self.client = get_llm_service('orchestrator')
    
    def generate_learning_plan(self, topic: str) -> Dict[str, Any]:
        """
        Generate a structured learning plan for a given topic.
        
        Args:
            topic: The learning objective topic
            
        Returns:
            Dictionary containing the structured plan
        """
        try:
            from orchestrator.prompts import get_orchestrator_prompt
            
            prompt = get_orchestrator_prompt(topic)
            
            logger.info(f"Generating learning plan for topic: {topic}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educational architect who creates comprehensive learning plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse the JSON response
            plan_data = json.loads(response.choices[0].message.content)
            
            # Log the generation (will be updated after learning objective is created)
            # self._log_generation(learning_objective, prompt, response.choices[0].message.content, True)
            
            logger.info(f"Successfully generated learning plan for topic: {topic}")
            return plan_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for topic {topic}: {e}")
            # self._log_generation(None, prompt, str(e), False)
            raise ValueError(f"Invalid JSON response from AI: {e}")
            
        except Exception as e:
            logger.error(f"Error generating learning plan for topic {topic}: {e}")
            # self._log_generation(None, prompt, str(e), False)
            raise
    
    def create_learning_objective(self, plan_data: Dict[str, Any]) -> LearningObjective:
        """
        Create a LearningObjective from the plan data.
        
        Args:
            plan_data: The structured plan from the orchestrator
            
        Returns:
            Created LearningObjective instance
        """
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
        """
        Create the knowledge components plan from the orchestrator data.
        
        Args:
            learning_objective: The learning objective instance
            plan_data: The structured plan from the orchestrator
            
        Returns:
            List of knowledge component plans
        """
        components_plan = plan_data['knowledge_components_plan']
        
        # Store the plan for worker AI to process
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
        """
        Create the comprehension check plan from the orchestrator data.
        
        Args:
            learning_objective: The learning objective instance
            plan_data: The structured plan from the orchestrator
            
        Returns:
            Comprehension check plan
        """
        check_plan = plan_data['comprehension_check_plan']
        
        comprehension_check_plan = {
            'learning_objective_id': str(learning_objective.id),
            'question_type': check_plan['question_type'],
            'purpose': check_plan['purpose']
        }
        
        logger.info(f"Created comprehension check plan for learning objective: {learning_objective.id}")
        return comprehension_check_plan
    
    def _log_generation(self, learning_objective: LearningObjective, prompt: str, response: str, success: bool, error_message: str = ""):
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


def orchestrate_content_generation(topic: str) -> Dict[str, Any]:
    """
    Main function to orchestrate content generation for a topic.
    
    Args:
        topic: The learning objective topic
        
    Returns:
        Dictionary containing the orchestration results
    """
    service = OrchestratorService()
    
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
