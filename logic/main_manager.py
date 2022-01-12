# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__

from logic.league import League
from gui import input_window

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
    output: list = list()
    for league in active_leagues:
        output.append(league.get_output())
        _print_league_output(league)


def _print_league_output(league):
    print("  |-------------------------------------------------------------------------------------------------|  ")
    print("  |                                         Neue Liga                                               |  ")
    print("  |-------------------------------------------------------------------------------------------------|  ")
    print("\n")
    print(league.get_output())
    print("  |-------------------------------------------------------------------------------------------------|  ")
    print(league.get_output()[0])
    print("  |-------------------------------------------------------------------------------------------------|  ")
    print(league.get_output()[1])
    print("  |-------------------------------------------------------------------------------------------------|  ")
    print(league.get_output()[2])
    print("  |-------------------------------------------------------------------------------------------------|  ")
    for line in league.get_output()[3]:
        print(line)
    print("  |-------------------------------------------------------------------------------------------------|  ")
    for line in league.get_output()[4]:
        print(line)
    print("  |-------------------------------------------------------------------------------------------------|  ")
    for line in league.get_output()[5]:
        print(line)
    print("  |-------------------------------------------------------------------------------------------------|  ")
    for line in league.get_output()[6]:
        print(line)
    print("\n\n")
