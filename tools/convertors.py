def to_utf8(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")

    if isinstance(value, str):
        return value

    raise ValueError("input value must be an instance of 'bytes' or 'str'")
