from datetime import datetime

def normalize_text(text):

    if not isinstance(text, str):
        return text

    return " ".join(text.strip().split())

def validate_required_text(value, error_message):

    if not isinstance(value, str) or value.strip() == "":
        raise ValueError(error_message)

    return normalize_text(value)

def validate_optional_integer(value, error_message):

    if value is None:
        return

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(error_message)

def validate_optional_number(value, error_message):

    if value is None:
        return

    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError(error_message)

def validate_date(value, error_message):

    if not isinstance(value, str):
        raise ValueError(error_message)

    value = value.strip()

    try:
        datetime.strptime(
            value,
            "%Y-%m-%d"
        )
    except ValueError as exc:
        raise ValueError(error_message) from exc

    return value

def validate_time(value, error_message):

    if not isinstance(value, str):
        raise ValueError(error_message)

    value = value.strip()

    try:
        parse_time(value)
    except ValueError as exc:
        raise ValueError(error_message) from exc

    return value

def parse_time(value):

    return datetime.strptime(
        value,
        "%H:%M"
    )
