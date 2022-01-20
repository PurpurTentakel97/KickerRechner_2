# Purpur Tentakel
# 12.01.2022
# KickerRechner // Main Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTableWidget, \
    QTableWidgetItem, QTabWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QAbstractItemView, QMessageBox, QFileDialog
from PyQt5.QtGui import QIntValidator

import transition
from gui.base_window import BaseWindow
from gui.enum_sheet import ListType, TableType, StartCheck
from gui import base_window


class LeagueListItem(QListWidgetItem):
    def __init__(self, index: int, league_name: str, league) -> None:
        super().__init__()
        self.index: int = index
        self.league: transition.LeagueInput = league
        self.league_name: str = league_name
        self.first_round_games: list[transition.GameInput] = list()
        self.second_round_games: list[transition.GameInput] = list()

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
            self.setText(self.game_name + "   //   " + str(self.score_team_1) + "  :  " + str(self.score_team_2))
        else:
            self.setText(self.game_name)

    def update_text(self) -> None:
        self._create_text()


class ResultOutput:
    def __init__(self, league_name: str, team_name_1: str, team_name_2: str, team_score_1: int, team_score_2: int,
                 first_round: bool, finished: bool) -> None:
        self.league_name: str = league_name
        self.team_name_1: str = team_name_1
        self.team_name_2: str = team_name_2
        self.team_score_1: int = team_score_1
        self.team_score_2: int = team_score_2
        self.first_round: bool = first_round
        self.finished: bool = finished


class MainWindow(BaseWindow):
    def __init__(self, initial_input: tuple, finished: bool) -> None:
        super().__init__()
        self._leagues = initial_input
        self._league_list_items: list[LeagueListItem] = list()
        self._current_game: transition.GameInput | None = None
        self._next_league_index: int = 0
        self.finished: bool = finished

        self._create_initial_ui()
        self._create_initial_text()
        self._create_initial_layout()
        self.set_window_information()

        self._create_leagues()
        self._set_league()
        if self.finished:
            self._display_finished()

    def _create_initial_ui(self) -> None:
        self.widget = QWidget()

        # Top Left
        self._league_lb: QLabel = QLabel()
        self._league_list: QListWidget = QListWidget()
        self._league_list.itemClicked.connect(self._set_league)

        # Top Right games
        self._first_round_btn: QPushButton = QPushButton()
        self._first_round_btn.clicked.connect(lambda x: self._set_round(first_round=True))
        self._second_round_btn: QPushButton = QPushButton()
        self._second_round_btn.clicked.connect(lambda x: self._set_round(first_round=False))

        self._day_list: QListWidget = QListWidget()
        self._day_list.itemClicked.connect(self._set_day)
        self._game_list: QListWidget = QListWidget()
        self._game_list.itemClicked.connect(self._set_game)

        # Top Right next game
        self._next_game_lb: QLabel = QLabel()
        self._team_1_lb: QLabel = QLabel()
        self._team_2_lb: QLabel = QLabel()
        self._score_1_le: QLineEdit = QLineEdit()
        self._score_1_le.setValidator(QIntValidator())
        self._score_1_le.setMaxLength(3)
        self._score_1_le.textChanged.connect(self._set_add_score_btn)
        self._score_1_le.returnPressed.connect(self._add_entry_return)
        self._score_2_le: QLineEdit = QLineEdit()
        self._score_2_le.setValidator(QIntValidator())
        self._score_2_le.setMaxLength(3)
        self._score_2_le.textChanged.connect(self._set_add_score_btn)
        self._score_2_le.returnPressed.connect(self._add_entry_return)
        self._add_score_btn: QPushButton = QPushButton()
        self._add_score_btn.setEnabled(False)
        self._add_score_btn.clicked.connect(lambda x: self._add_entry(StartCheck.START))

        # Bottom
        self._table_lb: QLabel = QLabel()
        self._table_tabs: QTabWidget = QTabWidget()
        self._first_round_table: QTableWidget = QTableWidget()
        self._first_round_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._second_round_table: QTableWidget = QTableWidget()
        self._second_round_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._total_table: QTableWidget = QTableWidget()
        self._total_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

        self.showMaximized()

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
        current_game: transition.GameInput = self._get_current_game()

        if first_round:
            games: list[transition.GameInput] = league_item.first_round_games
        else:
            games: list[transition.GameInput] = league_item.second_round_games

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

    def _create_games(self) -> None:
        self._clear_ui_list(ListType.GAME)
        league_item: LeagueListItem = self._get_current_league()
        day_item: DayListItem = self._get_current_day()
        current_game: transition.GameInput = self._get_current_game()

        if day_item.first_round:
            games: list[transition.GameInput] = league_item.first_round_games
        else:
            games: list[transition.GameInput] = league_item.second_round_games

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

    def set_window_information(self) -> None:
        self.setWindowTitle("KickerRechner")

    def _set_league(self) -> None:
        print(self.finished)
        if not self.finished:
            self._current_game: transition.GameInput | None = None
        else:
            league_item: LeagueListItem = self._league_list.currentItem()
            self._current_game = league_item.league.all_games[0]

        current_game: transition.GameInput = self._get_current_game()
        self._create_days(current_game.first_round)
        self._create_games()
        self._set_next_game()
        self._set_second_round()
        self._set_tables(TableType.FIRST)
        self._set_tables(TableType.SECOND)
        self._set_tables(TableType.TOTAL)

    def _set_round(self, first_round: bool) -> None:
        day_set: bool = self._create_days(first_round=first_round)
        if day_set:
            self._create_games()

        if first_round:
            self._first_round_btn.setStyleSheet("background-color: light grey")
            self._second_round_btn.setStyleSheet("background-color: white")
        else:
            self._first_round_btn.setStyleSheet("background-color: white")
            self._second_round_btn.setStyleSheet("background-color: light grey")

    def _set_day(self) -> None:
        self._create_games()

    def _set_game(self) -> None:
        league_item: LeagueListItem = self._get_current_league()
        game_item: GameListItem = self._game_list.currentItem()
        for game in league_item.league.all_games:
            if game.game_name == game_item.game_name:
                self._current_game = game
                break
        self._set_next_game()

    def _set_next_game(self) -> None:
        self._score_1_le.clear()
        self._score_2_le.clear()
        current_game: transition.GameInput = self._get_current_game()

        self._team_1_lb.setText(current_game.team_1_name + ":")
        self._team_2_lb.setText(current_game.team_2_name + ":")
        self._score_1_le.setPlaceholderText("Tore: " + current_game.team_1_name)
        self._score_2_le.setPlaceholderText("Tore: " + current_game.team_2_name)

        if current_game.finished:
            self._next_game_lb.setText("Spiel beartbeiten:")
            self._add_score_btn.setText("Ergebnis aktualisieren")
            self._score_1_le.setText(str(current_game.score_team_1))
            self._score_2_le.setText(str(current_game.score_team_2))
        else:
            self._next_game_lb.setText("Nächstes Spiel:")
            self._add_score_btn.setText("Ergebnis eintragen")

        self._set_add_score_btn()
        self._set_focus()

    def _set_second_round(self) -> None:
        league_item: LeagueListItem = self._get_current_league()
        current_game: transition.GameInput = self._get_current_game()

        if not league_item.league.second_round and self._table_tabs.currentIndex() == 1:
            self._table_tabs.setCurrentIndex(0)

        self._table_tabs.setTabEnabled(1, league_item.league.second_round)
        self._second_round_btn.setEnabled(league_item.league.second_round)

        if current_game.first_round:
            self._first_round_btn.setStyleSheet("background-color: light grey")
            self._second_round_btn.setStyleSheet("background-color: white")
            if not self._table_tabs.currentIndex() == 2:
                self._table_tabs.setCurrentIndex(0)
        else:
            self._first_round_btn.setStyleSheet("background-color: white")
            self._second_round_btn.setStyleSheet("background-color: light grey")
            if not self._table_tabs.currentIndex() == 2:
                self._table_tabs.setCurrentIndex(1)

    def _set_tables(self, table_type: TableType) -> None:
        league_item: LeagueListItem = self._get_current_league()

        dummy_list: tuple[list] | None = None
        dummy: QTableWidget | None = None
        match table_type:
            case TableType.FIRST:
                dummy_list: tuple[list] = league_item.league.first_round_table
                dummy: QTableWidget = self._first_round_table
            case TableType.SECOND:
                if not league_item.league.second_round:
                    return
                dummy_list: tuple[list] = league_item.league.second_round_table
                dummy: QTableWidget = self._second_round_table
            case TableType.TOTAL:
                dummy_list: tuple[list] = league_item.league.total_table
                dummy: QTableWidget = self._total_table

        dummy.clear()
        dummy.setRowCount(len(dummy_list))
        dummy.setColumnCount(len(dummy_list[0]))

        for row, _ in enumerate(dummy_list):
            for column, item in enumerate(dummy_list[row]):
                dummy.setItem(row, column, QTableWidgetItem(item))
        dummy.update()

    def _set_add_score_btn(self) -> None:
        self._add_score_btn.setEnabled(self._is_valid_input())

    def _set_focus(self) -> None:
        if len(self._score_1_le.text().strip()) == 0:
            self._score_1_le.setFocus()
        elif len(self._score_1_le.text().strip()) != 0 and len(self._score_2_le.text().strip()) != 0:
            self._score_1_le.setFocus()
        else:
            self._score_2_le.setFocus()

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

    def _get_current_game(self):
        if self._current_game is not None:
            return self._current_game
        else:
            league_item: LeagueListItem = self._get_current_league()
            return league_item.league.next_game

    def _is_valid_input(self, check: StartCheck = StartCheck.CHECK) -> bool:
        current_game: transition.GameInput = self._get_current_game()

        text: str = self._score_1_le.text()
        if len(text.strip()) == 0:
            if check == StartCheck.START:
                self.set_status_bar("Team %s hat keinen Eintrag" % current_game.team_1_name)
                self._score_1_le.setFocus()
            return False
        if not text.isdigit():
            if check == StartCheck.START:
                self.set_status_bar("%s ist keine valide Zahl" % text)
                self._score_1_le.setFocus()
            return False

        text: str = self._score_2_le.text()
        if len(text.strip()) == 0:
            if check == StartCheck.START:
                self.set_status_bar("Team %s hat keinen Eintrag" % current_game.team_2_name)
                self._score_2_le.setFocus()
            return False
        if not text.isdigit():
            if check == StartCheck.START:
                self.set_status_bar("%s ist keine valide Zahl" % text)
                self._score_2_le.setFocus()
            return False

        return True

    def _add_entry_return(self) -> None:
        self._add_entry(StartCheck.START)

    def _add_entry(self, start_check: StartCheck) -> None:
        if self._is_valid_input(start_check):
            league_item: LeagueListItem = self._get_current_league()
            current_game = self._get_current_game()
            team_score_1: int = int(self._score_1_le.text())
            team_score_2: int = int(self._score_2_le.text())
            output: ResultOutput = ResultOutput(league_name=league_item.league_name,
                                                team_name_1=current_game.team_1_name,
                                                team_name_2=current_game.team_2_name, team_score_1=team_score_1,
                                                team_score_2=team_score_2, first_round=current_game.first_round,
                                                finished=current_game.finished)
            if current_game.finished:
                if current_game.score_team_1 == team_score_1 and current_game.score_team_2 == team_score_2:
                    self.set_status_bar("Keine Änderung vorgenommen")
            transition.put_main_window_data_to_logic(output_=output)

    def _display_finished(self) -> None:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Turnier Beendet")
        msg.setInformativeText("Das Turnier ist beendet. Du kannst dir noch alle Tabellen und Ergebnisse angucken. "
                               "Wenn Bedarf besteht kannst du auch noch Ergebnisse ändern")
        msg.setWindowTitle("Turnier Beendet")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def update_data(self, update_input: tuple, next_league_index: int, finished: bool) -> None:
        self.finished: bool = finished
        self._next_league_index: int = next_league_index
        self._leagues: tuple = update_input
        self._create_leagues()
        self._set_league()
        if self.finished:
            self._display_finished()

    def _save(self) -> None:
        transition.crate_save_directory()
        file_name, check = QFileDialog.getSaveFileName(None, "Turnier speichern",
                                                       "saves", "KickerRechner(*.json)")
        if check:
            transition.save(filename=file_name)
        else:
            self.set_status_bar("Nicht gespeichert")

    def _load(self) -> None:
        if self._get_save_bool():
            self._save()
        self.load()

    def _load_autosave(self) -> None:
        if self.get_load_autosave_commit():
            if self._get_save_bool():
                self._save()
            self.load_autosave()

    def _restart(self) -> None:
        if self._get_restart_commit():
            if self._get_save_bool():
                self._save()
            self.restart()

    def _quit(self) -> None:
        if self._get_close_commit():
            if self._get_save_bool():
                self._save()
            self.quit()

    def _get_save_bool(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)

        msg.setText("Möchtest du Speichern?")
        msg.setInformativeText("Deine Daten gehen verloren, wenn du nicht speicherst.")
        msg.setWindowTitle("Speichern?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        return retval == QMessageBox.Yes

    def _get_close_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest du den KickerRechner schlißen?")
        msg.setWindowTitle("KickerRechner Beenden?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Yes

    def _get_restart_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest das Turnier neu starten?")
        msg.setInformativeText('Möchtest du das Turnier neu starten?'
                               'Es wird sich das Import-Window mit deiner Eingabe öffnen.')
        msg.setWindowTitle("Turnier Neustarten?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Yes


window: MainWindow | None = None


def create_main_window(initial_input: tuple, finished: bool) -> None:
    global window
    window = MainWindow(initial_input=initial_input, finished=finished)
    base_window.window = window
