from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Homework(models.Model):
    text = models.TextField(
        null=False,
        verbose_name='Text',
        help_text='Homework condition'
    )
    deadline = models.DateTimeField(
        null=False,
        default=datetime.max,
        verbose_name='Deadline',
        help_text='Homework deadline'
    )

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = "Homework"
        verbose_name_plural = "Homeworks"


class HomeworkAnswer(models.Model):
    student = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Student',
        help_text='Student who completed homework'
    )
    homework = models.ForeignKey(
        to=Homework,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Homework',
        help_text='Homework identifier'
    )
    file = models.CharField(
        max_length=256,
        null=False,
        verbose_name='FilePath',
        help_text='The path to the file attached to the homework'
    )

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = "HomeworkAnswer"
        verbose_name_plural = "HomeworkAnswers"


class HomeworkMark(models.Model):
    student = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Student',
        help_text='The student who gets the mark'
    )
    homework = models.ForeignKey(
        to=Homework,
        null=False,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Homework',
        help_text='Homework'
    )
    homework_answer = models.ForeignKey(
        to=HomeworkAnswer,
        null=False,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='HomeworkAnswer',
        help_text='The answer to which we are assessing'
    )
    mark = models.FloatField(
        null=False,
        default=0.0,
        verbose_name='Mark',
        help_text='Mark'
    )
    explanation = models.TextField(
        null=False,
        default='',
        verbose_name='Explanation',
        help_text='Explanation why student got this mark'
    )

    def __str__(self):
        return str(self.mark)

    class Meta:
        verbose_name = "HomeworkMark"
        verbose_name_plural = "HomeworkMarks"
