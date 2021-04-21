from datetime import datetime

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from Test.models import (
    Test,
    TestQuestions,
    TestQuestionAnswers,
    TestResult
)


class TestService:
    @staticmethod
    def check_test_request(deadline, date_format):
        if datetime.strptime(deadline, date_format) <= datetime.now():
            return Response(data={
                "message": "Deadline time can't be less then time now"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def create_test(test_name, deadline, date_format, sphere, serializer_class):
        test_data = {
            'name': test_name,
            'deadline': datetime.strptime(deadline, date_format),
            'sphere': sphere
        }

        serializer = serializer_class.get_serializer(Test)
        serialized_data = serializer(data=test_data)
        if serialized_data.is_valid():
            saved_data = serialized_data.save()
            return saved_data

    @staticmethod
    def create_answers(answers, test_id, created_question, serializer_class):
        for answer, is_correct in answers.items():
            answer_data = {
                'test': test_id,
                'question': TestQuestions.objects.filter(
                    id=created_question.id).first().id,
                'answer': answer,
                'is_correct': is_correct
            }
            serializer = serializer_class.get_serializer(TestQuestionAnswers)
            serialized_data = serializer(data=answer_data)
            if serialized_data.is_valid():
                serialized_data.save()

    @classmethod
    def create_questions(cls, questions, created_test, questions_value, serializer_class):
        counter = 0
        for question, answers in questions.items():
            test_id = Test.objects.filter(id=created_test.id).first().id
            question_data = {
                'test': test_id,
                'question': question,
                'question_value': questions_value[counter]
            }

            serializer = serializer_class.get_serializer(TestQuestions)
            serialized_data = serializer(data=question_data)
            saved_data = None

            if serialized_data.is_valid():
                saved_data = serialized_data.save()

            cls.create_answers(
                answers=answers,
                test_id=test_id,
                created_question=saved_data,
                serializer_class=serializer_class
            )
            counter += 1

    @staticmethod
    def check_answer_request(test_id, user_id):
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
                result_owner=user_id,
                test=test_id).exists():
            return Response(data={
                "message": "You already answered this test"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def create_user_answer(question_answer, test_id, user_id, serializer_class):
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
            if not TestQuestionAnswers.objects.filter(
                    id=answer_id,
                    question_id=question_id).exists():
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

        user_answer_data = {
            'test': test_id,
            'right_count': right_count,
            'wrong_count': wrong_count,
            'mark': mark / max_mark * 100,
            'result_owner': user_id
        }

        serializer = serializer_class.get_serializer(TestResult)
        serialized_data = serializer(data=user_answer_data)
        if serialized_data.is_valid():
            serialized_data.save()

        return user_answer_data
