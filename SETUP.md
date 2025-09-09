# Phoenix Knowledge Engine - Setup Guide

## Quick Start

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/)

### Automated Setup

1. **Clone and navigate to the project:**
   ```bash
   cd phoenix-knowledge-engine
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/setup.sh
   ```

3. **Start the development servers:**
   ```bash
   ./scripts/start-dev.sh
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database:**
   ```bash
   # Create PostgreSQL database
   createdb phoenix_knowledge_engine
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

6. **Start backend server:**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
   ```

4. **Start frontend server:**
   ```bash
   npm start
   ```

## Configuration

### Environment Variables

#### Backend (.env)
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/phoenix_knowledge_engine

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Django Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis Configuration (for Celery)
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Database Setup

### PostgreSQL Configuration

1. **Install PostgreSQL** (if not already installed)

2. **Create database:**
   ```sql
   CREATE DATABASE phoenix_knowledge_engine;
   CREATE USER phoenix_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE phoenix_knowledge_engine TO phoenix_user;
   ```

3. **Update DATABASE_URL in .env:**
   ```env
   DATABASE_URL=postgresql://phoenix_user:your_password@localhost:5432/phoenix_knowledge_engine
   ```

## API Keys

### OpenAI API Key

1. **Get API key from OpenAI:**
   - Visit https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Add to .env file:**
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

## Testing the Setup

### 1. Health Check
```bash
curl http://localhost:8000/api/health/
```

### 2. Generate Test Content
1. Open http://localhost:3000
2. Click "Generate Content"
3. Enter a topic like "The Pythagorean Theorem"
4. Click "Generate Content"

### 3. View Generated Content
1. Go to "Content" page
2. Click on the generated learning objective
3. Review the knowledge components and questions

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
django.db.utils.OperationalError: could not connect to server
```
**Solution:** Ensure PostgreSQL is running and DATABASE_URL is correct.

#### 2. OpenAI API Error
```
openai.error.AuthenticationError: Incorrect API key provided
```
**Solution:** Check your OpenAI API key in the .env file.

#### 3. Frontend Can't Connect to API
```
Network Error: axios Error
```
**Solution:** Ensure backend is running on port 8000 and REACT_APP_API_URL is correct.

#### 4. Migration Errors
```
django.db.utils.ProgrammingError: relation does not exist
```
**Solution:** Run migrations: `python manage.py migrate`

### Logs

#### Backend Logs
```bash
cd backend
source venv/bin/activate
python manage.py runserver --verbosity=2
```

#### Frontend Logs
```bash
cd frontend
npm start
```

## Development

### Adding New Features

1. **Backend Changes:**
   - Modify models in `database/models.py`
   - Create migrations: `python manage.py makemigrations`
   - Apply migrations: `python manage.py migrate`

2. **Frontend Changes:**
   - Modify components in `src/components/`
   - Add new pages in `src/pages/`
   - Update API calls in `src/services/api.js`

### Code Structure

```
phoenix-knowledge-engine/
├── backend/                 # Django backend
│   ├── phoenix/            # Main Django app
│   ├── database/           # Database models
│   ├── orchestrator/       # Orchestrator AI service
│   ├── worker/             # Worker AI service
│   ├── quality_control/    # Quality control system
│   └── api/                # REST API endpoints
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── public/
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## Production Deployment

### Backend Deployment

1. **Set production environment variables**
2. **Use production database**
3. **Configure static files**
4. **Set up reverse proxy (nginx)**
5. **Use production WSGI server (gunicorn)**

### Frontend Deployment

1. **Build production bundle:**
   ```bash
   npm run build
   ```
2. **Serve static files**
3. **Configure CDN if needed**

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Check the API documentation at http://localhost:8000/api/
4. Create an issue in the repository

## Next Steps

After successful setup:
1. Generate your first learning objective
2. Explore the three-layer AI architecture
3. Customize prompts for your specific needs
4. Set up monitoring and logging
5. Plan for production deployment
