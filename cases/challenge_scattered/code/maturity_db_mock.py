import maturity_db_mock_hop1
class MaturityRepository:
    @staticmethod
    def get_capped_horizon(orig, cap):
        return maturity_db_mock_hop1.execute(orig, cap)
