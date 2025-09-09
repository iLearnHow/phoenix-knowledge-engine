"""
URL configuration for the Phoenix Knowledge Engine API.
"""

from django.urls import path
from api import views

urlpatterns = [
    # Content generation
    path('generate/', views.ContentGenerationView.as_view(), name='content_generation'),
    
    # Learning objectives
    path('learning-objectives/', views.LearningObjectiveListView.as_view(), name='learning_objective_list'),
    path('learning-objectives/<uuid:learning_objective_id>/', views.LearningObjectiveDetailView.as_view(), name='learning_objective_detail'),
    
    # Validation
    path('validate/', views.ValidationView.as_view(), name='validation'),
    
    # System endpoints
    path('health/', views.health_check, name='health_check'),
    path('stats/', views.stats, name='stats'),
]
