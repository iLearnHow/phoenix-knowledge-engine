"""
Text Content Generator
Simplified text content generation for MVP
"""

import logging
from typing import Dict, Any, List
from django.conf import settings
from services.local_llm import get_llm_service
from avatars.service import avatar_service, AvatarType

logger = logging.getLogger('phoenix.content.text')


class TextContentGenerator:
    """
    Simplified text content generator.
    Uses single model with avatar-specific prompts.
    """
    
    def __init__(self):
        self.client = get_llm_service('text_generator')
        self.model = "gpt-3.5-turbo"  # Cost-effective model for MVP
    
    def generate_learning_objective_summary(self, 
                                          topic: str, 
                                          avatar_type: AvatarType = AvatarType.KELLY) -> Dict[str, Any]:
        """
        Generate a learning objective summary using the specified avatar.
        """
        try:
            avatar = avatar_service.get_avatar(avatar_type)
            system_prompt = avatar.get_system_prompt()
            
            prompt = f"""Create a brief, engaging summary for a learning objective about "{topic}".

{avatar.get_prompt_modifier('CORE_CONCEPT')}

Keep it to 2-3 sentences that capture the essence of what students will learn."""
            
            logger.info(f"Generating summary for topic: {topic} with {avatar.name}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            summary = response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated summary with {avatar.name}")
            return {
                'summary': summary,
                'avatar_used': avatar.name,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                'summary': f"Error generating summary: {str(e)}",
                'avatar_used': avatar.name,
                'success': False
            }
    
    def generate_knowledge_component(self, 
                                   topic: str,
                                   component_type: str,
                                   purpose: str,
                                   avatar_type: AvatarType = AvatarType.KELLY) -> Dict[str, Any]:
        """
        Generate a knowledge component using the specified avatar.
        """
        try:
            avatar = avatar_service.get_avatar(avatar_type)
            system_prompt = avatar.get_system_prompt()
            prompt_modifier = avatar.get_prompt_modifier(component_type)
            
            prompt = f"""Create {component_type.lower()} content about "{topic}".

Purpose: {purpose}
{prompt_modifier}

Keep it clear, educational, and appropriate for the content type."""
            
            logger.info(f"Generating {component_type} for topic: {topic} with {avatar.name}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated {component_type} with {avatar.name}")
            return {
                'content': content,
                'component_type': component_type,
                'avatar_used': avatar.name,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating {component_type}: {e}")
            return {
                'content': f"Error generating {component_type}: {str(e)}",
                'component_type': component_type,
                'avatar_used': avatar.name,
                'success': False
            }
    
    def generate_comprehension_check(self, 
                                   topic: str,
                                   purpose: str,
                                   avatar_type: AvatarType = AvatarType.KELLY) -> Dict[str, Any]:
        """
        Generate a comprehension check using the specified avatar.
        """
        try:
            avatar = avatar_service.get_avatar(avatar_type)
            system_prompt = avatar.get_system_prompt()
            quiz_style = avatar.get_quiz_style()
            
            prompt = f"""Create a multiple-choice quiz question about "{topic}".

Purpose: {purpose}
{quiz_style}

Return your response in this exact JSON format:
{{
  "question_text": "Clear, specific question about {topic}",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "explanation": "Brief explanation of why the correct answer is right"
}}"""
            
            logger.info(f"Generating comprehension check for topic: {topic} with {avatar.name}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            # Parse the JSON response
            import json
            quiz_data = json.loads(response.choices[0].message.content)
            
            logger.info(f"Successfully generated comprehension check with {avatar.name}")
            return {
                'quiz_data': quiz_data,
                'avatar_used': avatar.name,
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
                'avatar_used': avatar.name,
                'success': False
            }
    
    def generate_complete_lesson(self, 
                               topic: str,
                               avatar_type: AvatarType = AvatarType.KELLY) -> Dict[str, Any]:
        """
        Generate a complete lesson with all components using the specified avatar.
        """
        try:
            logger.info(f"Generating complete lesson for topic: {topic} with {avatar_type.value}")
            
            # Generate summary
            summary_result = self.generate_learning_objective_summary(topic, avatar_type)
            
            # Generate knowledge components
            component_types = ['CORE_CONCEPT', 'FACT', 'EXAMPLE', 'PRINCIPLE', 'WARNING']
            components = []
            
            for i, component_type in enumerate(component_types, 1):
                purpose = f"Component {i} of the lesson about {topic}"
                component_result = self.generate_knowledge_component(
                    topic, component_type, purpose, avatar_type
                )
                components.append(component_result)
            
            # Generate comprehension check
            check_result = self.generate_comprehension_check(
                topic, f"Test understanding of {topic}", avatar_type
            )
            
            return {
                'topic': topic,
                'avatar_used': avatar_type.value,
                'summary': summary_result,
                'components': components,
                'comprehension_check': check_result,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating complete lesson: {e}")
            return {
                'topic': topic,
                'avatar_used': avatar_type.value,
                'error': str(e),
                'success': False
            }


def generate_lesson_with_avatar(topic: str, avatar_preference: str = None) -> Dict[str, Any]:
    """
    Generate a complete lesson with avatar selection.
    """
    # Select avatar based on preference or topic
    if avatar_preference == 'ken':
        avatar_type = AvatarType.KEN
    elif avatar_preference == 'kelly':
        avatar_type = AvatarType.KELLY
    else:
        avatar_type = avatar_service.select_avatar_for_topic(topic)
    
    generator = TextContentGenerator()
    return generator.generate_complete_lesson(topic, avatar_type)
