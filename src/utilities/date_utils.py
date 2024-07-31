from datetime import datetime
from dateutil import parser

def from_string(str_date):
    if str_date is None:
        return None
    str_date = str(str_date).strip()
    try:
        return parser.parse(str_date)
    except (AttributeError, ValueError):
        raise ValueError("Invalid date format: " + str_date)
        formats = [
            "%b. %d, %Y", 
            "%b %d, %Y"
        ]
        for format in formats:
            try:
                return datetime.strptime(str_date, format)
            except (AttributeError, ValueError):
                return None
        return None