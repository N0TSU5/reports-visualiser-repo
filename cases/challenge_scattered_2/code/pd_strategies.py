import pd_strategies_hop1
class PDStrategyFactory:
    @staticmethod
    def get_strategy(name):
        return BaselinePDStrategy()
class BaselinePDStrategy:
    def calculate(self, base_log_odds, shift):
        return pd_strategies_hop1.execute(base_log_odds, shift)
