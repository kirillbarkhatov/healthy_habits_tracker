from rest_framework import serializers, validators

from .models import Habit
from .validators import validate_award_and_related_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычеч"""

    # Подключаем валидатор
    def validate(self, attrs):
        validate_award_and_related_habit(attrs, fields=['related_habit', 'award'])
        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
