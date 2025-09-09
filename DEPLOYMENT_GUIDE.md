# 🚀 Phoenix Knowledge Engine - Complete Deployment Guide

## 📋 **Overview**

This guide covers everything you need to deploy, customize, and monitor your Phoenix Knowledge Engine system.

## 🎯 **Quick Start (5 Minutes)**

### **1. Deploy to Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
./infrastructure/railway-deploy.sh
```

### **2. Deploy to Heroku**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Deploy
./infrastructure/heroku-deploy.sh
```

### **3. Deploy with Docker**
```bash
# Build and run
docker-compose up --build

# Access at http://localhost:8000
```

## 🎭 **Avatar Customization**

### **Basic Customization**
```python
from avatars.customization import AvatarCustomizer, PersonalityTrait, TeachingStyle

# Create customizer
customizer = AvatarCustomizer()

# Add personality traits to Kelly
customizer.add_personality_trait("kelly", PersonalityTrait.CREATIVE)
customizer.add_personality_trait("kelly", PersonalityTrait.ENTHUSIASTIC)

# Add expertise areas
customizer.add_expertise_area("kelly", "Creative Writing")
customizer.add_expertise_area("kelly", "Art History")

# Update prompt templates
customizer.update_prompt_template(
    "kelly", 
    "core_concept", 
    "Let's explore {topic} through a creative lens. Imagine this concept as a story..."
)

# Generate custom prompt
prompt = customizer.generate_custom_prompt(
    "kelly", 
    "core_concept", 
    "Photosynthesis",
    example="a plant in sunlight"
)
```

### **Advanced Customization**
```python
# Create completely custom avatar
from avatars.customization import AvatarConfig, TeachingStyle, PersonalityTrait

custom_avatar = AvatarConfig(
    name="Alex",
    role="Creative Educator",
    teaching_style=TeachingStyle.CREATIVE,
    personality_traits=[PersonalityTrait.CREATIVE, PersonalityTrait.ENTHUSIASTIC],
    expertise_areas=["Art", "Music", "Creative Writing", "Design"],
    voice_characteristics={
        "tone": "inspiring and creative",
        "pace": "dynamic",
        "emphasis": "imagination and creativity"
    },
    prompt_templates={
        "core_concept": "Let's paint a picture of {topic} in our minds...",
        "example": "Imagine this scenario: {example}. How does it make you feel?",
    },
    content_preferences={
        "structure": "storytelling and visual",
        "examples": "creative analogies and metaphors",
        "language": "poetic and inspiring"
    },
    interaction_style="creative, inspiring, visual",
    example_phrases=[
        "Let's paint this concept...",
        "Imagine if we could...",
        "What if we thought of it as...",
        "Let's create a story about..."
    ]
)

# Add to system
customizer.avatars["alex"] = custom_avatar
customizer.save_configs()
```

## 📚 **Topic Management**

### **Adding New Topics**
```python
from content.topic_manager import TopicManager, Topic, SubjectArea, DifficultyLevel, ContentType
from datetime import datetime

# Create topic manager
manager = TopicManager()

# Add a new topic
new_topic = Topic(
    name="Climate Change",
    subject_area=SubjectArea.SCIENCE,
    difficulty_level=DifficultyLevel.INTERMEDIATE,
    content_type=ContentType.CONCEPT,
    description="Understanding the causes and effects of global climate change",
    key_concepts=["greenhouse gases", "global warming", "carbon footprint"],
    learning_objectives=[
        "Understand the science behind climate change",
        "Identify human activities that contribute to climate change"
    ],
    prerequisites=["basic science", "environmental awareness"],
    estimated_duration=80,
    tags=["environment", "science", "sustainability"],
    created_date=datetime.now().isoformat(),
    last_updated=datetime.now().isoformat()
)

manager.add_topic(new_topic)
```

### **Bulk Topic Import**
```python
# Import topics from CSV or JSON
topics_data = [
    {
        "name": "Machine Learning Basics",
        "subject_area": "technology",
        "difficulty_level": "intermediate",
        "content_type": "concept",
        "description": "Introduction to AI and machine learning",
        "key_concepts": ["algorithms", "training data", "models"],
        "learning_objectives": ["Understand what ML is", "Recognize applications"],
        "prerequisites": ["basic programming", "statistics"],
        "estimated_duration": 75,
        "tags": ["AI", "programming", "data science"]
    }
    # ... more topics
]

# Add multiple topics
for topic_data in topics_data:
    topic = Topic(
        name=topic_data["name"],
        subject_area=SubjectArea(topic_data["subject_area"]),
        difficulty_level=DifficultyLevel(topic_data["difficulty_level"]),
        content_type=ContentType(topic_data["content_type"]),
        description=topic_data["description"],
        key_concepts=topic_data["key_concepts"],
        learning_objectives=topic_data["learning_objectives"],
        prerequisites=topic_data["prerequisites"],
        estimated_duration=topic_data["estimated_duration"],
        tags=topic_data["tags"],
        created_date=datetime.now().isoformat(),
        last_updated=datetime.now().isoformat()
    )
    manager.add_topic(topic)
```

### **Topic Discovery and Search**
```python
# Search for topics
math_topics = manager.search_topics("math")
science_topics = manager.search_topics("science")

# Get topics by difficulty
beginner_topics = manager.get_topics_by_difficulty(DifficultyLevel.BEGINNER)

# Get random topics for content generation
random_topics = manager.get_random_topics(5, SubjectArea.SCIENCE)

# Get learning path
path = manager.get_learning_path("Machine Learning Basics")
```

## 📊 **Monitoring and Alerts**

### **Basic Monitoring Setup**
```python
from monitoring.alert_system import MonitoringSystem, AlertLevel, AlertType

# Create monitoring system
monitoring = MonitoringSystem()

# Track API calls
monitoring.track_api_call("gpt-3.5-turbo", 100, 50, 1.2, True)

# Get metrics
summary = monitoring.get_metrics_summary()
print(f"Total cost: ${summary['total_cost']:.2f}")
print(f"Success rate: {summary['success_rate']:.1f}%")
```

### **Email Alerts Setup**
```python
# Configure email alerts in monitoring_config.json
{
  "alert_channels": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your-email@gmail.com",
      "password": "your-app-password",
      "from_email": "your-email@gmail.com",
      "to_emails": ["admin@yourcompany.com", "alerts@yourcompany.com"]
    }
  }
}
```

### **Slack Alerts Setup**
```python
# Configure Slack alerts
{
  "alert_channels": {
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
      "channel": "#alerts"
    }
  }
}
```

### **Custom Alert Thresholds**
```python
# Update thresholds
monitoring.thresholds = {
    "cost_daily_limit": 10.0,      # $10 per day
    "cost_monthly_limit": 100.0,   # $100 per month
    "response_time_limit": 3.0,    # 3 seconds max
    "error_rate_limit": 2.0,       # 2% max error rate
    "memory_usage_limit": 85.0,    # 85% max memory
    "cpu_usage_limit": 85.0        # 85% max CPU
}
```

## 🔧 **Advanced Configuration**

### **Environment Variables**
```bash
# Production environment
export DEBUG=False
export SECRET_KEY=your-super-secret-key
export OPENAI_API_KEY=sk-your-api-key
export DATABASE_URL=postgresql://user:pass@host:port/db
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Optional: Redis for caching
export REDIS_URL=redis://localhost:6379/0

# Optional: Email configuration
export EMAIL_HOST=smtp.gmail.com
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-app-password
```

### **Database Configuration**
```python
# For PostgreSQL (recommended for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'phoenix_knowledge'),
        'USER': os.getenv('DB_USER', 'phoenix_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### **Caching Configuration**
```python
# Redis caching for better performance
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 🚀 **Production Deployment**

### **Railway Deployment**
1. **Install Railway CLI**: `npm install -g @railway/cli`
2. **Login**: `railway login`
3. **Deploy**: `./infrastructure/railway-deploy.sh`
4. **Set environment variables** in Railway dashboard
5. **Access your app** at the provided URL

### **Heroku Deployment**
1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**: `heroku login`
3. **Deploy**: `./infrastructure/heroku-deploy.sh`
4. **Set environment variables**: `heroku config:set KEY=value`
5. **Access your app** at `https://your-app-name.herokuapp.com`

### **Docker Deployment**
```bash
# Build and run
docker-compose up --build -d

# Check logs
docker-compose logs -f

# Scale services
docker-compose up --scale web=3
```

### **AWS Deployment**
```bash
# Using AWS CLI
aws ecs create-cluster --cluster-name phoenix-knowledge-engine

# Deploy with ECS
aws ecs create-service --cluster phoenix-knowledge-engine --service-name phoenix-web
```

## 📈 **Performance Optimization**

### **Database Optimization**
```python
# Add database indexes
class LearningObjective(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['title', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
```

### **Caching Strategy**
```python
# Cache expensive operations
from django.core.cache import cache

def get_learning_plan(topic):
    cache_key = f"learning_plan_{topic}"
    result = cache.get(cache_key)
    
    if not result:
        result = generate_learning_plan(topic)
        cache.set(cache_key, result, 3600)  # Cache for 1 hour
    
    return result
```

### **API Rate Limiting**
```python
# Add rate limiting
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h', method='POST')
def generate_content(request):
    # Your view logic
    pass
```

## 🔒 **Security Best Practices**

### **API Key Security**
```python
# Use environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Rotate keys regularly
# Use different keys for different environments
```

### **Input Validation**
```python
# Validate all inputs
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_topic_input(topic):
    if not topic or len(topic.strip()) < 3:
        raise ValidationError("Topic must be at least 3 characters")
    
    if len(topic) > 200:
        raise ValidationError("Topic must be less than 200 characters")
```

### **CORS Configuration**
```python
# Configure CORS properly
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True
```

## 📊 **Monitoring Dashboard**

### **Health Check Endpoint**
```python
# Add health check
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'database': 'connected',
        'cache': 'connected'
    })
```

### **Metrics Endpoint**
```python
# Add metrics endpoint
def metrics(request):
    monitoring = MonitoringSystem()
    return JsonResponse(monitoring.get_metrics_summary())
```

## 🎉 **Success Checklist**

- [ ] **Deployment**: App is live and accessible
- [ ] **API Integration**: OpenAI API calls working
- [ ] **Cost Monitoring**: Budget alerts configured
- [ ] **Avatar Customization**: Kelly and Ken personalities set
- [ ] **Topic Management**: Topics added and organized
- [ ] **Monitoring**: Alerts and metrics working
- [ ] **Security**: Environment variables secured
- [ ] **Performance**: Caching and optimization enabled
- [ ] **Documentation**: Team trained on system
- [ ] **Backup**: Database backups configured

## 🆘 **Troubleshooting**

### **Common Issues**

**1. API Key Not Working**
```bash
# Check environment variables
echo $OPENAI_API_KEY

# Test API key
python -c "import openai; print(openai.api_key)"
```

**2. Database Connection Issues**
```bash
# Check database connection
python manage.py dbshell

# Run migrations
python manage.py migrate
```

**3. High Costs**
```python
# Check cost thresholds
monitoring.check_cost_thresholds(current_cost)

# Reduce model usage
# Use gpt-3.5-turbo instead of gpt-4
```

**4. Performance Issues**
```bash
# Check logs
tail -f monitoring.log

# Check metrics
python -c "from monitoring.alert_system import MonitoringSystem; print(MonitoringSystem().get_metrics_summary())"
```

## 📞 **Support**

- **Documentation**: Check this guide and README files
- **Logs**: Check `monitoring.log` for errors
- **Metrics**: Use monitoring dashboard
- **Alerts**: Check configured alert channels

---

**🎉 Congratulations! Your Phoenix Knowledge Engine is now fully deployed and operational!**
