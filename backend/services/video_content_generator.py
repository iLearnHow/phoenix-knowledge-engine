"""
Video Content Generator
Main service that creates Kelly's video content using her base video and AI-generated content
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .video_processor import KellyVideoProcessor
from .audio_generator import KellyAudioGenerator
from .model_router import model_router, TaskComplexity, UserTier
from .avatar_service import avatar_service, AvatarType

logger = logging.getLogger(__name__)

class KellyVideoContentGenerator:
    """
    Generates complete video content using Kelly's base video and AI content
    """
    
    def __init__(self, base_video_path: str, api_key: str = None):
        self.base_video_path = base_video_path
        self.api_key = api_key
        
        # Initialize services
        self.video_processor = KellyVideoProcessor(base_video_path)
        self.audio_generator = KellyAudioGenerator(api_key)
        
        # Content generation settings
        self.content_settings = {
            "max_component_duration": 30,  # seconds
            "min_component_duration": 5,   # seconds
            "transition_duration": 1,      # seconds
            "output_quality": "high"
        }
        
        # Ensure base video is analyzed
        self._ensure_video_analyzed()
    
    def _ensure_video_analyzed(self):
        """Ensure Kelly's base video has been analyzed"""
        metadata_file = os.path.join(os.path.dirname(self.base_video_path), "kelly_metadata.json")
        
        if not os.path.exists(metadata_file):
            logger.info("Analyzing Kelly's base video...")
            self.video_processor.analyze_video()
        else:
            logger.info("Kelly's video metadata found, loading...")
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                self.video_processor.metadata = metadata["video_properties"]
                self.video_processor.face_landmarks = metadata["face_landmarks"]
                self.video_processor.sync_points = metadata["sync_points"]
    
    def generate_lesson_video(self, topic: str, user_tier: UserTier = UserTier.BASIC) -> Dict[str, Any]:
        """
        Generate a complete lesson video with Kelly
        
        Args:
            topic: Learning topic
            user_tier: User subscription tier
            
        Returns:
            Complete lesson video information
        """
        logger.info(f"Generating lesson video for topic: {topic}")
        
        try:
            # Step 1: Generate text content using Kelly's personality
            text_content = self._generate_text_content(topic, user_tier)
            
            # Step 2: Generate audio for all content
            audio_content = self._generate_audio_content(text_content)
            
            # Step 3: Create video segments
            video_segments = self._create_video_segments(audio_content)
            
            # Step 4: Combine into final lesson video
            final_video = self._combine_video_segments(video_segments, topic)
            
            return {
                "success": True,
                "topic": topic,
                "final_video": final_video,
                "text_content": text_content,
                "audio_content": audio_content,
                "video_segments": video_segments,
                "duration": self._calculate_total_duration(audio_content)
            }
            
        except Exception as e:
            logger.error(f"Error generating lesson video: {e}")
            return {
                "success": False,
                "error": str(e),
                "topic": topic
            }
    
    def _generate_text_content(self, topic: str, user_tier: UserTier) -> Dict[str, Any]:
        """Generate text content using Kelly's personality and AI models"""
        logger.info("Generating text content with Kelly's personality")
        
        # Get Kelly's avatar response
        kelly_response = avatar_service.get_avatar_response(
            AvatarType.KELLY,
            topic,
            "orchestrator",
            TaskComplexity.MEDIUM,
            user_tier
        )
        
        # Generate content using the selected model
        # This would integrate with your existing orchestrator service
        # For now, we'll create a mock structure
        
        text_content = {
            "summary": f"Hi, I'm Kelly, and today we're going to explore {topic}. This is a fascinating topic that we'll break down step by step.",
            "components": [
                {
                    "type": "CORE_CONCEPT",
                    "content": f"The core concept of {topic} is fundamental to understanding this subject. Let me explain this clearly and methodically.",
                    "duration": 15
                },
                {
                    "type": "EXAMPLE",
                    "content": f"Here's a concrete example of {topic} in action. This will help you see how it works in practice.",
                    "duration": 20
                },
                {
                    "type": "PRINCIPLE",
                    "content": f"The key principle behind {topic} is important to remember. This principle guides how we apply this concept.",
                    "duration": 12
                }
            ],
            "quiz": {
                "question_text": f"Which of the following best describes the main concept of {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": f"The correct answer helps us understand {topic} better."
            }
        }
        
        return text_content
    
    def _generate_audio_content(self, text_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate audio for all text content"""
        logger.info("Generating audio content")
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(self.base_video_path), "generated_audio")
        os.makedirs(output_dir, exist_ok=True)
        
        audio_content = {
            "summary": None,
            "components": [],
            "quiz": None
        }
        
        # Generate summary audio
        if "summary" in text_content:
            summary_script = self.audio_generator.create_audio_script(text_content["summary"])
            summary_audio = self.audio_generator.generate_audio(
                summary_script,
                os.path.join(output_dir, "summary.mp3")
            )
            audio_content["summary"] = summary_audio
        
        # Generate component audio
        for i, component in enumerate(text_content.get("components", [])):
            component_script = self.audio_generator.create_audio_script(component["content"])
            component_audio = self.audio_generator.generate_audio(
                component_script,
                os.path.join(output_dir, f"component_{i}.mp3")
            )
            audio_content["components"].append(component_audio)
        
        # Generate quiz audio
        if "quiz" in text_content:
            quiz_script = self.audio_generator.create_audio_script(text_content["quiz"]["question_text"])
            quiz_audio = self.audio_generator.generate_audio(
                quiz_script,
                os.path.join(output_dir, "quiz.mp3")
            )
            audio_content["quiz"] = quiz_audio
        
        return audio_content
    
    def _create_video_segments(self, audio_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create video segments for each audio component"""
        logger.info("Creating video segments")
        
        video_segments = []
        
        # Create summary video segment
        if audio_content["summary"] and audio_content["summary"]["success"]:
            summary_video = self._create_single_video_segment(
                audio_content["summary"]["audio_path"],
                "summary"
            )
            video_segments.append(summary_video)
        
        # Create component video segments
        for i, component_audio in enumerate(audio_content["components"]):
            if component_audio["success"]:
                component_video = self._create_single_video_segment(
                    component_audio["audio_path"],
                    f"component_{i}"
                )
                video_segments.append(component_video)
        
        # Create quiz video segment
        if audio_content["quiz"] and audio_content["quiz"]["success"]:
            quiz_video = self._create_single_video_segment(
                audio_content["quiz"]["audio_path"],
                "quiz"
            )
            video_segments.append(quiz_video)
        
        return video_segments
    
    def _create_single_video_segment(self, audio_path: str, segment_name: str) -> Dict[str, Any]:
        """Create a single video segment with Kelly talking"""
        logger.info(f"Creating video segment: {segment_name}")
        
        # Get audio duration
        audio_duration = self._get_audio_duration(audio_path)
        
        # Create output path
        output_dir = os.path.join(os.path.dirname(self.base_video_path), "video_segments")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{segment_name}.mp4")
        
        # Create talking head video
        video_path = self.video_processor.create_talking_head_video(
            audio_path,
            output_path
        )
        
        return {
            "segment_name": segment_name,
            "video_path": video_path,
            "audio_path": audio_path,
            "duration": audio_duration,
            "success": True
        }
    
    def _combine_video_segments(self, video_segments: List[Dict[str, Any]], topic: str) -> Dict[str, Any]:
        """Combine all video segments into final lesson video"""
        logger.info("Combining video segments into final lesson")
        
        # Create output path
        output_dir = os.path.join(os.path.dirname(self.base_video_path), "final_videos")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')
        
        final_video_path = os.path.join(output_dir, f"kelly_lesson_{safe_topic}.mp4")
        
        # For now, we'll just copy the first segment as a placeholder
        # In production, use ffmpeg to properly combine segments
        if video_segments:
            import shutil
            shutil.copy2(video_segments[0]["video_path"], final_video_path)
        
        return {
            "video_path": final_video_path,
            "segments_count": len(video_segments),
            "total_duration": sum(seg.get("duration", 0) for seg in video_segments),
            "success": True
        }
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file"""
        # Simplified approach - in production, use librosa or similar
        return 10.0  # Placeholder duration
    
    def _calculate_total_duration(self, audio_content: Dict[str, Any]) -> float:
        """Calculate total duration of all audio content"""
        total_duration = 0
        
        if audio_content["summary"]:
            total_duration += audio_content["summary"].get("metadata", {}).get("estimated_duration", 0)
        
        for component in audio_content["components"]:
            total_duration += component.get("metadata", {}).get("estimated_duration", 0)
        
        if audio_content["quiz"]:
            total_duration += audio_content["quiz"].get("metadata", {}).get("estimated_duration", 0)
        
        return total_duration

def test_kelly_video_generation():
    """Test Kelly's video content generation"""
    print("🎬 Testing Kelly's Video Content Generation")
    print("=" * 60)
    
    # Test with Kelly's base video
    base_video_path = "../kelly2-welcome-pitch.mp4"
    
    if not os.path.exists(base_video_path):
        print(f"❌ Kelly's base video not found: {base_video_path}")
        return
    
    try:
        # Initialize generator
        generator = KellyVideoContentGenerator(base_video_path)
        
        # Generate test lesson
        result = generator.generate_lesson_video("The Pythagorean Theorem", UserTier.BASIC)
        
        if result["success"]:
            print("✅ Video lesson generated successfully!")
            print(f"   Topic: {result['topic']}")
            print(f"   Final Video: {result['final_video']['video_path']}")
            print(f"   Duration: {result['duration']:.2f} seconds")
            print(f"   Segments: {result['final_video']['segments_count']}")
        else:
            print(f"❌ Video generation failed: {result['error']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_kelly_video_generation()
