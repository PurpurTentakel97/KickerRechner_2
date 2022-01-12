# Purpur Tentakel
# 09.01.2022
# KickerRechner // enum

from enum import Enum


class StartCheck(Enum):
    START = 0
    CHECK = 1


# [league_name:str, second_round:bool,[game_name:str, team_1_name:str, team_2_name:str, game_day:int,
# first_round:bool, score_team_1:int, score_team_2:int, finished:bool], [[game_name:str, team_1_name:str,
# team_2_name:str, game_day:int, first_round:bool, score_team_1:int, score_team_2:int, finished:bool][next
# game]], [first_round_table:list],[second_round_table:list][total_table]]

class InputItem(Enum):
    NAME = 0
    SECOND_SOUND = 1
    NEXT_GAME = 2
    ALL_GAMES = 3
    FIRST_ROUND_TABLE = 4
    SECOND_ROUND_TABLE = 5
    TOTAL_TABLE = 6


