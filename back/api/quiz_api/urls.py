from django.urls import path
from api.quiz_api.api_views import (
    CreateQuiz,
    GiveQuizAnswer,
)

urlpatterns = [
    path(
        "quizzes/create/",
        CreateQuiz.as_view(),
        name='create_quiz'
    ),

    path(
        "quizzes/<int:id>/answer/",
        GiveQuizAnswer.as_view(),
        name='give_quiz_answer'
    )
]
