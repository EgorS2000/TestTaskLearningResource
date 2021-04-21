from rest_framework import routers

from Info.api_views import (
    Tasks,
    Stats
)

router = routers.DefaultRouter()
router.register(r'tasks/(?P<type>\w+)/(?P<status>\w+)', Tasks, basename='available_tasks')
router.register(r'tasks/stats', Stats, basename='stats')
urlpatterns = router.urls
