from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Quiz(models.Model):
    question = models.CharField(
        max_length=256,
        null=False,
        verbose_name='Question',
        help_text='Question for users'
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class QuizAnswer(models.Model):
    answer_text = models.CharField(
        max_length=128,
        null=False,
        default='',
        verbose_name='AnswerText',
        help_text='Possible answers for questions'
    )
    quiz = models.ForeignKey(
        Quiz,
        null=False,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Quiz',
        help_text='Quiz identifier'
    )

    def __str__(self):
        return str(self.answer_text)

    class Meta:
        verbose_name = "QuizAnswer"
        verbose_name_plural = "QuizAnswers"


class QuizUserAnswer(models.Model):
    answers = ArrayField(
        models.CharField(max_length=128),
        blank=False,
        verbose_name='Answers',
        help_text='Answer identifier'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )
    answer_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="AnswerOwner",
        help_text="Answer owner"
    )

    def __str__(self):
        return str(self.answers)

    class Meta:
        verbose_name = "QuizUserAnswer"
        verbose_name_plural = "QuizUserAnswers"
