import json
from time import sleep
import requests
from requests.exceptions import Timeout

import config


request_delay = 0
call_url = lambda x: str(config.service_url) + x
timeout = 10
auto_retry = True


class RequestError(BaseException):
    def __init__(self, code):
        super(RequestError, self).__init__(code)
        self.code = code


def call(path, request):
    try:
        response = requests.post(
            call_url(path),
            params={"auth": config.auth_token},
            data=json.dumps(request),
            timeout=10
        )
        if request_delay:
            sleep(request_delay)
        if response.status_code != 200:
            raise RequestError(response.status_code)
        return response.json()
    except Exception as e:
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
