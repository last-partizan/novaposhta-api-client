from datetime import date, datetime


DATE_FORMAT = "%d.%m.%Y"


def encoder(obj, default=str):
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT)
    return default(obj)

parse_date = lambda v: datetime.strptime(v).date()
