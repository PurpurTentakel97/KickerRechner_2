# Purpur Tentakel
# 12.01.2022
# KickerRechner //Transition
from logic import manager
from gui import input_window, main_window, base_window


class ResultInput:
    def __init__(self, league_name: str, team_name_1: str, team_name_2: str, team_score_1: int, team_score_2: int,
                 first_round: bool, finished: bool) -> None:
        self.league_name: str = league_name
        self.team_name_1: str = team_name_1
        self.team_name_2: str = team_name_2
        self.team_score_1: int = team_score_1
        self.team_score_2: int = team_score_2
        self.first_round: bool = first_round
        self.finished: bool = finished


class GameInput:
    def __init__(self, game_name: str, team_1_name: str, team_2_name: str, game_day: int, first_round: bool,
                 score_team_1: int = 0, score_team_2: int = 0, finished: bool = False) -> None:
        self.game_name: str = game_name
        self.team_1_name: str = team_1_name
        self.team_2_name: str = team_2_name
        self.game_day: int = game_day
        self.first_round: bool = first_round
        self.score_team_1: int = score_team_1
        self.score_team_2: int = score_team_2
        self.finished: bool = finished


class LeagueInput:
    def __init__(self, name: str, second_round: bool, finished: bool, next_game: GameInput,
                 all_games: tuple[GameInput],
                 first_round_table: tuple, second_round_table: tuple, total_table: tuple) -> None:
        self.name: str = name
        self.second_round: bool = second_round
        self.finished: bool = finished
        self.next_game: GameInput = next_game
        self.all_games: tuple[GameInput] = all_games
        self.first_round_table: tuple[list] = first_round_table
        self.second_round_table: tuple[list] | None = second_round_table
        self.total_table: tuple[list] = total_table


def create_first_input_window() -> None:
    input_window.create_first_input_window()


def create_input_window() -> None:
    input_window.create_input_window()


def put_logic_data_to_input_window(output_: tuple) -> None:
    input_window.window.update_data(input_=output_)


def put_logic_data_to_main_window(output_: tuple, next_league_index: int | None = None, finished: bool = False) -> None:
    input_: list[LeagueInput] = list()
    for league in output_:
        next_game: GameInput | None = None
        new_games: list[GameInput] = list()
        for game in league.all_games:
            new_game: GameInput = GameInput(game_name=game.game_name, team_1_name=game.team_1_name,
                                            team_2_name=game.team_2_name, game_day=game.game_day,
                                            first_round=game.first_round, score_team_1=game.score_team_1,
                                            score_team_2=game.score_team_2, finished=game.finished)
            new_games.append(new_game)
            if game == league.next_game:
                next_game: GameInput = new_game
        new_league: LeagueInput = LeagueInput(name=league.name, second_round=league.second_round,
                                              finished=league.finished, next_game=next_game, all_games=tuple(new_games),
                                              first_round_table=league.first_round_table,
                                              second_round_table=league.second_round_table,
                                              total_table=league.total_table)
        input_.append(new_league)
    if next_league_index is None:
        main_window.create_main_window(initial_input=tuple(input_))
    else:
        main_window.window.update_data(update_input=tuple(input_), next_league_index=next_league_index,
                                       finished=finished)


def put_input_window_data_to_logic(output_: tuple[list[str, bool, bool, list[str]]]) -> None:
    manager.process_data_from_input_window(initial_input=output_)


def put_main_window_data_to_logic(output_: main_window.ResultOutput) -> None:
    input_: ResultInput = ResultInput(league_name=output_.league_name, team_name_1=output_.team_name_1,
                                      team_name_2=output_.team_name_2, team_score_1=output_.team_score_1,
                                      team_score_2=output_.team_score_2, first_round=output_.first_round,
                                      finished=output_.finished)
    manager.process_data_from_main_window(input_)


def save(filename: str) -> None:
    manager.save(filename=filename)


def load(filename: str) -> None:
    manager.load(filename=filename)


def load_autosave() -> None:
    manager.load_autosave()


def restart() -> None:
    manager.restart()


def show_massage(massage: str) -> None:
    base_window.window.set_status_bar(massage=massage)


def crate_save_directory() -> None:
    manager.create_saves_directory()


def close_window() -> None:
    base_window.window.close_()
