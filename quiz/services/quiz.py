"""Модуль с реализацией сервиса квизов"""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuizService
from quiz.models import Quiz


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def list_quizzes(self) -> list[Quiz]:
        """Возвращает список всех квизов."""
        return list(Quiz.objects.all())

    def get_quiz(self, quiz_id: int) -> Quiz:
        """Возвращает квиз по его идентификатору."""
        return get_object_or_404(Quiz, id=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Возвращает список квизов по названию."""
        return list(Quiz.objects.filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создает новый квиз."""
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """Обновляет существующий квиз."""
        quiz = self.get_quiz(quiz_id)
        for key, value in data.items():
            setattr(quiz, key, value)
        quiz.save()
        return quiz

    def delete_quiz(self, quiz_id: int) -> None:
        """Удаляет квиз по его идентификатору."""
        quiz = self.get_quiz(quiz_id)
        quiz.delete()
