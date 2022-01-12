# Purpur Tentakel
# 09.01.2022
# KickerRechner // League

from logic.team import Team
from logic.game import Game
from logic.enum_sheet import TableType, Stats


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
                self._get_round_tables(table_type=TableType.FIRST),
                self._get_round_tables(table_type=TableType.SECOND),
                # self._get_round_tables(table_type=TableType.TOTAL)
            ]
            return output

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
                self._get_name_from_team(team_to_check=game.team_1),
                self._get_name_from_team(team_to_check=game.team_2),
                game.game_day,
                game.first_round,
                game.score_team_1,
                game.score_team_2,
                self.finished
            ]
            all_games.append(single_game)
        return all_games

    def _get_round_tables(self, table_type: TableType) -> list[list]:
        table: list[list[str]] = list()
        headers: list[str] = ["Rang", "Spiele"]
        ranked_teams_with_stats: list[dict] = self._get_ranked_teams_with_stats_for_round_tables(table_type=table_type)
        for team, *_ in ranked_teams_with_stats:
            headers.append(self._get_name_from_team(team_to_check=team))
        headers.extend(["Punkte", "Tor-Diff", "Tore", "Gegentore", "Bilanz"])
        table.append(headers)
        for index, team, stats in enumerate(ranked_teams_with_stats):
            row: list[str] = [str(index + 1), self._get_name_from_team(team_to_check=team)]
            for opponent, *_ in ranked_teams_with_stats:
                if team == opponent:
                    row.append("-----")
                else:
                    game: Game = self._get_game_from_teams_in_round_table_type(team_1=team, team_2=opponent,
                                                                               table_type=table_type)
                    result: str = game.get_result_string_from_team_view(team=team)
                    row.append(result)
            row.extend([str(stats.POINTS), str(stats.GOAL_DIFF), str(stats.GOAL), str(stats.COUNTER_GOALS),
                        str(stats.BALANCE)])
            table.append(row)
        return table

    def _get_total_table(self) -> list[list]:
        table: list[list[str]] = list()
        headers: list[str] = ["Rang", "Name", "Punkte", "Tor-diff", "Tore", "Gegentore", "Bilanz"]
        table.append(headers)
        ranked_teams_with_stats: list[dict] = self._get_ranked_teams_with_stats_for_total_table()
        for index, team, stats in enumerate(ranked_teams_with_stats):
            row: list[str] = [str(index + 1),
                              team.name,
                              str(stats.POINTS),
                              str(stats.GOAL_DIFF),
                              str(stats.GOAL),
                              str(stats.COUNTER_GOALS),
                              stats.BALANCE]
            table.append(row)
        return table

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

        teams_with_stats = list(teams_with_stats)
        teams_with_stats.sort(key=lambda x: (x[0][Stats.POINTS],
                                             x[0][Stats.GOAL_DIFF],
                                             x[0][Stats.GOALS],
                                             x[0][Stats.COUNTER_GOALS]), reverse=True)
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

        teams_with_stats = list(teams_with_stats)
        teams_with_stats.sort(key=lambda x: (x[0][Stats.POINTS],
                                             x[0][Stats.GOAL_DIFF],
                                             x[0][Stats.GOALS],
                                             x[0][Stats.COUNTER_GOALS]), reverse=True)
        return teams_with_stats
