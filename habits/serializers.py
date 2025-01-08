from rest_framework import serializers, validators

from .models import Habit
from .validators import validate_award_and_related_habit, validate_execution_time


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычеч"""

    execution_time = serializers.IntegerField(validators=[validate_execution_time])

    # Подключаем валидатор
    def validate(self, attrs):
        validate_award_and_related_habit(attrs, fields=['related_habit', 'award'])
        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
