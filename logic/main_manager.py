# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__
import json
import os

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


def create_saves_directory():
    if not os.path.exists("saves"):
        os.mkdir("saves")


def save(filename: str):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.mkdir(path)

    output: list = list()
    for league_index, league in enumerate(all_leagues):

        all_teams_output:list = list()
        for team_index, team in enumerate(league.teams):
            team_output: dict = {"name": team.name, "first_round_points": team.first_round_points,
                                 "second_round_points": team.second_round_points,
                                 "first_round_goals": team.first_round_goals,
                                 "second_round_goals": team.second_round_goals,
                                 "first_round_counter_goals": team.first_round_counter_goals,
                                 "second_round_counter_goals": team.second_round_counter_goals,
                                 "first_round_wins": team.first_round_wins, "second_round_wins": team.second_round_wins,
                                 "first_round_draw": team.first_round_draw, "second_round_draw": team.second_round_draw,
                                 "first_round_loose": team.first_round_loose,
                                 "second_round_loose": team.second_round_loose}
            all_teams_output.append(team_output)

        all_games_output: list = list()
        for game_index, game in enumerate(league.games):
            game_output: dict = {"name": game.game_name, "team_1_name": league.get_name_from_team(game.team_1),
                                 "team_2_name": league.get_name_from_team(game.team_2), "day": game.game_day,
                                 "first_round": game.first_round, "score_team_1": game.score_team_1,
                                 "score_team_2": game.score_team_2, "team_1_result": game.team_1_result,
                                 "team_2_result": game.team_2_result, "finished": game.finished}
            all_games_output.append(game_output)

        league_output: dict = {"name": league.name, "is_active": league.is_active,
                               "is_second_round": league.is_second_round, "finished": league.finished,
                               "teams": all_teams_output, "games": all_games_output}
        output.append(league_output)

    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
    _, tail = os.path.split(filename)
    transition.show_massage('Turnier gespeichert als "%s"' % tail)


def load(filename: str):
    if os.path.exists(filename):
        all_leagues.clear()
        active_leagues.clear()

        with open(filename, "r") as file:
            data: dict = json.load(file)
        for league_index in range(len(data)):
            league_data: dict = data[league_index]
            league: League = League(name=league_data["name"], is_active=league_data["is_active"],
                                    is_second_round=league_data["is_second_round"], is_load=True)

            for team_index in range(len(league_data["teams"])):
                team_data: dict = league_data["teams"][team_index]
                league.load_team(team_data=team_data)

            for game_index in range(len(league_data["games"])):
                game_data: dict = league_data["games"][game_index]
                league.load_game(game_data=game_data)

            all_leagues.append(league)
            if league.is_active:
                active_leagues.append(league)

        transition.close_window()
        _put_data_to_main_window()
        _, tail = os.path.split(filename)
        transition.show_massage('"%s" geladen' % tail)
    else:
        transition.show_massage("Datei nicht gefunden")
