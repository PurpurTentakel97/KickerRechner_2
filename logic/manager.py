# Purpur Tentakel
# 09.01.2022
# KickerRechner // Manager
# __Main_Sheet__

import json
import os
from os import listdir
from os.path import isfile, join

import transition
from logic.league import League, LeagueOutput

all_leagues: list[League] = list()
active_leagues: list[League] = list()
tail: str | None = None


def start():
    transition.create_first_input_window()


def process_data_from_input_window(initial_input: tuple[list[str, bool, bool, list[str]]]) -> None:
    all_leagues.clear()
    active_leagues.clear()
    for league_name, is_active, second_round, teams_names in initial_input:
        league: League = League(name=league_name, is_active=is_active, is_second_round=second_round,
                                team_names=teams_names)
        all_leagues.append(league)
        if is_active:
            active_leagues.append(league)
    _put_data_to_main_window()
    _autosave()


def process_data_from_main_window(input_) -> None:
    league: League = _get_league_from_name(input_.league_name)
    league.add_edit_entry(result_input=input_)
    _update_data_in_main_window()
    _autosave()


def _put_data_to_main_window() -> None:
    output: list[LeagueOutput] = list()
    for league in active_leagues:
        output.append(league.get_output())
    finished: bool = _is_tournaments_finished()
    transition.put_logic_data_to_main_window(output_=tuple(output), finished=finished)


def _update_data_to_input_window() -> None:
    output_: list = list()
    for league in all_leagues:
        team_names: list[str] = list()
        for team in league.teams:
            team_names.append(league.get_name_from_team(team))
        league_dict: dict = {"name": league.name,
                             "active": league.is_active,
                             "second_round": league.is_second_round,
                             "teams": team_names}
        output_.append(league_dict)
    transition.put_logic_data_to_input_window(output_=tuple(output_))
    if tail is not None:
        transition.show_massage("Grunddaten von %s geladen" % tail)
    else:
        transition.show_massage("Keine Daten Vorhanden")


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


def create_saves_directory() -> None:
    if not os.path.exists("saves"):
        os.mkdir("saves")


def create_auto_saves_directory() -> None:
    if not os.path.exists("saves/auto_saves"):
        os.makedirs("saves/auto_saves")


def save(filename: str) -> None:
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.mkdir(path)

    output: tuple = _get_save_output()

    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
    global tail
    _, tail = os.path.split(filename)
    transition.show_massage('Turnier gespeichert als "%s"' % tail)


def _autosave() -> None:
    create_auto_saves_directory()
    file_name, path = _get_last_auto_save()
    output_: tuple = _get_save_output()

    with open(path, "w") as file:
        json.dump(output_, file, indent=4)
    _, tail_ = os.path.split(file_name)
    transition.show_massage('Turnier gespeichert als "%s"' % tail_)


def load(filename: str) -> None:
    if os.path.exists(filename):
        all_leagues.clear()
        active_leagues.clear()

        with open(filename, "r") as file:
            data: dict = json.load(file)
        _load_data(data)

        transition.close_window()
        _put_data_to_main_window()
        global tail
        _, tail = os.path.split(filename)
        transition.show_massage('"%s" geladen' % tail)
    else:
        transition.show_massage("Datei nicht gefunden")


def load_autosave() -> None:
    if os.path.exists("saves/auto_saves"):
        all_leagues.clear()
        active_leagues.clear()
        files = [f for f in listdir("saves/auto_saves") if isfile(join("saves/auto_saves", f))]
        if not len(files) == 0:
            file_name, path = _get_last_auto_save(load_=True)
            with open(path, "r") as file:
                data: dict = json.load(file)
            _load_data(data)

            transition.close_window()
            _put_data_to_main_window()
            _, tail_ = os.path.split(file_name)
            transition.show_massage('"%s" geladen' % tail_)

        else:
            transition.show_massage("Kein Autosave vorhanden")
    else:
        transition.show_massage("Datei nicht gefunden")


def _get_last_auto_save(load_: bool = False):
    files = [f for f in listdir("saves/auto_saves") if isfile(join("saves/auto_saves", f))]
    if len(files) < 10 and not load_:
        file_name: str = "autosave%s.ks" % str(len(files) + 1)
        path: str = "saves/auto_saves/%s" % file_name
    else:
        file_name: str = str()
        total_time: float = float("inf")
        path: str = str()
        for name in files:
            time: float = os.path.getmtime("saves/auto_saves/%s" % name)
            if time < total_time:
                total_time: float = time
                path: str = f"saves/auto_saves/%s" % name
                file_name: str = name
    return file_name, path


def _get_save_output() -> tuple:
    output: list = list()
    for league_index, league in enumerate(all_leagues):

        all_teams_output: list = list()
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
    return tuple(output)


def _load_data(data) -> None:
    for league_index in range(len(data)):
        league_data: dict = data[league_index]
        league: League = League(name=league_data["name"], is_active=league_data["is_active"],
                                is_second_round=league_data["is_second_round"], is_load=True)

        league.finished = league_data["finished"]

        for team_index in range(len(league_data["teams"])):
            team_data: dict = league_data["teams"][team_index]
            league.load_team(team_data=team_data)

        for game_index in range(len(league_data["games"])):
            game_data: dict = league_data["games"][game_index]
            league.load_game(game_data=game_data)

        all_leagues.append(league)
        if league.is_active:
            active_leagues.append(league)


def restart() -> None:
    transition.close_window()
    transition.create_input_window()
    _update_data_to_input_window()
