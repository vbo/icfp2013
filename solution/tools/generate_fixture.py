import json

from ..lang import Int64
from .. import api


api.request_delay = 5


def generate_inputs():
    for a in range(256):
        r = Int64.random()
        rstr = str(hex(r)).rstrip("L")
        yield rstr

while True:
    train = api.train()
    inputs = list(generate_inputs())
    evaled = api.eval(train["id"], None, inputs)
    evaled["request"] = train
    evaled["request"]["input"] = inputs

    with open("/tmp/solver_fixture.jsons", "a") as fixture:
        fixture.write(json.dumps(evaled) + "\n")

