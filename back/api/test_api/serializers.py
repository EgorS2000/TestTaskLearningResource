from rest_framework import serializers
from Test.models import (
    Test,
    TestQuestions,
    TestQuestionAnswers,
    TestResult
)


class CreateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = [
            'name',
            'deadline',
            'sphere'
        ]


class CreateTestQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestions
        fields = [
            'test',
            'question',
            'question_value'
        ]


class CreateTestQuestionsAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionAnswers
        fields = [
            'test',
            'question',
            'answer',
            'is_correct'
        ]


class GiveTestAnswerSerializer(serializers.ModelSerializer):
    mark = serializers.FloatField()

    class Meta:
        model = TestResult
        fields = [
            'test',
            'right_count',
            'wrong_count',
            'mark',
            'result_owner'
        ]


class SummarySerializer(serializers.Serializer):
    @classmethod
    def get_serializer(cls, model):
        if model == Test:
            return CreateTestSerializer
        elif model == TestQuestions:
            return CreateTestQuestionsSerializer
        elif model == TestQuestionAnswers:
            return CreateTestQuestionsAnswersSerializer
        elif model == TestResult:
            return GiveTestAnswerSerializer
