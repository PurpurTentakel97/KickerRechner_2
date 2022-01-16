# Purpur Tentakel
# 10.01.2022
# KickerRechner // enum

from enum import Enum, IntEnum


class TableType(Enum):
    FIRST = 0
    SECOND = 1
    TOTAL = 2


class Stats(Enum):
    POINTS = 0
    GOAL_DIFF = 1
    GOALS = 2
    COUNTER_GOALS = 3
    BALANCE = 4


class Result(IntEnum):
    WIN = 3
    DRAW = 1
    LOOSE = 0
