from rest_framework import generics

from .models import Habit
from .serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitSerializer


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Получение одной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitListAPIView(generics.ListAPIView):
    """Получение списка привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
