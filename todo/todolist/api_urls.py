from rest_framework.routers import DefaultRouter
from todolist.views import TodolistViewSet, CategoriesViewSet

# подключаем роутер для адресов доступа к API

router = DefaultRouter()

app_name = "todolist"

router.register(
    prefix="tasks",
    viewset=TodolistViewSet,
    basename="tasks",
)

router.register(
    prefix="categories",
    viewset=CategoriesViewSet,
    basename="categories",
)

urlpatterns = router.urls
