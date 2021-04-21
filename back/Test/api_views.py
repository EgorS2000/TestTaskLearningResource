from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from Test.serializers import SummarySerializer
from services.test.services import TestService


class CreateTest(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SummarySerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        test_name = request.data.get('name')
        deadline = request.data.get('deadline')
        sphere = request.data.get('sphere')
        date_format = '%d/%m/%Y %H:%M:%S'

        response = TestService.check_test_request(
            deadline=deadline,
            date_format=date_format
        )
        if response:
            return response

        created_test = TestService.create_test(
            test_name=test_name,
            deadline=deadline,
            date_format=date_format,
            sphere=sphere,
            serializer_class=self.serializer_class
        )

        questions = request.data.get('questions')
        questions_value = request.data.get('questions_value')

        TestService.create_questions(
            questions=questions,
            created_test=created_test,
            questions_value=questions_value,
            serializer_class=self.serializer_class
        )

        return Response(
            data={"data": "Test successfully created"},
            status=status.HTTP_201_CREATED
        )


class GiveAnswerTest(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SummarySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        test_id = kwargs.get('id')
        user_id = request.user.id

        response = TestService.check_answer_request(
            test_id,
            user_id
        )
        if response:
            return response

        question_answer = request.data.get('question_answer')

        data = TestService.create_user_answer(
            question_answer=question_answer,
            test_id=test_id,
            user_id=user_id,
            serializer_class=self.serializer_class
        )
        if type(data) == Response:
            return data
        else:
            return Response(data=data, status=status.HTTP_201_CREATED)
