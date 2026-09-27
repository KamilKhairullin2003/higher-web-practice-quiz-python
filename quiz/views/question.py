"""Модуль с контроллерами для вопросов"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionListCreateView(APIView):
    """Контроллер для получения всех вопросов и создания вопроса"""

    service = QuestionService()

    def get(self, request: Request) -> Response:
        """Получение всех вопросов."""
        questions = self.service.list_questions()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Создание вопроса."""
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = serializer.validated_data['quiz']
        question = self.service.create_question(
            quiz.id,
            serializer.validated_data,
        )
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )


class QuestionDetailView(APIView):
    """Контроллер для получения, изменения и удаления вопроса по ID"""

    service = QuestionService()

    def get(self, request: Request, id: int) -> Response:
        """Получение вопроса по идентификатору."""
        question = self.service.get_question(id)
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, id: int) -> Response:
        """Изменение вопроса."""
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = self.service.update_question(id, serializer.validated_data)
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, id: int) -> Response:
        """Удаление вопроса."""
        self.service.delete_question(id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionByTextView(APIView):
    """Контроллер для поиска вопроса по тексту"""

    service = QuestionService()

    def get(self, request: Request, text: str) -> Response:
        """Получение вопросов по тексту."""
        questions = self.service.get_questions_by_text(text)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCheckAnswerView(APIView):
    """Контроллер для проверки ответа на вопрос"""

    service = QuestionService()

    def post(self, request: Request, id: int) -> Response:
        """Проверка ответа на вопрос."""
        answer = request.data.get('answer', '')
        is_correct = self.service.check_answer(id, str(answer))
        return Response(
            {'is_correct': is_correct},
            status=status.HTTP_200_OK,
        )
