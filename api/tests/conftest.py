import uuid

import pytest
from rest_framework.test import APIClient

from api.models import Answer, Question


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


@pytest.fixture
def test_question():
    """Фикстура для тестового вопроса"""
    return Question.objects.create(text="Тестовый вопрос для тестов")


@pytest.fixture
def test_answer(test_question):
    """Фикстура для тестового ответа"""
    return Answer.objects.create(
        question=test_question, user_id=uuid.uuid4(), text="Тестовый ответ на вопрос"
    )
