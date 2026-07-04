# Habit Tracker (Трекер привычек)

Бэкенд-часть SPA-приложения для отслеживания полезных привычек на Django REST Framework, Celery, PostgreSQL, Redis. Уведомления через Telegram-бота.

## Локальный запуск
1. Клонировать репозиторий.
2. `python -m venv venv && venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Создать `.env` на основе `.env.template`.
5. `python manage.py migrate && python manage.py runserver`
6. Для Celery: запустить Redis, `celery -A config worker -l info -P eventlet`, `celery -A config beat -l info`

## Запуск через Docker:
```bash
docker compose up -d --build
Сервисы: web (Django), db (PostgreSQL), redis, celery_worker, celery_beat, nginx (порт 80).

CI/CD и деплой
Push в develop/main → тесты, линтинг, сборка образов.

Успешные проверки → авто-деплой на сервер (требуются GitHub Secrets: SERVER_HOST, SERVER_USER, SSH_PRIVATE_KEY).

Ветки: main, develop. PR в develop.

Тесты и покрытие
bash
pytest --cov=. --cov-report=term-missing
Минимум 80% покрытия.

Структура
config/ – настройки Django, Celery

habits/, users/ – приложения

nginx/ – конфиг Nginx

Dockerfile, docker-compose.yml, entrypoint.sh

.github/workflows/deploy.yml
