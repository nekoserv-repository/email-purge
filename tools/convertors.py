
def to_utf8( input_string ):

  if isinstance(input_string, bytes):
    return input_string.decode("utf-8", "replace")

  if isinstance(input_string, str):
    return input_string

  raise ValueError("input_string must be an instance of 'bytes' or 'str'");
