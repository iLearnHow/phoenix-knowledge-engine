#!/usr/bin/env python3
"""
Test Kelly's Complete Video System
Tests video analysis, audio generation, and content creation
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load API key from environment
from dotenv import load_dotenv
load_dotenv()

from services.video_processor import analyze_kelly_video
from services.audio_generator import KellyAudioGenerator
from services.video_content_generator import KellyVideoContentGenerator
from services.model_router import UserTier

def test_video_analysis():
    """Test Kelly's video analysis"""
    print("🎬 Testing Kelly's Video Analysis")
    print("=" * 50)
    
    video_path = "../kelly2-welcome-pitch.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Kelly's video not found: {video_path}")
        return False
    
    result = analyze_kelly_video(video_path)
    
    if result["success"]:
        print("✅ Video analysis successful!")
        metadata = result["metadata"]
        print(f"   Resolution: {metadata['width']}x{metadata['height']}")
        print(f"   Duration: {metadata['duration']:.2f} seconds")
        print(f"   FPS: {metadata['fps']}")
        print(f"   File Size: {metadata['file_size']:,} bytes")
        print(f"   Face Landmarks: {result['face_landmarks_count']}")
        print(f"   Sync Points: {result['sync_points_count']}")
        return True
    else:
        print(f"❌ Video analysis failed: {result['error']}")
        return False

def test_audio_generation():
    """Test Kelly's audio generation"""
    print("\n🎤 Testing Kelly's Audio Generation")
    print("=" * 50)
    
    try:
        generator = KellyAudioGenerator()
        
        # Test text
        test_text = "Hi, I'm Kelly, and today we're going to explore the Pythagorean Theorem. This is a fascinating mathematical concept that we'll break down step by step."
        
        # Generate audio
        result = generator.generate_audio(test_text)
        
        if result["success"]:
            print("✅ Audio generation successful!")
            print(f"   File: {result['audio_path']}")
            print(f"   Size: {result['file_size']} bytes")
            print(f"   Voice: {result['voice_config']['voice']}")
            print(f"   Speed: {result['voice_config']['speed']}")
            return True
        else:
            print(f"❌ Audio generation failed: {result['error']}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_content_generation():
    """Test complete video content generation"""
    print("\n🎥 Testing Complete Video Content Generation")
    print("=" * 50)
    
    video_path = "../kelly2-welcome-pitch.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Kelly's video not found: {video_path}")
        return False
    
    try:
        generator = KellyVideoContentGenerator(video_path)
        
        # Generate test lesson
        result = generator.generate_lesson_video("The Pythagorean Theorem", UserTier.BASIC)
        
        if result["success"]:
            print("✅ Video lesson generation successful!")
            print(f"   Topic: {result['topic']}")
            print(f"   Final Video: {result['final_video']['video_path']}")
            print(f"   Duration: {result['duration']:.2f} seconds")
            print(f"   Segments: {result['final_video']['segments_count']}")
            return True
        else:
            print(f"❌ Video generation failed: {result['error']}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Kelly's Complete Video System Test")
    print("=" * 60)
    
    tests = [
        ("Video Analysis", test_video_analysis),
        ("Audio Generation", test_audio_generation),
        ("Video Content Generation", test_video_content_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Kelly's system is ready!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()