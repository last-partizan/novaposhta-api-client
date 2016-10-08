from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"
DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"


def encoder(obj, default=str):
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT)
    return default(obj)


parse_date = lambda v: datetime.strptime(v, DATE_FORMAT).date()
parse_datetime = lambda v: datetime.strptime(v, DATETIME_FORMAT)
