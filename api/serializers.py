import logging
import uuid

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Answer, Question

logger = logging.getLogger(__name__)


class AnswerSerializer(ModelSerializer):
    """
    Сериализатор для ответов.
    Используется для чтения данных ответов.
    """

    question_id = serializers.IntegerField(source="question.id", read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "question_id", "user_id", "text", "created_at"]
        read_only_fields = ["id", "created_at", "user_id"]


class QuestionSerializer(ModelSerializer):
    """
    Сериализатор для вопросов.
    Включает связанные ответы в виде вложенного списка.
    """

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "created_at", "answers"]
        read_only_fields = ["id", "created_at"]

    def validate_text(self, value):
        """
        Валидация текста вопроса.
        Args:
            value (str): Текст вопроса для валидации
        Returns:
            str: Валидированный текст
        Raises:
            ValidationError: Если текст пустой или содержит только пробелы
        """
        if not value or not value.strip():
            logger.warning("Попытка создания вопроса с пустым текстом")
            raise serializers.ValidationError("Текст вопроса не может быть пустым")
        return value.strip()


class AnswerCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания ответов.
    Позволяет указать user_id или генерирует его автоматически.
    """

    user_id = serializers.UUIDField(required=False)

    class Meta:
        model = Answer
        fields = ["text", "user_id"]

    def validate_user_id(self, value):
        """
        Валидация user_id.
        Args:
            value (str/UUID): user_id для валидации
        Returns:
            UUID: Валидированный UUID
        Raises:
            ValidationError: Если передан некорректный формат UUID
        """
        if value:
            try:
                return uuid.UUID(str(value))
            except ValueError:
                logger.warning(f"Некорректный формат UUID: {value}")
                raise serializers.ValidationError("Некорректный формат UUID")
        return value

    def validate_text(self, value):
        """
        Валидация текста ответа.
        Args:
            value (str): Текст ответа для валидации
        Returns:
            str: Валидированный текст
        Raises:
            ValidationError: Если текст пустой или содержит только пробелы
        """
        if not value or not value.strip():
            logger.warning("Попытка создания ответа с пустым текстом")
            raise serializers.ValidationError("Текст ответа не может быть пустым")
        return value.strip()
