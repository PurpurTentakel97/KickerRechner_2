# Purpur Tentakel
# 09.01.2022
# KickerRechner // League
from typing import Tuple

from logic.team import Team
from logic.game import Game
from logic.enum_sheet import TableType, Stats


class GameOutput:
    def __init__(self, game_name: str, team_1_name: str, team_2_name: str, game_day: int, first_round: bool,
                 score_team_1: int = 0, score_team_2: int = 0, finished: bool = False):
        self.game_name: str = game_name
        self.team_1_name: str = team_1_name
        self.team_2_name: str = team_2_name
        self.game_day: int = game_day
        self.first_round: bool = first_round
        self.score_team_1: int = score_team_1
        self.score_team_2: int = score_team_2
        self.finished: bool = finished


class LeagueOutput:
    def __init__(self, name: str, second_round: bool, finished: bool, next_game: GameOutput,
                 all_games: tuple[GameOutput],
                 first_round_table: tuple, second_round_table: tuple, total_table: tuple):
        self.name: str = name
        self.second_round: bool = second_round
        self.finished: bool = finished
        self.next_game: GameOutput = next_game
        self.all_games: tuple[GameOutput] = all_games
        self.first_round_table: tuple[list] = first_round_table
        self.second_round_table: tuple[list] | None = second_round_table
        self.total_table: tuple[list] = total_table


class League:
    def __init__(self, name: str, is_active: bool, is_second_round: bool, team_names: list[str]) -> None:
        self.name: str = name
        self.is_active: bool = is_active
        self.is_second_round: bool = is_second_round

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
                    final_game: Game = Game(game_name=team_name_2 + " : " + team_name_1,
                                            team_1=self.teams[team_1_int - 1],
                                            team_2=self.teams[team_2_int - 1], game_day=day, first_round=False)
                    self.games.append(final_game)

    def _set_league_finished(self) -> None:
        self.finished = True

    def get_output(self) -> LeagueOutput | bool:
        if self.finished:
            return self.finished
        else:
            next_game: GameOutput
            all_games: tuple[GameOutput]
            next_game, all_games = self._get_all_games()
            league_output: LeagueOutput = LeagueOutput(
                name=self.name,
                second_round=self.is_second_round,
                finished=self.finished,
                next_game=next_game,
                all_games=all_games,
                first_round_table=self._get_round_tables(TableType.FIRST),
                second_round_table=self._get_round_tables(TableType.SECOND),
                total_table=self._get_total_table())
            return league_output

    def _get_name_from_team(self, team_to_check: Team) -> str:
        for team in self.teams:
            if team == team_to_check:
                return team.name

    def _get_game_from_teams_in_round_table_type(self, team_1: Team, team_2: Team, table_type: TableType) -> Game:
        for game in self.games:
            if table_type == TableType.FIRST and game.first_round:
                if team_1 == game.team_1 and team_2 == game.team_2 or team_1 == game.team_2 and team_2 == game.team_1:
                    return game
            elif table_type == TableType.SECOND and not game.first_round:
                if team_1 == game.team_1 and team_2 == game.team_2 or team_1 == game.team_2 and team_2 == game.team_1:
                    return game

    def _get_all_games(self) -> tuple[GameOutput, tuple[GameOutput]]:
        all_games: list[GameOutput] = list()
        next_game: GameOutput | None = None
        for current_game in self.games:
            single_game: GameOutput = GameOutput(
                game_name=current_game.game_name,
                team_1_name=self._get_name_from_team(current_game.team_1),
                team_2_name=self._get_name_from_team(current_game.team_2),
                game_day=current_game.game_day,
                first_round=current_game.first_round)
            all_games.append(single_game)
            if next_game is None and not current_game.finished:
                next_game = single_game

        output: tuple[GameOutput, tuple[GameOutput]] = (next_game, tuple(all_games))
        return output

    def _get_round_tables(self, table_type: TableType) -> tuple[list[str]] | None:
        if table_type == TableType.SECOND and not self.is_second_round:
            return None
        table: list[list[str]] = list()
        headers: list[str] = ["Rang", "Spiele"]
        ranked_teams_with_stats: list[dict] = self._get_ranked_teams_with_stats_for_round_tables(table_type=table_type)
        for team, *_ in ranked_teams_with_stats:
            headers.append(self._get_name_from_team(team_to_check=team))
        headers.extend(["Punkte", "Tor-Diff", "Tore", "Gegentore", "Bilanz"])
        table.append(headers)
        for rank, (team, stats) in enumerate(ranked_teams_with_stats, start=1):
            row: list[str] = [str(rank), self._get_name_from_team(team_to_check=team)]
            for opponent, *_ in ranked_teams_with_stats:
                if team == opponent:
                    row.append("-----")
                else:
                    game: Game = self._get_game_from_teams_in_round_table_type(team_1=team, team_2=opponent,
                                                                               table_type=table_type)
                    result: str = game.get_result_string_from_team_view(team=team)
                    row.append(result)
            row.extend([str(stats[Stats.POINTS]),
                        str(stats[Stats.GOAL_DIFF]),
                        str(stats[Stats.GOALS]),
                        str(stats[Stats.COUNTER_GOALS]),
                        str(stats[Stats.BALANCE])])
            table.append(row)
        return tuple(table)

    def _get_total_table(self) -> tuple[list[str]]:
        table: list[list[str]] = list()
        headers: list[str] = ["Rang", "Name", "Punkte", "Tor-diff", "Tore", "Gegentore", "Bilanz"]
        table.append(headers)
        ranked_teams_with_stats: list[dict] = self._get_ranked_teams_with_stats_for_total_table()
        for index, (team, stats) in enumerate(ranked_teams_with_stats):
            row: list[str] = [str(index + 1),
                              team.name,
                              str(stats[Stats.POINTS]),
                              str(stats[Stats.GOAL_DIFF]),
                              str(stats[Stats.GOALS]),
                              str(stats[Stats.COUNTER_GOALS]),
                              stats[Stats.BALANCE]]
            table.append(row)
        return tuple(table)

    def _get_ranked_teams_with_stats_for_round_tables(self, table_type: TableType) -> list[dict]:
        teams_with_stats = dict()
        for team in self.teams:
            stats_of_team: dict[Stats] = dict()
            stats_of_team[Stats.POINTS] = team.first_round_points if table_type.FIRST else team.second_round_points
            stats_of_team[Stats.GOALS] = team.first_round_goals if table_type.FIRST else team.second_round_goals
            stats_of_team[Stats.COUNTER_GOALS] = team.first_round_counter_goals if table_type.FIRST \
                else team.second_round_counter_goals
            stats_of_team[Stats.GOAL_DIFF] = team.first_round_goals - team.first_round_counter_goals if table_type.FIRST \
                else team.second_round_goals - team.second_round_counter_goals
            stats_of_team[Stats.BALANCE] = (str(team.first_round_wins) + " / " + str(team.first_round_draw) + " / " +
                                            str(team.first_round_loose)) if table_type.FIRST else \
                (str(team.second_round_wins) + " / " + str(team.second_round_draw) + " / " +
                 str(team.second_round_loose))
            teams_with_stats[team] = stats_of_team

        teams_with_stats = list(teams_with_stats.items())
        teams_with_stats.sort(key=lambda x: (x[1][Stats.POINTS],
                                             x[1][Stats.GOAL_DIFF],
                                             x[1][Stats.GOALS],
                                             x[1][Stats.COUNTER_GOALS]), reverse=True)
        return teams_with_stats

    def _get_ranked_teams_with_stats_for_total_table(self) -> list[dict]:
        teams_with_stats = dict()
        for team in self.teams:
            stats_of_team: dict[Stats] = dict()
            stats_of_team[Stats.POINTS] = team.points
            stats_of_team[Stats.GOALS] = team.goals
            stats_of_team[Stats.COUNTER_GOALS] = team.counter_goals
            stats_of_team[Stats.GOAL_DIFF] = team.goals - team.counter_goals
            stats_of_team[Stats.BALANCE] = str(team.wins) + " / " + str(team.draw) + " / " + str(team.loose)
            teams_with_stats[team] = stats_of_team

        teams_with_stats = list(teams_with_stats.items())
        teams_with_stats.sort(key=lambda x: (x[1][Stats.POINTS],
                                             x[1][Stats.GOAL_DIFF],
                                             x[1][Stats.GOALS],
                                             x[1][Stats.COUNTER_GOALS]), reverse=True)
        return teams_with_stats
