from rest_framework import serializers
from Quiz.models import (
    Quiz,
    QuizAnswer,
    QuizUserAnswer
)


class CreateQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'question'
        ]


class CreateQuizAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = [
            'answer_text',
            'quiz'
        ]


class UserQuizAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizUserAnswer
        fields = [
            'answers',
            'answer_owner',
            'quiz'
        ]


class SummarySerializer(serializers.Serializer):
    @classmethod
    def get_serializer(cls, model):
        if model == Quiz:
            return CreateQuizSerializer
        elif model == QuizAnswer:
            return CreateQuizAnswersSerializer
        elif model == QuizUserAnswer:
            return UserQuizAnswersSerializer
