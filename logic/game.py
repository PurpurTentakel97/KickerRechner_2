# Purpur Tentakel
# 09.01.2022
# KickerRechner // Game

from logic.team import Team
from logic.enum_sheet import Result


class Game:
    def __init__(self, game_name: str, team_1: Team, team_2: Team, game_day: int, first_round: bool):
        self.game_name: str = game_name
        self.team_1: Team = team_1
        self.team_2: Team = team_2
        self.game_day: int = game_day
        self.first_round: bool = first_round

        self.score_team_1: int = int()
        self.score_team_2: int = int()
        self._team_1_result: Result | None = None
        self._team_2_result: Result | None = None
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

    def add_entry(self, result_input, team_1: Team):
        if team_1 == self.team_1:
            self.score_team_1: int = result_input.team_score_1
            self.score_team_2: int = result_input.team_score_2
        else:
            self.score_team_2: int = result_input.team_score_1
            self.score_team_1: int = result_input.team_score_2

        if self.score_team_1 > self.score_team_2:
            self._team_1_result: Result = Result.WIN
            self._team_2_result: Result = Result.LOOSE
        elif self.score_team_1 == self.score_team_2:
            self._team_1_result: Result = Result.DRAW
            self._team_2_result: Result = Result.DRAW
        else:
            self._team_1_result: Result = Result.LOOSE
            self._team_2_result: Result = Result.WIN

        self.finished: bool = True
        self._add_team_statistics()

    def _add_team_statistics(self):
        match self.first_round:
            case True:
                self.team_1.first_round_points += self._team_1_result
                self.team_2.first_round_points += self._team_2_result

                self.team_1.first_round_goals += self.score_team_1
                self.team_2.first_round_goals += self.score_team_2

                self.team_1.first_round_counter_goals += self.score_team_2
                self.team_2.first_round_counter_goals += self.score_team_1

                match self._team_1_result:
                    case Result.WIN:
                        self.team_1.first_round_wins += 1
                        self.team_2.first_round_loose += 1
                    case Result.DRAW:
                        self.team_1.first_round_draw += 1
                        self.team_2.first_round_draw += 1
                    case Result.LOOSE:
                        self.team_1.first_round_loose += 1
                        self.team_2.first_round_wins += 1

            case False:
                self.team_1.second_round_points += self._team_1_result
                self.team_2.second_round_points += self._team_2_result

                self.team_1.second_round_goals += self.score_team_1
                self.team_2.second_round_goals += self.score_team_2

                self.team_1.second_round_counter_goals += self.score_team_2
                self.team_2.second_round_counter_goals += self.score_team_1

                match self._team_1_result:
                    case Result.WIN:
                        self.team_1.second_round_wins += 1
                        self.team_2.second_round_loose += 1
                    case Result.DRAW:
                        self.team_1.second_round_draw += 1
                        self.team_2.second_round_draw += 1
                    case Result.LOOSE:
                        self.team_1.second_round_loose += 1
                        self.team_2.second_round_wins += 1

    def edit_entry(self):
        pass

    def _edit_team_statistics(self):
        pass
