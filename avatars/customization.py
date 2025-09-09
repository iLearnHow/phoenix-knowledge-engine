"""
Avatar Customization System for Phoenix Knowledge Engine
Allows fine-tuning of Kelly and Ken's personalities, prompts, and behaviors
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class TeachingStyle(Enum):
    ACADEMIC = "academic"
    PRACTICAL = "practical"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    CREATIVE = "creative"

class PersonalityTrait(Enum):
    WARM = "warm"
    PROFESSIONAL = "professional"
    ENTHUSIASTIC = "enthusiastic"
    PATIENT = "patient"
    DIRECT = "direct"
    ENCOURAGING = "encouraging"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    CONFIDENT = "confident"

@dataclass
class AvatarConfig:
    """Configuration for an avatar"""
    name: str
    role: str
    teaching_style: TeachingStyle
    personality_traits: List[PersonalityTrait]
    expertise_areas: List[str]
    voice_characteristics: Dict[str, str]
    prompt_templates: Dict[str, str]
    content_preferences: Dict[str, str]
    interaction_style: str
    example_phrases: List[str]

class AvatarCustomizer:
    """Main class for customizing avatar personalities"""
    
    def __init__(self, config_file: str = "avatar_configs.json"):
        self.config_file = config_file
        self.avatars = {}
        self.load_configs()
    
    def load_configs(self):
        """Load avatar configurations from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                for name, config_data in data.items():
                    self.avatars[name] = self._dict_to_avatar_config(config_data)
        else:
            self._create_default_configs()
    
    def save_configs(self):
        """Save avatar configurations to file"""
        data = {}
        for name, config in self.avatars.items():
            data[name] = self._avatar_config_to_dict(config)
        
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _dict_to_avatar_config(self, data: dict) -> AvatarConfig:
        """Convert dictionary to AvatarConfig"""
        return AvatarConfig(
            name=data['name'],
            role=data['role'],
            teaching_style=TeachingStyle(data['teaching_style']),
            personality_traits=[PersonalityTrait(t) for t in data['personality_traits']],
            expertise_areas=data['expertise_areas'],
            voice_characteristics=data['voice_characteristics'],
            prompt_templates=data['prompt_templates'],
            content_preferences=data['content_preferences'],
            interaction_style=data['interaction_style'],
            example_phrases=data['example_phrases']
        )
    
    def _avatar_config_to_dict(self, config: AvatarConfig) -> dict:
        """Convert AvatarConfig to dictionary"""
        return {
            'name': config.name,
            'role': config.role,
            'teaching_style': config.teaching_style.value,
            'personality_traits': [t.value for t in config.personality_traits],
            'expertise_areas': config.expertise_areas,
            'voice_characteristics': config.voice_characteristics,
            'prompt_templates': config.prompt_templates,
            'content_preferences': config.content_preferences,
            'interaction_style': config.interaction_style,
            'example_phrases': config.example_phrases
        }
    
    def _create_default_configs(self):
        """Create default avatar configurations"""
        # Kelly - Academic Specialist
        kelly_config = AvatarConfig(
            name="Kelly",
            role="Educational Specialist",
            teaching_style=TeachingStyle.ACADEMIC,
            personality_traits=[PersonalityTrait.WARM, PersonalityTrait.PROFESSIONAL, PersonalityTrait.PATIENT],
            expertise_areas=["Mathematics", "Science", "Literature", "History", "Critical Thinking"],
            voice_characteristics={
                "tone": "warm and professional",
                "pace": "moderate",
                "emphasis": "clarity and understanding",
                "style": "methodical and thorough"
            },
            prompt_templates={
                "core_concept": "Let's explore the fundamental concept of {topic}. This is a cornerstone principle that forms the foundation for deeper understanding...",
                "example": "To illustrate this concept, consider this example: {example}. Notice how this demonstrates the key principles we've been discussing...",
                "warning": "It's important to be aware of this common misconception: {misconception}. Many students initially think this way, but here's why it's incorrect...",
                "encouragement": "You're doing great! Understanding {topic} takes time, and you're making excellent progress. Let's continue building on what you've learned..."
            },
            content_preferences={
                "structure": "step-by-step explanations",
                "examples": "multiple analogies and real-world connections",
                "language": "clear, academic, accessible",
                "depth": "thorough and comprehensive"
            },
            interaction_style="methodical, patient, encouraging",
            example_phrases=[
                "Let's work through this step by step...",
                "This is a fundamental concept that...",
                "Think of it this way...",
                "Here's what's really happening...",
                "You're absolutely right to question that..."
            ]
        )
        
        # Ken - Practical Expert
        ken_config = AvatarConfig(
            name="Ken",
            role="Practical Application Expert",
            teaching_style=TeachingStyle.PRACTICAL,
            personality_traits=[PersonalityTrait.ENTHUSIASTIC, PersonalityTrait.DIRECT, PersonalityTrait.ENCOURAGING],
            expertise_areas=["Engineering", "Technology", "Business", "Problem Solving", "Real-world Applications"],
            voice_characteristics={
                "tone": "energetic and engaging",
                "pace": "dynamic",
                "emphasis": "practical application",
                "style": "hands-on and results-oriented"
            },
            prompt_templates={
                "core_concept": "Alright, let's dive into {topic} and see how this actually works in the real world! Here's the deal...",
                "example": "Check this out - here's a perfect example of {topic} in action: {example}. You can literally see this happening right now...",
                "warning": "Heads up! A lot of people mess this up because they think {misconception}. Don't fall into that trap - here's the right way...",
                "encouragement": "You've got this! {topic} might seem tricky at first, but once you see how it works in practice, it'll click. Let's make it happen!"
            },
            content_preferences={
                "structure": "hands-on, project-based",
                "examples": "immediate practical applications",
                "language": "conversational, energetic",
                "depth": "focused on application and results"
            },
            interaction_style="energetic, direct, results-focused",
            example_phrases=[
                "Let's get our hands dirty with this...",
                "Here's how this actually works in practice...",
                "You can use this right now to...",
                "This is where the rubber meets the road...",
                "Let's build something real with this..."
            ]
        )
        
        self.avatars = {
            "kelly": kelly_config,
            "ken": ken_config
        }
        self.save_configs()
    
    def customize_avatar(self, avatar_name: str, **kwargs) -> bool:
        """Customize an avatar's configuration"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return False
        
        config = self.avatars[avatar_name]
        
        # Update configuration based on provided parameters
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                print(f"⚠️  Unknown configuration key: {key}")
        
        self.save_configs()
        print(f"✅ Avatar '{avatar_name}' customized successfully")
        return True
    
    def add_personality_trait(self, avatar_name: str, trait: PersonalityTrait):
        """Add a personality trait to an avatar"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return False
        
        config = self.avatars[avatar_name]
        if trait not in config.personality_traits:
            config.personality_traits.append(trait)
            self.save_configs()
            print(f"✅ Added trait '{trait.value}' to {avatar_name}")
        else:
            print(f"ℹ️  Trait '{trait.value}' already exists for {avatar_name}")
        return True
    
    def remove_personality_trait(self, avatar_name: str, trait: PersonalityTrait):
        """Remove a personality trait from an avatar"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return False
        
        config = self.avatars[avatar_name]
        if trait in config.personality_traits:
            config.personality_traits.remove(trait)
            self.save_configs()
            print(f"✅ Removed trait '{trait.value}' from {avatar_name}")
        else:
            print(f"ℹ️  Trait '{trait.value}' not found for {avatar_name}")
        return True
    
    def update_prompt_template(self, avatar_name: str, template_type: str, new_template: str):
        """Update a prompt template for an avatar"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return False
        
        config = self.avatars[avatar_name]
        config.prompt_templates[template_type] = new_template
        self.save_configs()
        print(f"✅ Updated '{template_type}' template for {avatar_name}")
        return True
    
    def add_expertise_area(self, avatar_name: str, area: str):
        """Add an expertise area to an avatar"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return False
        
        config = self.avatars[avatar_name]
        if area not in config.expertise_areas:
            config.expertise_areas.append(area)
            self.save_configs()
            print(f"✅ Added expertise area '{area}' to {avatar_name}")
        else:
            print(f"ℹ️  Expertise area '{area}' already exists for {avatar_name}")
        return True
    
    def get_avatar_config(self, avatar_name: str) -> Optional[AvatarConfig]:
        """Get an avatar's configuration"""
        return self.avatars.get(avatar_name)
    
    def list_avatars(self) -> List[str]:
        """List all available avatars"""
        return list(self.avatars.keys())
    
    def generate_custom_prompt(self, avatar_name: str, content_type: str, topic: str, **kwargs) -> str:
        """Generate a custom prompt based on avatar configuration"""
        if avatar_name not in self.avatars:
            return f"Error: Avatar '{avatar_name}' not found"
        
        config = self.avatars[avatar_name]
        
        # Get the base template
        template = config.prompt_templates.get(content_type, f"Create {content_type} content about {topic}")
        
        # Format the template with the topic
        prompt = template.format(topic=topic, **kwargs)
        
        # Add personality-specific elements
        personality_intro = f"As {config.name}, a {config.role} with expertise in {', '.join(config.expertise_areas[:3])}, "
        personality_intro += f"I approach this with a {config.interaction_style} style. "
        
        # Add teaching style context
        style_context = {
            TeachingStyle.ACADEMIC: "Focus on building a solid theoretical foundation with clear explanations and multiple examples.",
            TeachingStyle.PRACTICAL: "Emphasize real-world applications and hands-on learning with immediate practical value.",
            TeachingStyle.CONVERSATIONAL: "Use a friendly, conversational tone that makes complex topics accessible and engaging.",
            TeachingStyle.TECHNICAL: "Provide detailed technical explanations with precise terminology and comprehensive coverage.",
            TeachingStyle.CREATIVE: "Use creative analogies, visual descriptions, and innovative approaches to make learning memorable."
        }
        
        style_instruction = style_context.get(config.teaching_style, "")
        
        # Combine everything
        full_prompt = f"{personality_intro}{style_instruction}\n\n{prompt}"
        
        return full_prompt
    
    def export_avatar_config(self, avatar_name: str, filename: str = None) -> str:
        """Export an avatar's configuration to a file"""
        if avatar_name not in self.avatars:
            print(f"❌ Avatar '{avatar_name}' not found")
            return ""
        
        config = self.avatars[avatar_name]
        if not filename:
            filename = f"{avatar_name}_config.json"
        
        with open(filename, 'w') as f:
            json.dump(self._avatar_config_to_dict(config), f, indent=2)
        
        print(f"✅ Exported {avatar_name} configuration to {filename}")
        return filename
    
    def import_avatar_config(self, filename: str, avatar_name: str = None):
        """Import an avatar configuration from a file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if not avatar_name:
            avatar_name = data.get('name', 'imported_avatar').lower()
        
        config = self._dict_to_avatar_config(data)
        self.avatars[avatar_name] = config
        self.save_configs()
        
        print(f"✅ Imported avatar configuration as '{avatar_name}'")
        return True

# Example usage and testing
if __name__ == "__main__":
    # Create customizer
    customizer = AvatarCustomizer()
    
    # List available avatars
    print("Available avatars:", customizer.list_avatars())
    
    # Get Kelly's configuration
    kelly_config = customizer.get_avatar_config("kelly")
    if kelly_config:
        print(f"\nKelly's teaching style: {kelly_config.teaching_style.value}")
        print(f"Kelly's traits: {[t.value for t in kelly_config.personality_traits]}")
    
    # Customize Kelly to be more creative
    customizer.add_personality_trait("kelly", PersonalityTrait.CREATIVE)
    customizer.add_expertise_area("kelly", "Creative Writing")
    
    # Update a prompt template
    customizer.update_prompt_template(
        "kelly", 
        "core_concept", 
        "Let's explore {topic} through a creative lens. Imagine this concept as a story..."
    )
    
    # Generate a custom prompt
    custom_prompt = customizer.generate_custom_prompt(
        "kelly", 
        "core_concept", 
        "Photosynthesis",
        example="a plant in sunlight"
    )
    
    print(f"\nCustom prompt for Kelly:\n{custom_prompt}")
