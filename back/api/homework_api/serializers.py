from rest_framework import serializers
from Homework.models import (
    HomeworkAnswer,
    HomeworkMark
)


class GiveAnswerHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAnswer
        fields = (
            'student',
            'homework',
            'file'
        )


class AssessHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkMark
        fields = (
            'student',
            'homework',
            'homework_answer',
            'mark',
            'explanation'
        )


class SummarySerializer(serializers.Serializer):
    @classmethod
    def get_serializer(cls, model):
        if model == HomeworkAnswer:
            return GiveAnswerHomeworkSerializer
        elif model == HomeworkMark:
            return AssessHomeworkSerializer
