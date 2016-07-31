from os import environ

_not_configured_msg = """
novaposhta-api-client settings must be defined in settings,
example,
NOVAPOSHTA_API_SETTINGS = {
    'api_key': '12345', # your api key, required
    'api_point': 'https://api.novaposhta.ua/v2.0/json/', # default, not required
}
"""
DEFAULT_API_ENDPOINT = 'https://api.novaposhta.ua/v2.0/json/'
API_SETTINGS = {
    'api_key': environ.get('NOVAPOSHTA_API_KEY', ''),
    'api_point': environ.get('NOVAPOSHTA_API_POINT', DEFAULT_API_ENDPOINT)
}

if "DJANGO_SETTINGS_MODULE" in environ:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    try:
        API_SETTINGS.update(settings.NOVAPOSHTA_API_SETTINGS)
    except AttributeError:
        raise ImproperlyConfigured(_not_configured_msg)
