from rest_framework import routers

from Test.api_views import (
    CreateTest,
    GiveAnswerTest
)

router = routers.DefaultRouter()
router.register(r'tests/create', CreateTest, basename='create_test')
router.register(r'tests/(?P<id>\d+)/answer', GiveAnswerTest, basename='give_answer')
urlpatterns = router.urls
