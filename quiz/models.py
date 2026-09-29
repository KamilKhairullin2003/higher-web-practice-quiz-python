"""Модуль с моделями приложения quiz"""

from django.core.exceptions import ValidationError
from django.db import models

from quiz.const import (
    CATEGORY_TITLE_MAX_LENGTH,
    CORRECT_ANSWER_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    DIFFICULTY_MAX_LENGTH,
    EXPLANATION_MAX_LENGTH,
    MIN_OPTIONS_COUNT,
    QUESTION_TEXT_MAX_LENGTH,
    QUIZ_TITLE_MAX_LENGTH,
)


def validate_options(value: list) -> None:
    """Проверяет, что поле options содержит список минимум из 2 вариантов."""
    if not isinstance(value, list) or len(value) < MIN_OPTIONS_COUNT:
        raise ValidationError(
            'Поле options должно содержать массив минимум из'
            f'{MIN_OPTIONS_COUNT} вариантов.'
        )


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(
        max_length=CATEGORY_TITLE_MAX_LENGTH,
        unique=True,
        verbose_name='Название категории',
    )

    class Meta:
        """Метаданные модели категории."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """Возвращает строковое представление."""
        return self.title


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(
        max_length=QUIZ_TITLE_MAX_LENGTH,
        verbose_name='Название квиза',
    )
    description = models.CharField(
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Описание квиза',
    )

    class Meta:
        """Метаданные модели квиза."""

        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'

    def __str__(self) -> str:
        """Возвращает строковое представление."""
        return self.title


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов"""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Категория'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Квиз',
    )
    text = models.CharField(
        max_length=QUESTION_TEXT_MAX_LENGTH,
        verbose_name='Текст вопроса',
    )
    description = models.CharField(
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Описание вопроса',
    )
    options = models.JSONField(
        validators=[validate_options],
        verbose_name='Варианты ответа',
    )
    correct_answer = models.CharField(
        max_length=CORRECT_ANSWER_MAX_LENGTH,
        verbose_name='Правильный ответ',
    )
    explanation = models.CharField(
        max_length=EXPLANATION_MAX_LENGTH,
        blank=True,
        default='',
        verbose_name='Объяснение ответа',
    )
    difficulty = models.CharField(
        max_length=DIFFICULTY_MAX_LENGTH,
        choices=Difficulty.choices,
        verbose_name='Сложность',
    )

    class Meta:
        """Метаданные модели вопроса."""

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        """Возвращает строковое представление."""
        return self.text
