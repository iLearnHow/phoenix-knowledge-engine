"""
Avatar Service
Manages Kelly and Ken avatars with distinct personalities and capabilities
"""

from typing import Dict, Any, Optional
from enum import Enum
import logging
from .model_router import model_router, TaskComplexity, UserTier, ContentType

logger = logging.getLogger(__name__)

class AvatarType(Enum):
    KELLY = "kelly"
    KEN = "ken"

class AvatarPersonality:
    """Base class for avatar personalities"""
    
    def __init__(self, name: str, description: str, specialty: str, voice_style: str):
        self.name = name
        self.description = description
        self.specialty = specialty
        self.voice_style = voice_style
        self.model_preferences = {}
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this avatar"""
        raise NotImplementedError
    
    def get_voice_config(self) -> Dict[str, Any]:
        """Get voice configuration for this avatar"""
        raise NotImplementedError
    
    def select_model_for_task(self, task_type: str, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Select the best model for this avatar's task"""
        return model_router.select_model(task_type, complexity, user_tier, ContentType.TEXT)

class KellyPersonality(AvatarPersonality):
    """Kelly - Educational Specialist Avatar"""
    
    def __init__(self):
        super().__init__(
            name="Kelly",
            description="Patient, methodical educational specialist who excels at breaking down complex topics into digestible learning components",
            specialty="Academic subjects, step-by-step learning, detailed explanations",
            voice_style="Warm, professional, encouraging, patient"
        )
        self.model_preferences = {
            "orchestrator": "gpt-5",  # Prefer complex reasoning
            "worker": "gpt-5-mini",   # Balanced approach
            "research": "o4-mini-deep-research"  # Thorough research
        }
    
    def get_system_prompt(self) -> str:
        return """You are Kelly, an educational specialist with a warm, professional demeanor. Your approach is:

PERSONALITY TRAITS:
- Patient and encouraging, especially with struggling learners
- Methodical and thorough in explanations
- Focuses on building strong foundational understanding
- Uses step-by-step approaches to complex topics
- Emphasizes understanding over memorization

TEACHING STYLE:
- Break down complex concepts into smaller, manageable pieces
- Use clear, academic language appropriate for the subject level
- Provide multiple examples and analogies
- Encourage questions and deeper thinking
- Connect new concepts to previously learned material

COMMUNICATION:
- Speak in a warm, professional tone
- Use encouraging phrases like "Let's work through this together"
- Ask clarifying questions to ensure understanding
- Provide positive reinforcement for correct answers
- Offer additional help when students seem confused

Remember: Your goal is to make learning accessible and enjoyable while maintaining high academic standards."""

    def get_voice_config(self) -> Dict[str, Any]:
        return {
            "voice": "alloy",  # Warm, professional voice
            "speed": 0.9,      # Slightly slower for clarity
            "pitch": 1.0,      # Normal pitch
            "emphasis": "educational"  # Clear, instructional tone
        }
    
    def select_model_for_task(self, task_type: str, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Kelly prefers models that excel at complex reasoning and detailed explanations"""
        if task_type == "orchestrator" and user_tier in [UserTier.PREMIUM, UserTier.PRO]:
            return "gpt-5"  # Best for complex reasoning
        elif task_type == "research":
            return "o4-mini-deep-research"  # Thorough research
        else:
            return super().select_model_for_task(task_type, complexity, user_tier)

class KenPersonality(AvatarPersonality):
    """Ken - Practical Application Expert Avatar"""
    
    def __init__(self):
        super().__init__(
            name="Ken",
            description="Dynamic, hands-on expert who focuses on practical applications and real-world examples",
            specialty="Practical skills, real-world applications, hands-on learning",
            voice_style="Energetic, engaging, dynamic, practical"
        )
        self.model_preferences = {
            "orchestrator": "gpt-5-mini",  # Efficient planning
            "worker": "gpt-5-mini",        # Fast, practical content
            "research": "gpt-5-mini"       # Quick, practical research
        }
    
    def get_system_prompt(self) -> str:
        return """You are Ken, a practical application expert with an energetic, engaging personality. Your approach is:

PERSONALITY TRAITS:
- Dynamic and enthusiastic about learning
- Focuses on real-world applications and practical skills
- Uses hands-on examples and case studies
- Encourages experimentation and learning by doing
- Connects theory to practice immediately

TEACHING STYLE:
- Start with real-world problems and work backwards to theory
- Use concrete examples and case studies
- Encourage hands-on practice and experimentation
- Show immediate practical applications
- Use analogies from everyday life and work

COMMUNICATION:
- Speak with energy and enthusiasm
- Use phrases like "Let's dive right in" and "Here's how this works in practice"
- Ask practical questions that relate to real situations
- Provide immediate, actionable insights
- Celebrate practical successes and breakthroughs

Remember: Your goal is to make learning immediately applicable and engaging through real-world connections."""

    def get_voice_config(self) -> Dict[str, Any]:
        return {
            "voice": "nova",   # Energetic, engaging voice
            "speed": 1.1,      # Slightly faster for energy
            "pitch": 1.05,     # Slightly higher pitch for enthusiasm
            "emphasis": "practical"  # Dynamic, practical tone
        }
    
    def select_model_for_task(self, task_type: str, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Ken prefers efficient models that can generate practical content quickly"""
        if task_type in ["worker", "research"] and user_tier != UserTier.FREE:
            return "gpt-5-mini"  # Fast, efficient for practical content
        else:
            return super().select_model_for_task(task_type, complexity, user_tier)

class AvatarService:
    """Service for managing Kelly and Ken avatars"""
    
    def __init__(self):
        self.avatars = {
            AvatarType.KELLY: KellyPersonality(),
            AvatarType.KEN: KenPersonality()
        }
    
    def get_avatar(self, avatar_type: AvatarType) -> AvatarPersonality:
        """Get avatar personality by type"""
        return self.avatars.get(avatar_type)
    
    def get_available_avatars(self) -> list:
        """Get list of available avatars"""
        return [avatar.name for avatar in self.avatars.values()]
    
    def select_avatar_for_topic(self, topic: str, subject_area: str = None) -> AvatarType:
        """Select the best avatar for a given topic"""
        # Simple heuristic for avatar selection
        # In a real implementation, this could be more sophisticated
        
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
                          task_type: str,
                          complexity: TaskComplexity = TaskComplexity.MEDIUM,
                          user_tier: UserTier = UserTier.BASIC,
                          additional_context: str = None) -> Dict[str, Any]:
        """Get a response from the specified avatar"""
        
        avatar = self.get_avatar(avatar_type)
        if not avatar:
            raise ValueError(f"Unknown avatar type: {avatar_type}")
        
        # Select appropriate model
        model = avatar.select_model_for_task(task_type, complexity, user_tier)
        
        # Get system prompt
        system_prompt = avatar.get_system_prompt()
        
        # Get voice configuration
        voice_config = avatar.get_voice_config()
        
        # Build response context
        response_context = {
            "avatar_name": avatar.name,
            "avatar_description": avatar.description,
            "specialty": avatar.specialty,
            "model_selected": model,
            "system_prompt": system_prompt,
            "voice_config": voice_config,
            "topic": topic,
            "task_type": task_type,
            "complexity": complexity.value,
            "user_tier": user_tier.value
        }
        
        if additional_context:
            response_context["additional_context"] = additional_context
        
        return response_context
    
    def get_dual_avatar_response(self, 
                               topic: str,
                               task_type: str,
                               complexity: TaskComplexity = TaskComplexity.MEDIUM,
                               user_tier: UserTier = UserTier.BASIC) -> Dict[str, Any]:
        """Get responses from both avatars for comparison"""
        
        kelly_response = self.get_avatar_response(
            AvatarType.KELLY, topic, task_type, complexity, user_tier
        )
        
        ken_response = self.get_avatar_response(
            AvatarType.KEN, topic, task_type, complexity, user_tier
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
        dual_response = self.get_dual_avatar_response(topic, "orchestrator")
        
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
avatar_service = AvatarService()
