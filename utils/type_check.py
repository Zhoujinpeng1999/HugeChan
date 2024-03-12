
def CheckValueType(value, value_type):
    if not isinstance(value, value_type):
        raise TypeError(f"Expected type {value_type}, got {type(value)}")

def CheckValueTypeWithList(value_type_pairs):
    for pair in value_type_pairs:
        CheckValueType(pair[0], pair[1])