from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import Answer, Question


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    """
    Административный интерфейс для модели Question.
    """

    list_filter = (
        "id",
        "text",
        "created_at",
    )


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    """
    Административный интерфейс для модели Answer.
    """

    list_filter = (
        "id",
        "question",
        "user_id",
        "created_at",
    )
