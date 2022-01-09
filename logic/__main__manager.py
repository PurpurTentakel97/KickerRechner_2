# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__

from logic.league import League
from gui import input_window


class LeagueManager:
    def __init__(self, initial_input: tuple):
        self.all_leagues: list[League] = list()
        self.active_leagues: list[League] = list()
        self._create_leagues(input_=initial_input)

    def _create_leagues(self, input_: tuple):
        for league_name, teams_names, is_second_round, is_active in input_:
            league = League(league_name, teams_names, is_second_round, is_active)
            self.all_leagues.append(league)
            if is_active:
                self.active_leagues.append(league)


if __name__ == "__main__":
    input_window.create_input_window()

league_manager = LeagueManager


def precess_data_from_input_window(user_input: tuple):
    global league_manager
    league_manager = LeagueManager(initial_input=user_input)
