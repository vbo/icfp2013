import json

from ..lang.int64 import generate_inputs
from .. import api


api.request_delay = 5

while True:
    train = api.train()
    inputs = list(generate_inputs())
    evaled = api.eval(inputs, train["id"], None)
    evaled["request"] = train
    evaled["request"]["input"] = inputs

    with open("/tmp/solver_fixture.jsons", "a") as fixture:
        fixture.write(json.dumps(evaled) + "\n")

