


def clean_phone(phone: str) -> str:
    """Очищает номер телефона от нецифровых символов."""
    return ''.join(filter(str.isdigit, phone))


def is_valid_phone(phone: str) -> bool:
    """Проверяет, соответствует ли номер телефона требованиям."""
    cleaned = clean_phone(phone)
    return len(cleaned) == 11 and cleaned[0] in {'7', '8'}


async def format_phone_number(phone: str) -> str:
    """
    Асинхронно форматирует номер телефона в заданный формат.
    Вызывает ValueError при невалидном номере.
    """
    if not is_valid_phone(phone):
        raise ValueError("Номер телефона невалиден")

    cleaned = clean_phone(phone)

    # Заменяем ведущую 8 на 7
    if cleaned[0] == '8':
        cleaned = '7' + cleaned[1:]

    # Форматируем номер по шаблону
    return "+7 ({}) {}-{}-{}".format(
        cleaned[1:4],
        cleaned[4:7],
        cleaned[7:9],
        cleaned[9:]
    )