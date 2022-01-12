# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__
import gui.main_window
from logic.league import League, LeagueOutput
from gui import input_window
from gui import main_window

all_leagues: list[League] = list()
active_leagues: list[League] = list()

if __name__ == "__main__":
    input_window.create_input_window()


def process_data_from_input_window(initial_input: tuple):
    for league_name, is_active, second_round, teams_names in initial_input:
        league: League = League(name=league_name, is_active=is_active, is_second_round=second_round,
                                team_names=teams_names)
        all_leagues.append(league)
        if is_active:
            active_leagues.append(league)
    _put_data_to_main_window()


def _put_data_to_main_window():
    output: list[LeagueOutput] = list()
    for league in active_leagues:
        output.append(league.get_output())
    gui.main_window.create_main_window(initial_input=tuple(output))
