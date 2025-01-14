import json
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone  # Используем timezone для работы с временем

from .models import Habit


@receiver(post_save, sender=Habit)
def schedule_habit_reminder(sender, instance, created, **kwargs):
    """Планирование задачи с учетом времени выполнения привычки"""
    task_name = f"Habit reminder for habit {instance.pk}"

    # Удаляем старую задачу, если она существует
    if not created:
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass

    # Рассчитываем время следующего выполнения
    now = timezone.now()  # Используем timezone.now(), чтобы получить осведомленное время
    habit_time = timezone.datetime.combine(now.date(), instance.time)

    # Преобразуем habit_time в осведомленное время, если оно наивное
    if timezone.is_naive(habit_time):
        habit_time = timezone.make_aware(habit_time)  # Преобразуем в осведомленное время

    # Если время уже прошло, планируем на следующий день
    if habit_time < now:
        habit_time += timezone.timedelta(days=instance.periodicity)

    # # Преобразуем habit_time в осведомленное время, если оно наивное
    # if timezone.is_naive(habit_time):
    #     habit_time = timezone.make_aware(habit_time)  # Преобразуем в осведомленное время

    # Создаем или находим расписание
    clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=habit_time)

    # Создаем задачу с расписанием
    PeriodicTask.objects.create(
        clocked=clocked_schedule,
        name=task_name,
        task="habits.tasks.send_habit_reminder",
        args=json.dumps([instance.pk]),
        one_off=True,  # Указываем, что задача выполняется один раз
    )


@receiver(post_delete, sender=Habit)
def delete_habit_reminders(sender, instance, **kwargs):
    """Удаление всех связанных задач при удалении привычки"""
    tasks = PeriodicTask.objects.filter(
        name__startswith=f"Habit reminder for habit {instance.pk}"
    )
    tasks.delete()



# import datetime
# import json
#
# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver
# from django_celery_beat.models import ClockedSchedule, PeriodicTask
#
# from .models import Habit
#
#
# @receiver(post_save, sender=Habit)
# def schedule_habit_reminder(sender, instance, created, **kwargs):
#     """Планирование задачи с учетом времени выполнения привычки"""
#     task_name = f"Habit reminder for habit {instance.pk}"
#
#     # Удаляем старую задачу, если она существует
#     if not created:
#         try:
#             task = PeriodicTask.objects.get(name=task_name)
#             task.delete()
#         except PeriodicTask.DoesNotExist:
#             pass
#
#     # Рассчитываем время следующего выполнения
#     now = datetime.datetime.now()
#     habit_time = datetime.datetime.combine(now.date(), instance.time)
#
#     # Если время уже прошло, планируем на следующий день
#     if habit_time < now:
#         habit_time += datetime.timedelta(days=instance.periodicity)
#
#     # Создаем или находим расписание
#     clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=habit_time)
#
#     # Создаем задачу с расписанием
#     PeriodicTask.objects.create(
#         clocked=clocked_schedule,
#         name=task_name,
#         task="habits.tasks.send_habit_reminder",
#         args=json.dumps([instance.pk]),
#         one_off=True,  # Указываем, что задача выполняется один раз
#     )
#
#
# @receiver(post_delete, sender=Habit)
# def delete_habit_reminders(sender, instance, **kwargs):
#     """Удаление всех связанных задач при удалении привычки"""
#     tasks = PeriodicTask.objects.filter(
#         name__startswith=f"Habit reminder for habit {instance.pk}"
#     )
#     tasks.delete()
