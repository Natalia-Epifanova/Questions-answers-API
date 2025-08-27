from django.urls import path

from api.apps import ApiConfig
from api.views import (AnswerCreateView, AnswerDetailView, QuestionDetailView,
                       QuestionListView)

app_name = ApiConfig.name

urlpatterns = [
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path(
        "questions/<int:question_id>/answers/",
        AnswerCreateView.as_view(),
        name="answer-create",
    ),
    path("answers/<int:pk>/", AnswerDetailView.as_view(), name="answer-detail"),
]
