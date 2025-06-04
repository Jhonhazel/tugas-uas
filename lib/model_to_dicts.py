from enum import Enum
def model_to_dict(obj):
    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)

        # Handle Enum types
        if isinstance(value, Enum):
            value = value.value

        # Handle datetime if needed
        if hasattr(value, "isoformat"):
            value = value.isoformat()

        result[column.name] = value
    return result
