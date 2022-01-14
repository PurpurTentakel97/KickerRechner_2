# Purpur Tentakel
# 09.01.2022
# KickerRechner // enum

from enum import Enum


class StartCheck(Enum):
    START = 0
    CHECK = 1


class TableType(Enum):
    FIRST = 0
    SECOND = 1
    TOTAL = 2


class ListType(Enum):
    LEAGUE = 0
    DAY = 1
    GAME = 2
