"""Модуль с тестами для сервисного слоя"""

import pytest

from quiz.models import Category, Difficulty, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


@pytest.mark.django_db
class TestCategoryService:
    """Тесты сервиса категорий"""

    def setup_method(self) -> None:
        """Подготавливает сервис"""
        self.service = CategoryService()

    def test_create_and_get_category(self) -> None:
        """Тест создания и получения категории"""
        category = self.service.create_category('Science')
        fetched = self.service.get_category(category.id)
        assert fetched.title == 'Science'

    def test_list_categories(self) -> None:
        """Тест получения списка всех категорий"""
        initial_count = len(self.service.list_categories())
        self.service.create_category('Math')
        self.service.create_category('History')
        assert len(self.service.list_categories()) == initial_count + 2

    def test_update_category(self) -> None:
        """Тест обновления категории"""
        category = Category.objects.create(title='Old')
        updated = self.service.update_category(category.id, {'title': 'New'})
        assert updated.title == 'New'

    def test_delete_category(self) -> None:
        """Тест удаления категории"""
        category = Category.objects.create(title='Temp')
        count_before = Category.objects.count()
        self.service.delete_category(category.id)
        assert Category.objects.count() == count_before - 1


@pytest.mark.django_db
class TestQuizService:
    """Тесты сервиса квизов"""

    def setup_method(self) -> None:
        """Подготавливает сервис"""
        self.service = QuizService()

    def test_create_and_get_quiz(self) -> None:
        """Тест создания и получения квиза"""
        quiz = self.service.create_quiz(
            {'title': 'Python Quiz', 'description': 'Basic Python'}
        )
        fetched = self.service.get_quiz(quiz.id)
        assert fetched.title == 'Python Quiz'
        assert fetched.description == 'Basic Python'

    def test_list_quizzes(self) -> None:
        """Тест получения списка квизов"""
        initial_count = len(self.service.list_quizzes())
        self.service.create_quiz({'title': 'Quiz 1'})
        assert len(self.service.list_quizzes()) == initial_count + 1

    def test_get_quizes_by_title(self) -> None:
        """Тест поиска квиза по названию"""
        self.service.create_quiz({'title': 'Django Advanced'})
        self.service.create_quiz({'title': 'FastAPI Basics'})
        results = self.service.get_quizes_by_title('Django')
        assert len(results) == 1
        assert results[0].title == 'Django Advanced'

    def test_update_quiz(self) -> None:
        """Тест обновления квиза"""
        quiz = self.service.create_quiz({'title': 'Old Quiz'})
        updated = self.service.update_quiz(quiz.id, {'title': 'Updated Quiz'})
        assert updated.title == 'Updated Quiz'

    def test_delete_quiz(self) -> None:
        """Тест удаления квиза"""
        quiz = self.service.create_quiz({'title': 'To Delete'})
        count_before = Quiz.objects.count()
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == count_before - 1


@pytest.mark.django_db
class TestQuestionService:
    """Тесты сервиса вопросов"""

    def setup_method(self) -> None:
        """Подготавливает сервис и базовые объекты"""
        self.service = QuestionService()
        self.category = Category.objects.create(title='Programming')
        self.quiz = Quiz.objects.create(title='General Tech')
        self.question_data = {
            'category': self.category,
            'text': 'What is PEP 8?',
            'description': 'Style guide question',
            'options': ['Style guide', 'Database', 'Framework'],
            'correct_answer': 'Style guide',
            'explanation': 'PEP 8 is the Python style guide',
            'difficulty': Difficulty.EASY,
        }

    def test_create_and_get_question(self) -> None:
        """Тест создания и получения вопроса"""
        question = self.service.create_question(
            self.quiz.id,
            self.question_data
        )
        fetched = self.service.get_question(question.id)
        assert fetched.text == 'What is PEP 8?'
        assert fetched.quiz.id == self.quiz.id

    def test_get_questions_by_text(self) -> None:
        """Тест поиска вопроса по тексту"""
        self.service.create_question(self.quiz.id, self.question_data)
        results = self.service.get_questions_by_text('PEP 8')
        assert len(results) == 1
        assert results[0].correct_answer == 'Style guide'

    def test_update_and_delete_question(self) -> None:
        """Тест обновления и удаления вопроса"""
        question = self.service.create_question(
            self.quiz.id,
            self.question_data
        )
        updated = self.service.update_question(
            question.id,
            {'text': 'Updated text?'}
        )
        assert updated.text == 'Updated text?'

        count_before = Question.objects.count()
        self.service.delete_question(question.id)
        assert Question.objects.count() == count_before - 1

    def test_check_answer_and_random_question(self) -> None:
        """Тест проверки ответа и случайного вопроса"""
        question = self.service.create_question(
            self.quiz.id,
            self.question_data
        )
        assert self.service.check_answer(question.id, 'Style guide') is True
        assert self.service.check_answer(question.id, 'Database') is False

        random_q = self.service.random_question_from_quiz(self.quiz.id)
        assert random_q.id == question.id
