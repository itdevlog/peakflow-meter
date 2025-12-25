# Диаграмма развертывания системы "Пикфлоуметр"

```mermaid
graph TB
    subgraph "Клиентские устройства"
        A[Мобильное устройство<br/>ребенка]
        B[ПК/планшет<br/>родителя]
        C[Telegram клиент]
    end

    subgraph "Облако/Сервер"
        subgraph "Веб-сервер"
            D[FastAPI Backend]
            E[React Frontend]
        end

        subgraph "База данных"
            F[PostgreSQL]
        end

        subgraph "Кеширование"
            G[Redis]
        end

        subgraph "Очередь задач"
            H[Celery Workers]
            I[Redis Message Broker]
        end
    end

    subgraph "Внешние сервисы"
        J[Telegram API]
        K[Let's Encrypt<br/>SSL]
    end

    A --> E
    B --> E
    C --> J
    E --> D
    D --> F
    D --> G
    D --> H
    H --> I
    I --> J
    D --> K

    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#e8f5e8
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#fce4ec
    style K fill:#fff9c4
```

## Описание компонентов

### Клиентские устройства
- **Мобильное устройство ребенка**: Основное устройство для ежедневного ввода замеров, поддерживает PWA или мобильный браузер
- **ПК/планшет родителя**: Для просмотра статистики, настройки профиля и управления системой
- **Telegram клиент**: Для получения уведомлений и быстрого ввода данных через бота

### Веб-сервер
- **FastAPI Backend**: Основной сервер приложения, обрабатывающий бизнес-логику, API запросы и аутентификацию
- **React Frontend**: Веб-интерфейс с адаптивным дизайном для различных устройств

### База данных
- **PostgreSQL**: Основная реляционная база данных для хранения всех данных приложения

### Кеширование
- **Redis**: Для кеширования часто запрашиваемых данных и сессий пользователей

### Очередь задач
- **Celery Workers**: Обработка фоновых задач, таких как отправка уведомлений и напоминаний
- **Redis Message Broker**: Очередь для асинхронной обработки задач

### Внешние сервисы
- **Telegram API**: Для интеграции с Telegram-ботом
- **Let's Encrypt SSL**: Для обеспечения безопасного соединения