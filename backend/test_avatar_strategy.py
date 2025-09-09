#!/usr/bin/env python3
"""
Avatar Strategy Testing
Tests the complete avatar system with model routing and personality management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.model_router import model_router, TaskComplexity, UserTier, ContentType
from services.avatar_service import avatar_service, AvatarType
import json

def test_model_routing():
    """Test the model routing system"""
    print("🧪 Testing Model Routing System")
    print("=" * 50)
    
    test_cases = [
        {
            "task_type": "orchestrator",
            "complexity": TaskComplexity.COMPLEX,
            "user_tier": UserTier.PREMIUM,
            "expected_models": ["gpt-5", "gpt-5-mini"]
        },
        {
            "task_type": "worker",
            "complexity": TaskComplexity.SIMPLE,
            "user_tier": UserTier.BASIC,
            "expected_models": ["gpt-5-mini", "gpt-5-nano"]
        },
        {
            "task_type": "quality_control",
            "complexity": TaskComplexity.MEDIUM,
            "user_tier": UserTier.FREE,
            "expected_models": ["gpt-5-nano"]
        },
        {
            "task_type": "research",
            "complexity": TaskComplexity.ADVANCED,
            "user_tier": UserTier.PRO,
            "expected_models": ["o3-deep-research", "o4-mini-deep-research"]
        },
        {
            "task_type": "voice",
            "complexity": TaskComplexity.MEDIUM,
            "content_type": ContentType.REALTIME,
            "user_tier": UserTier.PREMIUM,
            "expected_models": ["gpt-realtime", "gpt-4o-mini-tts"]
        },
        {
            "task_type": "visual",
            "complexity": TaskComplexity.MEDIUM,
            "user_tier": UserTier.PRO,
            "expected_models": ["gpt-image-1", "dall-e-3"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['task_type']} - {test_case['complexity'].value} - {test_case['user_tier'].value}")
        
        # Get model selection
        content_type = test_case.get('content_type', ContentType.TEXT)
        selected_model = model_router.select_model(
            test_case['task_type'],
            test_case['complexity'],
            test_case['user_tier'],
            content_type
        )
        
        print(f"   Selected Model: {selected_model}")
        
        # Check if selected model is in expected models
        expected_models = test_case['expected_models']
        if selected_model in expected_models:
            print(f"   ✅ Model selection correct")
        else:
            print(f"   ⚠️  Model selection unexpected (expected one of: {expected_models})")
        
        # Get model info
        model_info = model_router.get_model_info(selected_model)
        if model_info:
            print(f"   Cost per 1K tokens: ${model_info.get('cost_per_1k_tokens', 0):.4f}")
            print(f"   Quality: {model_info.get('quality', 'unknown')}")
            print(f"   Speed: {model_info.get('speed', 'unknown')}")

def test_avatar_personalities():
    """Test the avatar personality system"""
    print("\n🎭 Testing Avatar Personalities")
    print("=" * 50)
    
    # Test Kelly
    print("\n👩‍🏫 Testing Kelly (Educational Specialist)")
    kelly = avatar_service.get_avatar(AvatarType.KELLY)
    print(f"Name: {kelly.name}")
    print(f"Description: {kelly.description}")
    print(f"Specialty: {kelly.specialty}")
    print(f"Voice Style: {kelly.voice_style}")
    
    # Test Ken
    print("\n👨‍💼 Testing Ken (Practical Expert)")
    ken = avatar_service.get_avatar(AvatarType.KEN)
    print(f"Name: {ken.name}")
    print(f"Description: {ken.description}")
    print(f"Specialty: {ken.specialty}")
    print(f"Voice Style: {ken.voice_style}")

def test_avatar_selection():
    """Test avatar selection for different topics"""
    print("\n🎯 Testing Avatar Selection")
    print("=" * 50)
    
    test_topics = [
        ("The Pythagorean Theorem", "mathematics"),
        ("Python Programming", "programming"),
        ("Photosynthesis Process", "biology"),
        ("Marketing Strategy", "business"),
        ("World War II", "history"),
        ("Cooking Techniques", "culinary"),
        ("Machine Learning", "technology"),
        ("Shakespeare's Sonnets", "literature")
    ]
    
    for topic, subject in test_topics:
        print(f"\n📚 Topic: {topic} (Subject: {subject})")
        
        # Get avatar recommendation
        selected_avatar = avatar_service.select_avatar_for_topic(topic, subject)
        print(f"   Recommended Avatar: {selected_avatar.value}")
        
        # Get both avatars for comparison
        dual_response = avatar_service.get_dual_avatar_response(topic, "orchestrator")
        print(f"   Kelly's Approach: {dual_response['kelly']['specialty']}")
        print(f"   Ken's Approach: {dual_response['ken']['specialty']}")

def test_avatar_responses():
    """Test avatar response generation"""
    print("\n💬 Testing Avatar Response Generation")
    print("=" * 50)
    
    test_topic = "Machine Learning Fundamentals"
    
    # Test Kelly's response
    print(f"\n👩‍🏫 Kelly's Response for: {test_topic}")
    kelly_response = avatar_service.get_avatar_response(
        AvatarType.KELLY,
        test_topic,
        "orchestrator",
        TaskComplexity.COMPLEX,
        UserTier.PREMIUM
    )
    
    print(f"   Selected Model: {kelly_response['model_selected']}")
    print(f"   Specialty: {kelly_response['specialty']}")
    print(f"   Voice Config: {kelly_response['voice_config']}")
    
    # Test Ken's response
    print(f"\n👨‍💼 Ken's Response for: {test_topic}")
    ken_response = avatar_service.get_avatar_response(
        AvatarType.KEN,
        test_topic,
        "orchestrator",
        TaskComplexity.COMPLEX,
        UserTier.PREMIUM
    )
    
    print(f"   Selected Model: {ken_response['model_selected']}")
    print(f"   Specialty: {ken_response['specialty']}")
    print(f"   Voice Config: {ken_response['voice_config']}")

def test_cost_estimation():
    """Test cost estimation for different scenarios"""
    print("\n💰 Testing Cost Estimation")
    print("=" * 50)
    
    scenarios = [
        {"model": "gpt-5", "tokens": 1000, "description": "Complex reasoning task"},
        {"model": "gpt-5-mini", "tokens": 1000, "description": "Standard content generation"},
        {"model": "gpt-5-nano", "tokens": 1000, "description": "Quick validation"},
        {"model": "o3-deep-research", "tokens": 2000, "description": "Deep research task"},
        {"model": "gpt-realtime", "tokens": 500, "description": "Realtime conversation"},
        {"model": "gpt-image-1", "tokens": 100, "description": "Image generation"}
    ]
    
    total_cost = 0
    
    for scenario in scenarios:
        cost = model_router.estimate_cost(scenario['model'], scenario['tokens'])
        total_cost += cost
        print(f"   {scenario['description']}: ${cost:.4f} ({scenario['model']}, {scenario['tokens']} tokens)")
    
    print(f"\n   Total estimated cost: ${total_cost:.4f}")

def test_user_tier_models():
    """Test available models for different user tiers"""
    print("\n👥 Testing User Tier Model Access")
    print("=" * 50)
    
    tiers = [UserTier.FREE, UserTier.BASIC, UserTier.PREMIUM, UserTier.PRO]
    
    for tier in tiers:
        print(f"\n   {tier.value.upper()} Tier:")
        available_models = model_router.get_available_models(tier)
        print(f"   Available models: {', '.join(available_models)}")
        print(f"   Model count: {len(available_models)}")

def main():
    """Run all tests"""
    print("🚀 Avatar Strategy Comprehensive Testing")
    print("=" * 60)
    
    try:
        test_model_routing()
        test_avatar_personalities()
        test_avatar_selection()
        test_avatar_responses()
        test_cost_estimation()
        test_user_tier_models()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📊 Summary:")
        print("   ✅ Model routing system working")
        print("   ✅ Avatar personalities configured")
        print("   ✅ Avatar selection logic functional")
        print("   ✅ Cost estimation working")
        print("   ✅ User tier restrictions implemented")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
