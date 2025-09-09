"""
Database models for the Phoenix Knowledge Engine.
Based on the technical architecture specifications.
"""

import uuid
from django.db import models
from django.utils import timezone


class LearningObjective(models.Model):
    """
    Core learning objective that serves as the main entity.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('GENERATING', 'Generating'),
        ('READY', 'Ready'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="The main topic or concept")
    core_question = models.TextField(help_text="The central question this objective addresses")
    summary = models.TextField(help_text="Brief summary of the learning objective")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.status})"


class KnowledgeComponent(models.Model):
    """
    Atomic knowledge components that make up a learning objective.
    """
    TYPE_CHOICES = [
        ('CORE_CONCEPT', 'Core Concept'),
        ('FACT', 'Fact'),
        ('EXAMPLE', 'Example'),
        ('PRINCIPLE', 'Principle'),
        ('ANALOGY', 'Analogy'),
        ('WARNING', 'Warning'),
    ]
    
    VALIDATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
        ('REJECTED', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_objective = models.ForeignKey(
        LearningObjective, 
        on_delete=models.CASCADE, 
        related_name='knowledge_components'
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content = models.TextField(help_text="The actual content of this component")
    sort_order = models.IntegerField(help_text="Order of this component within the objective")
    validation_status = models.CharField(
        max_length=20, 
        choices=VALIDATION_STATUS_CHOICES, 
        default='PENDING'
    )
    validation_notes = models.TextField(blank=True, help_text="Notes from validation process")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['learning_objective', 'sort_order']
        indexes = [
            models.Index(fields=['learning_objective', 'type']),
            models.Index(fields=['validation_status']),
            models.Index(fields=['learning_objective', 'sort_order']),
        ]
    
    def __str__(self):
        return f"{self.learning_objective.title} - {self.get_type_display()}"


class ComprehensionCheck(models.Model):
    """
    Assessment components for testing understanding.
    """
    VALIDATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
        ('REJECTED', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_objective = models.ForeignKey(
        LearningObjective, 
        on_delete=models.CASCADE, 
        related_name='comprehension_checks'
    )
    question_text = models.TextField(help_text="The question text")
    options = models.JSONField(help_text="Array of answer options")
    correct_index = models.IntegerField(help_text="Index of the correct answer")
    explanation = models.TextField(help_text="Explanation of why the correct answer is right")
    validation_status = models.CharField(
        max_length=20, 
        choices=VALIDATION_STATUS_CHOICES, 
        default='PENDING'
    )
    validation_notes = models.TextField(blank=True, help_text="Notes from validation process")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['learning_objective', 'created_at']
        indexes = [
            models.Index(fields=['learning_objective']),
            models.Index(fields=['validation_status']),
        ]
    
    def __str__(self):
        return f"{self.learning_objective.title} - Question"


class GenerationQueue(models.Model):
    """
    Queue for managing content generation tasks.
    """
    STATUS_CHOICES = [
        ('QUEUED', 'Queued'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=255, help_text="The topic to generate content for")
    priority = models.IntegerField(default=0, help_text="Priority level (higher = more urgent)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUEUED')
    error_message = models.TextField(blank=True, help_text="Error message if generation failed")
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', 'created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.topic} ({self.status})"


class ValidationLog(models.Model):
    """
    Log of validation attempts and results.
    """
    STATUS_CHOICES = [
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('WARNING', 'Warning'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_id = models.UUIDField(help_text="ID of the content being validated")
    content_type = models.CharField(max_length=50, help_text="Type of content (knowledge_component, comprehension_check)")
    validation_type = models.CharField(max_length=50, help_text="Type of validation performed")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    details = models.JSONField(help_text="Additional validation details")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_id']),
            models.Index(fields=['validation_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.content_type} - {self.validation_type} ({self.status})"


class AIPrompt(models.Model):
    """
    Store AI prompts and their configurations for different tasks.
    """
    PROMPT_TYPE_CHOICES = [
        ('ORCHESTRATOR', 'Orchestrator'),
        ('WORKER', 'Worker'),
        ('QUALITY_CONTROL', 'Quality Control'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    prompt_type = models.CharField(max_length=50, choices=PROMPT_TYPE_CHOICES)
    template = models.TextField(help_text="The prompt template with placeholders")
    variables = models.JSONField(default=list, help_text="List of required variables for this prompt")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['prompt_type', 'name']
        indexes = [
            models.Index(fields=['prompt_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_prompt_type_display()} - {self.name}"


class GenerationLog(models.Model):
    """
    Log of AI generation attempts and results.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_objective = models.ForeignKey(
        LearningObjective, 
        on_delete=models.CASCADE, 
        related_name='generation_logs'
    )
    prompt_used = models.TextField(help_text="The prompt that was sent to the AI")
    ai_response = models.TextField(help_text="The response from the AI")
    generation_time = models.FloatField(help_text="Time taken for generation in seconds")
    tokens_used = models.IntegerField(help_text="Number of tokens used")
    success = models.BooleanField(help_text="Whether the generation was successful")
    error_message = models.TextField(blank=True, help_text="Error message if generation failed")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['learning_objective']),
            models.Index(fields=['success']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.learning_objective.title} - Generation Log"
