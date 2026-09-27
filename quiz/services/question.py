"""Модуль с реализацией сервиса вопросов"""

import random

from django.http import Http404
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.models import Question


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов"""

    def list_questions(self) -> list[Question]:
        """Возвращает список всех вопросов."""
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        """Возвращает вопрос по его идентификатору."""
        return get_object_or_404(Question, id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """Возвращает вопросы по тексту."""
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """Получение вопросов по идентификатору квиза."""
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """Создает новый вопрос."""
        question_data = data.copy()
        if quiz_id is not None and 'quiz' not in question_data:
            question_data['quiz_id'] = quiz_id
        return Question.objects.create(**question_data)

    def update_question(self, question_id: int, data: dict) -> Question:
        """Обновляет существующий вопрос."""
        question = self.get_question(question_id)
        for key, value in data.items():
            setattr(question, key, value)
        question.save()
        return question

    def delete_question(self, question_id: int) -> None:
        """Удаляет вопрос по его идентификатору."""
        question = self.get_question(question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """Проверяет ответ на вопрос."""
        question = self.get_question(question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """Возвращает случайный вопрос из указанного квиза."""
        questions = self.get_questions_for_quiz(quiz_id)
        if not questions:
            raise Http404('No questions at this quiz')  # for linter
        return random.choice(questions)
