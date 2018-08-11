import logging
import json

import attr
import requests

from . import conf
from . import serializer
from .exceptions import ApiError, AuthError

logger = logging.getLogger(__name__)


@attr.s
class NovaPoshta(object):
    """
    A base API class, that holds shared methods and settings for other models.
    Creates basic query object and provide `apiKey` and API endpoint configuration.
    """
    _registered_models = {}

    api_key  = attr.ib(default=conf.API_KEY)
    endpoint = attr.ib(default=conf.API_ENDPOINT)
    timeout  = attr.ib(default=None)

    def __getattr__(self, key):
        if key[0].isupper():
            model = self._registered_models[key]
            model.api = self
            setattr(self, key, model)
            return model
        raise AttributeError

    @classmethod
    def model(cls, decorated_class):
        cls._registered_models[decorated_class.__name__] = decorated_class
        return decorated_class

    @property
    def session(self):
        if not hasattr(self, "_session"):
            self._session = requests.Session()
            self._session.headers.update({
                "Content-Type": "application/json",
            })
        return self._session

    def send(self, url, model_name, method, method_props=None):
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
            'modelName': model_name,
            'calledMethod': method,
            'methodProperties': _clean_properties(method_props or {}),
            'apiKey': self.api_key,
        }

        logger.debug("send: %s\n%s", url, _safe_query_for_logging(**query))
        resp = self.session.post(
            url,
            json.dumps(query, default=serializer.encoder),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        resp = resp.json()
        logger.debug("received:\n%s", _truncate(json.dumps(resp, indent=2, ensure_ascii=False)))

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
        return resp["data"]

    def build_url(self, cls, method, test_url):
        endpoint = self.endpoint
        if 'testapi' in endpoint:
            return endpoint + test_url.format(
                cls=cls.__name__,
                method=method,
                format='json',
            )
        return endpoint


def _safe_query_for_logging(**q):
    if q["apiKey"]:
        q["apiKey"] = "*" * len(q["apiKey"])
    return json.dumps(
        q, indent=2, ensure_ascii=False, default=serializer.encoder,
    )


def _truncate(string, length=500):
    if len(string) > length:
        return "%s..." % string[:length]
    return string


def _clean_properties(method_properties):
    return dict((k, v) for k, v in method_properties.items() if v)
