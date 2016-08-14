from os import environ

API_ENDPOINT = environ.get('NOVAPOSHTA_API_POINT', 'https://api.novaposhta.ua/v2.0/json/')
API_KEY      = environ.get('NOVAPOSHTA_API_KEY', '')


if "DJANGO_SETTINGS_MODULE" in environ:
    from django.conf import settings
    try:
        API_KEY = settings.NOVAPOSHTA_API_SETTINGS["api_key"]
    except (AttributeError, KeyError):
        pass

    try:
        API_ENDPOINT = settings.NOVAPOSHTA_API_SETTINGS["api_endpoint"]
    except (AttributeError, KeyError):
        pass
