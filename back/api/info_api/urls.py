from django.urls import path
from api.info_api.api_views import (
    Tasks,
    Stats
)

urlpatterns = (
    path(
        "tasks/<str:type>/<str:status>/",
        Tasks.as_view(),
        name='available_tasks'
    ),
    path(
        "tasks/stats/",
        Stats.as_view(),
        name='stats'
    )
)
