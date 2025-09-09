"""
Simplified URL Configuration
Clean, focused API endpoints for the MVP
"""

from django.urls import path
from . import simplified_views

urlpatterns = [
    # Content Generation
    path('generate/', simplified_views.generate_content, name='generate_content'),
    path('test-avatars/', simplified_views.test_avatar_comparison, name='test_avatar_comparison'),
    
    # Avatar Management
    path('avatars/', simplified_views.get_avatars, name='get_avatars'),
    path('avatar-recommendation/', simplified_views.get_avatar_recommendation, name='get_avatar_recommendation'),
    
    # Monitoring
    path('cost-summary/', simplified_views.get_cost_summary, name='get_cost_summary'),
    path('health/', simplified_views.health_check, name='health_check'),
]
