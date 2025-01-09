from rest_framework import serializers, validators

from .models import Habit
from .validators import validate_award_and_related_habit, validate_execution_time, validate_related_habit, \
    validate_pleasant_habit, validate_periodicity


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычеч"""

    execution_time = serializers.IntegerField(default=0, validators=[validate_execution_time])
    periodicity = serializers.IntegerField(default=1, validators=[validate_periodicity])

    # Подключаем валидатор
    def validate(self, attrs):

        # Проверяем, что награда и связанная привычка не указаны одновременно
        validate_award_and_related_habit(attrs, fields=['related_habit', 'award'])

        # Проверяем связанную привычку
        validate_related_habit(attrs, field_name='related_habit')

        # Проверяем приятную привычку
        validate_pleasant_habit(attrs)

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
