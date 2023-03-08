from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from rest_framework.schemas.openapi import AutoSchema

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, LoginUserForm, TaskCreateForm, TaskUpdateForm
from .models import TodoList, Category

from rest_framework import viewsets, mixins
from .serializers import TodoSerializer, CategoriesSerializer
from .filters import TodolistFilterSet, CategoryFilterSet


# Классы представлений для модели Todolist
class AllTasksView(ListView):
    context_object_name = "tasks"

    # queryset = TodoList.objects.all()
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TodoList.objects.filter(author=self.request.user)
        else:
            return TodoList.objects.all()

    template_name = "todolist/index.html"
    paginate_by = 3


class ActiveTasksView(ListView):
    context_object_name = "tasks"
    # queryset = TodoList.objects.filter(is_completed=False)
    template_name = "todolist/active_tasks.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TodoList.objects.filter(author=self.request.user).filter(is_completed=False)
        else:
            return TodoList.objects.all()


class CompletedTasksView(ListView):
    # queryset = TodoList.objects.filter(is_completed=True)
    context_object_name = "tasks"
    template_name = "todolist/completed_tasks.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TodoList.objects.filter(author=self.request.user).filter(is_completed=True)
        else:
            return TodoList.objects.all()


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    model = TodoList
    # fields = ["name", "cat"]
    template_name = "todolist/task_create.html"
    success_url = "/"
    login_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskUpdateView(UpdateView):
    model = TodoList
    # fields = ["name", "is_completed", "cat"]
    form_class = TaskUpdateForm

    template_name = "todolist/task_update_form.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(DeleteView):
    model = TodoList
    success_url = "/"
    template_name = "todolist/task_delete.html"
    context_object_name = "task"


# отображаем название категорий и какие в них задачи
def categories_show(request):
    # categories = Category.objects.all()
    if request.user.is_authenticated:
        categories = Category.objects.filter(author=request.user)
    else:
        categories = Category.objects.all()
    paginator = Paginator(categories, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = dict()
    for i in page_obj:
        context[i] = context.get(i, TodoList.objects.filter(cat_id=i.pk).all())
    return render(request, "todolist/categories.html", context={"page_obj": page_obj, "context": context})


# классы представлений для модели Category
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]
    template_name = "todolist/category_create.html"
    success_url = "/categories"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


# Добавляем регистрацию и авторизацию
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "todolist/register.html"
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Category(name='разное', author=self.request.user).save()
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'todolist/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')
