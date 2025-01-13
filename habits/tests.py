from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User

class HabitTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом

        self.user = User.objects.create(
            email="test1@test1.ru",
        )

        self.habit = Habit.objects.create(
            time=time(12, 0),
            action="Полезная привычка",
            user=self.user
        )

        self.client.force_authenticate(user=self.user)


    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "execution_time": 0,
                    "periodicity": 1,
                    "location": "Где угодно",
                    "time": "12:00:00",
                    "action": "Полезная привычка",
                    "is_pleasant_habit": False,
                    "award": None,
                    "is_public": False,
                    "user": self.user.pk,
                    "related_habit": None
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
