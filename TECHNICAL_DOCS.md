# 📚 Техническая документация Cargo Track

## 🏗️ Архитектурная диаграмма

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Auth Service  │    │  Fleet Service  │    │ Warehouse Svc   │    │  Orders Service │
│   (Port 8000)   │    │   (Port 8001)   │    │   (Port 8002)   │    │   (Port 8003)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Auth DB       │    │   Fleet DB      │    │  Warehouse DB   │    │   Orders DB     │
│   (PostgreSQL)  │    │   (PostgreSQL)  │    │   (PostgreSQL)  │    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘

                                    │
                                    ▼
                        ┌─────────────────┐
                        │    RabbitMQ     │
                        │  (Message Bus)  │
                        └─────────────────┘
```

## 🔄 Event Flow Diagram

```
Orders Service          RabbitMQ           Fleet Service
     │                      │                    │
     │ 1. Create Order      │                    │
     │─────────────────────▶│                    │
     │                      │                    │
     │ 2. Publish           │                    │
     │   OrderCreated       │                    │
     │─────────────────────▶│                    │
     │                      │                    │
     │                      │ 3. Subscribe       │
     │                      │◀───────────────────│
     │                      │                    │
     │                      │ 4. Process Order   │
     │                      │   & Find Resources │
     │                      │                    │
     │                      │ 5. Publish         │
     │                      │   VehicleAssigned  │
     │                      │◀───────────────────│
     │                      │                    │
     │ 6. Subscribe         │                    │
     │◀─────────────────────│                    │
     │                      │                    │
     │ 7. Update Order      │                    │
     │   Status             │                    │
     │                      │                    │
```

## 📊 Структура базы данных

### Auth Service Database

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'dispatcher', 'driver', 'client')),
    is_active BOOLEAN DEFAULT TRUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tokens table
CREATE TABLE tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fleet Service Database

```sql
-- Drivers table
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_class VARCHAR(10) NOT NULL,
    license_expiry TIMESTAMP NOT NULL,
    medical_certificate_expiry TIMESTAMP NOT NULL,
    experience_years INTEGER NOT NULL,
    emergency_contact_name VARCHAR(200) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vehicles table
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL CHECK (vehicle_type IN ('truck', 'van', 'trailer')),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    capacity_weight DECIMAL(10,2) NOT NULL,
    capacity_volume DECIMAL(10,2) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    fuel_efficiency DECIMAL(5,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    insurance_expiry TIMESTAMP NOT NULL,
    registration_expiry TIMESTAMP NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Route Assignments table
CREATE TABLE route_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID REFERENCES drivers(id),
    vehicle_id UUID REFERENCES vehicles(id),
    order_id UUID NOT NULL,
    pickup_address TEXT NOT NULL,
    delivery_address TEXT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'assigned',
    notes TEXT
);
```

### Warehouse Service Database

```sql
-- Warehouses table
CREATE TABLE warehouses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    warehouse_type VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    total_capacity_weight DECIMAL(12,2) NOT NULL,
    total_capacity_volume DECIMAL(10,2) NOT NULL,
    available_capacity_weight DECIMAL(12,2) NOT NULL,
    available_capacity_volume DECIMAL(10,2) NOT NULL,
    temperature_controlled BOOLEAN DEFAULT FALSE,
    hazardous_materials_allowed BOOLEAN DEFAULT FALSE,
    operating_hours VARCHAR(100) DEFAULT '24/7',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cargo table
CREATE TABLE cargo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tracking_number VARCHAR(100) UNIQUE NOT NULL,
    cargo_type VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    weight DECIMAL(10,2) NOT NULL,
    volume DECIMAL(8,2) NOT NULL,
    dimensions JSONB,
    value DECIMAL(12,2) NOT NULL,
    insurance_amount DECIMAL(12,2) NOT NULL,
    temperature_requirements JSONB,
    humidity_requirements JSONB,
    hazardous_material BOOLEAN DEFAULT FALSE,
    hazardous_class VARCHAR(50),
    special_handling TEXT[],
    fragility_level VARCHAR(50) DEFAULT 'low',
    storage_duration INTEGER NOT NULL,
    expiration_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'received',
    warehouse_id UUID REFERENCES warehouses(id),
    location_in_warehouse VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Service Database

```sql
-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name VARCHAR(200) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    pickup_address TEXT NOT NULL,
    delivery_address TEXT NOT NULL,
    cargo_type VARCHAR(50) NOT NULL,
    cargo_weight DECIMAL(10,2) NOT NULL,
    cargo_volume DECIMAL(8,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    vehicle_id UUID,
    driver_id UUID,
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    pickup_date TIMESTAMP,
    delivery_date TIMESTAMP,
    delivery_deadline TIMESTAMP NOT NULL,
    special_requirements TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API Endpoints

### Auth Service API

#### Аутентификация
```http
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
```

#### Управление пользователями
```http
GET /users/
GET /users/{user_id}
PUT /users/{user_id}
DELETE /users/{user_id}
```

### Fleet Service API

#### Управление водителями
```http
GET /drivers/
POST /drivers/
GET /drivers/{driver_id}
PUT /drivers/{driver_id}
DELETE /drivers/{driver_id}
```

#### Управление транспортом
```http
GET /vehicles/
POST /vehicles/
GET /vehicles/{vehicle_id}
PUT /vehicles/{vehicle_id}
DELETE /vehicles/{vehicle_id}
```

#### Назначения маршрутов
```http
GET /route-assignments/
POST /route-assignments/
GET /route-assignments/{assignment_id}
PUT /route-assignments/{assignment_id}
```

### Warehouse Service API

#### Управление складами
```http
GET /warehouses/
POST /warehouses/
GET /warehouses/{warehouse_id}
PUT /warehouses/{warehouse_id}
DELETE /warehouses/{warehouse_id}
```

#### Управление грузами
```http
GET /cargo/
POST /cargo/
GET /cargo/{cargo_id}
PUT /cargo/{cargo_id}
DELETE /cargo/{cargo_id}
```

#### Проверка совместимости
```http
POST /compatibility/check
```

### Orders Service API

#### Управление заказами
```http
GET /orders/
POST /orders/
GET /orders/{order_id}
PUT /orders/{order_id}
DELETE /orders/{order_id}
```

#### Изменение статуса
```http
PUT /orders/{order_id}/status
```

## 📨 Event Models

### OrderCreated Event
```python
class OrderCreatedEvent(BaseModel):
    event_type: str = "order_created"
    order_id: str
    customer_name: str
    pickup_address: str
    delivery_address: str
    cargo_type: str
    cargo_weight: float
    cargo_volume: float
    delivery_deadline: datetime
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### VehicleAssigned Event
```python
class VehicleAssignedEvent(BaseModel):
    event_type: str = "vehicle_assigned"
    order_id: str
    vehicle_id: str
    driver_id: str
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### NoVehicleAvailable Event
```python
class NoVehicleAvailableEvent(BaseModel):
    event_type: str = "no_vehicle_available"
    order_id: str
    reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## 🔐 Аутентификация и авторизация

### JWT Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "admin",
  "exp": 1753557532
}
```

### Роли и права доступа

#### Admin
- Полный доступ ко всем сервисам
- Управление пользователями
- Просмотр всех данных

#### Dispatcher
- Создание и управление заказами
- Просмотр автопарка и складов
- Назначение маршрутов

#### Driver
- Просмотр назначенных маршрутов
- Обновление статуса доставки
- Ограниченный доступ к данным

#### Client
- Создание заказов
- Просмотр статуса своих заказов
- Ограниченный доступ

## 🧪 Тестирование

### Структура тестов
```
src/
├── conftest.py                    # Pytest конфигурация
├── test_main.py                   # Основные тесты
├── controllers/
│   └── test_*.py                  # Тесты контроллеров
├── use_cases/
│   └── test_*.py                  # Тесты бизнес-логики
├── repositories/
│   └── test_*.py                  # Тесты репозиториев
└── integration/
    └── test_*.py                  # Интеграционные тесты
```

### Типы тестов

#### Unit Tests
- Тестирование отдельных функций и методов
- Мокирование внешних зависимостей
- Быстрое выполнение

#### Integration Tests
- Тестирование взаимодействия компонентов
- Использование тестовой базы данных
- Проверка API endpoints

#### Event-Driven Tests
- Тестирование событий RabbitMQ
- Проверка асинхронного взаимодействия
- End-to-end сценарии

### Примеры тестов

#### Unit Test Example
```python
def test_create_order_use_case(f_order_repository, f_publisher):
    use_case = CreateOrderUseCase(f_order_repository, f_publisher)
    
    order_data = CreateOrderRequest(
        customer_name="Test Customer",
        customer_email="test@example.com",
        # ... other fields
    )
    
    result = use_case.execute(order_data)
    
    assert result.id is not None
    assert result.status == "pending"
```

#### Integration Test Example
```python
def test_create_order_endpoint(client, auth_headers):
    order_data = {
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        # ... other fields
    }
    
    response = client.post("/orders", json=order_data, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
```

## 📊 Мониторинг и логирование

### Структура логов
```json
{
  "event": "Order created",
  "logger": "CreateOrderUseCase",
  "level": "info",
  "timestamp": "2025-07-26T18:55:49.700022Z",
  "order_id": "2cea53ca-cf64-4610-8bc3-e761af9faa8f",
  "customer_name": "ООО Рога и Копыта"
}
```

### Уровни логирования
- **DEBUG** - детальная отладочная информация
- **INFO** - общая информация о работе системы
- **WARNING** - предупреждения
- **ERROR** - ошибки, требующие внимания
- **CRITICAL** - критические ошибки

### Метрики RabbitMQ
- Количество сообщений в секунду
- Размер очередей
- Время обработки сообщений
- Количество ошибок

## 🚀 Производительность

### Оптимизации
- Connection pooling для баз данных
- Кэширование часто используемых данных
- Асинхронная обработка событий
- Оптимизированные SQL запросы

### Масштабирование
- Горизонтальное масштабирование сервисов
- Репликация баз данных
- Кластеризация RabbitMQ
- Load balancing

## 🔧 Конфигурация

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/db_name

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_EXCHANGE=cargo_track_events

# JWT
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Logging
LOG_LEVEL=INFO
```

### Docker Configuration
```yaml
version: '3.8'
services:
  auth-service:
    build: ./auth
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@auth-db:5432/auth_db
    depends_on:
      - auth-db
    networks:
      - cargo-track-network
```

## 📈 Планы развития

### Краткосрочные планы
- Добавление уведомлений (email, SMS)
- Расширенная аналитика и отчеты
- Мобильное приложение для водителей

### Долгосрочные планы
- Интеграция с GPS трекерами
- Машинное обучение для оптимизации маршрутов
- Blockchain для прозрачности цепочек поставок
- IoT интеграция для мониторинга грузов 