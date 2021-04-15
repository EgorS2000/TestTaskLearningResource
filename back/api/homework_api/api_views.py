import sys
from datetime import datetime, date

import requests
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from common.utils import serialization

from TestTaskLearningResource.settings import (
    AUTO_MARK_HOMEWORK_URL,
    ADMIN_TOKEN_KEY,
    MAX_FILE_SIZE_IN_BYTES
)
from Homework.models import (
    Homework,
    HomeworkAnswer,
    HomeworkMark
)
from api.homework_api.serializers import SummarySerializer


class GiveAnswerHomework(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def create(self, request, *args, **kwargs):
        homework_id = kwargs.get('id')

        try:
            homework = Homework.objects.get(id=homework_id)
        except Homework.DoesNotExist:
            return Response(
                data={
                    "message": "No such homework"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if HomeworkAnswer.objects.filter(homework_id=homework_id, student=request.user).exists():
            return Response(
                data={
                    "message": "You are already answered this homework"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']
        file_size = sys.getsizeof(file)
        if file_size > MAX_FILE_SIZE_IN_BYTES:
            return Response(
                data={'message': "File size can't be larger then 2 MB"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_name = default_storage.save(
            f'homeworks/{str(date.today().strftime("%d-%m-%Y"))}/'
            f'{str(datetime.now().strftime("%H-%M-%S"))}/{file.name}',
            file
        )

        data = {
            'student': request.user.id,
            'homework': homework_id,
            'file': f'/media/{file_name}'
        }

        homework_answer_data = serialization(
            serializer=self.serializer_class.get_serializer(HomeworkAnswer),
            data=data,
            mode='create'
        )

        if homework.deadline < datetime.now():
            requests.post(url=AUTO_MARK_HOMEWORK_URL.
                          format(homework_answer_data_id=homework_answer_data.id),
                          headers={'Authorization': ADMIN_TOKEN_KEY},
                          data={'mark': 0.0,
                                "explanation": "You don't meet a deadline"}
                          )
            return Response(data={
                'data': "Answer uploaded successfully, "
                        "but you don't meet a deadline that's why, "
                        "you automatically get 0"
            },
                status=status.HTTP_201_CREATED
            )

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
        try:
            homework_answer = HomeworkAnswer.objects.get(id=answer_id)
            student = homework_answer.student_id
            homework = homework_answer.homework_id
        except HomeworkAnswer.DoesNotExist:
            return Response(data={
                'message': "No such answer"
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            HomeworkMark.objects.get(homework_answer_id=answer_id)
        except HomeworkMark.DoesNotExist:
            pass
        else:
            return Response(data={
                'message': "You have already rated this homework"
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'student': student,
            'homework': homework,
            'homework_answer': answer_id,
            'mark': float(mark / 10 * 100),
            'explanation': explanation
        }
        serialization(
            serializer=self.serializer_class.get_serializer(HomeworkMark),
            data=data,
            mode='create'
        )
        return Response(data={
            'data': "You've successfully rated homework"
        },
            status=status.HTTP_201_CREATED
        )
