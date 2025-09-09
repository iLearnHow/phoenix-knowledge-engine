"""
Model Router Service
Intelligent model selection based on task complexity, user tier, and cost optimization
"""

from typing import Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    ADVANCED = "advanced"

class UserTier(Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    PRO = "pro"

class ContentType(Enum):
    TEXT = "text"
    VOICE = "voice"
    VISUAL = "visual"
    REALTIME = "realtime"
    RESEARCH = "research"

class ModelRouter:
    """
    Intelligent model selection service for the Phoenix Knowledge Engine
    """
    
    def __init__(self):
        self.model_configs = self._initialize_model_configs()
        self.cost_tracking = {}
        self.usage_limits = self._initialize_usage_limits()
    
    def _initialize_model_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize model configurations with cost and capability data"""
        return {
            # Core Content Generation Models
            "gpt-5": {
                "cost_per_1k_tokens": 0.08,  # Estimated
                "capabilities": ["reasoning", "planning", "complex_content"],
                "max_tokens": 128000,
                "speed": "medium",
                "quality": "highest"
            },
            "gpt-5-mini": {
                "cost_per_1k_tokens": 0.03,  # Estimated
                "capabilities": ["content_generation", "examples", "standard_content"],
                "max_tokens": 128000,
                "speed": "fast",
                "quality": "high"
            },
            "gpt-5-nano": {
                "cost_per_1k_tokens": 0.01,  # Estimated
                "capabilities": ["validation", "fact_checking", "simple_content"],
                "max_tokens": 128000,
                "speed": "fastest",
                "quality": "good"
            },
            
            # Research Models
            "o3-deep-research": {
                "cost_per_1k_tokens": 0.25,  # Estimated
                "capabilities": ["deep_research", "complex_analysis", "academic_content"],
                "max_tokens": 128000,
                "speed": "slow",
                "quality": "highest"
            },
            "o4-mini-deep-research": {
                "cost_per_1k_tokens": 0.05,  # Estimated
                "capabilities": ["research", "fact_verification", "standard_research"],
                "max_tokens": 128000,
                "speed": "medium",
                "quality": "high"
            },
            
            # Voice Models
            "gpt-4o-mini-tts": {
                "cost_per_1k_chars": 0.015,  # Estimated
                "capabilities": ["text_to_speech", "voice_generation"],
                "max_tokens": 4000,
                "speed": "fast",
                "quality": "high"
            },
            "gpt-4o-transcribe": {
                "cost_per_minute": 0.01,  # Estimated
                "capabilities": ["speech_to_text", "audio_transcription"],
                "max_tokens": 4000,
                "speed": "fast",
                "quality": "high"
            },
            
            # Realtime Models
            "gpt-realtime": {
                "cost_per_1k_tokens": 0.15,  # Estimated
                "capabilities": ["realtime_chat", "interactive_conversation"],
                "max_tokens": 128000,
                "speed": "realtime",
                "quality": "high"
            },
            
            # Visual Models
            "gpt-image-1": {
                "cost_per_image": 0.08,  # Estimated
                "capabilities": ["image_generation", "visual_content"],
                "max_tokens": 1000,
                "speed": "medium",
                "quality": "highest"
            },
            "dall-e-3": {
                "cost_per_image": 0.04,  # Estimated
                "capabilities": ["image_generation", "visual_content"],
                "max_tokens": 1000,
                "speed": "medium",
                "quality": "high"
            }
        }
    
    def _initialize_usage_limits(self) -> Dict[str, Dict[str, float]]:
        """Initialize usage limits for cost control"""
        return {
            "daily": {
                "gpt-5": 50.0,
                "gpt-5-mini": 30.0,
                "gpt-5-nano": 20.0,
                "o3-deep-research": 100.0,
                "o4-mini-deep-research": 40.0,
                "gpt-4o-mini-tts": 20.0,
                "gpt-4o-transcribe": 15.0,
                "gpt-realtime": 80.0,
                "gpt-image-1": 60.0,
                "dall-e-3": 30.0
            },
            "monthly": {
                "gpt-5": 500.0,
                "gpt-5-mini": 300.0,
                "gpt-5-nano": 200.0,
                "o3-deep-research": 1000.0,
                "o4-mini-deep-research": 400.0,
                "gpt-4o-mini-tts": 200.0,
                "gpt-4o-transcribe": 150.0,
                "gpt-realtime": 800.0,
                "gpt-image-1": 600.0,
                "dall-e-3": 300.0
            }
        }
    
    def select_model(self, 
                    task_type: str,
                    complexity: TaskComplexity,
                    user_tier: UserTier,
                    content_type: ContentType = ContentType.TEXT,
                    estimated_tokens: int = 1000) -> str:
        """
        Select the optimal model based on task requirements and constraints
        
        Args:
            task_type: Type of task (orchestrator, worker, quality_control, etc.)
            complexity: Task complexity level
            user_tier: User subscription tier
            content_type: Type of content to generate
            estimated_tokens: Estimated token usage
            
        Returns:
            Selected model name
        """
        
        # Check if we're within budget limits
        if not self._check_budget_limits():
            return self._get_fallback_model(task_type, user_tier)
        
        # Model selection logic based on task type
        if task_type == "orchestrator":
            return self._select_orchestrator_model(complexity, user_tier)
        elif task_type == "worker":
            return self._select_worker_model(complexity, user_tier, content_type)
        elif task_type == "quality_control":
            return self._select_quality_control_model(complexity, user_tier)
        elif task_type == "research":
            return self._select_research_model(complexity, user_tier)
        elif task_type == "voice":
            return self._select_voice_model(content_type, user_tier)
        elif task_type == "visual":
            return self._select_visual_model(complexity, user_tier)
        elif task_type == "realtime":
            return self._select_realtime_model(user_tier)
        else:
            return self._get_default_model(user_tier)
    
    def _select_orchestrator_model(self, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Select model for orchestrator tasks"""
        if user_tier == UserTier.FREE:
            return "gpt-5-nano"
        elif complexity == TaskComplexity.ADVANCED and user_tier in [UserTier.PREMIUM, UserTier.PRO]:
            return "gpt-5"
        elif complexity == TaskComplexity.COMPLEX and user_tier in [UserTier.BASIC, UserTier.PREMIUM, UserTier.PRO]:
            return "gpt-5-mini"
        else:
            return "gpt-5-nano"
    
    def _select_worker_model(self, complexity: TaskComplexity, user_tier: UserTier, content_type: ContentType) -> str:
        """Select model for worker tasks"""
        if user_tier == UserTier.FREE:
            return "gpt-5-nano"
        elif content_type == ContentType.VISUAL:
            return "gpt-image-1" if user_tier in [UserTier.PREMIUM, UserTier.PRO] else "dall-e-3"
        elif complexity == TaskComplexity.ADVANCED and user_tier == UserTier.PRO:
            return "gpt-5"
        else:
            return "gpt-5-mini"
    
    def _select_quality_control_model(self, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Select model for quality control tasks"""
        # Quality control should be fast and cost-effective
        return "gpt-5-nano"
    
    def _select_research_model(self, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Select model for research tasks"""
        if user_tier == UserTier.FREE:
            return "gpt-5-nano"
        elif complexity == TaskComplexity.ADVANCED and user_tier == UserTier.PRO:
            return "o3-deep-research"
        else:
            return "o4-mini-deep-research"
    
    def _select_voice_model(self, content_type: ContentType, user_tier: UserTier) -> str:
        """Select model for voice tasks"""
        if content_type == ContentType.REALTIME:
            return "gpt-realtime" if user_tier in [UserTier.PREMIUM, UserTier.PRO] else "gpt-5-mini"
        else:
            return "gpt-4o-mini-tts"
    
    def _select_visual_model(self, complexity: TaskComplexity, user_tier: UserTier) -> str:
        """Select model for visual content generation"""
        if user_tier == UserTier.FREE:
            return "dall-e-3"  # Cheapest option
        elif complexity == TaskComplexity.ADVANCED and user_tier == UserTier.PRO:
            return "gpt-image-1"
        else:
            return "dall-e-3"
    
    def _select_realtime_model(self, user_tier: UserTier) -> str:
        """Select model for realtime interaction"""
        if user_tier in [UserTier.PREMIUM, UserTier.PRO]:
            return "gpt-realtime"
        else:
            return "gpt-5-mini"  # Fallback to standard model
    
    def _get_fallback_model(self, task_type: str, user_tier: UserTier) -> str:
        """Get fallback model when budget limits are exceeded"""
        fallback_models = {
            "orchestrator": "gpt-5-nano",
            "worker": "gpt-5-nano",
            "quality_control": "gpt-5-nano",
            "research": "gpt-5-nano",
            "voice": "gpt-5-mini",
            "visual": "dall-e-3",
            "realtime": "gpt-5-mini"
        }
        return fallback_models.get(task_type, "gpt-5-nano")
    
    def _get_default_model(self, user_tier: UserTier) -> str:
        """Get default model based on user tier"""
        if user_tier == UserTier.FREE:
            return "gpt-5-nano"
        elif user_tier == UserTier.BASIC:
            return "gpt-5-mini"
        else:
            return "gpt-5"
    
    def _check_budget_limits(self) -> bool:
        """Check if we're within budget limits"""
        # This would integrate with the budget monitoring system
        # For now, return True (implement actual budget checking)
        return True
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        return self.model_configs.get(model_name, {})
    
    def estimate_cost(self, model_name: str, tokens: int) -> float:
        """Estimate cost for using a model with given token count"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            return 0.0
        
        cost_per_1k = model_info.get("cost_per_1k_tokens", 0.0)
        return (tokens / 1000) * cost_per_1k
    
    def get_available_models(self, user_tier: UserTier) -> list:
        """Get list of available models for a user tier"""
        if user_tier == UserTier.FREE:
            return ["gpt-5-nano", "dall-e-3"]
        elif user_tier == UserTier.BASIC:
            return ["gpt-5-nano", "gpt-5-mini", "gpt-4o-mini-tts", "dall-e-3"]
        elif user_tier == UserTier.PREMIUM:
            return ["gpt-5-nano", "gpt-5-mini", "gpt-5", "gpt-4o-mini-tts", "gpt-4o-transcribe", 
                   "gpt-realtime", "gpt-image-1", "dall-e-3", "o4-mini-deep-research"]
        else:  # PRO
            return list(self.model_configs.keys())

# Global instance
model_router = ModelRouter()
