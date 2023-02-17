import datetime
from django.contrib import admin
from .models import TodoList, Category


@admin.action(description="Завершить задачу")
def activate(modeladmin, request, queryset):
    for query in queryset:
        if not query.time_end:
            queryset.update(is_completed=True)
            queryset.update(time_end=datetime.datetime.now())


@admin.action(description="Сделать задачу не завершённой")
def deactivate(modeladmin, request, queryset):
    queryset.update(is_completed=False)
    queryset.update(time_end=None)


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "time_begin", "time_end", "is_completed")

    list_filter = ["time_begin", "is_completed", "time_end"]
    list_editable = ("is_completed",)
    search_fields = ["name"]
    actions = [deactivate, activate]


@admin.register(Category)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    list_filter = ["name"]
    search_fields = ["name"]
