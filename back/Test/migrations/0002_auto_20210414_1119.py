# Generated by Django 3.2 on 2021-04-14 11:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Test', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Test', 'verbose_name_plural': 'Tests'},
        ),
        migrations.AlterModelOptions(
            name='testquestionanswers',
            options={'verbose_name': 'TestQuestionAnswer', 'verbose_name_plural': 'TestQuestionAnswers'},
        ),
        migrations.AlterModelOptions(
            name='testquestions',
            options={'verbose_name': 'TestQuestion', 'verbose_name_plural': 'TestQuestions'},
        ),
        migrations.AlterModelOptions(
            name='testresult',
            options={'verbose_name': 'TestResult', 'verbose_name_plural': 'TestResults'},
        ),
        migrations.AlterField(
            model_name='test',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999), help_text='Test deadline', verbose_name='Deadline'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(help_text='Test name', max_length=64, verbose_name='TestName'),
        ),
        migrations.AlterField(
            model_name='test',
            name='sphere',
            field=models.CharField(help_text='Scope to which the test relates', max_length=32, verbose_name='Sphere'),
        ),
        migrations.AlterField(
            model_name='testquestionanswers',
            name='answer',
            field=models.CharField(help_text='Answer identifier', max_length=128, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='testquestionanswers',
            name='is_correct',
            field=models.BooleanField(help_text='Is the answer correct or not', verbose_name='IsCorrect'),
        ),
        migrations.AlterField(
            model_name='testquestionanswers',
            name='question',
            field=models.ForeignKey(default=None, help_text='Question identifier', on_delete=django.db.models.deletion.CASCADE, to='Test.testquestions', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='testquestionanswers',
            name='test',
            field=models.ForeignKey(default=None, help_text='Test identifier', on_delete=django.db.models.deletion.CASCADE, to='Test.test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='testquestions',
            name='question',
            field=models.CharField(help_text='Question condition', max_length=256, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='testquestions',
            name='question_value',
            field=models.FloatField(default=None, help_text='Amount of points which you can receive for right answer to this question', verbose_name='QuestionValue'),
        ),
        migrations.AlterField(
            model_name='testquestions',
            name='test',
            field=models.ForeignKey(default=None, help_text='Test identifier', on_delete=django.db.models.deletion.CASCADE, to='Test.test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='mark',
            field=models.FloatField(default=0.0, help_text='Mark', verbose_name='Mark'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='result_owner',
            field=models.ForeignKey(help_text='Result owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ResultOwner'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='right_count',
            field=models.IntegerField(default=None, help_text='Amount of right answered questions', verbose_name='RightCount'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(default=None, help_text='Test identifier', on_delete=django.db.models.deletion.CASCADE, to='Test.test', verbose_name='Test'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='wrong_count',
            field=models.IntegerField(default=None, help_text='Amount of wrong answered questions', verbose_name='WrongCount'),
        ),
    ]
