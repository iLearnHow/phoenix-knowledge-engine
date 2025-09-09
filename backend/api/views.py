"""
API views for the Phoenix Knowledge Engine.
"""

import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from database.models import LearningObjective, KnowledgeComponent, ComprehensionCheck
from api.serializers import (
    LearningObjectiveSerializer, KnowledgeComponentSerializer,
    ComprehensionCheckSerializer, ContentGenerationRequestSerializer,
    ContentGenerationResponseSerializer, ValidationRequestSerializer,
    ValidationResponseSerializer
)
from orchestrator.service import orchestrate_content_generation
from worker.service import process_knowledge_components
from quality_control.service import validate_all_content

logger = logging.getLogger('phoenix.api')


class ContentGenerationView(APIView):
    """
    API view for generating educational content.
    """
    
    def post(self, request):
        """
        Generate content for a given topic.
        
        POST /api/generate/
        {
            "topic": "The Pythagorean Theorem",
            "priority": 1
        }
        """
        try:
            serializer = ContentGenerationRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            topic = serializer.validated_data['topic']
            priority = serializer.validated_data.get('priority', 0)
            
            logger.info(f"Received content generation request for topic: {topic}")
            
            # Orchestrate content generation
            orchestration_result = orchestrate_content_generation(topic)
            
            if orchestration_result['status'] == 'error':
                return Response({
                    'status': 'error',
                    'message': orchestration_result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            learning_objective = orchestration_result['learning_objective']
            knowledge_components_plan = orchestration_result['knowledge_components_plan']
            comprehension_check_plan = orchestration_result['comprehension_check_plan']
            
            # Process knowledge components
            worker_result = process_knowledge_components(
                str(learning_objective.id), 
                knowledge_components_plan
            )
            
            if worker_result['status'] == 'error':
                return Response({
                    'status': 'error',
                    'message': worker_result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Serialize response
            response_data = {
                'learning_objective': LearningObjectiveSerializer(learning_objective).data,
                'knowledge_components': KnowledgeComponentSerializer(
                    worker_result['knowledge_components'], many=True
                ).data,
                'comprehension_check': ComprehensionCheckSerializer(
                    worker_result['comprehension_check']
                ).data,
                'status': 'success',
                'message': 'Content generated successfully'
            }
            
            logger.info(f"Successfully generated content for topic: {topic}")
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LearningObjectiveListView(APIView):
    """
    API view for listing learning objectives.
    """
    
    def get(self, request):
        """
        Get a list of learning objectives.
        
        GET /api/learning-objectives/
        Query parameters:
        - status: Filter by status (DRAFT, GENERATING, READY, FAILED)
        - search: Search in title and core_question
        - page: Page number for pagination
        - page_size: Number of items per page
        """
        try:
            queryset = LearningObjective.objects.all()
            
            # Filter by status
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            # Search functionality
            search_query = request.query_params.get('search')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(core_question__icontains=search_query) |
                    Q(summary__icontains=search_query)
                )
            
            # Pagination
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            start = (page - 1) * page_size
            end = start + page_size
            
            total_count = queryset.count()
            learning_objectives = queryset[start:end]
            
            serializer = LearningObjectiveSerializer(learning_objectives, many=True)
            
            return Response({
                'results': serializer.data,
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_count + page_size - 1) // page_size
            })
            
        except Exception as e:
            logger.error(f"Error listing learning objectives: {e}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LearningObjectiveDetailView(APIView):
    """
    API view for individual learning objectives.
    """
    
    def get(self, request, learning_objective_id):
        """
        Get a specific learning objective with all its components.
        
        GET /api/learning-objectives/{id}/
        """
        try:
            learning_objective = get_object_or_404(LearningObjective, id=learning_objective_id)
            
            # Get all related components
            knowledge_components = learning_objective.knowledge_components.all()
            comprehension_checks = learning_objective.comprehension_checks.all()
            
            response_data = {
                'learning_objective': LearningObjectiveSerializer(learning_objective).data,
                'knowledge_components': KnowledgeComponentSerializer(
                    knowledge_components, many=True
                ).data,
                'comprehension_checks': ComprehensionCheckSerializer(
                    comprehension_checks, many=True
                ).data
            }
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Error getting learning objective {learning_objective_id}: {e}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidationView(APIView):
    """
    API view for validating content.
    """
    
    def post(self, request):
        """
        Validate all content for a learning objective.
        
        POST /api/validate/
        {
            "learning_objective_id": "uuid-string"
        }
        """
        try:
            serializer = ValidationRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            learning_objective_id = serializer.validated_data['learning_objective_id']
            
            logger.info(f"Received validation request for learning objective: {learning_objective_id}")
            
            # Validate all content
            validation_result = validate_all_content(str(learning_objective_id))
            
            if validation_result['status'] == 'error':
                return Response({
                    'status': 'error',
                    'message': validation_result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            logger.info(f"Successfully validated content for learning objective: {learning_objective_id}")
            return Response(validation_result)
            
        except Exception as e:
            logger.error(f"Error in validation: {e}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint.
    
    GET /api/health/
    """
    return Response({
        'status': 'healthy',
        'message': 'Phoenix Knowledge Engine API is running'
    })


@api_view(['GET'])
def stats(request):
    """
    Get system statistics.
    
    GET /api/stats/
    """
    try:
        stats_data = {
            'learning_objectives': {
                'total': LearningObjective.objects.count(),
                'draft': LearningObjective.objects.filter(status='DRAFT').count(),
                'generating': LearningObjective.objects.filter(status='GENERATING').count(),
                'ready': LearningObjective.objects.filter(status='READY').count(),
                'failed': LearningObjective.objects.filter(status='FAILED').count(),
            },
            'knowledge_components': {
                'total': KnowledgeComponent.objects.count(),
                'pending': KnowledgeComponent.objects.filter(validation_status='PENDING').count(),
                'approved': KnowledgeComponent.objects.filter(validation_status='APPROVED').count(),
                'flagged': KnowledgeComponent.objects.filter(validation_status='FLAGGED').count(),
                'rejected': KnowledgeComponent.objects.filter(validation_status='REJECTED').count(),
            },
            'comprehension_checks': {
                'total': ComprehensionCheck.objects.count(),
                'pending': ComprehensionCheck.objects.filter(validation_status='PENDING').count(),
                'approved': ComprehensionCheck.objects.filter(validation_status='APPROVED').count(),
                'flagged': ComprehensionCheck.objects.filter(validation_status='FLAGGED').count(),
                'rejected': ComprehensionCheck.objects.filter(validation_status='REJECTED').count(),
            }
        }
        
        return Response(stats_data)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
