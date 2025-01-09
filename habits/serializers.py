from rest_framework import serializers, validators

from .models import Habit
from .validators import validate_award_and_related_habit, validate_execution_time, validate_related_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычеч"""

    execution_time = serializers.IntegerField(default=0, validators=[validate_execution_time])

    # Подключаем валидатор
    def validate(self, attrs):
        # Проверяем связанную привычку
        validate_related_habit(attrs, field_name='related_habit')

        # Проверяем, что награда и связанная привычка не указаны одновременно
        validate_award_and_related_habit(attrs, fields=['related_habit', 'award'])
        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
