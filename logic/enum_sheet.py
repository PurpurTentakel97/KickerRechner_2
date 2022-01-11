# Purpur Tentakel
# 10.01.2022
# KickerRechner // enum

from enum import Enum


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
