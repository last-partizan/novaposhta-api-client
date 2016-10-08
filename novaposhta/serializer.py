from datetime import date, datetime

DATE_FORMAT_DOT = "%d.%m.%Y"

DATE_FORMAT_DASH = "%d-%m-%Y"
DATETIME_FORMAT_DASH = "%d-%m-%Y %H:%M:%S"


def encoder(obj, default=str):
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT_DOT)
    return default(obj)

parse_date_dot = lambda v: datetime.strptime(v, DATE_FORMAT_DOT).date()

parse_date = lambda v: datetime.strptime(v, DATE_FORMAT_DASH).date()
parse_datetime = lambda v: datetime.strptime(v, DATETIME_FORMAT_DASH)
