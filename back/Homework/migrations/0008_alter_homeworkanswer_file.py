# Generated by Django 3.2 on 2021-04-12 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homework', '0007_alter_homeworkanswer_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkanswer',
            name='file',
            field=models.CharField(max_length=256, verbose_name='file_path'),
        ),
    ]
