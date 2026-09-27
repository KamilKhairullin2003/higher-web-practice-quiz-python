"""Модуль настройки админ-панели для приложения quiz"""

from django.contrib import admin

from quiz.models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Category"""

    list_display = ('id', 'title')
    search_fields = ('title',)
    ordering = ('id',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Quiz"""

    list_display = ('id', 'title', 'description')
    search_fields = ('title', 'description')
    ordering = ('id',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Question"""

    list_display = ('id', 'text', 'category', 'quiz', 'difficulty')
    search_fields = ('text', 'description')
    list_filter = ('difficulty', 'category', 'quiz')
    ordering = ('id',)
