"""Модуль с вспомогательными утилитами для сервисов"""

from typing import TypeVar

from django.db.models import Model
from django.shortcuts import get_object_or_404

T = TypeVar('T', bound=Model)


def update_object(model: type[T], pk:int, data:dict) -> T:
    """Обновляет объект указанной моделипо первичному ключ."""
    instance = get_object_or_404(model, pk=pk)
    for key, value in data.items():
        setattr(instance, key, value)
    instance.save()
    return instance
