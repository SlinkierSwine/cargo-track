# Warehouse Service

Сервис управления складами и грузом для системы Cargo Track.

## Функциональность

- Управление складами
- Учет грузов и их характеристик
- Проверка соответствия груза возможностям транспорта

## Запуск

### С помощью Docker Compose

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8002

### Переменные окружения

Скопируйте `env.example` в `.env` и настройте переменные:

```bash
cp env.example .env
```

## API Endpoints

- `GET /` - Информация о сервисе
- `GET /health` - Проверка здоровья сервиса
- `GET /docs` - Swagger документация

## Архитектура

Сервис построен по принципам Clean Architecture:

- **Controllers** - HTTP endpoints
- **Use Cases** - Бизнес-логика
- **Repositories** - Работа с данными
- **Entities** - Модели данных

## Тестирование

```bash
pytest
``` 