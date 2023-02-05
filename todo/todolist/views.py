from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import TodoList


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
    fields = ["name"]
    template_name = "todolist/task_create.html"
    success_url = "/"


class TaskUpdateView(UpdateView):
    model = TodoList
    fields = ["name", "is_completed"]
    template_name = "todolist/task_update_form.html"
    success_url = "/"


class TaskDeleteView(DeleteView):
    model = TodoList
    success_url = "/"
    template_name = "todolist/task_delete.html"
    context_object_name = "task"
