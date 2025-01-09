from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner
from .models import Habit
from .paginators import FiveItemsPaginator
from .serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Получение одной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitListAPIView(generics.ListAPIView):
    """Получение списка привычек"""

    serializer_class = HabitSerializer
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Получение списка публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        return Habit.objects.filter(is_public=True)
