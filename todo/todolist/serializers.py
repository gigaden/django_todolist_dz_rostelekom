from rest_framework import serializers

from todolist.models import TodoList, Category


class TodoSerializer(serializers.ModelSerializer):
    """Сериализатор по модели TodoList."""

    class Meta:
        model = TodoList
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор по модели Category."""

    class Meta:
        model = Category
        fields = ["id", "name"]
