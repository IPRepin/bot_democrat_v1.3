def normalize_time(hour: int, minute: int) -> tuple[int, int]:
    """
    Нормализует часы и минуты, обрабатывая переполнение
    """
    # Если минуты больше 59, переносим излишек в часы
    if minute >= 60:
        extra_hours = minute // 60
        minute = minute % 60
        hour += extra_hours

    # Если часы больше 23, берем остаток от деления на 24
    if hour >= 24:
        hour = hour % 24

    return hour, minute


def parse_time(time_str: str) -> tuple[int, int]:
    """
    Парсит строку времени в часы и минуты
    """
    # Очищаем строку
    time_str = str(time_str).strip()

    # Если есть запятая, берем первое время
    if ',' in time_str:
        time_str = time_str.split(',')[0].strip()

    # Очищаем от всех символов кроме цифр и двоеточия
    time_str = ''.join(char for char in time_str if char.isdigit() or char == ':')

    try:
        if ':' in time_str:
            # Формат "15:00"
            time_parts = time_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        else:
            # Обработка числового формата
            if len(time_str) <= 2:
                # Если только часы (например "9" или "15")
                hour = int(time_str)
                minute = 0
            elif len(time_str) <= 4:
                # Формат "1930" или "930"
                time_str = time_str.zfill(4)
                hour = int(time_str[:2])
                minute = int(time_str[2:])
            else:
                # Если строка слишком длинная, пробуем интерпретировать первые 4 цифры
                hour = int(time_str[:2])
                minute = int(time_str[2:4])

        # Пытаемся нормализовать время
        hour, minute = normalize_time(hour, minute)

        # Финальная проверка на валидность
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError(f"Недопустимое значение времени после нормализации: {hour}:{minute}")

        return hour, minute

    except (ValueError, IndexError) as e:
        raise ValueError(f"Не удалось распарсить время '{time_str}': {str(e)}")
