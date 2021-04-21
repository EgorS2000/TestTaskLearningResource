from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.response import Response

from Homework.models import (
    Homework,
    HomeworkAnswer,
    HomeworkMark
)
from Quiz.models import (
    Quiz,
    QuizUserAnswer
)
from Test.models import (
    Test,
    TestResult
)


class InfoService:
    @staticmethod
    def correct_task(task_type, task_status):
        if task_type == 'test' and task_status == 'completed':
            task_status = 'evaluated'
        if task_type == 'quiz' and task_status == 'evaluated':
            task_status = 'completed'
        return task_type, task_status

    @staticmethod
    def get_quiz_info(task_status, user_id, serializer_class):
        result_data = []
        completed_quizzes = QuizUserAnswer.objects.filter(
            answer_owner=user_id)
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

                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)

        if task_status == 'completed':
            for completed_quiz in completed_quizzes:
                data = {
                    'task_id': completed_quiz.quiz_id,
                    'type': 'quiz',
                    'status': 'completed',
                    'deadline': None
                }

                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)

        return result_data

    @staticmethod
    def get_test_info(task_status, user_id, serializer_class):
        result_data = []
        evaluated_tests = TestResult.objects.filter(
            result_owner=user_id)
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
                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)

        if task_status == 'evaluated':
            for completed_test in evaluated_tests:
                data = {
                    'task_id': completed_test.test_id,
                    'type': 'test',
                    'status': 'evaluated',
                    'deadline': Test.objects.filter(
                        id=completed_test.test_id).first().deadline
                }

                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)

        return result_data

    @staticmethod
    def get_homework_info(task_status, user_id, serializer_class):
        result_data = []
        completed_homeworks_list = HomeworkAnswer.objects.filter(
            student=user_id)
        evaluated_homeworks_list = HomeworkMark.objects.filter(
            student=user_id)
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

                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)

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
                serializer = serializer_class
                serialized_data = serializer(data=data)
                if serialized_data.is_valid():
                    result_data.append(serialized_data.data)
        return result_data

    @staticmethod
    def check_stats(tests, homeworks):
        tests_trigger = False
        homeworks_trigger = False

        if tests.count() == 0:
            tests_trigger = True

        if homeworks.count() == 0:
            homeworks_trigger = True

        if tests_trigger and homeworks_trigger:
            return Response(data={
                'message': 'You have no evaluated tasks'
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_stats_info(tests, homeworks, average_tests_mark, average_homeworks_mark, serializer_class):
        tests_marks_list, tests_marks_list = [], []

        for test in tests:
            tests_marks_list.append(test.mark)

        homeworks_marks_list = []
        for homework in homeworks:
            homeworks_marks_list.append(homework.mark)

        if len(tests_marks_list) != 0:
            average_tests_mark = \
                sum(tests_marks_list) / len(tests_marks_list)

        if len(homeworks_marks_list) != 0:
            average_homeworks_mark = \
                sum(homeworks_marks_list) / len(homeworks_marks_list)

        average_mark = float(
            (average_tests_mark + average_homeworks_mark) / 2
        )
        data = {
            "average_mark": f'{average_mark}%',
            "average_tests_mark": f'{average_tests_mark}%',
            "average_homeworks_mark": f'{average_homeworks_mark}%'
        }
        serializer = serializer_class
        serialized_data = serializer(data=data)
        if serialized_data.is_valid():
            return serialized_data
