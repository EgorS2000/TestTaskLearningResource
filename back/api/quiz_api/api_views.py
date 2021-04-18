from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, get_object_or_404

from common.utils import serialization
from Quiz.models import (
    Quiz,
    QuizAnswer,
    QuizUserAnswer
)
from api.quiz_api.serializers import SummarySerializer


class CreateQuiz(CreateAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.data.get('question'):
            return Response(
                data={'message': "The quiz question is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data.get('answers'):
            return Response(
                data={'message': "Quiz answers are empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        quiz_data = {
            'question': request.data.get('question')
        }
        created_quiz = serialization(
            serializer=self.serializer_class.get_serializer(Quiz),
            data=quiz_data,
            mode='create'
        )

        answers_list = request.data.get('answers')

        for answer in answers_list:
            answers_data = {
                'answer_text': answer,
                'quiz': Quiz.objects.filter(id=created_quiz.id).first().id
            }
            serialization(
                serializer=self.serializer_class.get_serializer(QuizAnswer),
                data=answers_data,
                mode='create'
            )

        return Response(
            data={'data': 'Quiz was created'},
            status=status.HTTP_201_CREATED
        )


class GiveQuizAnswer(CreateAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_answers_list = request.data.get('answers')
        quiz = kwargs.get('id')

        get_object_or_404(queryset=Quiz, id=quiz)

        if QuizUserAnswer.objects.filter(
                answer_owner=request.user.id,
                quiz=quiz).exists():
            return Response(data={
                "message": "You already answered this quiz"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(user_answers_list) == 0:
            return Response(data={
                "message": "Enter your answers to this quiz"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for user_answer in user_answers_list:
            if not QuizAnswer.objects.filter(
                    quiz=quiz,
                    answer_text=user_answer).exists():
                return Response(data={
                    "message":
                        f"This quiz has no such answer '{user_answer}'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = {
            "answers": list(user_answers_list),
            "answer_owner": request.user.id,
            "quiz": quiz
        }

        serialization(
            serializer=self.serializer_class.get_serializer(QuizUserAnswer),
            data=data,
            mode='create'
        )

        return Response(
            data={'data': 'Answer saved successfully'},
            status=status.HTTP_201_CREATED
        )
