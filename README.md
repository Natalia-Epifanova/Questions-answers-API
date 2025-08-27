# API-сервис для вопросов и ответов

Django REST Framework сервис для управления вопросами и ответами.

## Функциональность

- Создание и управление вопросами
- Добавление ответов к вопросам
- Каскадное удаление вопросов с ответами
- Валидация данных
- Документация API через Swagger

## Технологии

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Pydantic для валидации

## Запуск проекта
1. Вариант 1: Docker (рекомендуется)

```git clone https://github.com/Natalia-Epifanova/Questions-answers-API```

```cd questions_answers_api```

Запуск с Docker

```docker-compose up --build```

- Приложение будет доступно по http://localhost:8000
- API документация: http://localhost:8000/swagger/

2. Вариант 2: Локальная установка

- Создание виртуального окружения

```python -m venv venv```

```source venv/bin/activate```  # Linux/Mac

```venv\Scripts\activate```     # Windows

- Установка зависимостей

```pip install -r requirements.txt```

- Настройка базы данных

```python manage.py migrate```

- Запуск сервера

```python manage.py runserver```

- Приложение будет доступно по http://127.0.0.1:8000


## API Endpoints
```GET /api/questions/``` - список вопросов

```POST /api/questions/``` - создать вопрос

```GET /api/questions/{id}/``` - получить вопрос с ответами

```DELETE /api/questions/{id}/``` - удалить вопрос

```POST /api/questions/{id}/answers/``` - добавить ответ

```GET /api/answers/{id}/``` - получить ответ

```DELETE /api/answers/{id}/``` - удалить ответ

## Документация
Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

## Тестирование (локально)

- Запуск всех тестов

```pytest```

- Запуск с покрытием кода

```pytest --cov=tasks --cov-report=html```

Разработано: Епифанова Наталия © 2025