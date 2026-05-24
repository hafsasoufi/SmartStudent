# SmartStudent - AI-Powered Student Assistant

A complete AI-driven platform for student success, featuring an intelligent orchestrator agent, specialized AI agents for different student needs, and a Flutter mobile application for access across all six core modules.

## Project Structure

```
.
├── backend/              # FastAPI Python backend
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy database models
│   ├── database.py      # Database configuration
│   ├── auth.py          # JWT authentication utilities
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── config.py        # Application settings
│   └── requirements.txt  # Python dependencies
│
├── flutter/             # Flutter Android mobile app
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/
│   │   ├── models/      # Data models
│   │   ├── providers/   # Riverpod state management
│   │   ├── services/    # API and storage services
│   │   ├── screens/     # UI screens
│   │   ├── routes/      # Navigation/routing
│   │   └── theme/       # Theme configuration
│   └── pubspec.yaml     # Flutter dependencies
│
└── README.md            # This file
```

## Backend Setup

### Prerequisites
- Python 3.9+
- PostgreSQL (or SQLite for development)
- Redis (optional, for caching)

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
- Database URL (PostgreSQL connection string)
- OpenAI API key
- JWT secret key (generate a strong one)
- Other API keys (Pinecone, Firebase, etc.)

6. Initialize the database:
```bash
python -c "from database import init_db; init_db()"
```

7. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with docs at `/docs`.

## Flutter App Setup

### Prerequisites
- Flutter SDK 3.0+
- Android SDK (for Android development)
- Xcode (for iOS development, optional)

### Installation

1. Navigate to the Flutter directory:
```bash
cd flutter
```

2. Get dependencies:
```bash
flutter pub get
```

3. Generate necessary files:
```bash
flutter pub run build_runner build
```

4. Configure Firebase:
   - Create a Firebase project in the Firebase Console
   - Add Android app configuration
   - Download and place `google-services.json` in `android/app/`

5. Update `firebase_options.dart` with your Firebase configuration

6. Run the app:
```bash
flutter run
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### User
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Chat
- `POST /api/chat` - Send message to orchestrator

## Features

### Core Modules
1. **Admin Module** - FAQs, documents, request tracking
2. **Planning Module** - Calendar, deadlines, smart reminders
3. **Exams Module** - Quizzes, practice exams, performance tracking
4. **Orientation Module** - Career advice, CV templates, internships
5. **Campus Module** - Events, clubs, study groups
6. **Well-being Module** - Mental health resources, wellness tracking

### Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- Pydantic - Data validation
- JWT - Secure authentication
- PostgreSQL - Relational database
- Redis - Caching and sessions
- LangGraph - Agent orchestration
- Pinecone - Vector database for RAG

**Frontend:**
- Flutter - Cross-platform mobile app
- Riverpod - State management
- Dio - HTTP client
- Hive - Local storage
- Firebase - Push notifications

## Environment Variables

### Backend (.env)
```
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/smartstudent
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
FIREBASE_CREDENTIALS=/path/to/credentials.json
```

### Flutter
Update `lib/config/app_config.dart`:
```dart
static const String apiBaseUrl = 'http://localhost:8000/api';
```

## Development Workflow

### Adding a New Endpoint

1. Create schema in `backend/schemas.py`
2. Create route in `backend/main.py` or a new route file
3. Test with the API docs at `/docs`
4. Update Flutter API service in `flutter/lib/services/api_service.dart`
5. Create Riverpod provider if needed

### Adding a New Screen

1. Create screen file in `flutter/lib/screens/`
2. Add route in `flutter/lib/routes/router.dart`
3. Update navigation as needed
4. Test in the app

## Database Schema

Key tables:
- `users` - User accounts
- `user_profiles` - Extended user information
- `messages` - Chat history
- `memories` - User context for agents
- `documents` - Documents for RAG
- `exams` - Exam records
- `events` - Campus events
- `plans` - User plans and deadlines

## Next Steps

1. **Implement LangGraph Orchestrator** - Multi-agent coordination
2. **Create Specialized Agents** - Admin, Planning, Exams, Orientation, Campus
3. **Integrate RAG System** - Document indexing with Pinecone
4. **Complete Module UI** - Full feature implementation for each module
5. **Testing & Deployment** - Unit tests, integration tests, CI/CD
6. **Localization** - Multi-language support (FR, AR, EN)

## Contributing

Follow these guidelines:
1. Use type hints in Python and Dart
2. Write docstrings for functions
3. Keep components modular and reusable
4. Test before committing
5. Use meaningful commit messages

## License

MIT License

## Support

For issues or questions:
1. Check existing documentation
2. Create an issue with detailed description
3. Contact the development team

---

**Version:** 1.0.0
**Last Updated:** May 2026
