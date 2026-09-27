"""Модуль с моделями приложения quiz"""

from django.db import models


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Возвращает строковое представление."""
        return self.title


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, default='')

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
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    text = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True, default='')
    options = models.JSONField()
    correct_answer = models.CharField(max_length=500)
    explanation = models.CharField(max_length=250, blank=True, default='')
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
    )

    def __str__(self) -> str:
        """Возвращает строковое представление."""
        return self.text
