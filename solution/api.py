import json
import time
import requests
from requests.exceptions import Timeout

import config


request_delay = 0
default_call_url = call_url = lambda x: str(config.service_url) + x
default_timeout = timeout = 10
default_auto_retry = auto_retry = True
last_api_request_time = 0


class RequestError(BaseException):
    def __init__(self, code):
        super(RequestError, self).__init__(code)
        self.code = code


class AlreadySolvedException(BaseException):
    pass


def call(path, request):
    global last_api_request_time

    elapsed_since_last_call = time.time() - last_api_request_time
    if elapsed_since_last_call < request_delay:
        time.sleep(request_delay - elapsed_since_last_call)

    try:
        # TODO: consider getting last api time AFTER the call (need to do that
        # in exception handler if sleeping is desired for auto_retry
        last_api_request_time = time.time()
        response = requests.post(
            call_url(path),
            params={"auth": config.auth_token},
            data=json.dumps(request),
            timeout=10
        )

        if response.status_code == 412:
            raise AlreadySolvedException()
        if response.status_code != 200:
            raise RequestError(response.status_code)
        return response.json()
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt) or isinstance(e, AlreadySolvedException):
            raise
        if not auto_retry:
            raise
        print "auto-retrying request call(%s, %s). Exception was %s" % (path, request, e)
        return call(path, request)


def train(size=None, operators=None):
    result = call("train", {"size": size, "operators": operators})
    return result


def eval(arguments, id=None, program=None):
    params = {
        "arguments": map(str, arguments)
    }
    if id:
        params['id'] = id
    else:
        params['program'] = program
    result = call("eval", params)
    return result

def guess(id, program):
    result = call("guess", {"id": id, "program": program})
    return result
