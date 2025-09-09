"""
Audio Generation Service
Generates Kelly's voice using OpenAI TTS and processes audio for video sync
"""

import os
import openai
from typing import Dict, Any, Optional
import logging
from pathlib import Path
import tempfile
import json

logger = logging.getLogger(__name__)

class KellyAudioGenerator:
    """
    Generates audio content using Kelly's voice profile
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Kelly's voice configuration
        self.voice_config = {
            "voice": "alloy",  # Warm, professional voice
            "speed": 0.9,      # Slightly slower for clarity
            "pitch": 1.0,      # Normal pitch
            "emphasis": "educational"  # Clear, instructional tone
        }
        
        # Audio output settings
        self.audio_settings = {
            "format": "mp3",
            "quality": "high",
            "sample_rate": 44100,
            "channels": 1  # Mono for better sync
        }
    
    def generate_audio(self, text: str, output_path: str = None) -> Dict[str, Any]:
        """
        Generate audio for Kelly using OpenAI TTS
        
        Args:
            text: Text to convert to speech
            output_path: Optional output path for audio file
            
        Returns:
            Dictionary with audio generation results
        """
        logger.info(f"Generating Kelly's audio for text: {text[:50]}...")
        
        try:
            # Create output directory if needed
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            else:
                # Create temporary file
                temp_dir = tempfile.mkdtemp()
                output_path = os.path.join(temp_dir, "kelly_audio.mp3")
            
            # Generate audio using OpenAI TTS
            response = self.client.audio.speech.create(
                model="tts-1",  # High quality TTS
                voice=self.voice_config["voice"],
                input=text,
                response_format="mp3"
            )
            
            # Save audio file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # Get audio metadata
            audio_metadata = self._get_audio_metadata(output_path)
            
            result = {
                "success": True,
                "audio_path": output_path,
                "text": text,
                "voice_config": self.voice_config,
                "metadata": audio_metadata,
                "file_size": os.path.getsize(output_path)
            }
            
            logger.info(f"Audio generated successfully: {output_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return {
                "success": False,
                "error": str(e),
                "text": text
            }
    
    def generate_lesson_audio(self, lesson_content: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """
        Generate audio for all components of a lesson
        
        Args:
            lesson_content: Lesson content with components
            output_dir: Directory to save audio files
            
        Returns:
            Dictionary with all generated audio files
        """
        logger.info("Generating audio for complete lesson")
        
        os.makedirs(output_dir, exist_ok=True)
        
        audio_files = {
            "summary": None,
            "components": [],
            "quiz": None
        }
        
        # Generate summary audio
        if "summary" in lesson_content:
            summary_audio = self.generate_audio(
                lesson_content["summary"],
                os.path.join(output_dir, "summary.mp3")
            )
            audio_files["summary"] = summary_audio
        
        # Generate component audio
        if "components" in lesson_content:
            for i, component in enumerate(lesson_content["components"]):
                component_audio = self.generate_audio(
                    component["content"],
                    os.path.join(output_dir, f"component_{i}.mp3")
                )
                audio_files["components"].append(component_audio)
        
        # Generate quiz audio
        if "quiz" in lesson_content and "question_text" in lesson_content["quiz"]:
            quiz_audio = self.generate_audio(
                lesson_content["quiz"]["question_text"],
                os.path.join(output_dir, "quiz.mp3")
            )
            audio_files["quiz"] = quiz_audio
        
        return {
            "success": True,
            "audio_files": audio_files,
            "output_dir": output_dir
        }
    
    def _get_audio_metadata(self, audio_path: str) -> Dict[str, Any]:
        """Get metadata for generated audio file"""
        try:
            # Simplified metadata extraction
            # In production, use librosa or similar for accurate metadata
            file_size = os.path.getsize(audio_path)
            
            # Estimate duration based on text length and speaking rate
            # This is a rough estimate - in production, use actual audio analysis
            estimated_duration = len(self.voice_config.get("text", "")) * 0.1  # Rough estimate
            
            return {
                "file_size": file_size,
                "estimated_duration": estimated_duration,
                "format": self.audio_settings["format"],
                "sample_rate": self.audio_settings["sample_rate"],
                "channels": self.audio_settings["channels"]
            }
        except Exception as e:
            logger.warning(f"Could not extract audio metadata: {e}")
            return {}
    
    def optimize_for_video_sync(self, audio_path: str, target_duration: float) -> str:
        """
        Optimize audio for video synchronization
        
        Args:
            audio_path: Path to audio file
            target_duration: Target duration in seconds
            
        Returns:
            Path to optimized audio file
        """
        logger.info(f"Optimizing audio for video sync: {target_duration}s")
        
        # This is a placeholder for audio optimization
        # In production, use audio processing libraries to:
        # 1. Adjust speed/pitch to match target duration
        # 2. Add silence padding if needed
        # 3. Normalize audio levels
        # 4. Ensure smooth transitions
        
        optimized_path = audio_path.replace(".mp3", "_optimized.mp3")
        
        # For now, just copy the file
        import shutil
        shutil.copy2(audio_path, optimized_path)
        
        return optimized_path
    
    def create_audio_script(self, content: str) -> str:
        """
        Create a natural-sounding script for Kelly
        
        Args:
            content: Raw content to convert to script
            
        Returns:
            Natural-sounding script for Kelly
        """
        # Add Kelly's natural speaking patterns
        script = content
        
        # Add natural pauses and emphasis
        script = script.replace(".", ". ")  # Add pause after sentences
        script = script.replace(":", ": ")  # Add pause after colons
        script = script.replace(";", "; ")  # Add pause after semicolons
        
        # Add Kelly's natural phrases
        if not script.startswith("Hi, I'm Kelly"):
            script = f"Hi, I'm Kelly, and today we're going to explore {script.lower()}"
        
        if not script.endswith("."):
            script += "."
        
        return script

def test_kelly_audio_generation():
    """Test Kelly's audio generation"""
    print("🎤 Testing Kelly's Audio Generation")
    print("=" * 50)
    
    # Test text
    test_text = "Welcome to our lesson on the Pythagorean Theorem. Today we'll learn how this fundamental mathematical principle applies to right triangles."
    
    try:
        generator = KellyAudioGenerator()
        
        # Generate audio
        result = generator.generate_audio(test_text)
        
        if result["success"]:
            print("✅ Audio generated successfully!")
            print(f"   File: {result['audio_path']}")
            print(f"   Size: {result['file_size']} bytes")
            print(f"   Voice: {result['voice_config']['voice']}")
        else:
            print(f"❌ Audio generation failed: {result['error']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_kelly_audio_generation()
