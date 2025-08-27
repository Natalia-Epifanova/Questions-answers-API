import logging
import uuid

from django.db import models

logger = logging.getLogger(__name__)


class Question(models.Model):
    """
    Модель вопроса.

    Attributes:
        text (TextField): Текст вопроса
        created_at (DateTimeField): Дата и время создания вопроса
    """

    text = models.TextField(verbose_name="Текст вопроса")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания вопроса"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

    def save(self, *args, **kwargs):
        """Переопределение метода save с логированием"""
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info(
                f"Создан новый вопрос: ID {self.id}, текст: {self.text[:50]}..."
            )
        else:
            logger.debug(f"Обновлен вопрос: ID {self.id}")

    def delete(self, *args, **kwargs):
        """Переопределение метода delete с логированием"""
        logger.warning(f"Удаление вопроса: ID {self.id}, текст: {self.text[:50]}...")
        super().delete(*args, **kwargs)


class Answer(models.Model):
    """
    Модель ответа на вопрос.

    Attributes:
        question (ForeignKey): Ссылка на вопрос
        user_id (UUIDField): Идентификатор пользователя
        text (TextField): Текст ответа
        created_at (DateTimeField): Дата и время создания ответа
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    user_id = models.UUIDField(
        default=uuid.uuid4, editable=False, verbose_name="ID пользователя"
    )
    text = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания ответа"
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ на вопрос {self.question.id}: {self.text[:50]}..."

    def save(self, *args, **kwargs):
        """Переопределение метода save с логированием"""
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info(
                f"Создан новый ответ: ID {self.id}, вопрос ID {self.question_id}, пользователь: {self.user_id}"
            )

    def delete(self, *args, **kwargs):
        """Переопределение метода delete с логированием"""
        logger.warning(f"Удаление ответа: ID {self.id}, вопрос ID {self.question_id}")
        super().delete(*args, **kwargs)
