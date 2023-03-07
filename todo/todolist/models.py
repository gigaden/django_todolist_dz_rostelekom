import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# создаём модель таблицы в нашей БД
class TodoList(models.Model):
    name = models.CharField(max_length=140, verbose_name="описание задачи")
    time_begin = models.DateTimeField(
        auto_now_add=True, verbose_name="время создания задачи"
    )
    time_end = models.DateTimeField(
        auto_now=False,
        default=False,
        verbose_name="время завершения задачи",
        blank=True,
        null=True,
    )
    is_completed = models.BooleanField(
        default=False, verbose_name="выполнена ли задача"
    )
    cat = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория", blank=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, verbose_name="Автор задачи", null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.is_completed:
            if self.time_end == None:
                self.time_end = datetime.datetime.now()
        else:
            self.time_end = None
        return super().save(*args, **kwargs)




class Category(models.Model):
    name = models.CharField(
        max_length=140, db_index=True, verbose_name="Название категории"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, verbose_name="Автор категории", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]
