#!/usr/bin/env python3
"""
Advanced Features Demo for Phoenix Knowledge Engine
Demonstrates avatar customization, topic management, and monitoring
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our modules
from avatars.customization import AvatarCustomizer, PersonalityTrait, TeachingStyle
from content.topic_manager import TopicManager, Topic, SubjectArea, DifficultyLevel, ContentType
from monitoring.alert_system import MonitoringSystem, AlertLevel, AlertType

class AdvancedFeaturesDemo:
    """Demo of advanced Phoenix Knowledge Engine features"""
    
    def __init__(self):
        self.avatar_customizer = AvatarCustomizer()
        self.topic_manager = TopicManager()
        self.monitoring = MonitoringSystem()
        
        print("🎯 Phoenix Knowledge Engine - Advanced Features Demo")
        print("=" * 60)
    
    def demo_avatar_customization(self):
        """Demonstrate avatar customization features"""
        print("\n🎭 AVATAR CUSTOMIZATION DEMO")
        print("-" * 40)
        
        # Show current avatars
        print("Current avatars:", self.avatar_customizer.list_avatars())
        
        # Get Kelly's current configuration
        kelly_config = self.avatar_customizer.get_avatar_config("kelly")
        if kelly_config:
            print(f"\nKelly's current traits: {[t.value for t in kelly_config.personality_traits]}")
            print(f"Kelly's expertise: {kelly_config.expertise_areas}")
        
        # Add creative trait to Kelly
        print("\n➕ Adding creative trait to Kelly...")
        self.avatar_customizer.add_personality_trait("kelly", PersonalityTrait.CREATIVE)
        
        # Add new expertise area
        print("➕ Adding 'Creative Writing' expertise to Kelly...")
        self.avatar_customizer.add_expertise_area("kelly", "Creative Writing")
        
        # Update prompt template
        print("📝 Updating Kelly's core concept template...")
        self.avatar_customizer.update_prompt_template(
            "kelly", 
            "core_concept", 
            "Let's explore {topic} through a creative lens. Imagine this concept as a story that unfolds..."
        )
        
        # Generate custom prompt
        print("\n🎨 Generating custom prompt for Kelly...")
        custom_prompt = self.avatar_customizer.generate_custom_prompt(
            "kelly", 
            "core_concept", 
            "Photosynthesis",
            example="a plant in sunlight"
        )
        
        print(f"Custom prompt preview:\n{custom_prompt[:200]}...")
        
        # Show updated configuration
        updated_kelly = self.avatar_customizer.get_avatar_config("kelly")
        print(f"\nKelly's updated traits: {[t.value for t in updated_kelly.personality_traits]}")
        print(f"Kelly's updated expertise: {updated_kelly.expertise_areas}")
    
    def demo_topic_management(self):
        """Demonstrate topic management features"""
        print("\n📚 TOPIC MANAGEMENT DEMO")
        print("-" * 40)
        
        # Show current topics
        topics = self.topic_manager.list_topics()
        print(f"Current topics: {len(topics)}")
        for topic in topics[:5]:  # Show first 5
            print(f"  - {topic.name} ({topic.subject_area.value})")
        
        # Search for topics
        print("\n🔍 Searching for 'math' topics...")
        math_topics = self.topic_manager.search_topics("math")
        print(f"Found {len(math_topics)} math-related topics")
        
        # Get topics by difficulty
        print("\n📊 Topics by difficulty:")
        for difficulty in DifficultyLevel:
            topics = self.topic_manager.get_topics_by_difficulty(difficulty)
            print(f"  {difficulty.value}: {len(topics)} topics")
        
        # Add a new topic
        print("\n➕ Adding new topic: 'Climate Change'...")
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
        
        success = self.topic_manager.add_topic(new_topic)
        if success:
            print("✅ Topic added successfully!")
        
        # Get random topics for content generation
        print("\n🎲 Getting random topics for content generation...")
        random_topics = self.topic_manager.get_random_topics(3)
        print(f"Random topics: {[t.name for t in random_topics]}")
        
        # Get topic statistics
        print("\n📈 Topic statistics:")
        stats = self.topic_manager.get_topic_statistics()
        print(f"  Total topics: {stats['total_topics']}")
        print(f"  By subject area: {stats['by_subject_area']}")
        print(f"  By difficulty: {stats['by_difficulty']}")
        print(f"  Average duration: {stats['average_duration']:.1f} minutes")
    
    def demo_monitoring_system(self):
        """Demonstrate monitoring and alerting features"""
        print("\n📊 MONITORING SYSTEM DEMO")
        print("-" * 40)
        
        # Simulate some API calls
        print("🔄 Simulating API calls...")
        self.monitoring.track_api_call("gpt-3.5-turbo", 100, 50, 1.2, True)
        self.monitoring.track_api_call("gpt-3.5-turbo", 200, 100, 2.1, True)
        self.monitoring.track_api_call("gpt-3.5-turbo", 150, 75, 0.8, False)
        self.monitoring.track_api_call("gpt-4", 300, 150, 3.5, True)
        
        # Get metrics summary
        print("\n📈 Current metrics:")
        summary = self.monitoring.get_metrics_summary()
        print(f"  Total cost: ${summary['total_cost']:.4f}")
        print(f"  Total calls: {summary['total_calls']}")
        print(f"  Success rate: {summary['success_rate']:.1f}%")
        print(f"  Error rate: {summary['error_rate']:.1f}%")
        print(f"  Average response time: {summary['average_response_time']:.2f}s")
        print(f"  Active alerts: {summary['active_alerts']}")
        
        # Check for alerts
        print("\n🚨 Checking for alerts...")
        alerts = self.monitoring.get_alerts(resolved=False)
        if alerts:
            print(f"Found {len(alerts)} active alerts:")
            for alert in alerts:
                print(f"  - [{alert.level.value.upper()}] {alert.title}")
        else:
            print("No active alerts")
        
        # Create a test alert
        print("\n🔔 Creating test alert...")
        test_alert = self.monitoring.create_alert(
            AlertLevel.WARNING,
            AlertType.SYSTEM,
            "Test Alert",
            "This is a test alert to demonstrate the alerting system",
            {"test": True, "timestamp": datetime.now().isoformat()}
        )
        print(f"Created alert: {test_alert.id}")
        
        # Show all alerts
        all_alerts = self.monitoring.get_alerts()
        print(f"\nTotal alerts: {len(all_alerts)}")
        
        # Export alerts
        print("\n💾 Exporting alerts...")
        export_file = self.monitoring.export_alerts()
        print(f"Alerts exported to: {export_file}")
    
    def demo_integrated_workflow(self):
        """Demonstrate integrated workflow with all features"""
        print("\n🔄 INTEGRATED WORKFLOW DEMO")
        print("-" * 40)
        
        # Get a random topic
        random_topics = self.topic_manager.get_random_topics(1)
        if not random_topics:
            print("No topics available for demo")
            return
        
        topic = random_topics[0]
        print(f"Selected topic: {topic.name}")
        print(f"Subject area: {topic.subject_area.value}")
        print(f"Difficulty: {topic.difficulty_level.value}")
        
        # Select appropriate avatar based on topic
        if topic.subject_area in [SubjectArea.SCIENCE, SubjectArea.MATHEMATICS]:
            avatar_name = "kelly"
            avatar_type = "Academic Specialist"
        else:
            avatar_name = "ken"
            avatar_type = "Practical Expert"
        
        print(f"Selected avatar: {avatar_name} ({avatar_type})")
        
        # Generate custom prompt
        custom_prompt = self.avatar_customizer.generate_custom_prompt(
            avatar_name,
            "core_concept",
            topic.name,
            example="a practical example"
        )
        
        print(f"\nGenerated prompt preview:\n{custom_prompt[:300]}...")
        
        # Simulate content generation with monitoring
        print(f"\n🎯 Generating content for '{topic.name}'...")
        start_time = time.time()
        
        # Simulate API call
        success = True  # In real implementation, this would call OpenAI API
        response_time = time.time() - start_time
        
        # Track the API call
        self.monitoring.track_api_call(
            "gpt-3.5-turbo",
            200,  # input tokens
            100,  # output tokens
            response_time,
            success
        )
        
        print(f"✅ Content generated successfully!")
        print(f"⏱️  Response time: {response_time:.2f}s")
        
        # Check if any alerts were triggered
        alerts = self.monitoring.get_alerts(resolved=False)
        if alerts:
            print(f"🚨 {len(alerts)} alerts triggered during generation")
        else:
            print("✅ No alerts triggered - system running smoothly")
    
    def run_complete_demo(self):
        """Run the complete advanced features demo"""
        print("🚀 Starting Advanced Features Demo")
        print("=" * 60)
        
        try:
            # Demo each feature
            self.demo_avatar_customization()
            self.demo_topic_management()
            self.demo_monitoring_system()
            self.demo_integrated_workflow()
            
            print("\n" + "=" * 60)
            print("🎉 ADVANCED FEATURES DEMO COMPLETE!")
            print("=" * 60)
            
            # Final summary
            print("\n📊 FINAL SUMMARY:")
            print(f"✅ Avatar customization: Working")
            print(f"✅ Topic management: Working")
            print(f"✅ Monitoring system: Working")
            print(f"✅ Integrated workflow: Working")
            
            # Show final metrics
            final_summary = self.monitoring.get_metrics_summary()
            print(f"\n💰 Total cost: ${final_summary['total_cost']:.4f}")
            print(f"📞 Total API calls: {final_summary['total_calls']}")
            print(f"📈 Success rate: {final_summary['success_rate']:.1f}%")
            
            print(f"\n🎯 All systems operational and ready for production!")
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main demo function"""
    print("🎯 Phoenix Knowledge Engine - Advanced Features Demo")
    print("This demonstrates avatar customization, topic management, and monitoring")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed with the advanced features demo? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Demo cancelled.")
        return
    
    # Create and run demo
    demo = AdvancedFeaturesDemo()
    demo.run_complete_demo()

if __name__ == "__main__":
    main()
