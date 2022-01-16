# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__
import os.path

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
    finished: bool = _is_tournaments_finished()
    output: list[LeagueOutput] = list()
    for league in active_leagues:
        output.append(league.get_output())
    transition.put_logic_data_to_main_window(output_=tuple(output), next_league_index=_get_next_league_index(),
                                             finished=finished)


def _get_league_from_name(league_name: str) -> League:
    for league in active_leagues:
        if league.name == league_name:
            return league


def _get_next_league_index() -> int:
    all_percent: list[float] = list()
    for league in active_leagues:
        if league.finished:
            all_percent.append(1.0)
            continue
        finished_game_counter: int = 0
        for game in league.games:
            if game.finished:
                finished_game_counter += 1
        all_games: int = len(league.games)
        percent: float = finished_game_counter / all_games
        all_percent.append(percent)

    low_number: float = 1.0
    for number in all_percent:
        if low_number > number:
            low_number = number

    next_index: int = all_percent.index(low_number)
    return next_index


def _is_tournaments_finished() -> bool:
    finished: bool = True
    for league in active_leagues:
        if not league.finished:
            finished: bool = False
            break
    return finished


def save(filename: str):
    pass
