# AI Resume Builder & ATS Optimizer

A comprehensive AI-powered resume builder and Applicant Tracking System (ATS) optimizer that helps you create professional resumes and optimize them for job applications using advanced NLP and machine learning.

## 🚀 Features

### Core Features
- **AI-Powered Resume Analysis**: Advanced ATS scoring using spaCy NLP with semantic analysis
- **Job Posting Scraper**: Automatically extract and format job descriptions from URLs
- **Professional Resume Builder**: Rich text editor with formatting options and PDF export
- **Cover Letter Generator**: AI-generated personalized cover letters with customizable tones
- **Real-time ATS Optimization**: Instant scoring and improvement suggestions
- **Professional PDF Export**: Download resumes in professional format with proper styling
- **User Authentication**: Secure JWT-based authentication system
- **Application Tracking**: Complete application lifecycle management
- **Interview Management**: Schedule and track interview feedback

### Technical Features
- **Advanced NLP**: spaCy integration for semantic analysis and keyword extraction
- **Smart Keyword Detection**: Intelligent identification of relevant skills and industry terms
- **Format Analysis**: Resume structure and readability assessment
- **Experience Level Detection**: Automatic experience classification
- **Multi-format Support**: PDF, DOCX, TXT file processing and parsing
- **Rich Text Editor**: Professional editing with formatting, lists, and styling
- **PDF Generation**: Client-side PDF creation with jsPDF
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

### User Experience
- **Professional UI**: Modern, responsive design with intuitive navigation
- **Real-time Analysis**: Instant ATS scoring and feedback
- **Side-by-side Comparison**: Job posting and resume comparison view
- **Progress Tracking**: Application status and interview management
- **Dashboard Analytics**: Visual insights into application performance
- **Dark/Light Mode**: User preference support

## 🏗️ Architecture

### Backend (FastAPI)
- **Python 3.11+** with FastAPI framework for high-performance API
- **PostgreSQL** database for data persistence and relationships
- **Redis** for caching, session management, and job queues
- **spaCy** for advanced NLP processing and semantic analysis
- **Ollama** integration for local LLM support and AI features
- **Docker** containerization for consistent deployment
- **JWT Authentication** for secure user sessions
- **SQLAlchemy ORM** for database operations

### Frontend (SvelteKit)
- **SvelteKit 5** for modern web development with SSR
- **TypeScript** for type safety and better development experience
- **Tailwind CSS** for utility-first styling and responsive design
- **Rich Text Editor** with professional formatting options
- **PDF Generation** with jsPDF for client-side document creation
- **Chart.js** for data visualization and analytics
- **Responsive Design** for all devices and screen sizes

## 📁 Project Structure

```
ai-resume-builder/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/        # API endpoints
│   │   │       │   ├── ai.py         # AI service endpoints
│   │   │       │   ├── applications.py # Application tracking
│   │   │       │   ├── ats.py        # ATS scoring endpoints
│   │   │       │   ├── auth.py       # Authentication endpoints
│   │   │       │   ├── interviews.py # Interview management
│   │   │       │   ├── jobs.py       # Job scraping endpoints
│   │   │       │   ├── resumes.py    # Resume management
│   │   │       │   └── users.py      # User management
│   │   │       └── router.py         # API router configuration
│   │   ├── core/
│   │   │   ├── config.py             # Application configuration
│   │   │   ├── database.py           # Database connection
│   │   │   └── security.py           # Security utilities
│   │   ├── models/
│   │   │   └── base.py               # Database models
│   │   ├── schemas/
│   │   │   └── schemas.py            # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ai_service.py         # AI integration service
│   │   │   ├── ats_service.py        # Main ATS scoring service
│   │   │   ├── ats_service_simple.py # Simple ATS service
│   │   │   ├── custom_model_service.py # Custom model integration
│   │   │   ├── job_scraper.py        # Job posting scraper
│   │   │   ├── model_factory.py      # Model factory pattern
│   │   │   ├── my_custom_model.py    # Custom model implementation
│   │   │   └── resume_parser.py      # Resume parsing service
│   │   ├── utils/                    # Utility functions
│   │   └── main.py                   # FastAPI application entry
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-docker.txt       # Docker-specific dependencies
│   ├── requirements-simple.txt       # Simple setup dependencies
│   ├── Dockerfile                    # Production Dockerfile
│   └── Dockerfile.simple             # Simple Dockerfile
├── frontend/                         # SvelteKit Frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/           # Reusable components
│   │   │   │   ├── ActivityFeed.svelte
│   │   │   │   ├── ApplicationChart.svelte
│   │   │   │   ├── CoverLetterGenerator.svelte
│   │   │   │   ├── JobLinkScraper.svelte
│   │   │   │   ├── JobPostingDisplay.svelte
│   │   │   │   ├── QuickActions.svelte
│   │   │   │   ├── RecentApplications.svelte
│   │   │   │   ├── ResumeUpload.svelte
│   │   │   │   ├── RichTextEditor.svelte
│   │   │   │   ├── StatsCard.svelte
│   │   │   │   └── UpcomingInterviews.svelte
│   │   │   ├── services/             # API services
│   │   │   │   ├── atsApi.ts         # ATS API integration
│   │   │   │   ├── atsAudit.ts       # ATS audit service
│   │   │   │   ├── atsExtractor.ts   # Keyword extraction
│   │   │   │   ├── atsScorer.ts      # ATS scoring service
│   │   │   │   ├── coverLetterService.ts # Cover letter service
│   │   │   │   ├── dashboard.ts      # Dashboard data service
│   │   │   │   ├── enhancedAtsScorer.ts # Enhanced ATS scoring
│   │   │   │   └── pdfService.ts     # PDF generation service
│   │   │   ├── stores/               # Svelte stores
│   │   │   │   └── auth.ts           # Authentication store
│   │   │   ├── types/                # TypeScript types
│   │   │   │   └── dashboard.ts      # Dashboard types
│   │   │   └── utils/                # Utility functions
│   │   │       ├── api.ts            # API utilities
│   │   │       ├── date.ts           # Date utilities
│   │   │       └── validation.ts     # Validation utilities
│   │   ├── routes/                   # SvelteKit routes
│   │   │   ├── +layout.svelte        # Root layout
│   │   │   ├── +page.svelte          # Home page
│   │   │   ├── applications/         # Application tracking
│   │   │   ├── cover-letters/        # Cover letter generation
│   │   │   ├── dashboard/            # User dashboard
│   │   │   ├── interviews/           # Interview management
│   │   │   ├── jobs/                 # Job search and scraping
│   │   │   ├── login/                # Authentication
│   │   │   ├── match/                # Resume-job matching
│   │   │   ├── register/             # User registration
│   │   │   └── resumes/              # Resume management
│   │   ├── app.css                   # Global styles
│   │   └── app.html                  # HTML template
│   ├── static/                       # Static assets
│   ├── package.json                  # Node.js dependencies
│   ├── svelte.config.js              # SvelteKit configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── vite.config.js                # Vite configuration
│   ├── Dockerfile                    # Frontend Dockerfile
│   └── Dockerfile.dev                # Development Dockerfile
├── docker/                           # Docker configuration
│   ├── init.sql                      # Database initialization
│   └── nginx.conf                    # Nginx configuration
├── uploads/                          # File upload directory
│   └── .gitkeep                      # Keep directory in git
├── .github/                          # GitHub Actions
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── docker-compose.yml                # Production Docker setup
├── docker-compose.dev.yml            # Development Docker setup
└── README.md                         # This file
```

## 📋 Prerequisites

### For Docker Setup
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git** (version 2.30+)

### For Local Development
- **Python** (version 3.11+)
- **Node.js** (version 18+)
- **PostgreSQL** (version 15+)
- **Redis** (version 7+)
- **Git** (version 2.30+)

## 🐳 Installation with Docker (Recommended)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/mahmudul-islam32/ai-resume-builder.git
cd ai-resume-builder

# Copy environment template
cp .env.example .env

# Edit environment variables (optional)
nano .env

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Database: localhost:5433
# Redis: localhost:6379
# Ollama: localhost:11434
```

### Docker Services
- **Frontend** (Port 3000): SvelteKit application with hot reload
- **Backend** (Port 8000): FastAPI application with auto-reload
- **Database** (Port 5433): PostgreSQL with persistent storage
- **Redis** (Port 6379): Caching and session management
- **Ollama** (Port 11434): Local LLM service for AI features

### Environment Configuration
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@db:5432/ai_resume

# Redis Configuration
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-here-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# OpenAI Configuration (Optional - for enhanced features)
OPENAI_API_KEY=your-openai-api-key-here

# Application Settings
APP_NAME=AI Resume Builder
DEBUG=true
ENVIRONMENT=development

# Database Pool Settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=AI Resume Builder API

# Email Settings (Optional)
SMTP_TLS=true
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Ollama Settings (Optional - for local LLM)
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2

# spaCy Model Settings
SPACY_MODEL=en_core_web_md
```

## 💻 Local Development Setup

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md

# Set up environment variables
cp ../.env.example ../.env
# Edit ../.env with your local settings

# Set up database
# Create PostgreSQL database and update DATABASE_URL in .env

# Run migrations (if using Alembic)
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Setup
```bash
# Install PostgreSQL
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/

# Start PostgreSQL service
# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS
brew services start postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE ai_resume;
CREATE USER ai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_resume TO ai_user;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://ai_user:your_password@localhost:5432/ai_resume
```

### Redis Setup
```bash
# Install Redis
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# Download from https://redis.io/download

# Start Redis
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew services start redis

# Test Redis connection
redis-cli ping
# Should return: PONG
```

## 🔧 Configuration

### Backend Configuration
The backend uses environment variables for configuration. Key settings:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_resume

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (Optional)
OPENAI_API_KEY=your-openai-api-key

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration
Frontend configuration is in `frontend/src/lib/utils/api.ts`:

```typescript
// API base URL
export const API_BASE_URL = 'http://localhost:8000';

// API endpoints
export const ENDPOINTS = {
  AUTH: '/api/v1/auth',
  RESUME: '/api/v1/resumes',
  JOBS: '/api/v1/jobs',
  ATS: '/api/v1/ats',
  APPLICATIONS: '/api/v1/applications',
  INTERVIEWS: '/api/v1/interviews',
  COVER_LETTERS: '/api/v1/cover-letters',
  USERS: '/api/v1/users',
  AI: '/api/v1/ai'
};
```

## 🚀 Usage Guide

### 1. User Registration & Authentication
1. Navigate to http://localhost:3000
2. Click "Register" to create a new account
3. Fill in your details and create account
4. Login with your credentials
5. Access your personalized dashboard

### 2. Resume Upload & Analysis
1. Go to "Resumes" section
2. Upload your resume (PDF, DOCX, TXT)
3. View automatic parsing and formatting
4. Edit resume content with rich text editor
5. Download optimized PDF version

### 3. Job Posting Analysis
1. Navigate to "Jobs" section
2. Paste a job posting URL
3. Let the scraper extract job details
4. View keyword analysis and requirements
5. Compare with your resume

### 4. ATS Optimization
1. Go to "Match" section
2. Upload resume and paste job URL
3. Get real-time ATS scoring
4. View improvement suggestions
5. Optimize resume based on feedback

### 5. Cover Letter Generation
1. Select job posting and resume
2. Choose writing tone and focus areas
3. Generate personalized cover letter
4. Edit and customize content
5. Download professional PDF

### 6. Application Tracking
1. Track all your job applications
2. Monitor application status
3. Schedule interviews
4. Record feedback and notes
5. View analytics and insights

## 🔍 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Resumes
- `POST /api/v1/resumes/upload` - Upload resume
- `GET /api/v1/resumes/` - List user resumes
- `GET /api/v1/resumes/{id}` - Get resume details
- `PUT /api/v1/resumes/{id}` - Update resume
- `DELETE /api/v1/resumes/{id}` - Delete resume

### ATS Analysis
- `POST /api/v1/ats/score-resume` - Score resume against job
- `GET /api/v1/ats/analysis/{id}` - Get analysis results
- `POST /api/v1/ats/extract-keywords` - Extract keywords from text

### Job Postings
- `POST /api/v1/jobs/scrape` - Scrape job posting
- `GET /api/v1/jobs/` - List scraped jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `DELETE /api/v1/jobs/{id}` - Delete job

### Applications
- `POST /api/v1/applications/` - Create application
- `GET /api/v1/applications/` - List applications
- `PUT /api/v1/applications/{id}` - Update application
- `DELETE /api/v1/applications/{id}` - Delete application

### Interviews
- `POST /api/v1/interviews/` - Schedule interview
- `GET /api/v1/interviews/` - List interviews
- `PUT /api/v1/interviews/{id}` - Update interview
- `DELETE /api/v1/interviews/{id}` - Cancel interview

### Cover Letters
- `POST /api/v1/cover-letters/generate` - Generate cover letter
- `GET /api/v1/cover-letters/` - List cover letters
- `PUT /api/v1/cover-letters/{id}` - Update cover letter
- `DELETE /api/v1/cover-letters/{id}` - Delete cover letter

### AI Services
- `POST /api/v1/ai/analyze-resume` - AI resume analysis
- `POST /api/v1/ai/generate-content` - AI content generation
- `POST /api/v1/ai/optimize-text` - AI text optimization

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_ats_service.py
```

### Frontend Tests
```bash
cd frontend

# Install test dependencies
npm install --save-dev vitest @testing-library/svelte

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

### Docker Tests
```bash
# Test all services
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Test specific service
docker-compose exec backend pytest tests/
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Reset Docker containers
docker-compose down -v
docker-compose up -d

# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

#### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d db
# Wait for database to start, then start other services
docker-compose up -d

# Check database connection
docker-compose exec db psql -U postgres -d ai_resume -c "\dt"
```

#### spaCy Issues
```bash
# Reinstall spaCy models
docker-compose exec backend python -m spacy download en_core_web_sm
docker-compose exec backend python -m spacy download en_core_web_md

# Test spaCy installation
docker-compose exec backend python -c "import spacy; nlp = spacy.load('en_core_web_md'); print('spaCy working!')"
```

#### Frontend Issues
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear SvelteKit cache
rm -rf .svelte-kit
npm run dev
```

#### API Connection Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check CORS settings
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/v1/auth/me
```

### Performance Optimization
- Enable Redis caching for better performance
- Use production-grade database for large datasets
- Configure proper CORS settings for production
- Set up proper logging and monitoring
- Use CDN for static assets in production
- Enable compression for API responses

### Security Best Practices
- Change default passwords
- Use strong SECRET_KEY
- Enable HTTPS in production
- Set up proper CORS origins
- Validate file uploads
- Implement rate limiting
- Use environment variables for secrets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write tests for new features
- Update documentation for API changes
- Follow conventional commit messages
- Add proper error handling
- Include type hints in Python code

### Code Style
```python
# Python (Backend)
def calculate_ats_score(resume_text: str, job_description: str) -> float:
    """Calculate ATS score for resume against job description."""
    # Implementation
    pass
```

```typescript
// TypeScript (Frontend)
interface AtsScore {
  overall_score: number;
  keyword_match: number;
  format_score: number;
}

const calculateScore = (resume: string, job: string): AtsScore => {
  // Implementation
};
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy** for advanced NLP capabilities and semantic analysis
- **FastAPI** for the excellent web framework and automatic documentation
- **SvelteKit** for the modern frontend framework and developer experience
- **Tailwind CSS** for the beautiful UI components and utility-first approach
- **Ollama** for local LLM integration and AI features
- **PostgreSQL** for robust database management
- **Redis** for caching and session management
- **Docker** for containerization and deployment

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review troubleshooting section
- Join our community discussions

## 🔄 Updates

Stay updated with the latest features and improvements:
- Watch the repository for updates
- Check the releases page
- Follow the changelog
- Subscribe to release notifications

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Set up reverse proxy (nginx)
# Configure SSL certificates
# Set up monitoring and logging
```

### Environment Variables for Production
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod_user:prod_password@prod_db:5432/ai_resume_prod
REDIS_URL=redis://prod_redis:6379
SECRET_KEY=your-production-secret-key
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

---

**Built with ❤️ using modern web technologies**

*AI Resume Builder - Making job applications smarter and more effective*
