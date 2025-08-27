import logging
import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.response import Response

from api.models import Answer, Question
from api.serializers import AnswerCreateSerializer, AnswerSerializer, QuestionSerializer

logger = logging.getLogger(__name__)


class QuestionListView(ListCreateAPIView):
    """
    API endpoint для получения списка вопросов и создания новых вопросов.

    Methods:
        GET: Возвращает список всех вопросов с ответами
        POST: Создает новый вопрос
    """

    queryset = Question.objects.all().prefetch_related("answers")
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        """Обработка GET запроса для получения списка вопросов"""
        logger.info("Запрос на получение списка вопросов")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Обработка POST запроса для создания вопроса"""
        logger.info("Запрос на создание нового вопроса")
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info(f"Вопрос успешно создан: ID {response.data.get('id')}")
        return response


class QuestionDetailView(RetrieveDestroyAPIView):
    """
    API endpoint для получения деталей вопроса и его удаления.

    Methods:
        GET: Возвращает детальную информацию о вопросе с ответами
        DELETE: Удаляет вопрос и все связанные ответы
    """

    queryset = Question.objects.all().prefetch_related("answers")
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        """Обработка GET запроса для получения деталей вопроса"""
        question_id = kwargs.get("pk")
        logger.info(f"Запрос на получение вопроса ID {question_id}")
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Обработка DELETE запроса для удаления вопроса"""
        question_id = kwargs.get("pk")
        logger.warning(f"Запрос на удаление вопроса ID {question_id}")
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            logger.info(f"Вопрос ID {question_id} успешно удален")
        return response


class AnswerCreateView(CreateAPIView):
    """
    API endpoint для создания ответов на вопросы.

    Methods:
        POST: Создает новый ответ для указанного вопроса
    """

    serializer_class = AnswerCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Обработка POST запроса для создания ответа.

        Проверяет существование вопроса перед созданием ответа.
        """
        question_id = self.kwargs["question_id"]
        logger.info(f"Запрос на создание ответа для вопроса ID {question_id}")

        if not Question.objects.filter(id=question_id).exists():
            logger.warning(
                f"Попытка создания ответа для несуществующего вопроса ID {question_id}"
            )
            return Response(
                {"error": "Нельзя добавить ответ на несуществующий вопрос"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Создание ответа с привязкой к вопросу.

        Args:
            serializer: Сериализатор с валидированными данными
        """
        question_id = self.kwargs["question_id"]
        question = get_object_or_404(Question, id=question_id)
        user_id = serializer.validated_data.get("user_id", uuid.uuid4())

        logger.debug(
            f"Создание ответа для вопроса ID {question_id}, пользователь: {user_id}"
        )
        serializer.save(question=question, user_id=user_id)


class AnswerDetailView(RetrieveDestroyAPIView):
    """
    API endpoint для получения и удаления ответов.

    Methods:
        GET: Возвращает детальную информацию об ответе
        DELETE: Удаляет ответ
    """

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get(self, request, *args, **kwargs):
        """Обработка GET запроса для получения ответа"""
        answer_id = kwargs.get("pk")
        logger.info(f"Запрос на получение ответа ID {answer_id}")
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Обработка DELETE запроса для удаления ответа"""
        answer_id = kwargs.get("pk")
        logger.warning(f"Запрос на удаление ответа ID {answer_id}")
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            logger.info(f"Ответ ID {answer_id} успешно удален")
        return response
