from rest_framework import routers

from Quiz.api_views import (
    CreateQuiz,
    GiveQuizAnswer,
)

router = routers.DefaultRouter()
router.register(f'quizzes/create', CreateQuiz, basename='create_quiz')
router.register(f'quizzes/(?P<id>\d+)/answer', GiveQuizAnswer, basename='quiz_answer')
urlpatterns = router.urls
