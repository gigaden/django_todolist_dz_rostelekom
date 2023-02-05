from django.urls import path
from .views import (
    ActiveTasksView,
    CompletedTasksView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    AllTasksView,
)

urlpatterns = [
    path("", AllTasksView.as_view(), name="index"),
    path("active_tasks/", ActiveTasksView.as_view(), name="active_tasks"),
    path("completed_tasks/", CompletedTasksView.as_view(), name="completed_tasks"),
    path("create_task/", TaskCreateView.as_view(), name="task_create"),
    path("update_task/<int:pk>", TaskUpdateView.as_view(), name="task_update"),
    path("delete_task/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),
]
