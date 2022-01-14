# Purpur Tentakel
# 12.01.2022
# KickerRechner // Main Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTableWidgetItem, QTabWidget, QHBoxLayout, QVBoxLayout, QGridLayout

from gui.base_window import BaseWindow
from gui.enum_sheet import TableType, ListType
from logic.league import LeagueOutput, GameOutput


class LeagueListItem(QListWidgetItem):
    def __init__(self, index: int, league_name: str) -> None:
        super().__init__()
        self.index: int = index
        self.league_name: str = league_name
        self.first_round_games: list[GameOutput] = list()
        self.second_round_games: list[GameOutput] = list()

        self._crate_text()

    def _crate_text(self) -> None:
        self.setText(self.league_name)


class DayListItem(QListWidgetItem):
    def __init__(self, game_day: int, league_name: str) -> None:
        super().__init__()
        self.game_day: int = game_day
        self.league_name: str = league_name

        self._create_text()

    def _create_text(self) -> None:
        self.setText("Spieltag " + str(self.game_day))


class GameListItem(QListWidgetItem):
    def __init__(self, league_name: str, game_name: str, score_team_1: int, score_team_2: int, finished: bool) -> None:
        super().__init__()
        self.league_name: str = league_name
        self.game_name: str = game_name
        self.score_team_1: int = score_team_1
        self.score_team_2: int = score_team_2
        self.finished: bool = finished

        self._create_text()

    def _create_text(self) -> None:
        if self.finished:
            self.setText(self.game_name + "//" + str(self.score_team_1) + ":" + str(self.score_team_2))
        else:
            self.setText(self.game_name)

    def update_text(self) -> None:
        self._create_text()


class MainWindow(BaseWindow):
    def __init__(self, initial_input: tuple[LeagueOutput]) -> None:
        super().__init__()
        self._leagues = initial_input
        print(self._leagues)
        self._league_list_items: list[LeagueListItem] = list()
        self._next_game: GameOutput | None = None
        self._next_league_index: int = 0

        self._create_initial_ui()
        self._create_initial_text()
        self._create_leagues()
        self._create_initial_layout()

    def _create_initial_ui(self) -> None:
        self.widget = QWidget()

        # Top Left
        self._league_lb = QLabel()
        self._league_list = QListWidget()

        # Top Right games
        self._game_tabs = QTabWidget()
        self._first_day_game_hbox = QHBoxLayout()  # Hinrunde
        self._second_day_game_hbox = QHBoxLayout()  # Rückrunde
        self._add_tabs_to_game_tabs()

        self._day_list = QListWidget()
        self._game_list = QListWidget()
        self._dummy_day_list = QListWidget()
        self._dummy_game_list = QListWidget()

        # Top Right next game
        self._next_game_lb = QLabel()
        self._team_1_lb = QLabel()
        self._team_2_lb = QLabel()
        self._score_1_le = QLineEdit()
        self._score_2_le = QLineEdit()
        self._add_score_btn = QPushButton()
        self._add_score_btn.setEnabled(False)

        # Bottom
        self._table_lb = QLabel()
        self._table_tabs = QTabWidget()
        self._first_round_table = QTableWidget()
        self._second_round_table = QTableWidget()
        self._total_table = QTableWidget()
        self._add_tabs_to_table_tabs()

    def _create_initial_text(self) -> None:
        # Top Left
        self._league_lb.setText("Ligen:")

        # Top Right games
        # no initial text

        # Top Right next game
        self._next_game_lb.setText("Nächstes Spiel:")
        self._add_score_btn.setText("Ergebnis hinzufügen")

    def _create_initial_layout(self) -> None:
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
        self._first_day_game_hbox.addWidget(self._day_list)
        self._first_day_game_hbox.addWidget(self._game_list)

        # created in UI
        self._second_day_game_hbox.addWidget(self._dummy_day_list)
        self._second_day_game_hbox.addWidget(self._dummy_game_list)

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

    def _create_leagues(self) -> None:
        self._clear_ui_list(ListType.LEAGUE)
        for index, league in enumerate(self._leagues):
            league_item: LeagueListItem = LeagueListItem(index=index, league_name=league.name)
            self._league_list_items.append(league_item)
            self._add_item_to_ui_list(list_type=ListType.LEAGUE, list_item=league_item)
            for game in league.all_games:
                if game.first_round:
                    league_item.first_round_games.append(game)
                else:
                    league_item.second_round_games.append(game)
        self._league_list.setCurrentItem(self._league_list_items[self._next_league_index])

    def _add_tabs_to_game_tabs(self) -> None:
        first_widget = QWidget()
        first_widget.setLayout(self._first_day_game_hbox)
        self._game_tabs.addTab(first_widget, "Hinrunde")
        second_widget = QWidget()
        second_widget.setLayout(self._second_day_game_hbox)
        self._game_tabs.addTab(second_widget, "Rückrunde")

    def _add_tabs_to_table_tabs(self) -> None:
        self._table_tabs.addTab(self._first_round_table, "Hinrunde")
        self._table_tabs.addTab(self._second_round_table, "Rückrunde")
        self._table_tabs.addTab(self._total_table, "Gesamt")

    def _add_item_to_ui_list(self, list_type: ListType, list_item: QListWidgetItem) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.addItem(list_item)
            case ListType.DAY:
                self._day_list.addItem(list_item)
                self._dummy_day_list.addItem(list_item)
            case ListType.GAME:
                self._game_list.addItem(list_item)
                self._dummy_game_list.addItem(list_item)

    def _set_second_round(self, league: LeagueOutput) -> None:
        self._game_tabs.setTabEnabled(1, league.second_round)
        self._table_tabs.setTabEnabled(1, league.second_round)

    def _set_ui_list_item(self, list_type: ListType, list_item: QListWidgetItem) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.setCurrentItem(list_item)
            case ListType.DAY:
                self._day_list.setCurrentItem(list_item)
                self._dummy_day_list.setCurrentItem(list_item)
            case ListType.GAME:
                self._game_list.setCurrentItem(list_item)
                self._dummy_game_list.setCurrentItem(list_item)

    def _clear_ui_list(self, list_type: ListType) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.clear()
                self._league_list_items.clear()
            case ListType.DAY:
                self._day_list.clear()
                self._dummy_day_list.clear()
            case ListType.GAME:
                self._game_list.clear()
                self._dummy_game_list.clear()


window: MainWindow | None = None


def create_main_window(initial_input: tuple):
    global window
    window = MainWindow(initial_input=initial_input)
