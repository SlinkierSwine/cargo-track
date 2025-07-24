# Orders Service - Business Logic Planning

## 1. Определение требований к созданию и управлению заказами

### Основные сущности:
- **Order** - заказ на перевозку груза
- **OrderStatus** - статус заказа
- **OrderAssignment** - назначение транспорта и водителя

### Поля заказа:
- customer_name, customer_email, customer_phone
- pickup_address, delivery_address
- cargo_type, cargo_weight, cargo_volume
- status (pending, assigned, in_transit, delivered, cancelled)
- vehicle_id, driver_id (nullable)
- estimated_cost, actual_cost
- pickup_date, delivery_date
- notes

### Use Cases для управления заказами:
1. **CreateOrderUseCase** - создание нового заказа
2. **GetOrderUseCase** - получение заказа по ID
3. **ListOrdersUseCase** - получение списка заказов с фильтрацией
4. **UpdateOrderUseCase** - обновление заказа
5. **DeleteOrderUseCase** - удаление заказа

## 2. Планирование логики назначения машины и водителя

### Требования к назначению:
- Проверка совместимости груза и транспорта (вес, объем)
- Проверка доступности водителя и транспорта
- Интеграция с fleet сервисом для получения доступных ресурсов
- Автоматическое назначение или ручное назначение

### Use Cases для назначения:
1. **AssignVehicleUseCase** - назначение транспорта
2. **AssignDriverUseCase** - назначение водителя
3. **AutoAssignUseCase** - автоматическое назначение транспорта и водителя
4. **CheckCompatibilityUseCase** - проверка совместимости груза и транспорта

### Интеграция с fleet сервисом:
- REST API вызовы для получения доступных транспорта и водителей
- Проверка статуса транспорта и водителей
- Резервирование ресурсов при назначении

## 3. Определение workflow отслеживания статуса заказа

### Статусы заказа:
1. **pending** - заказ создан, ожидает назначения
2. **assigned** - назначен транспорт и водитель
3. **in_transit** - в пути
4. **delivered** - доставлен
5. **cancelled** - отменен

### Workflow переходов:
- pending → assigned (при назначении транспорта/водителя)
- assigned → in_transit (при начале перевозки)
- in_transit → delivered (при завершении доставки)
- любой статус → cancelled (при отмене)

### Use Cases для изменения статуса:
1. **ChangeOrderStatusUseCase** - изменение статуса заказа
2. **StartTransportUseCase** - начало перевозки
3. **CompleteDeliveryUseCase** - завершение доставки
4. **CancelOrderUseCase** - отмена заказа

### Event-driven уведомления:
- Публикация событий при изменении статуса
- Интеграция с notification сервисом
- Уведомления клиента о статусе заказа

## 4. Интеграция с другими сервисами

### Fleet Service:
- Получение списка доступных транспорта
- Получение списка доступных водителей
- Проверка совместимости груза и транспорта
- Резервирование ресурсов

### Warehouse Service:
- Проверка наличия груза на складе
- Обновление статуса груза при назначении

### Auth Service:
- Аутентификация и авторизация пользователей
- Проверка ролей для доступа к операциям

### Notification Service:
- Отправка уведомлений о статусе заказа
- Уведомления о назначении водителя/транспорта

## 5. API Endpoints

### Orders Management:
- POST /orders - создание заказа
- GET /orders - список заказов
- GET /orders/{order_id} - получение заказа
- PUT /orders/{order_id} - обновление заказа
- DELETE /orders/{order_id} - удаление заказа

### Assignment:
- POST /orders/{order_id}/assign-vehicle - назначение транспорта
- POST /orders/{order_id}/assign-driver - назначение водителя
- POST /orders/{order_id}/auto-assign - автоматическое назначение

### Status Management:
- PUT /orders/{order_id}/status - изменение статуса
- POST /orders/{order_id}/start-transport - начало перевозки
- POST /orders/{order_id}/complete-delivery - завершение доставки
- POST /orders/{order_id}/cancel - отмена заказа

## 6. Event Types

### Публикуемые события:
- order.created - заказ создан
- order.vehicle_assigned - назначен транспорт
- order.driver_assigned - назначен водитель
- order.status_changed - изменен статус
- order.cancelled - заказ отменен

### Подписываемые события:
- vehicle.status_changed - изменение статуса транспорта
- driver.status_changed - изменение статуса водителя
- warehouse.cargo_available - груз доступен на складе 