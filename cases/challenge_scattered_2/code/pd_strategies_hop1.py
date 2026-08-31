import math
def execute(base_log_odds, shift):
    return 1.0 / (1.0 + math.exp(-(base_log_odds + shift)))
