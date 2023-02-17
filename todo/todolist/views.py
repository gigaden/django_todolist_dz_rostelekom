from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from rest_framework.schemas.openapi import AutoSchema

from .models import TodoList, Category

from rest_framework import viewsets, mixins
from .serializers import TodoSerializer, CategoriesSerializer
from .filters import TodolistFilterSet, CategoryFilterSet


# Классы представлений для модели Todolist
class AllTasksView(ListView):
    context_object_name = "tasks"
    queryset = TodoList.objects.all()
    template_name = "todolist/index.html"


class ActiveTasksView(ListView):
    context_object_name = "tasks"
    queryset = TodoList.objects.filter(is_completed=False)
    template_name = "todolist/active_tasks.html"


class CompletedTasksView(ListView):
    queryset = TodoList.objects.filter(is_completed=True)
    context_object_name = "tasks"
    template_name = "todolist/completed_tasks.html"


class TaskCreateView(CreateView):
    model = TodoList
    fields = ["name", "cat"]
    template_name = "todolist/task_create.html"
    success_url = "/"


class TaskUpdateView(UpdateView):
    model = TodoList
    fields = ["name", "is_completed", "cat"]
    template_name = "todolist/task_update_form.html"
    success_url = "/"


class TaskDeleteView(DeleteView):
    model = TodoList
    success_url = "/"
    template_name = "todolist/task_delete.html"
    context_object_name = "task"


# отображаем название категорий и какие в них задачи
def categories_show(request):
    categories = Category.objects.all()
    context = dict()
    for i in categories:
        context[i] = context.get(i, TodoList.objects.filter(cat_id=i.pk).all())
    return render(request, "todolist/categories.html", context={"context": context})


# классы представлений для модели Category
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]
    template_name = "todolist/category_create.html"
    success_url = "/categories"


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/categories"
    template_name = "todolist/category_delete.html"
    context_object_name = "cat"


# добавляем viewset drf для возможности работы по API
class TodolistViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer
    filterset_class = TodolistFilterSet

    # рисуем схему для API
    schema = AutoSchema(
        tags=["TodoList Tasks"],
        component_name="TodoList",
        operation_id_base="TodoList",
    )


class CategoriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filterset_class = CategoryFilterSet
