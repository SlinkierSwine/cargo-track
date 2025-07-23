# Fleet Service

Service for managing fleet vehicles and drivers.

## Features

- Vehicle management (type, number, capacity)
- Driver management
- Route assignment

## Setup

1. Copy environment file:
```bash
cp env.example .env
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Run tests:
```bash
docker-compose exec fleet-service pytest
```

## API Endpoints

- `GET /` - Service status
- `GET /health` - Health check

## Development

The service follows Clean Architecture principles with:
- Controllers layer for HTTP handling
- Use Cases layer for business logic
- Repositories layer for data access
- Entities layer for domain models

All code follows TDD (Test-Driven Development) approach. 