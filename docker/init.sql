-- Инициализационный скрипт для PostgreSQL

-- Создание расширения для работы с массивами (если необходимо)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Создание таблиц (если автоматическое создание не используется)

-- Создание индексов для улучшения производительности
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_measurements_child_id ON measurements(child_id);
CREATE INDEX IF NOT EXISTS idx_measurements_timestamp ON measurements(timestamp);
CREATE INDEX IF NOT EXISTS idx_reminders_child_id ON reminders(child_id);
CREATE INDEX IF NOT EXISTS idx_notifications_reminder_id ON notifications(reminder_id);

-- Пример добавления базового пользователя (для разработки)
-- INSERT INTO users (username, email, password_hash, role, is_active, created_at, updated_at)
-- VALUES ('admin', 'admin@peakflow.local', '$2b$12$LQv3c1yZJj8p5zL5F5YwVeH4TRBiTvMNh.jNXx1rzpVK5aERKvGRm', 'parent', true, NOW(), NOW())
-- ON CONFLICT (username) DO NOTHING;

-- Пример добавления профиля ребенка (для разработки)
-- INSERT INTO child_profiles (user_id, parent_id, first_name, last_name, birth_date, height, gender, created_at, updated_at)
-- VALUES (1, 1, 'Тестовый', 'Ребенок', '2015-01-01', 130, 'male', NOW(), NOW())
-- ON CONFLICT (user_id) DO NOTHING;

-- Настройка прав доступа
GRANT ALL PRIVILEGES ON DATABASE peakflow_db TO peakflow_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO peakflow_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO peakflow_user;