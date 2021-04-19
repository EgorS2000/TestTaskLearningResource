import os
from datetime import datetime, date

from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.response import Response
from common.utils import serialization

from Homework.models import (
    HomeworkAnswer,
    HomeworkMark
)


class HomeworkService:
    @staticmethod
    def check_homework_request(homework_id, user, file_size):
        if HomeworkAnswer.objects.filter(
                homework_id=homework_id,
                student=user).exists():
            return Response(
                data={
                    "message": "You are already answered this homework"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if file_size > int(os.getenv('MAX_FILE_SIZE_IN_BYTES')):
            return Response(
                data={'message': "File size can't be larger then 2 MB"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def user_answer_homework(file, user, homework_id, serializer_class):
        file_name = default_storage.save(
            f'homeworks/{str(date.today().strftime("%d-%m-%Y"))}/'
            f'{str(datetime.now().strftime("%H-%M-%S"))}/{file.name}',
            file
        )

        data = {
            'student': user.id,
            'homework': homework_id,
            'file': f'/media/{file_name}'
        }

        homework_answer_data = serialization(
            serializer=serializer_class.get_serializer(HomeworkAnswer),
            data=data,
            mode='create'
        )

        return homework_answer_data

    @staticmethod
    def assess_homework(homework_answer, answer_id, mark, explanation, serializer_class):
        data = {
            'student': homework_answer.student_id,
            'homework': homework_answer.homework_id,
            'homework_answer': answer_id,
            'mark': float(mark / 10 * 100),
            'explanation': explanation
        }
        serialization(
            serializer=serializer_class.get_serializer(HomeworkMark),
            data=data,
            mode='create'
        )

    @classmethod
    def check_homework_answer_date(cls, homework, homework_answer_data, serializer_class):
        if homework.deadline < datetime.now():
            cls.assess_homework(
                homework_answer=homework_answer_data,
                answer_id=homework_answer_data.id,
                mark=0,
                explanation="You don't meet a deadline",
                serializer_class=serializer_class
            )
            return Response(data={
                'data': "Answer uploaded successfully, "
                        "but you don't meet a deadline that's why, "
                        "you automatically get 0"
            },
                status=status.HTTP_201_CREATED
            )

    @staticmethod
    def check_user_answer(answer_id):
        if HomeworkMark.objects.filter(homework_answer_id=answer_id).exists():
            return Response(data={
                'message': "You have already rated this homework"
            },
                status=status.HTTP_400_BAD_REQUEST
            )
