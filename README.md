# TransplantAI

AI-powered kidney donor-patient matching system using machine learning and modern web technologies.

## Overview

TransplantAI is a full-stack application that leverages artificial intelligence to improve kidney transplant matching outcomes. It provides intelligent matching between donors and patients based on medical compatibility factors, using advanced machine learning models to optimize transplant success rates.

## Features

- **AI-Powered Matching**: Machine learning algorithms for optimal donor-patient pairing
- **Patient Management**: Track and manage patient profiles and medical history
- **Donor Database**: Maintain comprehensive donor information and compatibility metrics
- **Authentication**: Secure JWT-based authentication system
- **Real-time Dashboard**: Interactive web dashboard for medical professionals
- **API-First Architecture**: RESTful API for seamless integration

## Tech Stack

### Backend
- **Framework**: FastAPI 0.111.0
- **Server**: Uvicorn with async support
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT with Python-Jose
- **ML Models**: scikit-learn, XGBoost
- **API Client**: Groq for AI services

### Frontend
- **HTML5 Dashboard** with responsive design
- **Static file serving** through FastAPI
- **CSS styling** for professional UI

### Languages & Libraries
- Python 3.x
- NumPy, Pandas for data processing
- Joblib for model serialization

## Project Structure

```
kidney-transplant/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── database.py            # Database setup and ORM models
│   ├── dependencies.py        # Dependency injection
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas for validation
│   ├── ml/
│   │   ├── features.json      # Feature definitions for ML
│   │   └── model_meta.json    # Model metadata
│   ├── services/
│   │   ├── ai_service.py      # AI/Groq integration
│   │   └── ml_service.py      # Machine learning service
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── match.py           # Matching endpoints
│   │   └── history.py         # History tracking endpoints
│   └── utils/
│       └── errors.py          # Custom error handlers
├── frontend/
│   ├── index.html             # Main dashboard page
│   ├── dashboard.html         # Dashboard view
│   └── static/
│       └── style.css          # Styling
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python runtime specification
├── Procfile                  # Deployment configuration
└── render.yaml              # Render deployment config
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kidney-transplant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   GROQ_API_KEY=your-groq-api-key
   DATABASE_URL=sqlite:///./transplant.db
   ```

5. **Run the application**
   ```bash
   uvicorn backend.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/token/refresh` - Refresh access token

### Matching
- `POST /match/find` - Find donor-patient matches
- `GET /match/compatibility/{donor_id}/{patient_id}` - Check compatibility
- `GET /match/history` - Get matching history

### History
- `GET /history/patients` - Get patient history
- `GET /history/donors` - Get donor history
- `GET /health` - Health check endpoint

## Development

### Running Tests
```bash
pytest tests/
```

### Database Migrations
```bash
alembic upgrade head
```

### ML Model Training
The ML models are trained and stored in the `backend/ml/` directory. Model metadata is maintained in `model_meta.json`.

## Deployment

### Render Deployment
The application is configured for deployment on Render using:
- `render.yaml` - Deployment configuration
- `Procfile` - Process type definition
- `runtime.txt` - Python version specification

### Environment Variables for Production
Ensure these are set in your deployment environment:
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `GROQ_API_KEY` - Groq API key for AI services
- `DATABASE_URL` - Production database URL

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@transplantsai.com or open an issue in the repository.

## Acknowledgments

- FastAPI framework for building robust APIs
- XGBoost for machine learning
- Groq for AI services
- The medical research community for kidney transplant compatibility guidelines
