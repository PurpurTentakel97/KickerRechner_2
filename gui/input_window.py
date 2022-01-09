# Purpur Tentakel
# 09.01.2022
# KickerRechner // Input Window

import sys
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QLabel, QLineEdit, QCheckBox, QPushButton, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor

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
        self.setText("Liga " + str(self.index + 1))

    def update_text(self, new_name: str):
        self.name = new_name
        if len(self.name.strip(" ")) == 0:
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

        self._is_team_edit: bool = False

        self._set_window_information()
        self._create_initial_ui()
        self._crate_initial_league()
        self._set_initial_text()
        self._set_layout()

    def _create_initial_ui(self) -> None:
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
        self._active_cb.toggled.connect(self._set_current_league_active)
        self._second_round_cb = QCheckBox()
        self._second_round_cb.setChecked(True)
        self._second_round_cb.toggled.connect(self._set_current_league_second_round)

        self._team_name_lb = QLabel()
        self._team_name_le = QLineEdit()
        self._team_name_le.textChanged.connect(self._edit_current_team_name)
        self._edit_team_btn = QPushButton()
        self._edit_team_btn.setEnabled(False)
        self._edit_team_btn.pressed.connect(self._set_new_current_team_name)

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

    def _crate_initial_league(self) -> None:
        league = LeagueListItem(len(self.leagues))
        self._league_list.addItem(league)
        self._league_list.setCurrentItem(league)
        self.leagues.append(league)
        self.teams.append(list())

    def _set_initial_text(self) -> None:
        current_league: LeagueListItem = self._league_list.currentItem()
        # Left
        self._league_lb.setText("Ligen:")

        # Right
        self._league_name_lb.setText("Liagename:")
        self._league_name_le.setPlaceholderText("Liga " + str(current_league.index + 1))

        self._active_cb.setText("Liga Aktiv")
        self._second_round_cb.setText("Rückrunde Aktiv")

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

    def _set_layout(self) -> None:
        # Left
        league_list_lb_hbox = QHBoxLayout()
        league_list_lb_hbox.addWidget(self._league_lb)
        league_list_lb_hbox.addStretch()

        # League List

        leagues_vbox = QVBoxLayout()
        leagues_vbox.addLayout(league_list_lb_hbox)
        leagues_vbox.addWidget(self._league_list)

        # Right
        league_name_lb_hbox = QHBoxLayout()
        league_name_lb_hbox.addWidget(self._league_name_lb)
        league_name_lb_hbox.addStretch()

        # League LE

        cb_hbox = QHBoxLayout()
        cb_hbox.addWidget(self._active_cb)
        cb_hbox.addWidget(self._second_round_cb)
        cb_hbox.addStretch()

        team_name_lb_hbox = QHBoxLayout()
        team_name_lb_hbox.addWidget(self._team_name_lb)
        team_name_lb_hbox.addStretch()

        team_name_el_hbox = QHBoxLayout()
        team_name_el_hbox.addWidget(self._team_name_le)
        team_name_el_hbox.addWidget(self._edit_team_btn)

        team_btn_hbox = QHBoxLayout()
        team_btn_hbox.addWidget(self._add_team_btn)
        team_btn_hbox.addWidget(self._remove_team_btn)
        team_btn_hbox.addWidget(self._remove_all_teams_btn)
        team_btn_hbox.addStretch()

        team_list_lb_hbox = QHBoxLayout()
        team_list_lb_hbox.addWidget(self._teams_list_lb)
        team_list_lb_hbox.addStretch()

        # Team List

        right_vbox = QVBoxLayout()
        right_vbox.addLayout(league_name_lb_hbox)
        right_vbox.addWidget(self._league_name_le)
        right_vbox.addLayout(cb_hbox)
        right_vbox.addLayout(team_name_lb_hbox)
        right_vbox.addLayout(team_name_el_hbox)
        right_vbox.addLayout(team_btn_hbox)
        right_vbox.addLayout(team_list_lb_hbox)
        right_vbox.addWidget(self._teams_list)

        # Up
        up_hbox = QHBoxLayout()
        up_hbox.addLayout(leagues_vbox)
        up_hbox.addLayout(right_vbox)

        # Bottom
        bottom_hbox = QHBoxLayout()
        bottom_hbox.addWidget(self._add_league_btn)
        bottom_hbox.addWidget(self._remove_league_btn)
        bottom_hbox.addWidget(self._remove_all_leagues_btn)
        bottom_hbox.addStretch()
        bottom_hbox.addWidget(self._start_btn)

        # Global
        global_vbox = QVBoxLayout()
        global_vbox.addLayout(up_hbox)
        global_vbox.addLayout(bottom_hbox)

        self.setLayout(global_vbox)

        self.show()

    def _set_window_information(self) -> None:
        self.setWindowTitle("KickerRechner by Purpur Tentakel // Input Window")

    def _set_current_league_active(self) -> None:
        league: LeagueListItem = self._league_list.currentItem()
        if self._active_cb.isChecked():
            league.active = True
            league.setForeground(QColor('black'))
        else:
            league.active = False
            league.setForeground(QColor('grey'))

    def _set_current_league_second_round(self) -> None:
        league: LeagueListItem = self._league_list.currentItem()
        if self._second_round_cb.isChecked():
            league.second_round = True
            league.setBackground(QColor('white'))
        else:
            league.second_round = False
            league.setBackground(QColor('light grey'))

    def _set_new_current_team_name(self):
        pass

    def _add_league(self):
        pass

    def _add_team_to_current_league(self) -> None:
        team_name: str = self._team_name_le.text()
        current_league_index: int = self._league_list.currentItem().index
        if len(team_name.strip()) > 0:
            new_team: TeamListItem = TeamListItem(team_name.strip())
            for team in self.teams[current_league_index]:
                if team.name == new_team.name:
                    print("Team bereits vorhanden")  # TODO to UI
                    return
            self._teams_list.addItem(new_team)
            self.teams[current_league_index].append(new_team)
            self._team_name_le.clear()

        else:
            print("Kein Teamname vorhanden")  # TODO to UI

    def _edit_current_league_name(self) -> None:
        name: str = self._league_name_le.text()
        league: LeagueListItem = self._league_list.currentItem()
        league.update_text(name)

    def _edit_current_team_name(self) -> None:
        team_name: str = self._team_name_le.text()
        if len(team_name.strip()) == 0:
            self._add_team_btn.setEnabled(False)
            self._edit_team_btn.setEnabled(False)
        else:
            if self._is_team_edit:
                self._edit_team_btn.setEnabled(True)
            else:
                self._add_team_btn.setEnabled(True)

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
