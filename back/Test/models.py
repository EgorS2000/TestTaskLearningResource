from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        verbose_name='TestName',
        help_text='Test name'
    )
    deadline = models.DateTimeField(
        null=False,
        default=datetime.max,
        verbose_name='Deadline',
        help_text='Test deadline'
    )
    sphere = models.CharField(
        max_length=32,
        null=False,
        verbose_name='Sphere',
        help_text='Scope to which the test relates'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"


class TestQuestions(models.Model):
    test = models.ForeignKey(
        to=Test,
        null=False,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Test',
        help_text='Test identifier'
    )
    question = models.CharField(
        max_length=256,
        null=False,
        verbose_name='Question',
        help_text='Question condition'
    )
    question_value = models.FloatField(
        null=False,
        default=None,
        verbose_name='QuestionValue',
        help_text='Amount of points which you can receive for right answer to this question'
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = "TestQuestion"
        verbose_name_plural = "TestQuestions"


class TestQuestionAnswers(models.Model):
    test = models.ForeignKey(
        to=Test,
        null=False,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Test',
        help_text='Test identifier'
    )
    question = models.ForeignKey(
        to=TestQuestions,
        null=False,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Question',
        help_text='Question identifier'
    )
    answer = models.CharField(
        max_length=128,
        null=False,
        verbose_name='Answer',
        help_text='Answer identifier'
    )
    is_correct = models.BooleanField(
        null=False,
        verbose_name='IsCorrect',
        help_text='Is the answer correct or not'
    )

    def __str__(self):
        return str(self.answer)

    class Meta:
        verbose_name = "TestQuestionAnswer"
        verbose_name_plural = "TestQuestionAnswers"


class TestResult(models.Model):
    test = models.ForeignKey(
        to=Test,
        null=False,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Test',
        help_text='Test identifier'
    )
    right_count = models.IntegerField(
        null=False,
        default=None,
        verbose_name='RightCount',
        help_text='Amount of right answered questions'
    )
    wrong_count = models.IntegerField(
        null=False,
        default=None,
        verbose_name='WrongCount',
        help_text='Amount of wrong answered questions'
    )
    mark = models.FloatField(
        null=False,
        default=0.0,
        verbose_name='Mark',
        help_text='Mark'
    )
    result_owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="ResultOwner",
        help_text="Result owner",
    )

    def __str__(self):
        return str(self.mark)

    class Meta:
        verbose_name = "TestResult"
        verbose_name_plural = "TestResults"
