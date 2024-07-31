from uuid import *
def dollar_string_to_float(s) -> float:
    try:
        return float(s.replace("$", "").replace(",", ""))
    except (AttributeError, ValueError):
        return None
    
def is_uuid(s) -> UUID:
    try:
        UUID(s)
        return True
    except ValueError:
        return False

def to_uuid(s) -> UUID:
    try:
        return UUID(s)
    except ValueError:
        return None