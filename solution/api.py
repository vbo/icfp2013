import json
import requests
import config


class RequestError(BaseException):
    pass


def call(path, request):
    response = requests.post(
        str(config.service_url) + path,
        params={"auth": config.auth_token},
        data=json.dumps(request)
    )
    if response.status_code != 200:
        raise RequestError(response.status_code)
    return response.json()


def train(size=None, operators=None):
    result = call("train", {"size": size, "operators": operators})
    return result
