from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from Quiz.models import (
    Quiz,
    QuizAnswer,
    QuizUserAnswer
)


class QuizService:
    @staticmethod
    def check_quiz_request(question, answers):
        if not question:
            return Response(
                data={'message': "The quiz question is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not answers:
            return Response(
                data={'message': "Quiz answers are empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def create_quiz(question, serializer_class):
        quiz_data = {
            'question': question
        }
        serializer = serializer_class.get_serializer(Quiz)
        serialized_data = serializer(data=quiz_data)
        if serialized_data.is_valid():
            return serialized_data.save()

    @staticmethod
    def create_answers(answers, created_quiz, serializer_class):
        answers_list = answers

        for answer in answers_list:
            answers_data = {
                'answer_text': answer,
                'quiz': Quiz.objects.filter(id=created_quiz.id).first().id
            }

            serializer = serializer_class.get_serializer(QuizAnswer)
            serialized_data = serializer(data=answers_data)
            if serialized_data.is_valid():
                serialized_data.save()

    @staticmethod
    def check_answer_request(quiz, user_id, user_answers_list):
        get_object_or_404(queryset=Quiz, id=quiz)

        if QuizUserAnswer.objects.filter(
                answer_owner=user_id,
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

    @staticmethod
    def create_user_answer(quiz, user_id, user_answers_list, serializer_class):
        user_answer_data = {
            "answers": list(user_answers_list),
            "answer_owner": user_id,
            "quiz": quiz
        }

        serializer = serializer_class.get_serializer(QuizUserAnswer)
        serialized_data = serializer(data=user_answer_data)
        if serialized_data.is_valid():
            serialized_data.save()
