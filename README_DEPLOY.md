# Развертывание системы "Пикфлоуметр"

Данный документ описывает процесс развертывания системы "Пикфлоуметр" с использованием Docker и Docker Compose.

## Требования

- Docker (v20.10 или выше)
- Docker Compose (v2.0 или выше)
- Git

## Подготовка к развертыванию

1. Склонируйте репозиторий:
   ```bash
   git clone <url-репозитория>
   cd peakflow-meter
   ```

2. Установите права на выполнение для скрипта развертывания:
   ```bash
   chmod +x deploy.sh
   ```

## Конфигурация

Создайте файл `.env` в корне проекта с необходимыми переменными:

```env
# Ключ для подписи JWT токенов (сгенерируйте случайный ключ)
SECRET_KEY=ваш_секретный_ключ

# Алгоритм шифрования
ALGORITHM=HS256

# Время жизни токена (в минутах)
ACCESS_TOKEN_EXPIRE_MINUTES=30

# URL базы данных
DATABASE_URL=postgresql://peakflow_user:peakflow_pass@db:5432/peakflow_db

# URL Redis
REDIS_URL=redis://redis:6379/0

# Токен Telegram бота (получите у @BotFather)
TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

## Развертывание

### Автоматическое развертывание

Запустите скрипт развертывания:

```bash
./deploy.sh
```

### Ручное развертывание

1. Перейдите в директорию docker:
   ```bash
   cd docker
   ```

2. Запустите сервисы:
   ```bash
   docker-compose up --build -d
   ```

3. Выполните миграции базы данных (если требуется):
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## Структура сервисов

Система состоит из следующих сервисов:

- `db`: PostgreSQL база данных
- `redis`: Redis для кеширования и брокера задач
- `backend`: Основное API приложение на FastAPI
- `frontend`: Веб-интерфейс на React
- `celery_worker`: Воркер для асинхронных задач
- `celery_beat`: Планировщик задач
- `nginx`: Обратный прокси сервер

## Проверка работоспособности

После развертывания проверьте статус сервисов:

```bash
docker-compose ps
```

Для просмотра логов:

```bash
docker-compose logs -f
```

## Доступ к системе

- Веб-интерфейс: `http://localhost`
- API: `http://localhost/api/`
- Документация API: `http://localhost/docs`

## Обновление системы

1. Остановите текущие контейнеры:
   ```bash
   docker-compose down
   ```

2. Обновите код:
   ```bash
   git pull origin main
   ```

3. Пересоберите и запустите контейнеры:
   ```bash
   docker-compose up --build -d
   ```

## Остановка системы

Для остановки всех сервисов:

```bash
cd docker
docker-compose down
```

## Мониторинг и логирование

Логи всех сервисов доступны через Docker Compose:

```bash
# Просмотр логов всех сервисов
docker-compose logs

# Просмотр логов конкретного сервиса
docker-compose logs backend

# Постоянный мониторинг логов
docker-compose logs -f
```

## Безопасность

- Все пароли и токены должны быть заданы в файле `.env`
- Используйте SSL сертификаты в продакшене
- Регулярно обновляйте образы контейнеров
- Настройте брандмауэр для ограничения доступа

## Резервное копирование

Для создания резервной копии базы данных:

```bash
docker exec peakflow_db pg_dump -U peakflow_user peakflow_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

Для восстановления из резервной копии:

```bash
docker exec -i peakflow_db psql -U peakflow_user peakflow_db < backup_file.sql
```

## Устранение неполадок

### Проблемы с доступом к API

- Убедитесь, что все сервисы запущены: `docker-compose ps`
- Проверьте логи: `docker-compose logs backend`
- Убедитесь, что порты не заняты другими приложениями

### Проблемы с Telegram-ботом

- Проверьте, что токен бота указан правильно
- Убедитесь, что вебхук настроен: `curl http://localhost/telegram/set-webhook`
- Проверьте логи бота: `docker-compose logs backend`

### Проблемы с производительностью

- Увеличьте объем памяти для контейнеров
- Добавьте кеширование в приложение
- Оптимизируйте запросы к базе данных