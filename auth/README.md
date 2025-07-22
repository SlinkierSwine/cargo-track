# Auth Service

Authentication and authorization service for the Cargo Track system.

## Setup

1. Copy environment variables:
```bash
cp env.example .env
```

2. Update the `.env` file with your configuration.

3. Run with Docker Compose:
```bash
docker-compose up --build
```

## API Endpoints

- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

## Development

The service follows Clean Architecture principles with the following structure:

- `controllers/` - FastAPI route handlers
- `use_cases/` - Business logic
- `repositories/` - Data access layer
- `entities/` - Pydantic models
- `config/` - Configuration and settings 