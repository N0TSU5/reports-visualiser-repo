import mock_ead_service_hop1
class MockEADClient:
    @staticmethod
    def post(endpoint, payload):
        if endpoint == '/api/v1/ead/calculate':
            return mock_ead_service_hop1.execute(payload)
