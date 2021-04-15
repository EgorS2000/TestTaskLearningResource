from rest_framework import status
from rest_framework.response import Response


def serialization(**kwargs):
    serialized_data = None
    serializer = kwargs.get('serializer')

    if kwargs.get('mode') == 'create' or 'get':
        serialized_data = serializer(data=kwargs.get('data'))

    if kwargs.get('mode') == 'update':
        serialized_data = serializer(
            instance=kwargs.get('instance'),
            data=kwargs.get('data')
        )

    if serialized_data.is_valid():
        if kwargs.get('mode') == 'create':
            saved_data = serialized_data.save()
            return saved_data
        if kwargs.get('mode') == 'get':
            return serialized_data

    return Response(
        data={"message": serialized_data.errors},
        status=status.HTTP_400_BAD_REQUEST
    )
