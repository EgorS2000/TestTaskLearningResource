from rest_framework import serializers


class TasksSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(
        help_text="Task identifier"
    )
    type = serializers.CharField(
        help_text="Task type"
    )
    status = serializers.CharField(
        help_text="Task status"
    )
    deadline = serializers.DateTimeField(
        allow_null=True,
        help_text="Deadline"
    )


class StaticsSerializer(serializers.Serializer):
    average_mark = serializers.CharField(
        help_text="Average mark for all evaluated tasks"
    )
    average_tests_mark = serializers.CharField(
        help_text="Average mark for all evaluated tests"
    )
    average_homeworks_mark = serializers.CharField(
        help_text="Average mark for all evaluated homeworks"
    )
