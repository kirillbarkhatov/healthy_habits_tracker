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
