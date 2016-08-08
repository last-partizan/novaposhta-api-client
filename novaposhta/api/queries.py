# coding: utf-8
from __future__ import unicode_literals
import logging

try:
    from urllib2 import Request, urlopen
except ImportError:
    #  python3
    from urllib.request import Request, urlopen

from .. import serializer
from ..conf import API_SETTINGS
from .exceptions import ApiError, AuthError

logger = logging.getLogger(__name__)


def send(cls, method, method_props=None, test_url=None):
    """
    Primary function for API requests and data fetching.
    It uses `urllib2` and `json` libs for requests to API through `HTTP` protocol.
    Modifies API template and then makes request to API endpoint.

    :param method:
        name of the API method, should be passed for every request
    :type method:
        str or unicode
    :param method_props:
        additional params for API methods.
    :type method_props:
        dict
    :return:
        dictionary with fetched info
    :rtype:
        dict
    """
    query = {
        'modelName': cls.__name__,
        'calledMethod': method,
        'methodProperties': _clean_properties(method_props or {}),
        'apiKey': API_SETTINGS['api_key']
    }

    url = _get_api_url(cls, method, test_url or cls.test_url)
    data = serializer.dumps(query, indent=2, ensure_ascii=False)
    logger.debug("send: %s\n%s", url, data)
    req = Request(url, serializer.dumps(query).encode('utf-8'))
    resp_raw = urlopen(req).read().decode('utf-8')
    resp = serializer.loads(resp_raw)
    logger.debug("received:\n%s", serializer.dumps(resp, indent=2, ensure_ascii=False))
    if resp["warnings"]:
        logger.warning(
            "Api returned warning list:\n%s",
            [" * %s" % s for s in resp["warnings"]]
        )
    if not resp["success"]:
        if resp["errorCodes"] == ['20000200068']:
            errcls = AuthError
        else:
            errcls = ApiError
        raise errcls(resp["errorCodes"], resp["errors"])
    if isinstance(resp["data"], dict):
        return cls(**resp["data"])
    else:
        return [cls(**attrs) for attrs in resp["data"]]


def _clean_properties(method_properties):
    return dict((k, v) for k, v in method_properties.items() if v)


def _get_api_url(cls, method, test_url):
    endpoint = API_SETTINGS['api_point']
    if 'testapi' in endpoint:
        return endpoint + test_url.format(
            cls=cls.__name__,
            method=method,
            format='json',
        )
    return endpoint


