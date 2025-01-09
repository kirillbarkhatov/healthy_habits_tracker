from rest_framework import serializers


def validate_award_and_related_habit(attrs, fields):
    """Валидатор, исключающий одновременный выбор связанной привычки и указания вознаграждения
    Проверяет, что заполнено только одно из указанных полей или ни одно из них.

    :param attrs: словарь с данными
    :param fields: список полей для проверки
    :raises ValidationError: если более одного поля заполнено
    """
    # Считаем количество заполненных полей
    filled_fields = [field for field in fields if attrs.get(field) not in (None, '')]

    if len(filled_fields) > 1:
        raise serializers.ValidationError(
            f"Можно заполнить только одно из полей: {', '.join(fields)}."
        )


def validate_execution_time(value):
    """Валидатор времени выполнения"""

    if value not in range(121):
        raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")


def validate_related_habit(attrs, field_name='related_habit'):
    """Валидатор - в связанные привычки могут попадать только привычки с признаком приятной привычки"""

    related_habit = attrs.get(field_name)
    if related_habit and not related_habit.is_pleasant_habit:
        raise serializers.ValidationError(
            {field_name: "Связанная привычка должна быть отмечена как приятная."}
        )


def validate_pleasant_habit(attrs):
    """Валидатор - у приятной привычки не может быть вознаграждения или связанной привычки"""

    is_pleasant_habit = attrs.get("is_pleasant_habit")
    related_habit = attrs.get("related_habit")
    award = attrs.get("award")
    if is_pleasant_habit and (related_habit or award):
        raise serializers.ValidationError(
            {"У приятной привычки не может быть вознаграждения или связанной привычки"}
        )

