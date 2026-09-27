"""Модуль с контроллерами для категорий"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CategoryListCreateView(APIView):
    """Контроллер для получения списка категорий и создания новой категории"""

    service = CategoryService()

    def get(self, request: Request) -> Response:
        """Получение всех категорий."""
        categories = self.service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Создание новой категории."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self.service.create_category(
            title=serializer.validated_data['title'],
        )
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetailView(APIView):
    """Контроллер для получения, изменения и удаления категории по ID"""

    service = CategoryService()

    def get(self, request: Request, id: int) -> Response:
        """Получение категории по идентификатору."""
        category = self.service.get_category(id)
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, id: int) -> Response:
        """Изменение категории."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self.service.update_category(id, serializer.validated_data)
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, id: int) -> Response:
        """Удаление категории."""
        self.service.delete_category(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
