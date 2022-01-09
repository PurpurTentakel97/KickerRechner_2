# Purpur Tentakel
# 09.01.2022
# KickerRechner // Input Window

import sys

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QLabel, QLineEdit, QCheckBox, QPushButton
from gui.base_window import BaseWindow


class LeagueListItem(QListWidgetItem):
    def __init__(self, index: int):
        super().__init__()
        self.name: str = str()
        self.index: int = index
        self.active: bool = True
        self.second_round: bool = True

        self._set_text()

    def _set_text(self):
        self.setText("liga " + str(self.index + 1))

    def update_text(self, new_name: str):
        self.name = new_name
        if len(self.name) == 0:
            self._set_text()
        else:
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
        self._create_initial_team()
        self._set_initial_text()
        self._set_layout()

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
        self._edit_team_btn = QPushButton()
        self._edit_team_btn.setEnabled(False)

        self._add_team_btn = QPushButton()
        self._add_team_btn.setEnabled(False)
        self._add_team_btn.pressed.connect(self._add_team_to_current_league)
        self._remove_team_btn = QPushButton()
        self._remove_team_btn.setEnabled(False)
        self._remove_team_btn.pressed.connect(self._remove_team_from_current_league)
        self._remove_all_teams_btn = QPushButton()
        self._remove_all_teams_btn.setEnabled(False)
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
        self._start_btn.setEnabled(False)
        self._start_btn.pressed.connect(self._start)

    def _crate_initial_league(self):
        league = LeagueListItem(len(self.leagues) + 1)
        self._league_list.addItem(league)
        self._league_list.setCurrentItem(league)
        self.leagues.append(league)
        self.teams.append(list())

    def _set_initial_text(self):
        current_league: LeagueListItem = self._league_list.currentItem()
        # Left
        self._league_lb.setText("Ligen:")

        # Right
        self._league_name_lb.setText("Liagename:")
        self._league_name_le.setPlaceholderText("Liga" + str(current_league.index + 1))

        self._active_cb.setText("Aktiv")
        self._second_round_cb.setText("Aktiv")

        self._team_name_lb.setText("Teamname:")
        self._team_name_le.setPlaceholderText("Neues Team")
        self._edit_team_btn.setText("Teamname bearbeiten")

        self._add_team_btn.setText("Team hinzufügen")
        self._remove_team_btn.setText("Team entfernen")
        self._remove_all_teams_btn.setText("Alle Teams entfernen")

        self._teams_list_lb.setText("Teams:")

        # Bottom
        self._remove_all_leagues_btn.setText("Alle Ligen entfernen")
        self._remove_league_btn.setText("Liga entfernen")
        self._add_league_btn.setText("Liga hinzufügen")
        self._start_btn.setText("Turnier starten")

    def _set_layout(self):

        self.show()

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
