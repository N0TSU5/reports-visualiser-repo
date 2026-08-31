
class MaturityRepository:
    @staticmethod
    def get_capped_horizon(orig, cap):
        return min(orig, cap)
