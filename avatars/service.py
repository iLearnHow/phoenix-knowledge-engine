"""
Simplified Avatar Service
Manages Kelly and Ken avatars with distinct personalities
"""

from typing import Dict, Any, Optional
from enum import Enum
import logging

from .kelly.personality import KellyPersonality
from .ken.personality import KenPersonality

logger = logging.getLogger(__name__)


class AvatarType(Enum):
    KELLY = "kelly"
    KEN = "ken"


class SimplifiedAvatarService:
    """Simplified service for managing Kelly and Ken avatars"""
    
    def __init__(self):
        self.avatars = {
            AvatarType.KELLY: KellyPersonality(),
            AvatarType.KEN: KenPersonality()
        }
    
    def get_avatar(self, avatar_type: AvatarType):
        """Get avatar personality by type"""
        return self.avatars.get(avatar_type)
    
    def get_available_avatars(self) -> list:
        """Get list of available avatars"""
        return [avatar.name for avatar in self.avatars.values()]
    
    def select_avatar_for_topic(self, topic: str, subject_area: str = None) -> AvatarType:
        """Select the best avatar for a given topic"""
        # Simple heuristic for avatar selection
        academic_subjects = [
            "mathematics", "physics", "chemistry", "biology", "history", 
            "literature", "philosophy", "theoretical", "research", "analysis"
        ]
        
        practical_subjects = [
            "programming", "engineering", "business", "marketing", "design",
            "cooking", "fitness", "crafts", "technology", "application"
        ]
        
        topic_lower = topic.lower()
        subject_lower = (subject_area or "").lower()
        
        # Check if topic or subject area suggests academic focus
        if any(term in topic_lower or term in subject_lower for term in academic_subjects):
            return AvatarType.KELLY
        
        # Check if topic or subject area suggests practical focus
        elif any(term in topic_lower or term in subject_lower for term in practical_subjects):
            return AvatarType.KEN
        
        # Default to Kelly for general educational content
        else:
            return AvatarType.KELLY
    
    def get_avatar_response(self, 
                          avatar_type: AvatarType,
                          topic: str,
                          content_type: str = None,
                          additional_context: str = None) -> Dict[str, Any]:
        """Get a response from the specified avatar"""
        
        avatar = self.get_avatar(avatar_type)
        if not avatar:
            raise ValueError(f"Unknown avatar type: {avatar_type}")
        
        # Build response context
        response_context = {
            "avatar_name": avatar.name,
            "avatar_description": avatar.description,
            "specialty": avatar.specialty,
            "system_prompt": avatar.get_system_prompt(),
            "voice_config": avatar.get_voice_config(),
            "topic": topic,
            "content_type": content_type
        }
        
        # Add content-specific modifiers
        if content_type:
            response_context["prompt_modifier"] = avatar.get_prompt_modifier(content_type)
            response_context["quiz_style"] = avatar.get_quiz_style()
        
        if additional_context:
            response_context["additional_context"] = additional_context
        
        return response_context
    
    def get_dual_avatar_response(self, 
                               topic: str,
                               content_type: str = None) -> Dict[str, Any]:
        """Get responses from both avatars for comparison"""
        
        kelly_response = self.get_avatar_response(
            AvatarType.KELLY, topic, content_type
        )
        
        ken_response = self.get_avatar_response(
            AvatarType.KEN, topic, content_type
        )
        
        return {
            "kelly": kelly_response,
            "ken": ken_response,
            "comparison": {
                "kelly_approach": "Academic, methodical, detailed",
                "ken_approach": "Practical, hands-on, immediate application",
                "recommended_for": {
                    "kelly": "Complex theoretical topics, academic subjects, detailed explanations",
                    "ken": "Practical skills, real-world applications, hands-on learning"
                }
            }
        }
    
    def get_avatar_recommendation(self, topic: str, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get avatar recommendation based on topic and user preferences"""
        
        # Select avatar based on topic
        recommended_avatar = self.select_avatar_for_topic(topic)
        
        # Get both avatars for comparison
        dual_response = self.get_dual_avatar_response(topic)
        
        recommendation = {
            "recommended_avatar": recommended_avatar.value,
            "reasoning": f"Selected {recommended_avatar.value} based on topic analysis",
            "alternatives": {
                "kelly": "Choose Kelly for academic, detailed approach",
                "ken": "Choose Ken for practical, hands-on approach"
            },
            "both_avatars": dual_response
        }
        
        if user_preferences:
            # Consider user preferences in recommendation
            if user_preferences.get("learning_style") == "practical":
                recommendation["recommended_avatar"] = "ken"
                recommendation["reasoning"] = "User prefers practical learning style"
            elif user_preferences.get("learning_style") == "academic":
                recommendation["recommended_avatar"] = "kelly"
                recommendation["reasoning"] = "User prefers academic learning style"
        
        return recommendation


# Global instance
avatar_service = SimplifiedAvatarService()
