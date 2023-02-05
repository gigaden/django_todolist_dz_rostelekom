import datetime

from django.db import models


# создаём модель таблицы в нашей БД
class TodoList(models.Model):
    name = models.CharField(max_length=140, help_text="описание задачи")
    time_begin = models.DateTimeField(
        auto_now_add=True, help_text="время создания задачи"
    )
    time_end = models.DateTimeField(
        auto_now=False,
        default=False,
        help_text="время завершения задачи",
        blank=True,
        null=True,
    )
    is_completed = models.BooleanField(default=False, help_text="выполнена ли задача")

    def save(self, *args, **kwargs):
        if self.is_completed:
            if self.time_end == None:
                self.time_end = datetime.datetime.now()
        else:
            self.time_end = None
        return super().save(*args, **kwargs)
