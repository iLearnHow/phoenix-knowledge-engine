# Phoenix Knowledge Engine - MVP Implementation

## Overview

This is the MVP implementation of the Autonomous Knowledge Engine, featuring the three-layer AI architecture for automated educational content generation.

## Architecture

### Three-Layer System
1. **Orchestrator AI**: Breaks down learning objectives into structured plans
2. **Worker AI**: Generates atomic content pieces based on specific prompts
3. **Quality Control**: Validates content before database insertion

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Node.js 18+ (for frontend)
- OpenAI API key (for MVP)

### Installation

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database Setup**
```bash
# Create database
createdb phoenix_knowledge_engine

# Run migrations
python manage.py migrate
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### Running the Application

1. **Start the backend server**
```bash
cd backend
python manage.py runserver
```

2. **Start the frontend**
```bash
cd frontend
npm run dev
```

3. **Access the application**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Admin: http://localhost:8000/admin

## Project Structure

```
phoenix-knowledge-engine/
├── backend/                 # Django backend
│   ├── phoenix/            # Main Django app
│   ├── orchestrator/       # Orchestrator AI service
│   ├── worker/             # Worker AI service
│   ├── quality_control/    # Quality control system
│   ├── database/           # Database models and migrations
│   └── api/                # REST API endpoints
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   └── public/
├── infrastructure/         # Infrastructure as Code
│   ├── terraform/          # Terraform configurations
│   └── docker/             # Docker configurations
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

## Features

- ✅ Three-layer AI architecture
- ✅ PostgreSQL database with proper schema
- ✅ REST API for content generation
- ✅ React frontend for topic submission
- ✅ Quality control pipeline
- ✅ Real-time content generation status
- ✅ Content validation and approval workflow

## Development

### Adding New Content Types
1. Update the `KnowledgeComponentType` enum in `database/models.py`
2. Add corresponding prompts in `worker/prompts.py`
3. Update the frontend components to handle the new type

### Customizing AI Prompts
Edit the prompt templates in:
- `orchestrator/prompts.py` - Orchestrator AI prompts
- `worker/prompts.py` - Worker AI prompts
- `quality_control/prompts.py` - Quality control prompts

## API Documentation

### Generate Content
```http
POST /api/generate/
Content-Type: application/json

{
  "topic": "The Pythagorean Theorem",
  "priority": 1
}
```

### Get Content Status
```http
GET /api/content/{content_id}/
```

### List Generated Content
```http
GET /api/content/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

