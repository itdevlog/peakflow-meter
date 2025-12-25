# Диаграммы последовательности для системы "Пикфлоуметр"

## 1. Сценарий: Регистрация родителя и добавление ребенка

```mermaid
sequenceDiagram
    participant Parent as Родитель
    participant FE as Веб-интерфейс
    participant BE as Backend
    participant DB as База данных
    participant Email as Email сервис

    Parent->>FE: Открывает страницу регистрации
    FE->>Parent: Показывает форму регистрации
    Parent->>FE: Вводит данные и отправляет форму
    FE->>BE: POST /api/auth/register
    BE->>DB: Создать пользователя (роль: родитель)
    DB-->>BE: Подтверждение создания
    BE-->>Email: Отправить письмо подтверждения
    BE-->>FE: Подтверждение регистрации
    FE-->>Parent: Перенаправление на личный кабинет
    Parent->>FE: Добавить ребенка
    FE->>BE: POST /api/user/child-profile
    BE->>DB: Создать профиль ребенка
    DB-->>BE: Подтверждение создания
    BE-->>FE: Подтверждение создания ребенка
    FE-->>Parent: Отображение профиля ребенка
```

## 2. Сценарий: Добавление замера ребенком

```mermaid
sequenceDiagram
    participant Child as Ребенок
    participant FE as Веб-интерфейс
    participant BE as Backend
    participant DB as База данных
    participant ZoneCalc as Калькулятор зон

    Child->>FE: Открывает интерфейс добавления замера
    FE->>BE: GET /api/user/child-profile
    BE->>DB: Получить профиль ребенка
    DB-->>BE: Возвращение профиля
    BE-->>FE: Возвращение профиля
    FE->>Child: Отображение формы с информацией ребенка
    Child->>FE: Вводит значение замера и отправляет
    FE->>BE: POST /api/measurements
    BE->>ZoneCalc: Рассчитать зону по значению и профилю
    ZoneCalc-->>BE: Возвращение зоны (зеленая/желтая/красная)
    BE->>DB: Сохранить замер с зоной
    DB-->>BE: Подтверждение сохранения
    BE-->>FE: Подтверждение добавления
    FE-->>Child: Отображение результата и цветовой индикации
```

## 3. Сценарий: Просмотр статистики родителем

```mermaid
sequenceDiagram
    participant Parent as Родитель
    participant FE as Веб-интерфейс
    participant BE as Backend
    participant DB as База данных

    Parent->>FE: Входит в личный кабинет родителя
    FE->>BE: GET /api/user/profile
    BE->>DB: Получить профиль родителя
    DB-->>BE: Возвращение профиля
    BE-->>FE: Возвращение профиля
    FE->>BE: GET /api/user/child-profile
    BE->>DB: Получить профили детей родителя
    DB-->>BE: Возвращение профилей детей
    BE-->>FE: Возвращение профилей детей
    FE->>BE: GET /api/measurements (с фильтрами)
    BE->>DB: Получить замеры ребенка
    DB-->>BE: Возвращение истории замеров
    BE-->>FE: Возвращение данных для графиков
    FE->>Parent: Отображение графиков и статистики
    Parent->>FE: Фильтрация данных
    FE->>BE: GET /api/measurements (с новыми фильтрами)
    BE->>DB: Получить отфильтрованные замеры
    DB-->>BE: Возвращение отфильтрованных данных
    BE-->>FE: Возвращение отфильтрованных данных
    FE-->>Parent: Обновление графиков
```

## 4. Сценарий: Настройка напоминаний

```mermaid
sequenceDiagram
    participant Parent as Родитель
    participant FE as Веб-интерфейс
    participant BE as Backend
    participant DB as База данных
    participant TaskQueue as Очередь задач

    Parent->>FE: Открывает настройки напоминаний
    FE->>BE: GET /api/reminders
    BE->>DB: Получить текущие настройки напоминаний
    DB-->>BE: Возвращение настроек
    BE-->>FE: Возвращение настроек
    FE->>Parent: Отображение текущих настроек
    Parent->>FE: Изменяет настройки и сохраняет
    FE->>BE: PUT /api/reminders
    BE->>DB: Обновить настройки напоминаний
    DB-->>BE: Подтверждение обновления
    BE->>TaskQueue: Обновить задачи напоминаний
    TaskQueue-->>BE: Подтверждение обновления задач
    BE-->>FE: Подтверждение сохранения
    FE-->>Parent: Сообщение об успешном сохранении
```

## 5. Сценарий: Получение уведомлений через Telegram-бота

```mermaid
sequenceDiagram
    participant Telegram as Telegram
    participant Bot as Telegram-бот
    participant BE as Backend
    participant DB as База данных
    participant TaskQueue as Очередь задач

    Note over Telegram,TaskQueue: Периодическая задача (Celery)
    TaskQueue->>BE: Запуск задачи отправки напоминаний
    BE->>DB: Получить активные напоминания
    DB-->>BE: Возвращение списка напоминаний
    loop Для каждого напоминания
        BE->>DB: Получить информацию о ребенке и родителе
        DB-->>BE: Возвращение информации
        BE->>Bot: Отправить сообщение через Telegram API
        Bot->>Telegram: Отправить сообщение пользователю
    end
    Telegram->>Bot: Пользователь отвечает боту
    Bot->>BE: POST /api/telegram/webhook
    BE->>DB: Обработать команду пользователя
    DB-->>BE: Подтверждение обработки
    BE-->>Bot: Ответ на команду
    Bot-->>Telegram: Отправить ответ пользователю