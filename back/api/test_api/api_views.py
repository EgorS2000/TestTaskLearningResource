from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, get_object_or_404

from common.utils import serialization
from Test.models import (
    Test,
    TestQuestions,
    TestQuestionAnswers,
    TestResult
)
from api.test_api.serializers import SummarySerializer


class CreateTest(CreateAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        test_name = request.data.get('name')
        deadline = request.data.get('deadline')
        sphere = request.data.get('sphere')
        date_format = '%d/%m/%Y %H:%M:%S'

        if datetime.strptime(deadline, date_format) <= datetime.now():
            return Response(data={
                "message": "Deadline time can't be less then time now"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'name': test_name,
            'deadline': datetime.strptime(deadline, date_format),
            'sphere': sphere
        }

        created_test = serialization(
            serializer=self.serializer_class.get_serializer(Test),
            data=data,
            mode='create'
        )

        questions = request.data.get('questions')
        questions_value = request.data.get('questions_value')

        counter = 0
        for question, answers in questions.items():
            test_id = Test.objects.filter(id=created_test.id).first().id
            question_data = {
                'test': test_id,
                'question': question,
                'question_value': questions_value[counter]
            }
            created_question = serialization(
                serializer=self.serializer_class.get_serializer(TestQuestions),
                data=question_data,
                mode='create'
            )
            for answer, is_correct in answers.items():
                answer_data = {
                    'test': test_id,
                    'question': TestQuestions.objects.filter(
                        id=created_question.id).first().id,
                    'answer': answer,
                    'is_correct': is_correct
                }
                serialization(
                    serializer=self.serializer_class.get_serializer(
                        TestQuestionAnswers
                    ),
                    data=answer_data,
                    mode='create'
                )
            counter += 1

        return Response(
            data={"data": "Test successfully created"},
            status=status.HTTP_201_CREATED
        )


class GiveAnswerTest(CreateTest):
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        test_id = kwargs.get('id')

        if get_object_or_404(
                queryset=Test,
                id=test_id).deadline < datetime.now():
            return Response(data={
                "message":
                    "You can't answer this test because "
                    "you didn't meet deadline"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if TestResult.objects.filter(
                result_owner=request.user.id,
                test=test_id).exists():
            return Response(data={
                "message": "You already answered this test"},
                status=status.HTTP_400_BAD_REQUEST
            )

        question_answer = request.data.get('question_answer')

        wrong_count, right_count, mark, max_mark = 0, 0, 0, 0

        for question_id, answer_id in question_answer.items():
            try:
                question_value = TestQuestions.objects.filter(
                    id=int(question_id)).first().question_value
            except AttributeError:
                return Response(data={
                    "message": "There are no such question"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                TestQuestionAnswers.objects.filter(
                    id=answer_id,
                    question_id=question_id).first().is_correct
            except AttributeError:
                return Response(data={
                    "message": "There are no such answer to this question"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                is_correct = TestQuestionAnswers.objects.filter(
                    id=answer_id).first().is_correct
            except AttributeError:
                return Response(data={
                    "message": "There are no such answer"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            max_mark += question_value
            if is_correct:
                mark += question_value
                right_count += 1
            else:
                wrong_count += 1

        data = {
            'test': test_id,
            'right_count': right_count,
            'wrong_count': wrong_count,
            'mark': mark / max_mark * 100,
            'result_owner': request.user.id
        }
        serialization(
            serializer=self.serializer_class.get_serializer(TestResult),
            data=data,
            mode='create'
        )

        return Response(data=data, status=status.HTTP_201_CREATED)
