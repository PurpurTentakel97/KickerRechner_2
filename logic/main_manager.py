# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__

from logic.league import League
from gui import input_window


class LeagueManager:
    def __init__(self):
        self.all_leagues: list[League] = list()
        self.active_leagues: list[League] = list()

    def create_leagues(self, initial_input: tuple):
        for league_name, is_second_round, is_active, teams_names in initial_input:
            league = League(name=league_name, is_second_round=is_second_round, is_active=is_active,
                            team_names=teams_names)
            self.all_leagues.append(league)
            if is_active:
                self.active_leagues.append(league)

    def get_output(self) -> tuple:
        output: list[list[str, bool, list[str, str, str, int, bool, int, int, bool],
                          list[list[str, str, str, int, bool, int, int, bool]], list[list], list[list], list[
                              list]]] = list()
        for league in self.all_leagues:
            output.append(league.get_output())
        return tuple(output)


league_manager = LeagueManager


def _create_league_manager():
    global league_manager
    league_manager = LeagueManager()


if __name__ == "__main__":
    _create_league_manager()
    input_window.create_input_window()


def process_data_from_input_window(initial_input: tuple):
    print(initial_input)
    league_manager.create_leagues(self=LeagueManager(), initial_input=initial_input)
    _put_data_to_main_window()


def _put_data_to_main_window():
    league_manager.get_output(self=LeagueManager())
