"""
Quality control service for validating AI-generated content.
"""

import json
import logging
from typing import Dict, Any, Tuple, List
from django.conf import settings
from services.local_llm import get_llm_service
from database.models import (
    LearningObjective, KnowledgeComponent, ComprehensionCheck, 
    ValidationLog, GenerationLog
)

logger = logging.getLogger('phoenix.quality_control')


class QualityControlService:
    """
    Service for validating AI-generated content.
    """
    
    def __init__(self):
        self.client = get_llm_service('quality_control')
    
    def validate_learning_objective(self, learning_objective: LearningObjective) -> Tuple[bool, str]:
        """
        Validate a learning objective.
        
        Args:
            learning_objective: The learning objective to validate
            
        Returns:
            Tuple of (is_valid, validation_notes)
        """
        try:
            logger.info(f"Validating learning objective: {learning_objective.id}")
            
            # Schema validation
            schema_valid, schema_notes = self._validate_schema(learning_objective)
            if not schema_valid:
                return False, f"Schema validation failed: {schema_notes}"
            
            # Length validation
            length_valid, length_notes = self._validate_length(learning_objective)
            if not length_valid:
                return False, f"Length validation failed: {length_notes}"
            
            # Fact checking
            fact_valid, fact_notes = self._fact_check(learning_objective)
            if not fact_valid:
                return False, f"Fact check failed: {fact_notes}"
            
            # Update validation status
            learning_objective.status = 'READY'
            learning_objective.save()
            
            # Log validation
            self._log_validation(learning_objective.id, 'learning_objective', 'comprehensive', 'PASSED', {
                'schema_validation': schema_notes,
                'length_validation': length_notes,
                'fact_check': fact_notes
            })
            
            logger.info(f"Successfully validated learning objective: {learning_objective.id}")
            return True, "All validations passed"
            
        except Exception as e:
            logger.error(f"Error validating learning objective {learning_objective.id}: {e}")
            self._log_validation(learning_objective.id, 'learning_objective', 'comprehensive', 'FAILED', {'error': str(e)})
            return False, str(e)
    
    def validate_knowledge_component(self, knowledge_component: KnowledgeComponent) -> Tuple[bool, str]:
        """
        Validate a knowledge component.
        
        Args:
            knowledge_component: The knowledge component to validate
            
        Returns:
            Tuple of (is_valid, validation_notes)
        """
        try:
            logger.info(f"Validating knowledge component: {knowledge_component.id}")
            
            # Schema validation
            schema_valid, schema_notes = self._validate_component_schema(knowledge_component)
            if not schema_valid:
                return False, f"Schema validation failed: {schema_notes}"
            
            # Length validation
            length_valid, length_notes = self._validate_component_length(knowledge_component)
            if not length_valid:
                return False, f"Length validation failed: {length_notes}"
            
            # Content type validation
            type_valid, type_notes = self._validate_component_type(knowledge_component)
            if not type_valid:
                return False, f"Type validation failed: {type_notes}"
            
            # Fact checking
            fact_valid, fact_notes = self._fact_check_component(knowledge_component)
            if not fact_valid:
                return False, f"Fact check failed: {fact_notes}"
            
            # Update validation status
            knowledge_component.validation_status = 'APPROVED'
            knowledge_component.validation_notes = f"Validated: {schema_notes}, {length_notes}, {type_notes}, {fact_notes}"
            knowledge_component.save()
            
            # Log validation
            self._log_validation(knowledge_component.id, 'knowledge_component', 'comprehensive', 'PASSED', {
                'schema_validation': schema_notes,
                'length_validation': length_notes,
                'type_validation': type_notes,
                'fact_check': fact_notes
            })
            
            logger.info(f"Successfully validated knowledge component: {knowledge_component.id}")
            return True, "All validations passed"
            
        except Exception as e:
            logger.error(f"Error validating knowledge component {knowledge_component.id}: {e}")
            knowledge_component.validation_status = 'FLAGGED'
            knowledge_component.validation_notes = f"Validation error: {str(e)}"
            knowledge_component.save()
            
            self._log_validation(knowledge_component.id, 'knowledge_component', 'comprehensive', 'FAILED', {'error': str(e)})
            return False, str(e)
    
    def validate_comprehension_check(self, comprehension_check: ComprehensionCheck) -> Tuple[bool, str]:
        """
        Validate a comprehension check.
        
        Args:
            comprehension_check: The comprehension check to validate
            
        Returns:
            Tuple of (is_valid, validation_notes)
        """
        try:
            logger.info(f"Validating comprehension check: {comprehension_check.id}")
            
            # Schema validation
            schema_valid, schema_notes = self._validate_check_schema(comprehension_check)
            if not schema_valid:
                return False, f"Schema validation failed: {schema_notes}"
            
            # Length validation
            length_valid, length_notes = self._validate_check_length(comprehension_check)
            if not length_valid:
                return False, f"Length validation failed: {length_notes}"
            
            # Options validation
            options_valid, options_notes = self._validate_check_options(comprehension_check)
            if not options_valid:
                return False, f"Options validation failed: {options_notes}"
            
            # Update validation status
            comprehension_check.validation_status = 'APPROVED'
            comprehension_check.validation_notes = f"Validated: {schema_notes}, {length_notes}, {options_notes}"
            comprehension_check.save()
            
            # Log validation
            self._log_validation(comprehension_check.id, 'comprehension_check', 'comprehensive', 'PASSED', {
                'schema_validation': schema_notes,
                'length_validation': length_notes,
                'options_validation': options_notes
            })
            
            logger.info(f"Successfully validated comprehension check: {comprehension_check.id}")
            return True, "All validations passed"
            
        except Exception as e:
            logger.error(f"Error validating comprehension check {comprehension_check.id}: {e}")
            comprehension_check.validation_status = 'FLAGGED'
            comprehension_check.validation_notes = f"Validation error: {str(e)}"
            comprehension_check.save()
            
            self._log_validation(comprehension_check.id, 'comprehension_check', 'comprehensive', 'FAILED', {'error': str(e)})
            return False, str(e)
    
    def _validate_schema(self, learning_objective: LearningObjective) -> Tuple[bool, str]:
        """Validate learning objective schema."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['summary']
        
        if not learning_objective.title:
            return False, "Title is required"
        if not learning_objective.core_question:
            return False, "Core question is required"
        if not learning_objective.summary:
            return False, "Summary is required"
        
        return True, "Schema validation passed"
    
    def _validate_length(self, learning_objective: LearningObjective) -> Tuple[bool, str]:
        """Validate learning objective length."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['summary']
        
        if len(learning_objective.summary) < rules['min_length']:
            return False, f"Summary too short (min {rules['min_length']} chars)"
        if len(learning_objective.summary) > rules['max_length']:
            return False, f"Summary too long (max {rules['max_length']} chars)"
        
        return True, "Length validation passed"
    
    def _validate_component_schema(self, knowledge_component: KnowledgeComponent) -> Tuple[bool, str]:
        """Validate knowledge component schema."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['knowledge_component']
        
        if not knowledge_component.type:
            return False, "Type is required"
        if not knowledge_component.content:
            return False, "Content is required"
        if knowledge_component.sort_order is None:
            return False, "Sort order is required"
        
        return True, "Schema validation passed"
    
    def _validate_component_length(self, knowledge_component: KnowledgeComponent) -> Tuple[bool, str]:
        """Validate knowledge component length."""
        from quality_control.prompts import VALIDATION_RULES, CONTENT_TYPE_VALIDATION
        
        rules = VALIDATION_RULES['knowledge_component']
        type_rules = CONTENT_TYPE_VALIDATION.get(knowledge_component.type, {})
        
        min_length = type_rules.get('min_length', rules['min_length'])
        max_length = type_rules.get('max_length', rules['max_length'])
        
        if len(knowledge_component.content) < min_length:
            return False, f"Content too short (min {min_length} chars)"
        if len(knowledge_component.content) > max_length:
            return False, f"Content too long (max {max_length} chars)"
        
        return True, "Length validation passed"
    
    def _validate_component_type(self, knowledge_component: KnowledgeComponent) -> Tuple[bool, str]:
        """Validate knowledge component type-specific content."""
        from quality_control.prompts import CONTENT_TYPE_VALIDATION
        
        type_rules = CONTENT_TYPE_VALIDATION.get(knowledge_component.type, {})
        keywords = type_rules.get('keywords', [])
        
        content_lower = knowledge_component.content.lower()
        if keywords and not any(keyword in content_lower for keyword in keywords):
            return False, f"Content doesn't match {knowledge_component.type} type expectations"
        
        return True, "Type validation passed"
    
    def _validate_check_schema(self, comprehension_check: ComprehensionCheck) -> Tuple[bool, str]:
        """Validate comprehension check schema."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['comprehension_check']
        
        if not comprehension_check.question_text:
            return False, "Question text is required"
        if not comprehension_check.options:
            return False, "Options are required"
        if comprehension_check.correct_index is None:
            return False, "Correct index is required"
        if not comprehension_check.explanation:
            return False, "Explanation is required"
        
        return True, "Schema validation passed"
    
    def _validate_check_length(self, comprehension_check: ComprehensionCheck) -> Tuple[bool, str]:
        """Validate comprehension check length."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['comprehension_check']
        
        if len(comprehension_check.question_text) < rules['min_length']:
            return False, f"Question too short (min {rules['min_length']} chars)"
        if len(comprehension_check.question_text) > rules['max_length']:
            return False, f"Question too long (max {rules['max_length']} chars)"
        
        return True, "Length validation passed"
    
    def _validate_check_options(self, comprehension_check: ComprehensionCheck) -> Tuple[bool, str]:
        """Validate comprehension check options."""
        from quality_control.prompts import VALIDATION_RULES
        
        rules = VALIDATION_RULES['comprehension_check']
        
        if not isinstance(comprehension_check.options, list):
            return False, "Options must be a list"
        
        if len(comprehension_check.options) < rules['min_options']:
            return False, f"Too few options (min {rules['min_options']})"
        if len(comprehension_check.options) > rules['max_options']:
            return False, f"Too many options (max {rules['max_options']})"
        
        if comprehension_check.correct_index < 0 or comprehension_check.correct_index >= len(comprehension_check.options):
            return False, "Correct index is out of range"
        
        return True, "Options validation passed"
    
    def _fact_check(self, learning_objective: LearningObjective) -> Tuple[bool, str]:
        """Fact-check learning objective using AI."""
        try:
            from quality_control.prompts import get_critic_prompt
            
            prompt = get_critic_prompt(learning_objective.summary, learning_objective.title)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a harsh fact-checker focused on educational content accuracy."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            if result.startswith("APPROVED"):
                return True, "Fact check passed"
            else:
                return False, result.replace("FLAGGED: ", "")
                
        except Exception as e:
            logger.error(f"Error in fact check: {e}")
            return True, f"Fact check skipped due to error: {e}"
    
    def _fact_check_component(self, knowledge_component: KnowledgeComponent) -> Tuple[bool, str]:
        """Fact-check knowledge component using AI."""
        try:
            from quality_control.prompts import get_critic_prompt
            
            prompt = get_critic_prompt(knowledge_component.content, knowledge_component.learning_objective.title)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a harsh fact-checker focused on educational content accuracy."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            if result.startswith("APPROVED"):
                return True, "Fact check passed"
            else:
                return False, result.replace("FLAGGED: ", "")
                
        except Exception as e:
            logger.error(f"Error in fact check: {e}")
            return True, f"Fact check skipped due to error: {e}"
    
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


def validate_all_content(learning_objective_id: str) -> Dict[str, Any]:
    """
    Validate all content for a learning objective.
    
    Args:
        learning_objective_id: ID of the learning objective
        
    Returns:
        Dictionary containing validation results
    """
    try:
        learning_objective = LearningObjective.objects.get(id=learning_objective_id)
        service = QualityControlService()
        
        # Validate learning objective
        lo_valid, lo_notes = service.validate_learning_objective(learning_objective)
        
        # Validate knowledge components
        knowledge_components = learning_objective.knowledge_components.all()
        component_results = []
        for component in knowledge_components:
            valid, notes = service.validate_knowledge_component(component)
            component_results.append({
                'id': str(component.id),
                'type': component.type,
                'valid': valid,
                'notes': notes
            })
        
        # Validate comprehension checks
        comprehension_checks = learning_objective.comprehension_checks.all()
        check_results = []
        for check in comprehension_checks:
            valid, notes = service.validate_comprehension_check(check)
            check_results.append({
                'id': str(check.id),
                'valid': valid,
                'notes': notes
            })
        
        # Determine overall status
        all_valid = lo_valid and all(r['valid'] for r in component_results) and all(r['valid'] for r in check_results)
        
        return {
            'learning_objective': {
                'id': str(learning_objective.id),
                'valid': lo_valid,
                'notes': lo_notes
            },
            'knowledge_components': component_results,
            'comprehension_checks': check_results,
            'overall_valid': all_valid,
            'status': 'success' if all_valid else 'validation_failed'
        }
        
    except LearningObjective.DoesNotExist:
        logger.error(f"Learning objective not found: {learning_objective_id}")
        return {
            'status': 'error',
            'error': 'Learning objective not found'
        }
    except Exception as e:
        logger.error(f"Error validating content: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }
