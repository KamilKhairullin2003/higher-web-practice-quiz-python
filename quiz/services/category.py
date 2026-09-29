"""Модуль с реализацией сервиса категорий"""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.services.utils import update_object


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self) -> list[Category]:
        """Метод для получения списка категорий."""
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category:
        """Метод для получения категории по идентификатору."""
        return get_object_or_404(Category, id=category_id)

    def create_category(self, title: str) -> Category:
        """Создает категорию вопросов."""
        category, _ = Category.objects.get_or_create(title=title)
        return category

    def update_category(self, category_id: int, data: dict) -> Category:
        """Обновляет категорию новыми данными."""
        return update_object(Category, category_id, data)

    def delete_category(self, category_id: int) -> None:
        """Удаляет категорию."""
        self.get_category(category_id).delete()
