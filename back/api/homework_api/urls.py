from django.urls import path
from api.homework_api.api_views import (
    GiveAnswerHomework,
    AssessHomework,
)

urlpatterns = [
    path(
        "homeworks/<int:id>/answer/",
        GiveAnswerHomework.as_view(),
        name='answer_homework'
    ),
    path(
        "homeworks/<int:id>/answer/mark/",
        AssessHomework.as_view(),
        name='mark_answered_homework'
    )
]
