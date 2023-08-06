import math

# Utility
# threshold in game is 0.5
# _my_round_threshold_up(number=quantity, decimals=0, threshold=0.5) is
# used for determining if a Spaceship survives battle:
# quantity of Spaceship is 0.5 -> _my_round_threshold_up will return 1.0 ->
# -> the Spaceship will survive
# 0.49 -> 0.0 -> will not

# Why quantity is float? Why Spaceship doesn't have an actual HP? , etc.
# the Game works this way
#       ¯\_(ツ)_/¯

def _my_truncate(number, decimals: int, safe: bool = False) -> float:
    multiplier = 10 ** decimals
    result = int(number * multiplier) / multiplier
    if safe:
        if result == 0:
            result = 1 / multiplier
    return result

def _my_round_up(number) -> int:
    return math.ceil(number)

def _my_round_down(number) -> int:
    return math.floor(number)

def _my_round_threshold_up(number, decimals: int, threshold: float) -> float:
    multiplier = 10 ** decimals
    return math.floor(number * multiplier + threshold) / multiplier

def _my_round_threshold_down(number, decimals: int, threshold: float) -> float:
    multiplier = 10 ** decimals
    return math.ceil(number * multiplier - threshold) / multiplier
