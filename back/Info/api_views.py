from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Homework.models import HomeworkMark
from Test.models import TestResult
from Info.serializers import (
    TasksSerializer,
    StaticsSerializer
)
from services.info.services import InfoService


class Tasks(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        task_type = kwargs.get('type')
        task_status = kwargs.get('status')
        user_id = request.user.id
        result_data = None

        task_type, task_status = InfoService.correct_task(
            task_type=task_type,
            task_status=task_status
        )

        if task_type == "quiz":
            result_data = InfoService.get_quiz_info(
                task_status=task_status,
                user_id=user_id,
                serializer_class=self.serializer_class
            )

        if task_type == "test":
            result_data = InfoService.get_test_info(
                task_status=task_status,
                user_id=user_id,
                serializer_class=self.serializer_class
            )

        if task_type == "homework":
            result_data = InfoService.get_homework_info(
                task_status=task_status,
                user_id=user_id,
                serializer_class=self.serializer_class
            )

        return Response(data={
            'data': result_data
        },
            status=status.HTTP_200_OK
        )


class Stats(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = StaticsSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.user.id

        tests = TestResult.objects.filter(result_owner=user_id)
        homeworks = HomeworkMark.objects.filter(student=user_id)

        response = InfoService.check_stats(
            tests=tests,
            homeworks=homeworks
        )
        if response:
            return response

        serialized_data = InfoService.get_stats_info(
            tests=tests,
            homeworks=homeworks,
            average_tests_mark=0.0,
            average_homeworks_mark=0.0,
            serializer_class=self.serializer_class
        )

        return Response(data={
            'data': serialized_data.data
        },
            status=status.HTTP_200_OK
        )
