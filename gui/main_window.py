# Purpur Tentakel
# 12.01.2022
# KickerRechner // Main Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTabWidget, QHBoxLayout, QVBoxLayout, QGridLayout

from gui.base_window import BaseWindow
from logic.league import LeagueOutput, GameOutput


class LeagueListItem(QListWidgetItem):
    def __init__(self, league_name: str, finished: bool = False):
        super().__init__()
        self.league_name: str = league_name
        self.finished: bool = finished

        self.first_round_days: list[DayListItem] = list()
        self.second_round_days: list[DayListItem] = list()


class DayListItem(QListWidgetItem):
    def __init__(self, game_day: int, first_round_bool, league_name: str):
        super().__init__()
        self.game_day: int = game_day
        self.first_round_bool: bool = first_round_bool
        self.league_name: str = league_name

        self.games: list[GameListItem] = list()


class GameListItem(QListWidgetItem):
    def __init__(self, league_name: str, game_name: str, team_1_name: str, team_2_name: str, game_day: int,
                 first_round: bool, score_team_1: int, score_team_2: int, finished: bool):
        super().__init__()
        self.league_name: str = league_name
        self.game_name: str = game_name
        self.team_1_name: str = team_1_name
        self.team_2_name: str = team_2_name
        self.game_day: int = game_day
        self.first_round: bool = first_round
        self.score_team_1: int = score_team_1
        self.score_team_2: int = score_team_2
        self.finished: bool = finished


class MainWindow(BaseWindow):
    def __init__(self, initial_input: tuple[LeagueOutput]):
        super().__init__()
        self._input = initial_input
        self._leagues: list[LeagueListItem] = list()
        self._next_game: GameOutput | None = None

        self._create_initial_ui()
        self._create_initial_text()
        self._create_first_next_game()
        self._create_initial_layout()

    def _create_initial_ui(self):
        self.widget = QWidget()

        # Top Left
        self._league_lb = QLabel()
        self._league_list = QListWidget()

        # Top Right games
        self._game_tabs = QTabWidget()
        self._first_day_game_hbox = QHBoxLayout()  # Hinrunde
        self._second_day_game_hbox = QHBoxLayout()  # Rückrunde
        self._add_tabs_to_game_tabs()

        self._first_day_list = QListWidget()
        self._first_game_list = QListWidget()
        self._second_day_list = QListWidget()
        self._second_game_list = QListWidget()

        # Top Right next game
        self._next_game_lb = QLabel()
        self._team_1_lb = QLabel()
        self._team_2_lb = QLabel()
        self._score_1_le = QLineEdit()
        self._score_2_le = QLineEdit()
        self._add_score_btn = QPushButton()

        # Bottom
        self._table_lb = QLabel()
        self._table_tabs = QTabWidget()
        self._first_round_table = QTableWidget()
        self._second_round_table = QTableWidget()
        self._total_table = QTableWidget()
        self._add_tabs_to_table_tabs()

    def _create_initial_text(self):
        # Top Left
        self._league_lb.setText("Ligen:")

        # Top Right games
        # no initial text

        # Top Right next game
        self._next_game_lb.setText("Nächstes Spiel:")
        self._add_score_btn.setText("Ergebnis hinzufügen")

    def _create_initial_layout(self):
        # Top Left
        league_lb_hbox = QHBoxLayout()
        league_lb_hbox.addWidget(self._league_lb)
        league_lb_hbox.addStretch()

        league_vbox = QVBoxLayout()
        league_vbox.addLayout(league_lb_hbox)
        league_vbox.addWidget(self._league_list)

        # Top Right games
        # game_tabs
        # created in UI
        self._first_day_game_hbox.addWidget(self._first_day_list)
        self._first_day_game_hbox.addWidget(self._first_game_list)

        # created in UI
        self._second_day_game_hbox.addWidget(self._second_day_list)
        self._second_day_game_hbox.addWidget(self._second_game_list)

        # Top Right next game
        next_game_lb_hbox = QHBoxLayout()
        next_game_lb_hbox.addWidget(self._next_game_lb)
        next_game_lb_hbox.addStretch()

        add_game_gl = QGridLayout()
        add_game_gl.addWidget(self._team_1_lb, 0, 0)

        add_game_gl.addWidget(QLabel("gegen"), 1, 0)
        add_game_gl.addWidget(self._team_2_lb, 2, 0)
        add_game_gl.addWidget(self._score_1_le, 0, 1)
        add_game_gl.addWidget(self._score_2_le, 2, 1)
        add_game_gl.addWidget(self._add_score_btn, 2, 2)

        add_game_hbox = QHBoxLayout()
        add_game_hbox.addLayout(add_game_gl)
        add_game_hbox.addStretch()

        top_right_vbox = QVBoxLayout()
        top_right_vbox.addWidget(self._game_tabs)
        top_right_vbox.addLayout(next_game_lb_hbox)
        top_right_vbox.addLayout(add_game_hbox)

        # Top
        top_hbox = QHBoxLayout()
        top_hbox.addLayout(league_vbox)
        top_hbox.addLayout(top_right_vbox)

        # Global
        global_vbox = QVBoxLayout()
        global_vbox.addLayout(top_hbox)
        global_vbox.addWidget(self._table_tabs)

        self.widget.setLayout(global_vbox)
        self.set_widget(widget=self.widget)

        self.show()

    def _create_first_next_game(self):
        self._next_game: GameOutput = self._input[0].next_game
        self._team_1_lb.setText(self._next_game.team_1_name + ":")
        self._team_2_lb.setText(self._next_game.team_2_name + ":")
        self._score_1_le.setPlaceholderText("Score " + self._next_game.team_1_name)
        self._score_2_le.setPlaceholderText("Score " + self._next_game.team_2_name)

    def _create_first_leagues(self):
        for league in self._input:
            league_item: LeagueListItem = LeagueListItem(league_name=league.name)
            self._leagues.append(league_item)
            for game in league.all_games:
                day_item: DayListItem = DayListItem(game_day=game.game_day, first_round_bool=game.first_round,
                                                    league_name=league.name)
                if game.first_round:
                    league_item.first_round_days.append(day_item)

                else:
                    league_item.second_round_days.append(day_item)

                game_item: GameListItem = GameListItem(league_name=league.name, game_name=game.game_name,
                                                       team_1_name=game.team_1_name, team_2_name=game.team_2_name,
                                                       game_day=game.game_day, first_round=game.first_round,
                                                       score_team_1=game.score_team_1, score_team_2=game.score_team_2,
                                                       finished=game.finished)
                day_item.games.append(game_item)

    def _add_tabs_to_game_tabs(self):
        first_widget = QWidget()
        first_widget.setLayout(self._first_day_game_hbox)
        self._game_tabs.addTab(first_widget, "Hinrunde")
        second_widget = QWidget()
        second_widget.setLayout(self._second_day_game_hbox)
        self._game_tabs.addTab(second_widget, "Rückrunde")

    def _add_tabs_to_table_tabs(self):
        self._table_tabs.addTab(self._first_round_table, "Hinrunde")
        self._table_tabs.addTab(self._second_round_table, "Rückrunde")
        self._table_tabs.addTab(self._total_table, "Gesamt")


window: MainWindow | None = None


def create_main_window(initial_input: tuple):
    global window
    window = MainWindow(initial_input=initial_input)
