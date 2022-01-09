# Purpur Tentakel
# 09.01.2022
# KickerRechner // League

from logic.team import Team
from logic.game import Game


class League:
    def __init__(self, name: str, team_names: list[str], is_second_round: bool, is_active: bool) -> None:
        self.name: str = name
        self.is_second_round: bool = is_second_round
        self.is_active: bool = is_active

        self.teams: list[Team] = list()
        self.games: list[Game] = list()

        self._create_teams(team_names=team_names)
        self._create_games()

    def _create_teams(self, team_names: list[str]) -> None:
        for team_name in team_names:
            self.teams.append(Team(team_name))

    def _create_games(self) -> None:
        teams_int: list[int] = list()
        for team_index in range(len(self.teams)):
            teams_int.append(team_index + 1)
        matches: dict[int, dict] = dict()
        inv_matches: dict[int, dict] = dict()
        if not len(self.teams) % 2 == 0:
            teams_int.append(len(teams_int) + 1)
            even = False
        else:
            even = True
        for team_1 in teams_int[:-1]:
            matches_day: dict[int, int] = dict()
            inv_matches_day: dict[int, int] = dict()
            if even:
                matches_day[team_1] = teams_int[-1]
                if self.is_second_round:
                    inv_matches_day[teams_int[-1]] = team_1
            for team_2 in teams_int[:-1]:
                game: list[int] = []
                if team_2 <= len(teams_int[:-1]) / 2:
                    node_1 = (team_1 + team_2) % len(teams_int[:-1])
                    node_2 = (team_1 - team_2) % len(teams_int[:-1])
                    if type(node_1) == int:
                        if node_1 == 0:
                            node_1 = len(teams_int[:-1])
                        game.append(node_1)
                    if type(node_2) == int:
                        if node_2 == 0:
                            node_2 = len(teams_int[:-1])
                        game.append(node_2)
                if len(game) == 2:
                    matches_day[game[0]] = game[1]  # Hinrunde
                    if self.is_second_round:
                        inv_matches_day[game[1]] = game[0]  # Rückrunde

            matches[team_1] = matches_day
            if self.is_second_round:
                inv_matches[team_1] = inv_matches_day

        for day, games in matches.items():
            for team_1_int, team_2_int in games.items():
                team_name_1 = self._get_name_from_team(team_to_check=self.teams[team_1_int - 1])
                team_name_2 = self._get_name_from_team(team_to_check=self.teams[team_2_int - 1])
                final_game = Game(team_name_1 + " : " + team_name_2, self.teams[team_1_int - 1],
                                  self.teams[team_2_int - 1], day, True)
                self.games.append(final_game)

        if self.is_second_round:
            for day, games in inv_matches.items():
                for team_1_int, team_2_int in games.items():
                    team_name_1 = self._get_name_from_team(team_to_check=self.teams[team_1_int - 1])
                    team_name_2 = self._get_name_from_team(team_to_check=self.teams[team_2_int - 1])
                    final_game = Game(team_name_1 + " : " + team_name_2, self.teams[team_1_int - 1],
                                      self.teams[team_2_int - 1], day, False)
                    self.games.append(final_game)

    def _get_name_from_team(self, team_to_check: Team) -> str:
        for team in self.teams:
            if team == team_to_check:
                return team.name
