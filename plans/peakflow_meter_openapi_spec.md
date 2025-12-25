# Спецификация API системы "Пикфлоуметр" (OpenAPI 3.0)

## Обзор

Спецификация API для системы "Пикфлоуметр", разработанная в соответствии с OpenAPI 3.0. API предоставляет интерфейс для взаимодействия с системой как для веб-интерфейса, так и для Telegram-бота.

## Base URL

```
https://api.peakflow-meter.com/api/v1
```

## Аутентификация

API использует JWT-аутентификацию. Для доступа к защищенным эндпоинтам необходимо включить заголовок:

```
Authorization: Bearer {jwt_token}
```

## Компоненты

### Схемы (Schemas)

#### User
```yaml
type: object
properties:
  id:
    type: integer
    example: 1
  username:
    type: string
    example: "parent123"
  email:
    type: string
    format: email
    example: "parent@example.com"
  role:
    type: string
    enum: ["parent", "child"]
    example: "parent"
  is_active:
    type: boolean
    example: true
 created_at:
    type: string
    format: date-time
    example: "2023-01-01T10:00Z"
```

#### ChildProfile
```yaml
type: object
properties:
  id:
    type: integer
    example: 1
  user_id:
    type: integer
    example: 2
  parent_id:
    type: integer
    example: 1
  first_name:
    type: string
    example: "Иван"
  last_name:
    type: string
    example: "Иванов"
  birth_date:
    type: string
    format: date
    example: "2015-05-15"
  height:
    type: integer
    example: 140
  gender:
    type: string
    enum: ["male", "female"]
    example: "male"
 best_result:
    type: integer
    example: 480
  calculated_zones:
    type: object
    properties:
      green_min:
        type: integer
        example: 384
      yellow_min:
        type: integer
        example: 28
      red_min:
        type: integer
        example: 287
```

#### Measurement
```yaml
type: object
properties:
  id:
    type: integer
    example: 1
  child_id:
    type: integer
    example: 1
  value:
    type: integer
    example: 450
  timestamp:
    type: string
    format: date-time
    example: "2023-01-01T08:00:00Z"
  zone:
    type: string
    enum: ["green", "yellow", "red"]
    example: "green"
  notes:
    type: string
    example: "Ребенок чувствует себя хорошо"
  created_at:
    type: string
    format: date-time
    example: "2023-01-01T08:05:00Z"
```

#### Reminder
```yaml
type: object
properties:
  id:
    type: integer
    example: 1
  child_id:
    type: integer
    example: 1
  time_of_day:
    type: string
    format: time
    example: "08:00:00"
  days_of_week:
    type: array
    items:
      type: integer
      minimum: 1
      maximum: 7
    example: [1, 2, 3, 4, 5]
  is_active:
    type: boolean
    example: true
 notification_type:
    type: string
    enum: ["telegram", "email", "both"]
    example: "telegram"
```

#### ErrorResponse
```yaml
type: object
properties:
  detail:
    type: string
    example: "Пользователь не найден"
```

## Эндпоинты

### Аутентификация

#### `POST /auth/login`
Аутентификация пользователя

##### Request
```json
{
  "username": "string",
  "password": "string"
}
```

##### Responses
- `200`: Успешная аутентификация
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```
- `401`: Неверные учетные данные

#### `POST /auth/register`
Регистрация родителя

##### Request
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

##### Responses
- `200`: Успешная регистрация
- `400`: Неверные данные
- `409`: Пользователь с таким email уже существует

#### `POST /auth/child-register`
Регистрация ребенка (только родителем)

##### Request
```json
{
  "first_name": "string",
  "last_name": "string",
  "birth_date": "2020-01-01",
  "height": 120,
  "gender": "male"
}
```

##### Responses
- `200`: Успешная регистрация ребенка
- `401`: Неавторизованный доступ
- `403`: Только для родителей

### Управление пользователями

#### `GET /user/profile`
Получение профиля текущего пользователя

##### Responses
- `200`: 
```json
{
  "id": 1,
  "username": "parent123",
  "email": "parent@example.com",
  "role": "parent",
  "is_active": true,
  "created_at": "2023-01-01T10:00:00Z"
}
```

#### `PUT /user/profile`
Обновление профиля пользователя

##### Request
```json
{
  "username": "newusername",
  "email": "newemail@example.com"
}
```

##### Responses
- `200`: Профиль успешно обновлен
- `400`: Неверные данные

#### `GET /user/child-profile`
Получение профиля ребенка (доступно родителю или самому ребенку)

##### Query Parameters
- `child_id`: ID ребенка

##### Responses
- `200`: 
```json
{
  "id": 1,
  "user_id": 2,
  "parent_id": 1,
  "first_name": "Иван",
  "last_name": "Иванов",
  "birth_date": "2015-05-15",
  "height": 140,
  "gender": "male",
  "best_result": 480,
  "calculated_zones": {
    "green_min": 384,
    "yellow_min": 28,
    "red_min": 287
  }
}
```

#### `PUT /user/child-profile`
Обновление профиля ребенка (только родителем)

##### Query Parameters
- `child_id`: ID ребенка

##### Request
```json
{
  "first_name": "Петр",
  "last_name": "Петров",
  "height": 145,
  "best_result": 500
}
```

##### Responses
- `200`: Профиль успешно обновлен
- `401`: Неавторизованный доступ
- `403`: Нет прав на изменение

### Замеры

#### `POST /measurements`
Добавление нового замера

##### Request
```json
{
  "child_id": 1,
  "value": 450,
  "notes": "Ребенок чувствует себя хорошо"
}
```

##### Responses
- `200`: 
```json
{
  "id": 1,
  "child_id": 1,
  "value": 450,
  "timestamp": "2023-01-01T08:00:00Z",
  "zone": "green",
  "notes": "Ребенок чувствует себя хорошо",
  "created_at": "2023-01-01T08:05:00Z"
}
```
- `400`: Неверные данные
- `403`: Нет прав на добавление замера для этого ребенка

#### `GET /measurements`
Получение истории замеров

##### Query Parameters
- `child_id`: ID ребенка (обязательный)
- `from_date`: Начальная дата (опционально)
- `to_date`: Конечная дата (опционально)
- `limit`: Количество записей (опционально, по умолчанию 50)
- `offset`: Смещение (опционально, по умолчанию 0)

##### Responses
- `200`: 
```json
{
  "measurements": [
    {
      "id": 1,
      "child_id": 1,
      "value": 450,
      "timestamp": "2023-01-01T08:00:00Z",
      "zone": "green",
      "notes": "Ребенок чувствует себя хорошо",
      "created_at": "2023-01-01T08:05:00Z"
    }
  ],
  "total": 1,
  "offset": 0,
  "limit": 50
}
```

#### `GET /measurements/latest`
Получение последнего замера для ребенка

##### Query Parameters
- `child_id`: ID ребенка (обязательный)

##### Responses
- `200`: 
```json
{
  "id": 1,
  "child_id": 1,
  "value": 450,
  "timestamp": "2023-01-01T08:00:00Z",
  "zone": "green",
  "notes": "Ребенок чувствует себя хорошо",
  "created_at": "2023-01-01T08:05:00Z"
}
```

#### `DELETE /measurements/{id}`
Удаление замера (только родителем)

##### Path Parameters
- `id`: ID замера

##### Responses
- `204`: Замер успешно удален
- `403`: Нет прав на удаление
- `404`: Замер не найден

### Расчет зон

#### `GET /zones/current`
Получение текущих границ зон для ребенка

##### Query Parameters
- `child_id`: ID ребенка (обязательный)

##### Responses
- `200`: 
```json
{
  "child_id": 1,
  "calculated_at": "2023-01-01T10:00:00Z",
  "green_min": 384,
  "yellow_min": 288,
  "red_min": 287,
  "calculation_method": "age_and_height"
}
```

#### `GET /zones/status`
Получение текущего статуса по последнему замеру

##### Query Parameters
- `child_id`: ID ребенка (обязательный)

##### Responses
- `200`: 
```json
{
  "child_id": 1,
  "last_measurement_value": 450,
  "last_measurement_time": "2023-01-01T08:00:00Z",
  "current_zone": "green",
  "percentage_of_normal": 92.0
}
```

### Графики и статистика

#### `GET /statistics/overview`
Общая статистика для родительского интерфейса

##### Query Parameters
- `child_id`: ID ребенка (обязательный)

##### Responses
- `200`: 
```json
{
  "child_id": 1,
  "period_from": "2023-01-01",
  "period_to": "2023-01-31",
  "total_measurements": 30,
  "green_zone_percentage": 80.0,
  "yellow_zone_percentage": 15.0,
  "red_zone_percentage": 5.0,
  "average_value": 430,
  "best_value": 480,
  "trend": "improving"
}
```

#### `GET /statistics/chart-data`
Данные для построения графиков

##### Query Parameters
- `child_id`: ID ребенка (обязательный)
- `from_date`: Начальная дата
- `to_date`: Конечная дата
- `chart_type`: Тип графика (daily, weekly, monthly)

##### Responses
- `200`: 
```json
{
  "child_id": 1,
  "chart_type": "daily",
  "data": [
    {
      "date": "2023-01-01",
      "value": 450,
      "zone": "green",
      "normal_percentage": 92.0
    }
  ]
}
```

### Уведомления и напоминания

#### `GET /reminders`
Получение настроек напоминаний

##### Query Parameters
- `child_id`: ID ребенка (обязательный)

##### Responses
- `200`: 
```json
{
  "reminders": [
    {
      "id": 1,
      "child_id": 1,
      "time_of_day": "08:00:00",
      "days_of_week": [1, 2, 3, 4, 5],
      "is_active": true,
      "notification_type": "telegram"
    }
  ]
}
```

#### `PUT /reminders`
Обновление настроек напоминаний

##### Request
```json
{
  "child_id": 1,
  "time_of_day": "08:00:00",
  "days_of_week": [1, 2, 3, 4, 5],
  "is_active": true,
  "notification_type": "telegram"
}
```

##### Responses
- `200`: Настройки успешно обновлены
- `400`: Неверные данные
- `403`: Нет прав на изменение

#### `POST /reminders/test`
Тестирование отправки напоминания

##### Request
```json
{
  "child_id": 1,
  "message": "Тестовое напоминание"
}
```

##### Responses
- `200`: Напоминание успешно отправлено
- `400`: Ошибка при отправке

### Telegram-бот

#### `POST /telegram/webhook`
Вебхук для получения сообщений от Telegram

##### Request
```json
{
  "update_id": 123456,
  "message": {
    "message_id": 1,
    "from": {
      "id": 123456789,
      "first_name": "Иван",
      "username": "ivan123"
    },
    "chat": {
      "id": 123456789,
      "type": "private"
    },
    "date": 1672531200,
    "text": "/start"
  }
}
```

##### Responses
- `200`: Обработка успешна

#### `POST /telegram/send-message`
Отправка сообщений в Telegram (для уведомлений)

##### Request
```json
{
  "telegram_id": 123456789,
  "message": "Напоминание: не забудьте сделать замер!"
}
```

##### Responses
- `200`: 
```json
{
  "success": true,
  "message_id": 1
}
```
- `400`: Ошибка при отправке

## Примеры использования

### Пример 1: Добавление замера через веб-интерфейс
```
POST /api/v1/measurements
Authorization: Bearer {token}
Content-Type: application/json

{
  "child_id": 1,
  "value": 450,
  "notes": "Утром после пробуждения"
}
```

### Пример 2: Получение истории замеров
```
GET /api/v1/measurements?child_id=1&from_date=2023-01-01&to_date=2023-01-31
Authorization: Bearer {token}
```

### Пример 3: Получение текущего статуса ребенка
```
GET /api/v1/zones/status?child_id=1
Authorization: Bearer {token}
```

## Безопасность

Все эндпоинты, кроме аутентификации, требуют JWT-токен в заголовке Authorization. Система реализует ролевую модель доступа, где родители имеют доступ к информации своих детей, а дети - только к своей информации.

## Ошибки

Система возвращает стандартные HTTP-коды ошибок:
- `400 Bad Request` - неверные параметры запроса
- `401 Unauthorized` - отсутствует или невалидный токен
- `403 Forbidden` - недостаточно прав для выполнения операции
- `404 Not Found` - запрашиваемый ресурс не найден
- `422 Unprocessable Entity` - ошибка валидации данных
- `500 Internal Server Error` - внутренняя ошибка сервера