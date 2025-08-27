from django.db import models
import uuid

class Question(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    user_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID пользователя"
    )
    text = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания ответа")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ на вопрос{self.question.id}: {self.text[:50]}..."