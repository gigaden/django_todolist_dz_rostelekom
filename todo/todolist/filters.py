from django_filters import rest_framework as dj_filters
from .models import TodoList, Category


class TodolistFilterSet(dj_filters.FilterSet):
    """Набор фильтров для представления для модели задач."""

    title = dj_filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_active = dj_filters.BooleanFilter(field_name="is_completed")

    order_by_field = "ordering"

    class Meta:
        model = TodoList
        fields = [
            "name",
            "is_completed",
        ]

class CategoryFilterSet(dj_filters.FilterSet):
    """Набор фильров для представления для модели категорий."""

    title = dj_filters.CharFilter(field_name="name", lookup_expr="icontains")

    order_by_field = "ordering"

    class Meta:
        model = Category
        fields = [
            "name",
        ]

