"""
Simplified API Views
Clean, focused API endpoints for the MVP
"""

import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from core.orchestrator.service import orchestrate_content_generation
from core.worker.service import process_knowledge_components, process_comprehension_check
from core.quality_control.service import validate_learning_objective
from content.text.generator import generate_lesson_with_avatar
from avatars.service import avatar_service, AvatarType
from monitoring.cost_monitor import cost_monitor

logger = logging.getLogger('phoenix.api')


@api_view(['POST'])
def generate_content(request):
    """
    Generate educational content for a topic.
    Simplified endpoint for MVP.
    """
    try:
        topic = request.data.get('topic')
        avatar_preference = request.data.get('avatar', 'auto')  # auto, kelly, ken
        
        if not topic:
            return Response(
                {'error': 'Topic is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"Generating content for topic: {topic}")
        
        # Generate content using simplified system
        result = generate_lesson_with_avatar(topic, avatar_preference)
        
        if result['success']:
            return Response({
                'status': 'success',
                'topic': topic,
                'avatar_used': result['avatar_used'],
                'content': result
            })
        else:
            return Response({
                'status': 'error',
                'error': result.get('error', 'Unknown error')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error in generate_content: {e}")
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_avatars(request):
    """
    Get available avatars and their information.
    """
    try:
        avatars = avatar_service.get_available_avatars()
        
        avatar_info = []
        for avatar_name in avatars:
            if avatar_name == "Kelly":
                avatar_type = AvatarType.KELLY
            else:
                avatar_type = AvatarType.KEN
            
            avatar = avatar_service.get_avatar(avatar_type)
            avatar_info.append({
                'name': avatar.name,
                'description': avatar.description,
                'specialty': avatar.specialty,
                'voice_style': avatar.voice_style
            })
        
        return Response({
            'avatars': avatar_info
        })
        
    except Exception as e:
        logger.error(f"Error in get_avatars: {e}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_avatar_recommendation(request):
    """
    Get avatar recommendation for a topic.
    """
    try:
        topic = request.GET.get('topic')
        if not topic:
            return Response(
                {'error': 'Topic parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        recommendation = avatar_service.get_avatar_recommendation(topic)
        
        return Response(recommendation)
        
    except Exception as e:
        logger.error(f"Error in get_avatar_recommendation: {e}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_cost_summary(request):
    """
    Get cost monitoring summary.
    """
    try:
        days = int(request.GET.get('days', 7))
        summary = cost_monitor.get_usage_summary(days)
        
        return Response({
            'summary': summary,
            'budget_limits': {
                'daily': cost_monitor.daily_limit,
                'monthly': cost_monitor.monthly_limit
            }
        })
        
    except Exception as e:
        logger.error(f"Error in get_cost_summary: {e}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for monitoring.
    """
    try:
        return Response({
            'status': 'healthy',
            'timestamp': str(datetime.now()),
            'version': '1.0.0'
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def test_avatar_comparison(request):
    """
    Test endpoint to compare both avatars on the same topic.
    """
    try:
        topic = request.data.get('topic')
        if not topic:
            return Response(
                {'error': 'Topic is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate with both avatars
        kelly_result = generate_lesson_with_avatar(topic, 'kelly')
        ken_result = generate_lesson_with_avatar(topic, 'ken')
        
        return Response({
            'topic': topic,
            'kelly': kelly_result,
            'ken': ken_result,
            'comparison': {
                'kelly_approach': 'Academic, methodical, detailed',
                'ken_approach': 'Practical, hands-on, immediate application'
            }
        })
        
    except Exception as e:
        logger.error(f"Error in test_avatar_comparison: {e}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
