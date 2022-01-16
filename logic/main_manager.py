# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__
import transition
from logic.league import League, LeagueOutput

all_leagues: list[League] = list()
active_leagues: list[League] = list()

if __name__ == "__main__":
    transition.create_input_window()


def process_data_from_input_window(initial_input: tuple[list[str, bool, bool, list[str]]]):
    for league_name, is_active, second_round, teams_names in initial_input:
        league: League = League(name=league_name, is_active=is_active, is_second_round=second_round,
                                team_names=teams_names)
        all_leagues.append(league)
        if is_active:
            active_leagues.append(league)
    _put_data_to_main_window()


def process_data_from_main_window(input_) -> None:
    league: League = _get_league_from_name(input_.league_name)
    league.add_edit_entry(result_input=input_)
    _update_data_in_main_window()


def _put_data_to_main_window() -> None:
    output: list[LeagueOutput] = list()
    for league in active_leagues:
        output.append(league.get_output())
    transition.put_logic_data_to_main_window(tuple(output))


def _update_data_in_main_window() -> None:
    output: list[LeagueOutput] = list()
    for league in active_leagues:
        output.append(league.get_output())
    transition.put_logic_data_to_main_window(output_=tuple(output),next_league_index=0)


def _get_league_from_name(league_name: str) -> League:
    for league in active_leagues:
        if league.name == league_name:
            return league
