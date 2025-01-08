from django.urls import path

from .apps import HabitsConfig
from . import views


app_name = HabitsConfig.name


urlpatterns = [
    path("habit/", views.HabitListAPIView.as_view(), name="habit_list"),
    path("habit/<int:pk>", views.HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("habit/create", views.HabitCreateAPIView.as_view(), name="habit_create"),
    path("habit/<int:pk>/update", views.HabitUpdateAPIView.as_view(), name="habit_update"),
    path(
        "habit/<int:pk>/delete", views.HabitDestroyAPIView.as_view(), name="habit_delete"
    ),
]