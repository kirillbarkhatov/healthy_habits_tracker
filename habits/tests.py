import datetime
import json
from datetime import time
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.tasks import send_habit_reminder
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом

        self.user = User.objects.create(
            email="test1@test1.ru",
        )

        self.habit = Habit.objects.create(
            time=time(12, 0), action="Полезная привычка", user=self.user
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
                    "related_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self):
        url = reverse("habits:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habit_create")

        data = {
            "time": "12:01:00",
            "action": "Приятная привычка",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habits:habit_create")

        data = {
            "time": "12:01:00",
            "action": "Приятная привычка",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        self.client.post(url, data)

        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"related_habit": Habit.objects.get(action="Приятная привычка").pk}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("related_habit"), Habit.objects.get(action="Приятная привычка").pk
        )

    def test_lesson_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)


@patch("habits.tasks.send_telegram_message")
def test_send_habit_reminder_with_mock(self, mock_send_message):
    send_habit_reminder(self.habit.pk)

    # Проверяем, что send_telegram_message вызван
    mock_send_message.assert_called_once_with(
        "123456789",
        "Напоминание: Прогулка в Парк в 10:00.\nНе забудьте про награду: Мороженое!",
    )


class SendHabitReminderTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", tg_chat_id="123456789")

        self.habit = Habit.objects.create(
            user=self.user,
            action="Прогулка",
            location="Парк",
            time=datetime.time(10, 0),
            award="Мороженое",
            periodicity=1,
        )

    def test_send_habit_reminder(self):
        # Выполняем задачу
        send_habit_reminder(self.habit.pk)

        # Проверяем, что сообщение было отправлено (можно замокать send_telegram_message)
        # В реальных тестах вы можете использовать mock для проверки вызова функции.
        # Для примера проверим создание следующей задачи:

        next_execution = datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=self.habit.periodicity),
            self.habit.time,
        )

        clocked_schedule = ClockedSchedule.objects.filter(
            clocked_time=next_execution
        ).first()
        self.assertIsNotNone(clocked_schedule)

        periodic_task = PeriodicTask.objects.filter(
            clocked=clocked_schedule,
            task="habits.tasks.send_habit_reminder",
            args=json.dumps([self.habit.pk]),
            one_off=True,
        ).first()

        self.assertIsNotNone(periodic_task)
        self.assertEqual(
            periodic_task.name, f"Habit reminder for habit {self.habit.pk}"
        )

    def test_habit_does_not_exist(self):
        # Очистка всех объектов, если необходимо
        ClockedSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()
        # Тестируем случай, когда habit не существует
        send_habit_reminder(999)  # Несуществующий ID
        # Никакие задачи не должны быть созданы
        self.assertFalse(ClockedSchedule.objects.exists())
        self.assertFalse(PeriodicTask.objects.exists())
