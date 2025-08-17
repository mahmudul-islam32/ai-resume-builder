# AI Resume Builder

A comprehensive AI-powered resume tailoring and job application tracking system.

## Features

- **User Management**: Registration, login with JWT authentication
- **Resume Upload**: PDF/DOCX parsing and preview
- **Job Link Processing**: Automatic job description scraping
- **AI Resume Tailoring**: Intelligent keyword suggestions and resume optimization
- **AI Cover Letter Generation**: Personalized cover letters
- **Application Tracker**: Complete application lifecycle tracking
- **Interview Management**: Interview scheduling and feedback tracking

## Tech Stack

- **Frontend**: SvelteKit 5
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Deployment**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Quick Start

### Using Docker (Recommended)

1. **Clone and start the application:**
   ```bash
   git clone <your-repo>
   cd ai-resume
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

That's it! The application will automatically:
- Set up the PostgreSQL database
- Build and start the backend API
- Build and start the frontend
- Create all necessary tables

### Stop the application
```bash
docker-compose -f docker-compose.dev.yml down
```

### Optional: Add AI API Keys

To enable AI features, edit the `.env` file and add your API keys:
```bash
OPENAI_API_KEY=your-openai-api-key
```

Then restart the services:
```bash
docker-compose -f docker-compose.dev.yml restart backend
```

### Troubleshooting

If you encounter build issues:
1. Clean up Docker: `docker system prune -f`
2. Rebuild: `docker-compose -f docker-compose.dev.yml up --build --force-recreate`

### Development Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `.env.example` for required environment variables.

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## License

MIT License
