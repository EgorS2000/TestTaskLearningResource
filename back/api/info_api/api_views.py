from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from common.utils import serialization
from Quiz.models import (
    Quiz,
    QuizUserAnswer
)
from Test.models import (
    Test,
    TestResult
)
from Homework.models import (
    Homework,
    HomeworkAnswer,
    HomeworkMark
)
from api.info_api.serializers import (
    TasksSerializer,
    StaticsSerializer
)


class Tasks(ListAPIView):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task_type = kwargs.get('type')
        task_status = kwargs.get('status')
        if task_type == 'test' and task_status == 'completed':
            task_status = 'evaluated'
        if task_type == 'quiz' and task_status == 'evaluated':
            task_status = 'completed'

        result_data = []
        if task_type == "quiz":
            completed_quizzes = QuizUserAnswer.objects.filter(
                answer_owner=request.user.id)
            if task_status == "set":
                completed_quizzes_id_list = []
                for completed_quiz in completed_quizzes:
                    completed_quizzes_id_list.append(completed_quiz.quiz_id)

                all_quizzes_list = get_list_or_404(klass=Quiz)

                set_quizzes = []
                for quiz in all_quizzes_list:
                    if quiz.id not in completed_quizzes_id_list:
                        set_quizzes.append(quiz)

                for set_quiz in set_quizzes:
                    data = {
                        'task_id': set_quiz.id,
                        'type': 'quiz',
                        'status': 'set',
                        'deadline': None
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

            if task_status == 'completed':
                for completed_quiz in completed_quizzes:
                    data = {
                        'task_id': completed_quiz.quiz_id,
                        'type': 'quiz',
                        'status': 'completed',
                        'deadline': None
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

        if task_type == 'test':
            evaluated_tests = TestResult.objects.filter(
                result_owner=request.user.id)
            if task_status == 'set':
                evaluated_tests_id_list = []
                for evaluated_test in evaluated_tests:
                    evaluated_tests_id_list.append(evaluated_test.test_id)

                all_tests_list = get_list_or_404(klass=Test)

                set_tests = []
                for test in all_tests_list:
                    if test.id not in evaluated_tests_id_list:
                        set_tests.append(test)

                for set_test in set_tests:
                    data = {
                        'task_id': set_test.id,
                        'type': 'test',
                        'status': 'set',
                        'deadline': None
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

            if task_status == 'evaluated':
                for completed_test in evaluated_tests:
                    data = {
                        'task_id': completed_test.test_id,
                        'type': 'test',
                        'status': 'evaluated',
                        'deadline': Test.objects.filter(
                            id=completed_test.test_id).first().deadline
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

        if task_type == 'homework':
            completed_homeworks_list = HomeworkAnswer.objects.filter(
                student=request.user.id)
            evaluated_homeworks_list = HomeworkMark.objects.filter(
                student=request.user.id)
            if task_status == 'set':
                completed_homework_id_list = []
                evaluated_homework_id_list = []

                for completed_homework in completed_homeworks_list:
                    completed_homework_id_list.append(
                        completed_homework.homework_id)

                for evaluated_homework in evaluated_homeworks_list:
                    evaluated_homework_id_list.append(
                        evaluated_homework.homework_answer_id)

                all_homeworks_list = get_list_or_404(klass=Homework)

                set_homeworks = []
                for homework in all_homeworks_list:
                    if homework.id not in completed_homework_id_list and \
                            homework.id not in evaluated_homework_id_list:
                        set_homeworks.append(homework)

                for set_homework in set_homeworks:
                    data = {
                        'task_id': set_homework.id,
                        'type': 'homework',
                        'status': 'set',
                        'deadline': Homework.objects.filter(
                            id=set_homework.id).first().deadline
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

            if task_status == 'completed':
                evaluated_homework_id_list = []

                for evaluated_homework in evaluated_homeworks_list:
                    evaluated_homework_id_list.append(
                        evaluated_homework.homework_answer_id)

                all_homeworks_list = get_list_or_404(klass=HomeworkAnswer)

                completed_homeworks = []
                for homework in all_homeworks_list:
                    if homework.id not in evaluated_homework_id_list:
                        completed_homeworks.append(homework)

                for completed_homework in completed_homeworks:
                    data = {
                        'task_id': completed_homework.homework_id,
                        'type': 'homework',
                        'status': 'completed',
                        'deadline':
                            Homework.objects.filter(
                                id=completed_homework.homework_id
                            ).first().deadline
                    }
                    result_data.append(data)
            if task_status == 'evaluated':
                for evaluated_homework in evaluated_homeworks_list:
                    data = {
                        'task_id': evaluated_homework.homework_id,
                        'type': 'homework',
                        'status': 'evaluated',
                        'deadline':
                            Homework.objects.filter(
                                id=evaluated_homework.homework_id
                            ).first().deadline
                    }
                    serialization_data = serialization(
                        serializer=self.serializer_class,
                        data=data,
                        mode='get'
                    )
                    result_data.append(serialization_data.data)

        return Response(data={
            'data': result_data
        },
            status=status.HTTP_200_OK
        )


class Stats(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StaticsSerializer
    average_homeworks_mark, average_tests_mark = 0.0, 0.0

    def get(self, request, *args, **kwargs):
        tests_trigger = False
        homeworks_trigger = False
        tests = TestResult.objects.filter(result_owner=request.user.id)
        if tests.count() == 0:
            tests_trigger = True
        homeworks = HomeworkMark.objects.filter(student=request.user.id)
        if homeworks.count() == 0:
            homeworks_trigger = True

        if tests_trigger and homeworks_trigger:
            return Response(data={
                'message': 'You have no evaluated tasks'
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        tests_marks_list, tests_marks_list = [], []

        for test in tests:
            tests_marks_list.append(test.mark)

        homeworks_marks_list = []
        for homework in homeworks:
            homeworks_marks_list.append(homework.mark)

        if len(tests_marks_list) != 0:
            self.average_tests_mark = \
                sum(tests_marks_list) / len(tests_marks_list)

        if len(homeworks_marks_list) != 0:
            self.average_homeworks_mark = \
                sum(homeworks_marks_list) / len(homeworks_marks_list)

        average_mark = float(
            (self.average_tests_mark + self.average_homeworks_mark) / 2
        )
        data = {
            "average_mark": f'{average_mark}%',
            "average_tests_mark": f'{self.average_tests_mark}%',
            "average_homeworks_mark": f'{self.average_homeworks_mark}%'
        }
        serialized_data = serialization(
            serializer=self.serializer_class,
            data=data,
            mode='get'
        )

        return Response(data={
            'data': serialized_data.data
        },
            status=status.HTTP_200_OK
        )
