import uuid
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from api.models import Answer, Question


@pytest.mark.django_db
class TestQuestionModel:
    """Тесты для модели Question"""

    def test_create_question_success(self):
        """Тест создания вопроса"""
        question = Question.objects.create(text="Тестовый вопрос")
        assert question.text == "Тестовый вопрос"
        assert question.id is not None
        assert question.created_at is not None

    def test_empty_question_text_validation(self):
        """Тест валидации пустого текста вопроса"""
        with pytest.raises(ValidationError):
            question = Question(text="")
            question.full_clean()

    def test_question_str_representation(self):
        """Тест строкового представления вопроса"""
        question = Question.objects.create(
            text="Очень длинный текст вопроса который должен быть обрезан"
        )
        assert "Вопрос: Очень длинный текст вопроса который должен быть об..." in str(
            question
        )

    @patch("api.models.logger.info")
    def test_question_save_logs_info_on_create(self, mock_logger):
        """Тест логирования при создании вопроса"""
        question = Question(text="Вопрос для тестирования логирования")
        question.save()

        mock_logger.assert_called_once()
        call_args = mock_logger.call_args[0][0]
        assert "Создан новый вопрос: ID" in call_args
        assert "текст: Вопрос для тестирования логирования" in call_args

    @patch("api.models.logger.debug")
    def test_question_save_logs_debug_on_update(self, mock_logger):
        """Тест логирования при обновлении вопроса"""
        question = Question.objects.create(text="Исходный текст")
        question.text = "Обновленный текст"
        question.save()

        mock_logger.assert_called_once_with(f"Обновлен вопрос: ID {question.id}")

    @patch("api.models.logger.warning")
    def test_question_delete_logs_warning(self, mock_logger):
        """Тест логирования при удалении вопроса"""
        question = Question.objects.create(text="Вопрос для удаления")
        question_id = question.id
        question_text = question.text[:50]

        question.delete()

        mock_logger.assert_called_once_with(
            f"Удаление вопроса: ID {question_id}, текст: {question_text}..."
        )


@pytest.mark.django_db
class TestAnswerModel:
    """Тесты для модели Answer"""

    def test_create_answer_success(self, test_question):
        """Тест создания ответа"""
        answer = Answer.objects.create(
            question=test_question, user_id=uuid.uuid4(), text="Тестовый ответ"
        )
        assert answer.text == "Тестовый ответ"
        assert answer.question == test_question
        assert answer.id is not None
        assert answer.created_at is not None

    def test_answer_str_representation(self, test_question):
        """Тест строкового представления ответа"""
        answer = Answer.objects.create(
            question=test_question,
            user_id=uuid.uuid4(),
            text="Очень длинный текст ответа который должен быть обрезан",
        )
        assert (
            f"Ответ на вопрос {test_question.id}: Очень длинный текст ответа который должен быть обр..."
            in str(answer)
        )

    def test_answer_cascade_delete(self, test_question):
        """Тест каскадного удаления ответов при удалении вопроса"""
        for i in range(3):
            Answer.objects.create(
                question=test_question, user_id=uuid.uuid4(), text=f"Ответ {i}"
            )

        assert Answer.objects.filter(question=test_question).count() == 3
        test_question.delete()
        assert Answer.objects.filter(question_id=test_question.id).count() == 0

    def test_multiple_answers_same_user(self, test_question):
        """Тест создания нескольких ответов одним пользователем на один вопрос"""
        user_id = uuid.uuid4()
        for i in range(3):
            Answer.objects.create(
                question=test_question,
                user_id=user_id,
                text=f"Ответ {i} от одного пользователя",
            )

        assert (
            Answer.objects.filter(question=test_question, user_id=user_id).count() == 3
        )

    @patch("api.models.logger.warning")
    def test_answer_delete_logs_warning(self, mock_logger):
        """Тест логирования при удалении ответа"""
        question = Question.objects.create(text="Вопрос")
        answer = Answer.objects.create(
            question=question, user_id=uuid.uuid4(), text="Ответ для удаления"
        )
        answer_id = answer.id
        question_id = answer.question_id

        answer.delete()

        mock_logger.assert_called_once_with(
            f"Удаление ответа: ID {answer_id}, вопрос ID {question_id}"
        )
