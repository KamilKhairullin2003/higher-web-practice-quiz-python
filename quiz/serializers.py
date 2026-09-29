"""Модуль с сериализаторами приложения quiz"""

from rest_framework import serializers

from quiz.const import MIN_OPTIONS_COUNT
from quiz.models import Category, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        """Метаданные сериализатора."""

        model = Category
        fields = ('id', 'title')


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
    )
    quiz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(),
        source='quiz',
    )

    class Meta:
        """Метаданные сериализатора."""

        model = Question
        fields = (
            'id',
            'category_id',
            'quiz_id',
            'text',
            'description',
            'options',
            'correct_answer',
            'explanation',
            'difficulty',
        )

    def validate_options(self, value: list) -> list:
        """Проверяет количество вариантов ответа."""
        if not isinstance(value, list) or len(value) < MIN_OPTIONS_COUNT:
            raise serializers.ValidationError(
                f'Поле options должно содержать массив минимум из '
                f'{MIN_OPTIONS_COUNT} вариантов ответа.'
            )
        return value

    def validate(self, data: dict) -> dict:
        """Проверяет, что правильный ответ входит в список вариантов ответа."""
        options = data.get('options', [])
        correct_answer = data.get('correct_answer')
        if correct_answer not in options:
            raise serializers.ValidationError(
                'Правильный ответ должен быть одним из'
                'вариантов ответа в options.'
            )
        return data


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Quiz
        fields = ('id', 'title', 'description', 'questions')
