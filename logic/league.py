# Purpur Tentakel
# 09.01.2022
# KickerRechner // League

from logic.team import Team
from logic.game import Game
from logic.enum_sheet import TableType


class League:
    def __init__(self, name: str, is_second_round: bool, is_active: bool, team_names: list[str]) -> None:
        self.name: str = name
        self.is_second_round: bool = is_second_round
        self.is_active: bool = is_active

        self.teams: list[Team] = list()
        self.games: list[Game] = list()
        self.finished: bool = False

        self._create_teams(team_names=team_names)
        self._create_games()

    def _create_teams(self, team_names: list[str]) -> None:
        for team_name in team_names:
            self.teams.append(Team(name=team_name))

    def _create_games(self) -> None:
        teams_int: list[int] = list()
        for team_index in range(len(self.teams)):
            teams_int.append(team_index + 1)
        matches: dict[int, dict[int, int]] = dict()
        inv_matches: dict[int, dict[int, int]] = dict()
        if not len(self.teams) % 2 == 0:
            teams_int.append(len(teams_int) + 1)
            even: bool = False
        else:
            even: bool = True
        for team_1 in teams_int[:-1]:
            matches_day: dict[int, int] = dict()
            inv_matches_day: dict[int, int] = dict()
            if even:
                matches_day[team_1]: dict = teams_int[-1]
                if self.is_second_round:
                    inv_matches_day[teams_int[-1]]: dict = team_1
            for team_2 in teams_int[:-1]:
                game: list[int] = []
                if team_2 <= len(teams_int[:-1]) / 2:
                    node_1 = (team_1 + team_2) % len(teams_int[:-1])
                    node_2 = (team_1 - team_2) % len(teams_int[:-1])
                    if type(node_1) == int:
                        if node_1 == 0:
                            node_1: int = len(teams_int[:-1])
                        game.append(node_1)
                    if type(node_2) == int:
                        if node_2 == 0:
                            node_2: int = len(teams_int[:-1])
                        game.append(node_2)
                if len(game) == 2:
                    matches_day[game[0]]: list = game[1]  # Hinrunde
                    if self.is_second_round:
                        inv_matches_day[game[1]]: list = game[0]  # Rückrunde

            matches[team_1]: dict = matches_day
            if self.is_second_round:
                inv_matches[team_1]: dict = inv_matches_day

        for day, games in matches.items():
            for team_1_int, team_2_int in games.items():
                team_name_1: str = self._get_name_from_team(team_to_check=self.teams[team_1_int - 1])
                team_name_2: str = self._get_name_from_team(team_to_check=self.teams[team_2_int - 1])
                final_game: Game = Game(game_name=team_name_1 + " : " + team_name_2, team_1=self.teams[team_1_int - 1],
                                        team_2=self.teams[team_2_int - 1], game_day=day, first_round=True)
                self.games.append(final_game)

        if self.is_second_round:
            for day, games in inv_matches.items():
                for team_1_int, team_2_int in games.items():
                    team_name_1: str = self._get_name_from_team(team_to_check=self.teams[team_1_int - 1])
                    team_name_2: str = self._get_name_from_team(team_to_check=self.teams[team_2_int - 1])
                    final_game: Game = Game(game_name=team_name_1 + " : " + team_name_2,
                                            team_1=self.teams[team_1_int - 1],
                                            team_2=self.teams[team_2_int - 1], game_day=day, first_round=False)
                    self.games.append(final_game)

    def _set_league_finished(self) -> None:
        self.finished = True

    def get_output(self) -> list:
        if self.finished:
            return [self.finished]
        # [league_name:str, second_round:bool,[game_name:str, team_1_name:str, team_2_name:str, game_day:int,
        # first_round:bool, score_team_1:int, score_team_2:int, finished:bool], [[game_name:str, team_1_name:str,
        # team_2_name:str, game_day:int, first_round:bool, score_team_1:int, score_team_2:int, finished:bool][next
        # game]], [first_round_table:list],[second_round_table:list][total_table]]
        else:
            output: list[str, bool, list[str, str, str, int, bool, int, int, bool],
                         list[list[str, str, str, int, bool, int, int, bool]], list[list], list[list], list[list]] = [
                self.name,
                self.is_second_round,
                self._get_next_game(),
                self._get_all_games(),
                self._get_tables(table_type=TableType.FIRST),
                self._get_tables(table_type=TableType.SECOND),
                self._get_tables(table_type=TableType.TOTAL)
            ]
            return output

    def _get_name_from_team(self, team_to_check: Team) -> str:
        for team in self.teams:
            if team == team_to_check:
                return team.name

    def _get_next_game(self) -> list:
        current_game: str = ""
        for game in self.games:
            if not game.finished:
                current_game: Game = game
        if current_game == "":
            self._set_league_finished()
            return [self.finished]
        else:
            next_game: list[str, str, str, int, bool, int, int, bool] = [
                current_game.game_name,
                self._get_name_from_team(team_to_check=current_game.team_1),
                self._get_name_from_team(team_to_check=current_game.team_2),
                current_game.game_day,
                current_game.first_round,
                current_game.score_team_1,
                current_game.score_team_2,
                current_game.finished
            ]
            return next_game

    def _get_all_games(self) -> list[list]:
        all_games: list[list[str, str, str, int, bool, int, int, bool]] = list()
        for game in self.games:
            single_game: list[str, str, str, int, bool, int, int, bool] = [
                game.game_name,
                self._get_name_from_team(game.team_1),
                self._get_name_from_team(game.team_2),
                game.game_day,
                game.first_round,
                game.score_team_1,
                game.score_team_2,
                self.finished
            ]
            all_games.append(single_game)
        return all_games

    def _get_tables(self, table_type: TableType) -> list[list]:
        pass
