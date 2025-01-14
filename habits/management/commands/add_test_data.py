from django.core.management import call_command
from django.core.management.base import BaseCommand

from habits.models import Habit
from users.models import User


class Command(BaseCommand):
    help = "Добавление данных из фикстур"

    def handle(self, *args, **kwargs):

        # Удаляем существующие записи
        Habit.objects.all().delete()
        User.objects.all().delete()

        # создание фикстур - команды для терминала
        # python -Xutf8 manage.py dumpdata users.User --output user_fixture.json --indent 4
        # python -Xutf8 manage.py dumpdata habits.Habit --output habit_fixture.json --indent 4

        # Добавляем данные из фикстур
        call_command("loaddata", "user_fixture.json", format="json")
        self.stdout.write(
            self.style.SUCCESS("Пользователи загружены из фикстур успешно")
        )
        call_command("loaddata", "habit_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Привычки загружены из фикстур успешно"))

        # Обновление паролей и их хешей
        for user in User.objects.all():
            user.set_password("123qwe456rty")
            user.save()
