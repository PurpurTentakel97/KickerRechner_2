# Purpur Tentakel
# 09.01.2022
# KickerRechner // Input Window
import sys

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QLabel, QLineEdit, QCheckBox, QPushButton
from gui.base_window import BaseWindow


class LeagueListItem(QListWidgetItem):
    def __init__(self, name: str, index: int):
        super().__init__()
        self.name: str = name
        self.index: int = index

        self._set_text()

    def _set_text(self):
        self.setText(self.name)

    def update_text(self, new_name: str):
        self.name = new_name
        self.setText(self.name)

    def update_index(self, index: int):
        self.index = index


class TeamListItem(QListWidgetItem):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

        self.set_text()

    def set_text(self):
        self.setText(self.name)

    def update_text(self, new_name: str):
        self.name = new_name
        self.setText(self.name)


class InputWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.leagues: list[LeagueListItem] = list()
        self.teams: list[list[TeamListItem]] = list()
        self._team_edit: bool = False

        self._set_window_information()
        self._create_initial_ui()

        self.show()

    def _create_initial_ui(self):
        # Left
        self._league_lb = QLabel()
        self._league_list = QListWidget()
        self._league_list.itemClicked.connect(self._set_current_league)

        # Right
        self._league_name_lb = QLabel()
        self._league_name_le = QLineEdit()
        self._league_name_le.textChanged.connect(self._edit_current_league_name)

        self._active_cb = QCheckBox()
        self._active_cb.setChecked(True)
        self._active_cb.toggled.connect(self._edit_current_league_active)
        self._second_round_cb = QCheckBox()
        self._second_round_cb.setChecked(True)
        self._second_round_cb.toggled.connect(self._edit_current_league_second_round)

        self._team_name_lb = QLabel()
        self._team_name_le = QLineEdit()

        self._add_team_btn = QPushButton()
        self._add_team_btn.pressed.connect(self._add_team_to_current_league)
        self._remove_team_btn = QPushButton()
        self._remove_team_btn.pressed.connect(self._remove_team_from_current_league)
        self._remove_all_teams_btn = QPushButton()
        self._remove_all_teams_btn.pressed.connect(self._remove_all_teams_from_current_league)

        self._teams_list_lb = QLabel()
        self._teams_list = QListWidget()
        self._teams_list.itemClicked.connect(self._set_current_team)

        # Bottom
        self._remove_all_leagues_btn = QPushButton()
        self._remove_all_leagues_btn.pressed.connect(self._remove_all_leagues)
        self._remove_league_btn = QPushButton()
        self._remove_league_btn.pressed.connect(self._remove_league)
        self._add_league_btn = QPushButton()
        self._add_league_btn.pressed.connect(self._add_league)

        self._start_btn = QPushButton()
        self._start_btn.pressed.connect(self._start)

    def _set_window_information(self):
        self.setWindowTitle("KickerRechner by Purpur Tentakel // Input Window")

    def _add_league(self):
        pass

    def _add_team_to_current_league(self):
        pass

    def _edit_current_league_name(self):
        pass

    def _edit_current_league_active(self):
        pass

    def _edit_current_league_second_round(self):
        pass

    def _remove_league(self):
        pass

    def _remove_all_leagues(self):
        pass

    def _remove_team_from_current_league(self):
        pass

    def _remove_all_teams_from_current_league(self):
        pass

    def _set_current_league(self):
        pass

    def _set_current_team(self):
        pass

    def _start(self):
        pass


window = InputWindow


def create_input_window():
    app = QApplication(sys.argv)
    global window
    window = InputWindow()
    app.exec_()
