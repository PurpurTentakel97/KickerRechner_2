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

    def get_result_string_from_team_view(self, team: Team) -> str:
        if not self.finished:
            return "- : -"
        elif team == self.team_1:
            return str(self.score_team_1) + " : " + str(self.score_team_2)
        elif team == self.team_2:
            return str(self.score_team_2) + " : " + str(self.score_team_1)
        else:
            print("Team not in Game")  # TODO to UI
