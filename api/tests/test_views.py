import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_questions_list(api_client, test_question):
    """Тест получения списка вопросов"""
    url = reverse("api:question-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["text"] == test_question.text


@pytest.mark.django_db
def test_create_question_valid_data(api_client):
    """Тест создания вопроса с валидными данными"""
    url = reverse("api:question-list")
    data = {"text": "Новый тестовый вопрос"}
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data["text"] == data["text"]
    assert "id" in response.data


@pytest.mark.django_db
def test_create_question_empty_text(api_client):
    """Тест создания вопроса с пустым текстом"""
    url = reverse("api:question-list")
    data = {"text": ""}
    response = api_client.post(url, data)

    assert response.status_code == 400
    assert "text" in response.data


@pytest.mark.django_db
def test_get_question_detail(api_client, test_question):
    """Тест получения деталей вопроса"""
    url = reverse("api:question-detail", kwargs={"pk": test_question.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["text"] == test_question.text
    assert "answers" in response.data


@pytest.mark.django_db
def test_delete_question(api_client, test_question):
    """Тест удаления вопроса"""
    url = reverse("api:question-detail", kwargs={"pk": test_question.id})
    response = api_client.delete(url)

    assert response.status_code == 204

    from api.models import Question

    assert Question.objects.filter(id=test_question.id).exists() is False


@pytest.mark.django_db
def test_create_answer_valid_data(api_client, test_question):
    """Тест создания ответа с валидными данными"""
    url = reverse("api:answer-create", kwargs={"question_id": test_question.id})
    data = {"text": "Новый тестовый ответ"}
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data["text"] == data["text"]
    assert "id" in response.data


@pytest.mark.django_db
def test_create_answer_nonexistent_question(api_client):
    """Тест создания ответа для несуществующего вопроса"""
    url = reverse("api:answer-create", kwargs={"question_id": 999})
    data = {"text": "Новый тестовый ответ"}
    response = api_client.post(url, data)

    assert response.status_code == 404
    assert "error" in response.data


@pytest.mark.django_db
def test_get_answer_detail(api_client, test_answer):
    """Тест получения деталей ответа"""
    url = reverse("api:answer-detail", kwargs={"pk": test_answer.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["text"] == test_answer.text


@pytest.mark.django_db
def test_delete_answer(api_client, test_answer):
    """Тест удаления ответа"""
    url = reverse("api:answer-detail", kwargs={"pk": test_answer.id})
    response = api_client.delete(url)

    assert response.status_code == 204

    from api.models import Answer

    assert Answer.objects.filter(id=test_answer.id).exists() is False
