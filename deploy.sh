#!/bin/bash

# Скрипт для развертывания системы Пикфлоуметр

set -e  # Выходить при ошибках

echo "=== Скрипт развертывания системы Пикфлоуметр ==="

# Проверяем, установлены ли необходимые инструменты
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Проверяем, существует ли файл .env
if [ ! -f .env ]; then
    echo "Файл .env не найден. Создаем шаблон..."
    cat > .env << EOF
# Конфигурационный файл для системы Пикфлоуметр
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f709f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://peakflow_user:peakflow_pass@db:5432/peakflow_db
REDIS_URL=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=
EOF
    echo "Создан файл .env. Пожалуйста, обновите его с актуальными значениями."
fi

# Проверяем, существует ли директория docker
if [ ! -d "docker" ]; then
    echo "Директория docker не найдена."
    exit 1
fi

# Переходим в директорию docker
cd docker

echo "=== Сборка и запуск контейнеров ==="
docker-compose up --build -d

echo "=== Ожидание запуска базы данных ==="
sleep 10

echo "=== Выполнение миграций базы данных (если применимо) ==="
# В реальной системе здесь будет команда для выполнения миграций Alembic
# docker-compose exec backend alembic upgrade head

echo "=== Проверка состояния контейнеров ==="
docker-compose ps

echo "=== Система успешно развернута ==="
echo "Фронтенд доступен по адресу: http://localhost"
echo "API доступно по адресу: http://localhost/api/"
echo "Документация API: http://localhost/docs"

echo ""
echo "Для остановки системы используйте:"
echo "  cd docker && docker-compose down"
echo ""
echo "Для просмотра логов используйте:"
echo "  cd docker && docker-compose logs -f"