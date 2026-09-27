"""Модуль с реализацией сервиса категорий"""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category


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
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category:
        """Обновляет категорию новыми данными."""
        category = self.get_category(category_id)
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete_category(self, category_id: int) -> None:
        """Удаляет категорию."""
        category = self.get_category(category_id)
        category.delete()
