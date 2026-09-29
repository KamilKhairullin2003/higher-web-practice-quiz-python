"""Модуль с тестами для контроллеров API"""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestCategoryAPI:
    """Тесты ручек категорий"""

    def test_create_and_get_category(self, client: Client) -> None:
        """Тест создания и получения категории"""
        create_url = reverse('category-create')
        response = client.post(
            create_url,
            {'title': 'History'},
            content_type='application/json',
        )
        assert response.status_code == HTTPStatus.CREATED

        get_url = reverse('category-get-by-id')
        response = client.get(get_url)
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]['title'] == 'History'

    def test_category_detail_update_delete(self, client: Client) -> None:
        """Тест получения по ID, обновления и удаления категории"""
        create_resp = client.post(
            reverse('category-create'),
            {'title': 'Geography'},
            content_type='application/json',
        )
        cat_id = create_resp.json()['id']
        detail_url = reverse('category-detail', kwargs={'id': cat_id})

        get_resp = client.get(detail_url)
        assert get_resp.status_code == HTTPStatus.OK
        assert get_resp.json()['title'] == 'Geography'

        put_resp = client.put(
            detail_url,
            {'title': 'World Geography'},
            content_type='application/json',
        )
        assert put_resp.status_code == HTTPStatus.OK
        assert put_resp.json()['title'] == 'World Geography'

        del_resp = client.delete(detail_url)
        assert del_resp.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
class TestQuizAndQuestionAPI:
    """Тесты ручек квизов и вопросов"""

    def test_quiz_crud_and_search(self, client: Client) -> None:
        """Тест CRUD операций и поиска по названию для квиза"""
        list_url = reverse('quiz-list-create')
        create_resp = client.post(
            list_url,
            {'title': 'Django Quiz', 'description': 'Test your Django skills'},
            content_type='application/json',
        )
        assert create_resp.status_code == HTTPStatus.CREATED
        quiz_id = create_resp.json()['id']

        assert client.get(list_url).status_code == HTTPStatus.OK

        by_title_url = reverse('quiz-by-title', kwargs={'title': 'Django'})
        title_resp = client.get(by_title_url)
        assert title_resp.status_code == HTTPStatus.OK
        assert len(title_resp.json()) == 1

        detail_url = reverse('quiz-detail', kwargs={'id': quiz_id})
        put_resp = client.put(
            detail_url,
            {'title': 'Django Pro Quiz', 'description': 'Updated'},
            content_type='application/json',
        )
        assert put_resp.status_code == HTTPStatus.OK
        assert put_resp.json()['title'] == 'Django Pro Quiz'

        assert client.delete(detail_url).status_code == HTTPStatus.NO_CONTENT

    def test_question_crud_check_and_random(self, client: Client) -> None:
        """
        Тест на проверку crud операций модели вопроса.

        Создания вопроса, поиска по тексту,
        проверки ответа и случайного вопроса.
        """
        cat_resp = client.post(
            reverse('category-create'),
            {'title': 'IT'},
            content_type='application/json',
        )
        quiz_resp = client.post(
            reverse('quiz-list-create'),
            {'title': 'Backend Quiz'},
            content_type='application/json',
        )
        cat_id = cat_resp.json()['id']
        quiz_id = quiz_resp.json()['id']

        question_payload = {
            'category_id': cat_id,
            'quiz_id': quiz_id,
            'text': 'What is DRF?',
            'description': 'Framework question',
            'options': ['Django REST Framework', 'Database Relational Field'],
            'correct_answer': 'Django REST Framework',
            'explanation': 'DRF stands for Django REST Framework',
            'difficulty': 'easy',
        }

        q_list_url = reverse('question-list-create')
        q_resp = client.post(
            q_list_url,
            question_payload,
            content_type='application/json'
        )
        assert q_resp.status_code == HTTPStatus.CREATED
        q_id = q_resp.json()['id']

        by_text_url = reverse('question-by-text', kwargs={'text': 'DRF'})
        assert len(client.get(by_text_url).json()) == 1

        check_url = reverse('question-check', kwargs={'id': q_id})
        check_resp = client.post(
            check_url,
            {'answer': 'Django REST Framework'},
            content_type='application/json',
        )
        assert check_resp.status_code == HTTPStatus.OK
        assert check_resp.json()['is_correct'] is True

        random_url = reverse('quiz-random-question', kwargs={'id': quiz_id})
        random_resp = client.get(random_url)
        assert random_resp.status_code == HTTPStatus.OK
        assert random_resp.json()['id'] == q_id

        q_detail_url = reverse('question-detail', kwargs={'id': q_id})
        question_payload['text'] = 'What is Django REST Framework?'
        assert client.put(
            q_detail_url, question_payload, content_type='application/json'
        ).status_code == 200
        assert client.delete(q_detail_url).status_code == HTTPStatus.NO_CONTENT
