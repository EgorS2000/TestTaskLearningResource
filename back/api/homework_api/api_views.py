import sys

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from Homework.models import (
    Homework, HomeworkAnswer,
)
from services.homework_services.services import HomeworkService
from api.homework_api.serializers import SummarySerializer


class GiveAnswerHomework(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def create(self, request, *args, **kwargs):
        homework_id = kwargs.get('id')
        user = request.user

        file = request.FILES['file']
        file_size = sys.getsizeof(file)

        homework = get_object_or_404(
            queryset=Homework,
            id=homework_id
        )

        response = HomeworkService.check_homework_request(
            homework_id=homework_id,
            user=user,
            file_size=file_size
        )
        if response:
            return response

        homework_answer_data = HomeworkService.user_answer_homework(
            file=file,
            user=user,
            homework_id=homework_id,
            serializer_class=self.serializer_class
        )

        response = HomeworkService.check_homework_answer_date(
            homework=homework,
            homework_answer_data=homework_answer_data,
            serializer_class=self.serializer_class
        )
        if response:
            return response

        return Response(data={
            'data': 'Answer uploaded successfully'
        },
            status=status.HTTP_201_CREATED
        )


class AssessHomework(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def create(self, request, *args, **kwargs):
        answer_id = kwargs.get('id')
        mark = float(request.data.get('mark'))
        explanation = request.data.get('explanation')

        homework_answer = get_object_or_404(
            queryset=HomeworkAnswer,
            id=answer_id
        )

        response_1 = HomeworkService.check_user_answer(answer_id=answer_id)
        if response_1:
            return response_1

        HomeworkService.assess_homework(
            homework_answer=homework_answer,
            answer_id=answer_id,
            mark=mark,
            explanation=explanation,
            serializer_class=self.serializer_class
        )

        return Response(data={
            'data': "You've successfully rated homework"
        },
            status=status.HTTP_201_CREATED
        )
