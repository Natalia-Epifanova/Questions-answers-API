import uuid

import pytest

from api.serializers import AnswerCreateSerializer, QuestionSerializer


@pytest.mark.django_db
class TestQuestionSerializer:
    """Тесты для QuestionSerializer"""

    def test_valid_question_data(self):
        """Тест валидных данных вопроса"""
        data = {"text": "Валидный текст вопроса"}
        serializer = QuestionSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["text"] == "Валидный текст вопроса"

    def test_empty_question_text(self):
        """Тест пустого текста вопроса"""
        data = {"text": ""}
        serializer = QuestionSerializer(data=data)
        assert serializer.is_valid() is False
        assert "text" in serializer.errors
        assert "This field may not be blank." in str(serializer.errors["text"][0])

    def test_whitespace_question_text(self):
        """Тест текста вопроса только из пробелов"""
        data = {"text": "   "}
        serializer = QuestionSerializer(data=data)
        assert serializer.is_valid() is False
        assert "text" in serializer.errors

    def test_text_stripping(self):
        """Тест обрезки пробелов в тексте вопроса"""
        data = {"text": "   Текст с пробелами   "}
        serializer = QuestionSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["text"] == "Текст с пробелами"


@pytest.mark.django_db
class TestAnswerCreateSerializer:
    """Тесты для AnswerCreateSerializer"""

    def test_valid_answer_data(self):
        """Тест валидных данных ответа"""
        data = {"text": "Валидный текст ответа"}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["text"] == "Валидный текст ответа"

    def test_valid_answer_with_user_id(self):
        """Тест валидных данных ответа с user_id"""
        user_id = uuid.uuid4()
        data = {"text": "Валидный текст ответа", "user_id": str(user_id)}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["user_id"] == user_id

    def test_empty_answer_text(self):
        """Тест пустого текста ответа"""
        data = {"text": ""}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "text" in serializer.errors
        assert "This field may not be blank." in str(serializer.errors["text"][0])

    def test_invalid_uuid_format(self):
        """Тест невалидного формата UUID"""
        data = {"text": "Текст ответа", "user_id": "invalid-uuid"}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "user_id" in serializer.errors
        assert "Must be a valid UUID" in str(serializer.errors["user_id"][0])

    def test_text_stripping_answer(self):
        """Тест обрезки пробелов в тексте ответа"""
        data = {"text": "   Текст с пробелами   "}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["text"] == "Текст с пробелами"

    def test_answer_without_user_id(self):
        """Тест ответа без указания user_id"""
        data = {"text": "Текст ответа"}
        serializer = AnswerCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert "user_id" not in serializer.validated_data
