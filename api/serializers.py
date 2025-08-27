import logging

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


class AnswerCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания ответов.
    Позволяет указать user_id или генерирует его автоматически.
    """

    user_id = serializers.UUIDField(required=False)

    class Meta:
        model = Answer
        fields = ["id", "text", "user_id"]
        read_only_fields = [
            "id",
        ]
