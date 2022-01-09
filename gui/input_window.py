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

        self._set_window_information()
        self._create_initial_ui()

        self.show()

    def _create_initial_ui(self):
        # Left
        self._league_lb = QLabel()
        self._league_list = QListWidget()

        # Right
        self._league_name_lb = QLabel()
        self._league_name_le = QLineEdit()

        self._active_cb = QCheckBox()
        self._active_cb.setChecked(True)
        self._second_round_cb = QCheckBox()
        self._second_round_cb.setChecked(True)

        self._team_name_lb = QLabel()
        self._team_name_le = QLineEdit()

        self._add_team_btn = QPushButton()
        self._remove_team_btn = QPushButton()
        self._remove_all_teams_btn = QPushButton()

        self._teams_list_lb = QLabel()
        self._teams_list = QListWidget()

        # Bottom
        self._remove_all_leagues_btn = QPushButton()
        self._remove_league_btn = QPushButton()
        self._add_league_btn = QPushButton()

        self._start_btn = QPushButton()

    def _set_window_information(self):
        self.setWindowTitle("KickerRechner by Purpur Tentakel // Input Window")


window = InputWindow


def create_input_window():
    app = QApplication(sys.argv)
    global window
    window = InputWindow()
    app.exec_()
