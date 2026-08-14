# Pratap's AI Portfolio Backend

Django backend for an interactive AI-powered portfolio chatbot.

## Setup

```bash
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Running

The app will be available at `http://localhost:8000`

- **Chat Interface**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`

## How It Works

1. **Profile Data**: Loads `profile.json` from `Ai-Engineer/AiPortfolio/` on startup
2. **Chat**: Each conversation creates a new `Conversation` object in the database
3. **Messages**: All messages (user + AI) are stored in the `Message` model
4. **LLM**: Uses Groq's API with the system prompt from `hr_assistant.py`

## Database

Uses SQLite by default. Change in `config/settings.py` for PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_portfolio',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Features

- ✅ Multi-turn conversation memory
- ✅ Persistent conversation history (SQLite)
- ✅ Tailwind CSS UI
- ✅ Mobile responsive
- ✅ Admin panel to view messages
- ✅ No auth required (can add later)

## Environment

Set `GROQ_API_KEY` in `.env`:

```
GROQ_API_KEY=your_key_here
```

## Deployment

For production:

1. Set `DEBUG=False` in settings.py
2. Collect static files: `python manage.py collectstatic`
3. Use Gunicorn: `pip install gunicorn && gunicorn config.wsgi`
4. Deploy to Render/Railway/Heroku
