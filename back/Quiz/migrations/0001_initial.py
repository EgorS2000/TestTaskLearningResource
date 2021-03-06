# Generated by Django 3.2 on 2021-04-15 15:34

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='Question for users', max_length=256, verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='QuizUserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), help_text='Answer identifier', size=None, verbose_name='Answers')),
                ('answer_owner', models.ForeignKey(help_text='Answer owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='AnswerOwner')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.quiz')),
            ],
            options={
                'verbose_name': 'QuizUserAnswer',
                'verbose_name_plural': 'QuizUserAnswers',
            },
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(default='', help_text='Possible answers for questions', max_length=128, verbose_name='AnswerText')),
                ('quiz', models.ForeignKey(default=None, help_text='Quiz identifier', on_delete=django.db.models.deletion.CASCADE, to='Quiz.quiz', verbose_name='Quiz')),
            ],
            options={
                'verbose_name': 'QuizAnswer',
                'verbose_name_plural': 'QuizAnswers',
            },
        ),
    ]
