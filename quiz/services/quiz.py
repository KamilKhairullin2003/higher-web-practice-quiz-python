"""Модуль с реализацией сервиса квизов"""

from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuizService
from quiz.models import Question, Quiz
from quiz.services.utils import update_object


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def _get_base_queryset(self) -> QuerySet[Quiz]:
        """
        Возвращает QuerySet

        Возвращает QuerySet квизов с предзагруженными вопросами
        и их связями.
        """
        questions_prefetch = Prefetch(
            'questions',
            queryset=Question.objects.select_related('category', 'quiz'),
        )
        return Quiz.objects.prefetch_related(questions_prefetch)

    def list_quizzes(self) -> list[Quiz]:
        """Возвращает список всех квизов."""
        return list(self._get_base_queryset().all())

    def get_quiz(self, quiz_id: int) -> Quiz:
        """Возвращает квиз по его идентификатору."""
        return get_object_or_404(self._get_base_queryset(), id=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Возвращает список квизов по названию."""
        return list(self._get_base_queryset().filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создает новый квиз."""
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """Обновляет существующий квиз."""
        return update_object(Quiz, quiz_id, data)

    def delete_quiz(self, quiz_id: int) -> None:
        """Удаляет квиз по его идентификатору."""
        self.get_quiz(quiz_id).delete()
