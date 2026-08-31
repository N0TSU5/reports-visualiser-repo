import math
class PDStrategyFactory:
    @staticmethod
    def get_strategy(name):
        return BaselinePDStrategy()
class BaselinePDStrategy:
    def calculate(self, base_log_odds, shift):
        return 1.0 / (1.0 + math.exp(-(base_log_odds + shift)))
