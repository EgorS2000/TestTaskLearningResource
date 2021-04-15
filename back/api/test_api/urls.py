from django.urls import path
from api.test_api.api_views import (
    CreateTest,
    GiveAnswerTest
)

urlpatterns = [

    path(
        "tests/create/",
        CreateTest.as_view(),
        name='create_test'
    ),

    path(
        "tests/<int:id>/answer/",
        GiveAnswerTest.as_view(),
        name='give_answer'
    )
]
