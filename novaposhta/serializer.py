import json
from datetime import date, datetime


DATE_FORMAT = "%d.%m.%Y"


def dumps(obj):
    return json.dumps(obj, default=encoder)


def encoder(obj, default=str):
    if isinstance(obj, date):
        return obj.strftime(DATE_FORMAT)
    return default(obj)


loads = json.loads


parse_date = lambda v: datetime.strptime(v).date()
