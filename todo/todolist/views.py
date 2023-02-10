from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from .models import TodoList, Category


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


def categories_show(request):
    categories = Category.objects.all()
    context = dict()
    for i in categories:
        context[i] = context.get(i, TodoList.objects.filter(cat_id=i.pk).all())
    return render(request, 'todolist/categories.html', context={'context': context})


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


'''class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'todolist/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))'''