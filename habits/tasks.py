import json
from celery import shared_task
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone  # Используем timezone для работы с временем

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания и создание следующей задачи"""
    try:
        habit = Habit.objects.get(pk=habit_id)

        # Отправка сообщения в Telegram
        if habit.user and habit.user.tg_chat_id:
            message = (
                f"Напоминание: {habit.action} в {habit.location} в {habit.time.strftime('%H:%M')}.\n"
                f"Не забудьте про награду: {habit.award}!"
            )
            send_telegram_message(habit.user.tg_chat_id, message)

        # Создание новой задачи на следующий день с учетом периодичности
        now = timezone.now()  # Получаем текущее время с учетом часового пояса
        next_execution = timezone.datetime.combine(
            now.date() + timezone.timedelta(days=habit.periodicity), habit.time
        )

        # Преобразуем next_execution в осведомленное время, если оно наивное
        if timezone.is_naive(next_execution):
            next_execution = timezone.make_aware(next_execution)  # Преобразуем в осведомленное время

        # Если время уже прошло, планируем задачу на следующий день
        if next_execution < now:
            next_execution += timezone.timedelta(days=habit.periodicity)

        # # Преобразуем next_execution в осведомленное время, если оно наивное
        # if timezone.is_naive(next_execution):
        #     next_execution = timezone.make_aware(next_execution)  # Преобразуем в осведомленное время

        # Создание или нахождение расписания
        clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=next_execution)

        # Создание задачи с расписанием
        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f"Habit reminder for habit {habit.pk} - {next_execution}",
            task="habits.tasks.send_habit_reminder",
            args=json.dumps([habit.pk]),
            one_off=True,  # Указываем, что задача выполняется один раз
        )

    except Habit.DoesNotExist:
        pass



# import datetime
# import json
#
# from celery import shared_task
# from django_celery_beat.models import ClockedSchedule, PeriodicTask
#
# from .models import Habit
# from .services import send_telegram_message
#
#
# @shared_task
# def send_habit_reminder(habit_id):
#     """Отправка напоминания и создание следующей задачи"""
#     try:
#         habit = Habit.objects.get(pk=habit_id)
#
#         # Отправка сообщения в Telegram
#         if habit.user and habit.user.tg_chat_id:
#             message = (
#                 f"Напоминание: {habit.action} в {habit.location} в {habit.time.strftime('%H:%M')}.\n"
#                 f"Не забудьте про награду: {habit.award}!"
#             )
#             send_telegram_message(habit.user.tg_chat_id, message)
#
#         # Создание новой задачи на следующий день с учетом периодичности
#         next_execution = datetime.datetime.combine(
#             datetime.date.today() + datetime.timedelta(days=habit.periodicity),
#             habit.time,
#         )
#
#         clocked_schedule, _ = ClockedSchedule.objects.get_or_create(
#             clocked_time=next_execution
#         )
#
#         PeriodicTask.objects.create(
#             clocked=clocked_schedule,
#             name=f"Habit reminder for habit {habit.pk} - {next_execution}",
#             task="habits.tasks.send_habit_reminder",
#             args=json.dumps([habit.pk]),
#             one_off=True,
#         )
#
#     except Habit.DoesNotExist:
#         pass
