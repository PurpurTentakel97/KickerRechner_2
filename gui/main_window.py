# Purpur Tentakel
# 12.01.2022
# KickerRechner // Main Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTableWidgetItem, QTabWidget, QHBoxLayout, QVBoxLayout, QGridLayout

from gui.base_window import BaseWindow
from gui.enum_sheet import ListType, TableType
from logic.league import LeagueOutput, GameOutput


class LeagueListItem(QListWidgetItem):
    def __init__(self, index: int, league_name: str, league: LeagueOutput) -> None:
        super().__init__()
        self.index: int = index
        self.league: LeagueOutput = league
        self.league_name: str = league_name
        self.first_round_games: list[GameOutput] = list()
        self.second_round_games: list[GameOutput] = list()

        self._crate_text()

    def _crate_text(self) -> None:
        self.setText(self.league_name)


class DayListItem(QListWidgetItem):
    def __init__(self, game_day: int, league_name: str, first_round: bool) -> None:
        super().__init__()
        self.game_day: int = game_day
        self.league_name: str = league_name
        self.first_round: bool = first_round

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
        self._current_game: GameOutput | None = None
        self._next_league_index: int = 0

        self._create_initial_ui()
        self._create_initial_text()
        self._create_initial_layout()

        self._create_leagues()
        self._set_next_league()

    def _create_initial_ui(self) -> None:
        self.widget = QWidget()

        # Top Left
        self._league_lb: QLabel = QLabel()
        self._league_list: QListWidget = QListWidget()

        # Top Right games
        self._first_round_btn: QPushButton = QPushButton()
        self._second_round_btn: QPushButton = QPushButton()

        self._day_list: QListWidget = QListWidget()
        self._game_list: QListWidget = QListWidget()

        # Top Right next game
        self._next_game_lb: QLabel = QLabel()
        self._team_1_lb: QLabel = QLabel()
        self._team_2_lb: QLabel = QLabel()
        self._score_1_le: QLineEdit = QLineEdit()
        self._score_2_le: QLineEdit = QLineEdit()
        self._add_score_btn: QPushButton = QPushButton()
        self._add_score_btn.setEnabled(False)

        # Bottom
        self._table_lb: QLabel = QLabel()
        self._table_tabs: QTabWidget = QTabWidget()
        self._first_round_table: QTableWidget = QTableWidget()
        self._second_round_table: QTableWidget = QTableWidget()
        self._total_table: QTableWidget = QTableWidget()
        self._add_tabs_to_table_tabs()

    def _create_initial_text(self) -> None:
        # Top Left
        self._league_lb.setText("Ligen:")

        # Top Right games
        self._first_round_btn.setText("Hinrunde")
        self._second_round_btn.setText("Rückrunde")

        # Top Right next game
        self._next_game_lb.setText("Nächstes Spiel:")
        self._add_score_btn.setText("Ergebnis hinzufügen")

    def _create_initial_layout(self) -> None:
        # Top Left
        league_lb_hbox: QHBoxLayout = QHBoxLayout()
        league_lb_hbox.addWidget(self._league_lb)
        league_lb_hbox.addStretch()

        league_vbox: QVBoxLayout = QVBoxLayout()
        league_vbox.addLayout(league_lb_hbox)
        league_vbox.addWidget(self._league_list)

        # Top Right games
        # created in UI
        games_hbox: QHBoxLayout = QHBoxLayout()
        games_hbox.addWidget(self._first_round_btn)
        games_hbox.addWidget(self._second_round_btn)
        games_hbox.addStretch()

        games_list_hbox: QHBoxLayout = QHBoxLayout()
        games_list_hbox.addWidget(self._day_list)
        games_list_hbox.addWidget(self._game_list)

        games_vbox: QVBoxLayout = QVBoxLayout()
        games_vbox.addLayout(games_hbox)
        games_vbox.addLayout(games_list_hbox)

        # Top Right next game
        next_game_lb_hbox: QHBoxLayout = QHBoxLayout()
        next_game_lb_hbox.addWidget(self._next_game_lb)
        next_game_lb_hbox.addStretch()

        add_game_gl: QGridLayout = QGridLayout()
        add_game_gl.addWidget(self._team_1_lb, 0, 0)
        add_game_gl.addWidget(QLabel("gegen"), 1, 0)
        add_game_gl.addWidget(self._team_2_lb, 2, 0)
        add_game_gl.addWidget(self._score_1_le, 0, 1)
        add_game_gl.addWidget(self._score_2_le, 2, 1)
        add_game_gl.addWidget(self._add_score_btn, 2, 2)

        add_game_hbox: QHBoxLayout = QHBoxLayout()
        add_game_hbox.addLayout(add_game_gl)
        add_game_hbox.addStretch()

        top_right_vbox: QVBoxLayout = QVBoxLayout()
        top_right_vbox.addLayout(games_vbox)
        top_right_vbox.addLayout(next_game_lb_hbox)
        top_right_vbox.addLayout(add_game_hbox)

        # Top
        top_hbox: QHBoxLayout = QHBoxLayout()
        top_hbox.addLayout(league_vbox)
        top_hbox.addLayout(top_right_vbox)

        # Global
        global_vbox: QVBoxLayout = QVBoxLayout()
        global_vbox.addLayout(top_hbox)
        global_vbox.addWidget(self._table_tabs)

        self.widget.setLayout(global_vbox)
        self.set_widget(widget=self.widget)

        self.show()

    def _create_leagues(self) -> None:
        self._clear_ui_list(ListType.LEAGUE)
        self._clear_ui_list(ListType.DAY)
        self._clear_ui_list(ListType.GAME)
        for index, league in enumerate(self._leagues):
            league_item: LeagueListItem = LeagueListItem(index=index, league_name=league.name, league=league)
            self._add_item_to_ui_list(list_type=ListType.LEAGUE, list_item_1=league_item)
            for game in league.all_games:
                if game.first_round:
                    league_item.first_round_games.append(game)
                else:
                    league_item.second_round_games.append(game)
        self._league_list.setCurrentItem(self._league_list_items[self._next_league_index])

    def _create_days(self, first_round: bool) -> bool:
        self._clear_ui_list(ListType.DAY)
        self._clear_ui_list(ListType.GAME)

        league_item: LeagueListItem = self._get_current_league()
        current_game: GameOutput = self._get_current_game()

        if first_round:
            games: list[GameOutput] = league_item.first_round_games
        else:
            games: list[GameOutput] = league_item.second_round_games

        day_set: bool = False
        counter: int = 0
        for game in games:
            if counter < game.game_day:
                new_day: DayListItem = DayListItem(game_day=game.game_day, league_name=league_item.league_name,
                                                   first_round=game.first_round)
                self._day_list.addItem(new_day)
                counter += 1
                if current_game in games and current_game.game_day == game.game_day:
                    self._day_list.setCurrentItem(new_day)
                    day_set: bool = True
        return day_set

    def _create_games(self, first_round: bool):
        self._clear_ui_list(ListType.GAME)
        league_item: LeagueListItem = self._get_current_league()
        day_item: DayListItem = self._get_current_day()
        current_game: GameOutput = self._get_current_game()

        if first_round:
            games: list[GameOutput] = league_item.first_round_games
        else:
            games: list[GameOutput] = league_item.second_round_games

        for game in games:
            if game.game_day == day_item.game_day:
                new_game: GameListItem = GameListItem(league_name=league_item.league_name, game_name=game.game_name,
                                                      score_team_1=game.score_team_1, score_team_2=game.score_team_2,
                                                      finished=game.finished)
                self._game_list.addItem(new_game)
                if current_game in games and current_game.game_name == game.game_name:
                    self._game_list.setCurrentItem(new_game)

    def _add_tabs_to_table_tabs(self) -> None:
        self._table_tabs.addTab(self._first_round_table, "Hinrunde")
        self._table_tabs.addTab(self._second_round_table, "Rückrunde")
        self._table_tabs.addTab(self._total_table, "Gesamt")

    def _add_item_to_ui_list(self, list_type: ListType, list_item_1: QListWidgetItem) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.addItem(list_item_1)
                self._league_list_items.append(list_item_1)
            case ListType.DAY:
                self._day_list.addItem(list_item_1)
            case ListType.GAME:
                self._game_list.addItem(list_item_1)

    def _set_next_league(self):
        current_game: GameOutput = self._get_current_game()
        self._create_days(current_game.first_round)
        self._create_games(current_game.first_round)
        self._set_next_game()
        self._set_second_round()

    def _set_next_game(self):
        self._score_1_le.clear()
        self._score_2_le.clear()
        current_game: GameOutput = self._get_current_game()

        self._team_1_lb.setText(current_game.team_1_name + ":")
        self._team_2_lb.setText(current_game.team_2_name + ":")
        self._score_1_le.setPlaceholderText("Tore: " + current_game.team_1_name)
        self._score_2_le.setPlaceholderText("Tore: " + current_game.team_2_name)

        if current_game.finished:
            self._next_game_lb.setText("Spiel beartbeiten:")
            self._add_score_btn.setText("Ergebnis aktualisieren")
            self._score_1_le.setText(current_game.score_team_1)
            self._score_2_le.setText(current_game.score_team_2)
        else:
            self._next_game_lb.setText("Nächstes Spiel:")
            self._add_score_btn.setText("Ergebnis eintragen")

        self._set_add_score_btn()

    def _set_second_round(self):
        league_item: LeagueListItem = self._get_current_league()
        if not league_item.league.second_round and self._table_tabs.currentIndex() == 1:
            self._table_tabs.setCurrentIndex(0)
        self._second_round_btn.setEnabled(league_item.league.second_round)
        self._table_tabs.setTabEnabled(1, league_item.league.second_round)

    def _set_add_score_btn(self):
        self._add_score_btn.setEnabled(self._is_valid_input())

    def _set_ui_list_item(self, list_type: ListType, list_item_1: QListWidgetItem) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.setCurrentItem(list_item_1)
            case ListType.DAY:
                self._day_list.setCurrentItem(list_item_1)
            case ListType.GAME:
                self._game_list.setCurrentItem(list_item_1)

    def _clear_ui_list(self, list_type: ListType) -> None:
        match list_type:
            case ListType.LEAGUE:
                self._league_list.clear()
                self._league_list_items.clear()
            case ListType.DAY:
                self._day_list.clear()
            case ListType.GAME:
                self._game_list.clear()

    def _get_current_league(self) -> LeagueListItem:
        return self._league_list.currentItem()

    def _get_current_day(self) -> DayListItem:
        return self._day_list.currentItem()

    def _get_current_game(self) -> GameOutput:
        if self._current_game is not None:
            return self._current_game
        else:
            league_item: LeagueListItem = self._get_current_league()
            return league_item.league.next_game

    def _is_valid_input(self) -> bool:
        return False


window: MainWindow | None = None


def create_main_window(initial_input: tuple):
    global window
    window = MainWindow(initial_input=initial_input)
