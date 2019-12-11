from collections import OrderedDict


class ApiError(Exception):
    """
    Base class for api exceptions
    """

    def __init__(self, codes, errors):
        self.errors = OrderedDict(zip(ignore_empty(codes), errors))

    def __str__(self):
        return "\n".join(
            [" * %s: %s" % (k,v) for k,v in self.errors.items()]
        )


class AuthError(ApiError):
    message = 'API key is wrong, outdated or not provided'

    def __str__(self):
        return "%s (%s)" % ((self.message,) + tuple(self.errors.values()))


def ignore_empty(lst):
    for v in lst:
        yield v
    while True:
        yield "error"
