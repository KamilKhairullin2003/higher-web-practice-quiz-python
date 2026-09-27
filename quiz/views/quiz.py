"""Модуль с контроллерами для квизов"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


class QuizListCreateView(APIView):
    """Контроллер для получения всех квизов и создания квиза"""

    service = QuizService()

    def get(self, request: Request) -> Response:
        """Получение всех квизов."""
        quizzes = self.service.list_quizzes()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Создание нового квиза."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = self.service.create_quiz(serializer.validated_data)
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_201_CREATED,
        )


class QuizDetailView(APIView):
    """Контроллер для получения, обновления и удаления квиза по ID"""

    service = QuizService()

    def get(self, request: Request, id: int) -> Response:
        """Получение квиза по идентификатору."""
        quiz = self.service.get_quiz(id)
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, id: int) -> Response:
        """Изменение квиза."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = self.service.update_quiz(id, serializer.validated_data)
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, id: int) -> Response:
        """Удаление квиза."""
        self.service.delete_quiz(id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizByTitleView(APIView):
    """Контроллер для поиска квизов по названию"""

    service = QuizService()

    def get(self, request: Request, title: str) -> Response:
        """Получение квизов по названию."""
        quizzes = self.service.get_quizes_by_title(title)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizRandomQuestionView(APIView):
    """Контроллер для получения случайного вопроса из квиза"""

    question_service = QuestionService()

    def get(self, request: Request, id: int) -> Response:
        """Получение случайного вопроса по идентификатору квиза."""
        question = self.question_service.random_question_from_quiz(id)
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )
