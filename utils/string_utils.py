


def get_signed_value(value, decimal_places, comma=False, prefix="", suffix=""):
    if value >= 0:
        return f"+ \\{prefix}{value:{',' if comma else ''}.{decimal_places}f}{suffix}"
    else:
        return f"- \\{prefix}{-value:{',' if comma else ''}.{decimal_places}f}{suffix}"

