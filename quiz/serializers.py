"""Модуль с сериализаторами приложения quiz"""

from rest_framework import serializers

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
        """Проверяет, что options является списком минимум из 2 элементов"""
        if not isinstance(value, list) or len(value) < 2:
            raise serializers.ValidationError(
                'Поле options должно содержать массив минимум из'
                '2 вариантов ответа.'
            )
        return value


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Quiz
        fields = ('id', 'title', 'description', 'questions')
