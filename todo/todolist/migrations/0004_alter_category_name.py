# Generated by Django 4.1.5 on 2023-02-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todolist", "0003_alter_todolist_cat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                db_index=True, max_length=140, verbose_name="Название категории"
            ),
        ),
    ]