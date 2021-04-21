from rest_framework import routers

from Homework.api_views import (
    GiveAnswerHomework,
    AssessHomework,
)

router = routers.DefaultRouter()
router.register(r'homeworks/(?P<id>\d+)/answer', GiveAnswerHomework, basename='answer_homework')
router.register(r'homeworks/(?P<id>\d+)/answer/mark', AssessHomework, basename='mark_answered_homework')
urlpatterns = router.urls
