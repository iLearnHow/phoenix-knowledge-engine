"""
API serializers for the Phoenix Knowledge Engine.
"""

from rest_framework import serializers
from database.models import (
    LearningObjective, KnowledgeComponent, ComprehensionCheck,
    GenerationQueue, ValidationLog, GenerationLog
)


class LearningObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for LearningObjective model."""
    
    knowledge_components_count = serializers.SerializerMethodField()
    comprehension_checks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningObjective
        fields = [
            'id', 'title', 'core_question', 'summary', 'status',
            'created_at', 'updated_at', 'completed_at',
            'knowledge_components_count', 'comprehension_checks_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    
    def get_knowledge_components_count(self, obj):
        return obj.knowledge_components.count()
    
    def get_comprehension_checks_count(self, obj):
        return obj.comprehension_checks.count()


class KnowledgeComponentSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeComponent model."""
    
    class Meta:
        model = KnowledgeComponent
        fields = [
            'id', 'learning_objective', 'type', 'content', 'sort_order',
            'validation_status', 'validation_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ComprehensionCheckSerializer(serializers.ModelSerializer):
    """Serializer for ComprehensionCheck model."""
    
    class Meta:
        model = ComprehensionCheck
        fields = [
            'id', 'learning_objective', 'question_text', 'options',
            'correct_index', 'explanation', 'validation_status',
            'validation_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GenerationQueueSerializer(serializers.ModelSerializer):
    """Serializer for GenerationQueue model."""
    
    class Meta:
        model = GenerationQueue
        fields = [
            'id', 'topic', 'priority', 'status', 'error_message',
            'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'started_at', 'completed_at']


class ValidationLogSerializer(serializers.ModelSerializer):
    """Serializer for ValidationLog model."""
    
    class Meta:
        model = ValidationLog
        fields = [
            'id', 'content_id', 'content_type', 'validation_type',
            'status', 'details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GenerationLogSerializer(serializers.ModelSerializer):
    """Serializer for GenerationLog model."""
    
    class Meta:
        model = GenerationLog
        fields = [
            'id', 'learning_objective', 'prompt_used', 'ai_response',
            'generation_time', 'tokens_used', 'success', 'error_message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ContentGenerationRequestSerializer(serializers.Serializer):
    """Serializer for content generation requests."""
    
    topic = serializers.CharField(max_length=255, help_text="The topic to generate content for")
    priority = serializers.IntegerField(default=0, help_text="Priority level (higher = more urgent)")


class ContentGenerationResponseSerializer(serializers.Serializer):
    """Serializer for content generation responses."""
    
    learning_objective = LearningObjectiveSerializer()
    knowledge_components = KnowledgeComponentSerializer(many=True)
    comprehension_check = ComprehensionCheckSerializer()
    status = serializers.CharField()
    message = serializers.CharField()


class ValidationRequestSerializer(serializers.Serializer):
    """Serializer for validation requests."""
    
    learning_objective_id = serializers.UUIDField(help_text="ID of the learning objective to validate")


class ValidationResponseSerializer(serializers.Serializer):
    """Serializer for validation responses."""
    
    learning_objective = serializers.DictField()
    knowledge_components = serializers.ListField()
    comprehension_checks = serializers.ListField()
    overall_valid = serializers.BooleanField()
    status = serializers.CharField()
