def execute(payload):
    return payload['bal'] + (payload['ccf'] * payload['undrawn'])
