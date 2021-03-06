# Generated by Django 3.2 on 2021-04-10 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Homework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworkanswer',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='student'),
        ),
        migrations.AddField(
            model_name='homeworkmark',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='student'),
        ),
    ]
