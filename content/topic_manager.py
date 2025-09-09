"""
Topic Management System for Phoenix Knowledge Engine
Manages educational topics, categories, and content generation
"""

import json
import os
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class SubjectArea(Enum):
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    LANGUAGE_ARTS = "language_arts"
    SOCIAL_STUDIES = "social_studies"
    ARTS = "arts"
    TECHNOLOGY = "technology"
    HEALTH = "health"
    BUSINESS = "business"
    LANGUAGES = "languages"
    PHILOSOPHY = "philosophy"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ContentType(Enum):
    CONCEPT = "concept"
    SKILL = "skill"
    THEORY = "theory"
    PROCESS = "process"
    PRINCIPLE = "principle"
    METHOD = "method"

@dataclass
class Topic:
    """Represents an educational topic"""
    name: str
    subject_area: SubjectArea
    difficulty_level: DifficultyLevel
    content_type: ContentType
    description: str
    key_concepts: List[str]
    learning_objectives: List[str]
    prerequisites: List[str]
    estimated_duration: int  # in minutes
    tags: List[str]
    created_date: str
    last_updated: str

class TopicManager:
    """Manages educational topics and content generation"""
    
    def __init__(self, topics_file: str = "topics_database.json"):
        self.topics_file = topics_file
        self.topics = {}
        self.categories = {}
        self.load_topics()
        self._create_default_topics()
    
    def load_topics(self):
        """Load topics from file"""
        if os.path.exists(self.topics_file):
            with open(self.topics_file, 'r') as f:
                data = json.load(f)
                for topic_name, topic_data in data.items():
                    self.topics[topic_name] = self._dict_to_topic(topic_data)
    
    def save_topics(self):
        """Save topics to file"""
        data = {}
        for topic_name, topic in self.topics.items():
            data[topic_name] = self._topic_to_dict(topic)
        
        with open(self.topics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _dict_to_topic(self, data: dict) -> Topic:
        """Convert dictionary to Topic"""
        return Topic(
            name=data['name'],
            subject_area=SubjectArea(data['subject_area']),
            difficulty_level=DifficultyLevel(data['difficulty_level']),
            content_type=ContentType(data['content_type']),
            description=data['description'],
            key_concepts=data['key_concepts'],
            learning_objectives=data['learning_objectives'],
            prerequisites=data['prerequisites'],
            estimated_duration=data['estimated_duration'],
            tags=data['tags'],
            created_date=data['created_date'],
            last_updated=data['last_updated']
        )
    
    def _topic_to_dict(self, topic: Topic) -> dict:
        """Convert Topic to dictionary"""
        return {
            'name': topic.name,
            'subject_area': topic.subject_area.value,
            'difficulty_level': topic.difficulty_level.value,
            'content_type': topic.content_type.value,
            'description': topic.description,
            'key_concepts': topic.key_concepts,
            'learning_objectives': topic.learning_objectives,
            'prerequisites': topic.prerequisites,
            'estimated_duration': topic.estimated_duration,
            'tags': topic.tags,
            'created_date': topic.created_date,
            'last_updated': topic.last_updated
        }
    
    def _create_default_topics(self):
        """Create default topics if none exist"""
        if not self.topics:
            default_topics = [
                # Mathematics
                Topic(
                    name="The Pythagorean Theorem",
                    subject_area=SubjectArea.MATHEMATICS,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    content_type=ContentType.THEORY,
                    description="A fundamental theorem in geometry relating the sides of a right triangle",
                    key_concepts=["right triangle", "hypotenuse", "legs", "squares", "proof"],
                    learning_objectives=[
                        "Understand the relationship between the sides of a right triangle",
                        "Apply the theorem to solve problems",
                        "Recognize when the theorem can be used"
                    ],
                    prerequisites=["basic geometry", "squares and square roots"],
                    estimated_duration=45,
                    tags=["geometry", "algebra", "proofs"],
                    created_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                ),
                
                # Science
                Topic(
                    name="Photosynthesis",
                    subject_area=SubjectArea.SCIENCE,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    content_type=ContentType.PROCESS,
                    description="The process by which plants convert light energy into chemical energy",
                    key_concepts=["chlorophyll", "light reactions", "dark reactions", "glucose", "oxygen"],
                    learning_objectives=[
                        "Explain the overall process of photosynthesis",
                        "Identify the inputs and outputs",
                        "Understand the role of chlorophyll"
                    ],
                    prerequisites=["basic biology", "cell structure"],
                    estimated_duration=60,
                    tags=["biology", "plants", "energy", "chemistry"],
                    created_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                ),
                
                # Economics
                Topic(
                    name="Supply and Demand",
                    subject_area=SubjectArea.BUSINESS,
                    difficulty_level=DifficultyLevel.BEGINNER,
                    content_type=ContentType.PRINCIPLE,
                    description="The fundamental economic principle that determines market prices",
                    key_concepts=["supply", "demand", "equilibrium", "price", "quantity"],
                    learning_objectives=[
                        "Understand the law of supply and demand",
                        "Analyze market equilibrium",
                        "Predict price changes based on market factors"
                    ],
                    prerequisites=["basic math", "logical thinking"],
                    estimated_duration=50,
                    tags=["economics", "markets", "pricing"],
                    created_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                ),
                
                # Technology
                Topic(
                    name="Machine Learning Basics",
                    subject_area=SubjectArea.TECHNOLOGY,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    content_type=ContentType.CONCEPT,
                    description="Introduction to artificial intelligence and machine learning concepts",
                    key_concepts=["algorithms", "training data", "models", "prediction", "supervised learning"],
                    learning_objectives=[
                        "Understand what machine learning is",
                        "Distinguish between different types of learning",
                        "Recognize real-world applications"
                    ],
                    prerequisites=["basic programming", "statistics"],
                    estimated_duration=75,
                    tags=["AI", "programming", "data science"],
                    created_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                ),
                
                # Language Arts
                Topic(
                    name="Literary Analysis",
                    subject_area=SubjectArea.LANGUAGE_ARTS,
                    difficulty_level=DifficultyLevel.INTERMEDIATE,
                    content_type=ContentType.SKILL,
                    description="The process of examining and interpreting literary works",
                    key_concepts=["theme", "character", "plot", "symbolism", "tone"],
                    learning_objectives=[
                        "Identify literary elements in texts",
                        "Analyze author's purpose and techniques",
                        "Write effective literary analysis essays"
                    ],
                    prerequisites=["reading comprehension", "writing skills"],
                    estimated_duration=90,
                    tags=["literature", "writing", "analysis"],
                    created_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                )
            ]
            
            for topic in default_topics:
                self.topics[topic.name] = topic
            
            self.save_topics()
    
    def add_topic(self, topic: Topic) -> bool:
        """Add a new topic"""
        if topic.name in self.topics:
            print(f"⚠️  Topic '{topic.name}' already exists")
            return False
        
        self.topics[topic.name] = topic
        self.save_topics()
        print(f"✅ Added topic: {topic.name}")
        return True
    
    def update_topic(self, topic_name: str, **kwargs) -> bool:
        """Update an existing topic"""
        if topic_name not in self.topics:
            print(f"❌ Topic '{topic_name}' not found")
            return False
        
        topic = self.topics[topic_name]
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(topic, key):
                setattr(topic, key, value)
            else:
                print(f"⚠️  Unknown field: {key}")
        
        # Update timestamp
        topic.last_updated = datetime.now().isoformat()
        
        self.save_topics()
        print(f"✅ Updated topic: {topic_name}")
        return True
    
    def delete_topic(self, topic_name: str) -> bool:
        """Delete a topic"""
        if topic_name not in self.topics:
            print(f"❌ Topic '{topic_name}' not found")
            return False
        
        del self.topics[topic_name]
        self.save_topics()
        print(f"✅ Deleted topic: {topic_name}")
        return True
    
    def get_topic(self, topic_name: str) -> Optional[Topic]:
        """Get a topic by name"""
        return self.topics.get(topic_name)
    
    def list_topics(self, subject_area: SubjectArea = None, difficulty: DifficultyLevel = None) -> List[Topic]:
        """List topics with optional filtering"""
        topics = list(self.topics.values())
        
        if subject_area:
            topics = [t for t in topics if t.subject_area == subject_area]
        
        if difficulty:
            topics = [t for t in topics if t.difficulty_level == difficulty]
        
        return topics
    
    def search_topics(self, query: str) -> List[Topic]:
        """Search topics by name, description, or tags"""
        query_lower = query.lower()
        results = []
        
        for topic in self.topics.values():
            if (query_lower in topic.name.lower() or 
                query_lower in topic.description.lower() or 
                any(query_lower in tag.lower() for tag in topic.tags)):
                results.append(topic)
        
        return results
    
    def get_random_topics(self, count: int = 5, subject_area: SubjectArea = None) -> List[Topic]:
        """Get random topics for content generation"""
        available_topics = self.list_topics(subject_area)
        
        if len(available_topics) <= count:
            return available_topics
        
        return random.sample(available_topics, count)
    
    def get_topics_by_difficulty(self, difficulty: DifficultyLevel) -> List[Topic]:
        """Get all topics of a specific difficulty level"""
        return [topic for topic in self.topics.values() if topic.difficulty_level == difficulty]
    
    def get_topics_by_subject(self, subject_area: SubjectArea) -> List[Topic]:
        """Get all topics in a specific subject area"""
        return [topic for topic in self.topics.values() if topic.subject_area == subject_area]
    
    def get_learning_path(self, topic_name: str) -> List[Topic]:
        """Get a learning path including prerequisites"""
        if topic_name not in self.topics:
            return []
        
        topic = self.topics[topic_name]
        path = []
        
        # Add prerequisites
        for prereq in topic.prerequisites:
            matching_topics = self.search_topics(prereq)
            if matching_topics:
                path.extend(matching_topics)
        
        # Add the main topic
        path.append(topic)
        
        return path
    
    def generate_topic_suggestions(self, user_interests: List[str], count: int = 10) -> List[Topic]:
        """Generate topic suggestions based on user interests"""
        suggestions = []
        
        for interest in user_interests:
            matching_topics = self.search_topics(interest)
            suggestions.extend(matching_topics)
        
        # Remove duplicates and limit count
        seen = set()
        unique_suggestions = []
        for topic in suggestions:
            if topic.name not in seen:
                seen.add(topic.name)
                unique_suggestions.append(topic)
                if len(unique_suggestions) >= count:
                    break
        
        return unique_suggestions
    
    def get_topic_statistics(self) -> Dict:
        """Get statistics about the topic database"""
        stats = {
            'total_topics': len(self.topics),
            'by_subject_area': {},
            'by_difficulty': {},
            'by_content_type': {},
            'average_duration': 0,
            'most_common_tags': {}
        }
        
        total_duration = 0
        all_tags = []
        
        for topic in self.topics.values():
            # Count by subject area
            subject = topic.subject_area.value
            stats['by_subject_area'][subject] = stats['by_subject_area'].get(subject, 0) + 1
            
            # Count by difficulty
            difficulty = topic.difficulty_level.value
            stats['by_difficulty'][difficulty] = stats['by_difficulty'].get(difficulty, 0) + 1
            
            # Count by content type
            content_type = topic.content_type.value
            stats['by_content_type'][content_type] = stats['by_content_type'].get(content_type, 0) + 1
            
            # Calculate average duration
            total_duration += topic.estimated_duration
            
            # Collect tags
            all_tags.extend(topic.tags)
        
        stats['average_duration'] = total_duration / len(self.topics) if self.topics else 0
        
        # Count most common tags
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        stats['most_common_tags'] = dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return stats
    
    def export_topics(self, filename: str = None) -> str:
        """Export all topics to a file"""
        if not filename:
            filename = f"topics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump({name: self._topic_to_dict(topic) for name, topic in self.topics.items()}, f, indent=2)
        
        print(f"✅ Exported {len(self.topics)} topics to {filename}")
        return filename
    
    def import_topics(self, filename: str) -> bool:
        """Import topics from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            imported_count = 0
            for topic_name, topic_data in data.items():
                if topic_name not in self.topics:
                    topic = self._dict_to_topic(topic_data)
                    self.topics[topic_name] = topic
                    imported_count += 1
            
            self.save_topics()
            print(f"✅ Imported {imported_count} new topics from {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing topics: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Create topic manager
    manager = TopicManager()
    
    # List all topics
    print("Available topics:")
    for topic in manager.list_topics():
        print(f"  - {topic.name} ({topic.subject_area.value})")
    
    # Search for topics
    math_topics = manager.search_topics("math")
    print(f"\nMath-related topics: {[t.name for t in math_topics]}")
    
    # Get random topics
    random_topics = manager.get_random_topics(3)
    print(f"\nRandom topics: {[t.name for t in random_topics]}")
    
    # Get statistics
    stats = manager.get_topic_statistics()
    print(f"\nTopic statistics: {stats}")
    
    # Add a new topic
    new_topic = Topic(
        name="Climate Change",
        subject_area=SubjectArea.SCIENCE,
        difficulty_level=DifficultyLevel.INTERMEDIATE,
        content_type=ContentType.CONCEPT,
        description="Understanding the causes and effects of global climate change",
        key_concepts=["greenhouse gases", "global warming", "carbon footprint", "renewable energy"],
        learning_objectives=[
            "Understand the science behind climate change",
            "Identify human activities that contribute to climate change",
            "Explore solutions and mitigation strategies"
        ],
        prerequisites=["basic science", "environmental awareness"],
        estimated_duration=80,
        tags=["environment", "science", "sustainability"],
        created_date=datetime.now().isoformat(),
        last_updated=datetime.now().isoformat()
    )
    
    manager.add_topic(new_topic)
    print(f"\nAdded new topic: {new_topic.name}")
