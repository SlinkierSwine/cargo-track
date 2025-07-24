# Orders Service

Service for managing cargo transportation orders.

## Features

- Order creation and management
- Vehicle and driver assignment
- Order status tracking
- Integration with fleet and warehouse services

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
docker-compose exec orders-service pytest
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

## Event-Driven Architecture

The service uses RabbitMQ for event-driven communication with other services:
- Publisher for publishing order events
- Subscriber for listening to events from other services 