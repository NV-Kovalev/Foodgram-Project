from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User = get_user_model()


def get_post_delete_method(
        self, request, pk,
        obj=None,
        model=None,
        serializer=None):
    """
    Дополнительный метод для однотипных post, delete запросов.
    Только для моделей состоящих из поля связанного
    с моделью пользователя и объекта.

    obj - Объект который нужно связать с моделью пользователя
    model - Модель через которую проходит связь
    serializer - Сериализатор для ответа пользователю после операции.
    """
    validated_data = {}
    for field in model._meta.get_fields():
        if field.name != 'id' and field.name != 'user':
            validated_data[field.name] = obj
        if field.name == 'user':
            validated_data[field.name] = request.user

    if request.method == 'POST':

        if obj == request.user:
            return Response(
                {"errors": "Ошибка при добавлении"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if model.objects.filter(**validated_data).exists():
            return Response(
                {"errors": "Ошибка при добавлении"},
                status=status.HTTP_400_BAD_REQUEST
            )

        model.objects.create(**validated_data)
        serializer = serializer(
            obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':

        if model.objects.filter(**validated_data).exists():
            model.objects.get(**validated_data).delete()
            return Response()
        return Response(
                {"errors": "Ошибка при удалении"},
                status=status.HTTP_400_BAD_REQUEST)
