# Purpur Tentakel
# 09.01.2022
# KickerRechner // Game

from logic.team import Team


class Game:
    def __init__(self, game_name: str, team_1: Team, team_2: Team, game_day: int, first_round: bool):
        self.game_name: str = game_name
        self.team_1: Team = team_1
        self.team_2: Team = team_2
        self.game_day: int = game_day
        self.first_round: bool = first_round

        self.score_team_1: int = int()
        self.score_team_2: int = int()
        self.finished: bool = False
