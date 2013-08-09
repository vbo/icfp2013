import json
from time import sleep
import requests

import config


request_delay = 0


class RequestError(BaseException):
    def __init__(self, code):
        super(RequestError, self).__init__(code)
        self.code = code


def call(path, request):
    response = requests.post(
        str(config.service_url) + path,
        params={"auth": config.auth_token},
        data=json.dumps(request)
    )
    if request_delay:
        sleep(request_delay)
    if response.status_code != 200:
        raise RequestError(response.status_code)
    return response.json()


def train(size=None, operators=None):
    result = call("train", {"size": size, "operators": operators})
    return result


def eval(id, program, arguments):
    result = call("eval", {"id": id, "program": program, "arguments": map(str, arguments)})
    return result

def guess(id, program):
    result = call("guess", {"id": id, "program": program})
    return result
