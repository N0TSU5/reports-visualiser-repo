
class MockEADClient:
    @staticmethod
    def post(endpoint, payload):
        if endpoint == '/api/v1/ead/calculate':
            return payload['bal'] + (payload['ccf'] * payload['undrawn'])
