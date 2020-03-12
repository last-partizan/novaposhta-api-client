from datetime import date, datetime

DATE_FORMAT_DOT = "%d.%m.%Y"
DATETIME_FORMAT_DOT = "%d.%m.%Y %H:%M:%S"

DATE_FORMAT_DASH = "%d-%m-%Y"
DATETIME_FORMAT_DASH = "%d-%m-%Y %H:%M:%S"

ALL_FORMATS = [
    DATETIME_FORMAT_DASH,
    DATETIME_FORMAT_DOT,
    DATE_FORMAT_DOT,
    DATE_FORMAT_DASH,
]


def encoder(obj, default=str):
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT_DOT)
    return default(obj)


parse_date_dot = lambda v: datetime.strptime(v, DATE_FORMAT_DOT).date() if v else None
parse_datetime_dot = lambda v: datetime.strptime(v, DATETIME_FORMAT_DOT) if v else None

parse_date = lambda v: datetime.strptime(v, DATE_FORMAT_DASH).date() if v else None
parse_datetime = lambda v: datetime.strptime(v, DATETIME_FORMAT_DASH) if v else None


def parse_datetime_universal(v):
    if not v:
        return None
    for fmt in ALL_FORMATS:
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
