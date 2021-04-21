from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from Quiz.serializers import SummarySerializer
from Quiz.services import QuizService


class CreateQuiz(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SummarySerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        question = request.data.get('question')
        answers = request.data.get('answers')

        response = QuizService.check_quiz_request(
            question=question,
            answers=answers
        )
        if response:
            return response

        created_quiz = QuizService.create_quiz(
            question=question,
            serializer_class=self.serializer_class
        )

        QuizService.create_answers(
            answers=answers,
            created_quiz=created_quiz,
            serializer_class=self.serializer_class
        )

        return Response(
            data={'data': 'Quiz was created'},
            status=status.HTTP_201_CREATED
        )


class GiveQuizAnswer(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SummarySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user_answers_list = request.data.get('answers')
        quiz = kwargs.get('id')
        user_id = request.user.id

        response = QuizService.check_answer_request(
            quiz=quiz,
            user_id=user_id,
            user_answers_list=user_answers_list
        )
        if response:
            return response

        QuizService.create_user_answer(
            quiz=quiz,
            user_id=user_id,
            user_answers_list=user_answers_list,
            serializer_class=self.serializer_class
        )

        return Response(
            data={'data': 'Answer saved successfully'},
            status=status.HTTP_201_CREATED
        )
