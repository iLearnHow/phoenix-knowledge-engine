"""
Simplified Quality Control service for validating AI-generated content.
Uses single model with optimized prompts for cost efficiency.
"""

import logging
from typing import Dict, Any, List
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import ValidationLog

logger = logging.getLogger('phoenix.quality_control')


class SimplifiedQualityControlService:
    """
    Simplified service for content validation.
    Uses single model with different validation prompts.
    """
    
    def __init__(self):
        self.client = get_llm_service('quality_control')
        self.model = "gpt-3.5-turbo"  # Cost-effective model for MVP
    
    def validate_content(self, content: str, content_type: str, topic: str) -> Dict[str, Any]:
        """
        Validate content using AI-powered quality control.
        Optimized for cost and accuracy.
        """
        try:
            prompt = self._create_validation_prompt(content, content_type, topic)
            
            logger.info(f"Validating {content_type} content for topic: {topic}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a quality control expert. Validate educational content for accuracy, clarity, and appropriateness."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for consistent validation
                max_tokens=200  # Reduced for cost efficiency
            )
            
            validation_result = response.choices[0].message.content.strip()
            
            # Parse validation result
            is_valid = self._parse_validation_result(validation_result)
            
            logger.info(f"Validation result for {content_type}: {'PASSED' if is_valid else 'FAILED'}")
            
            return {
                'is_valid': is_valid,
                'validation_notes': validation_result,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error validating {content_type} content: {e}")
            return {
                'is_valid': False,
                'validation_notes': f"Validation error: {str(e)}",
                'success': False
            }
    
    def validate_knowledge_component(self, component) -> bool:
        """
        Validate a knowledge component.
        Returns True if valid, False otherwise.
        """
        result = self.validate_content(
            component.content,
            component.type,
            component.learning_objective.title
        )
        
        # Update component status
        if result['is_valid']:
            component.validation_status = 'APPROVED'
        else:
            component.validation_status = 'FLAGGED'
        
        component.validation_notes = result['validation_notes']
        component.save()
        
        # Log validation
        self._log_validation(component.id, 'knowledge_component', 'ai_validation', 
                           'PASSED' if result['is_valid'] else 'FAILED', result)
        
        return result['is_valid']
    
    def validate_comprehension_check(self, check) -> bool:
        """
        Validate a comprehension check.
        Returns True if valid, False otherwise.
        """
        result = self.validate_content(
            check.question_text,
            'comprehension_check',
            check.learning_objective.title
        )
        
        # Update check status
        if result['is_valid']:
            check.validation_status = 'APPROVED'
        else:
            check.validation_status = 'FLAGGED'
        
        check.validation_notes = result['validation_notes']
        check.save()
        
        # Log validation
        self._log_validation(check.id, 'comprehension_check', 'ai_validation',
                           'PASSED' if result['is_valid'] else 'FAILED', result)
        
        return result['is_valid']
    
    def _create_validation_prompt(self, content: str, content_type: str, topic: str) -> str:
        """Create an optimized validation prompt."""
        return f"""Validate this {content_type} content about "{topic}":

Content: "{content}"

Check for:
1. Accuracy - Is the information correct?
2. Clarity - Is it clear and understandable?
3. Appropriateness - Is it suitable for educational use?
4. Completeness - Does it fully address the topic?

Respond with:
- "VALID" if the content passes all checks
- "INVALID: [reason]" if there are issues

Keep your response concise and specific."""
    
    def _parse_validation_result(self, result: str) -> bool:
        """Parse the validation result to determine if content is valid."""
        result_lower = result.lower().strip()
        return result_lower.startswith('valid')
    
    def _log_validation(self, content_id: str, content_type: str, validation_type: str, 
                       status: str, details: Dict[str, Any]):
        """Log validation attempt."""
        try:
            ValidationLog.objects.create(
                content_id=content_id,
                content_type=content_type,
                validation_type=validation_type,
                status=status,
                details=details
            )
        except Exception as e:
            logger.error(f"Failed to log validation: {e}")


def validate_learning_objective(learning_objective) -> Dict[str, Any]:
    """
    Validate all components of a learning objective.
    Simplified version for MVP.
    """
    service = SimplifiedQualityControlService()
    
    validation_results = {
        'learning_objective_id': str(learning_objective.id),
        'components_validated': 0,
        'components_passed': 0,
        'components_failed': 0,
        'checks_validated': 0,
        'checks_passed': 0,
        'checks_failed': 0,
        'overall_status': 'PENDING'
    }
    
    # Validate knowledge components
    for component in learning_objective.knowledge_components.all():
        validation_results['components_validated'] += 1
        if service.validate_knowledge_component(component):
            validation_results['components_passed'] += 1
        else:
            validation_results['components_failed'] += 1
    
    # Validate comprehension checks
    for check in learning_objective.comprehension_checks.all():
        validation_results['checks_validated'] += 1
        if service.validate_comprehension_check(check):
            validation_results['checks_passed'] += 1
        else:
            validation_results['checks_failed'] += 1
    
    # Determine overall status
    total_components = validation_results['components_validated']
    total_checks = validation_results['checks_validated']
    total_passed = validation_results['components_passed'] + validation_results['checks_passed']
    total_items = total_components + total_checks
    
    if total_items == 0:
        validation_results['overall_status'] = 'NO_CONTENT'
    elif total_passed == total_items:
        validation_results['overall_status'] = 'ALL_PASSED'
        learning_objective.status = 'READY'
    elif total_passed >= total_items * 0.8:  # 80% pass rate
        validation_results['overall_status'] = 'MOSTLY_PASSED'
        learning_objective.status = 'READY'
    else:
        validation_results['overall_status'] = 'NEEDS_REVIEW'
        learning_objective.status = 'DRAFT'
    
    learning_objective.save()
    
    logger.info(f"Validation complete for {learning_objective.title}: {validation_results['overall_status']}")
    return validation_results
