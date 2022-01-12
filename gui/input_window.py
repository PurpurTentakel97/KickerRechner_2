# Purpur Tentakel
# 09.01.2022
# KickerRechner // Input Window

import sys

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QLabel, QLineEdit, QCheckBox, QPushButton, \
    QHBoxLayout, QVBoxLayout, QMessageBox, QWidget
from PyQt5.QtGui import QColor

from gui.base_window import BaseWindow
from gui.enum_sheet import StartCheck

from logic import main_manager


class LeagueListItem(QListWidgetItem):
    def __init__(self, index: int) -> None:
        super().__init__()
        self.name: str = str()
        self.index: int = index
        self.active: bool = True
        self.second_round: bool = True

        self._set_text()

    def _set_text(self) -> None:
        self.setText("Liga " + str(self.index + 1))

    def update_text(self, new_name: str) -> None:
        self.name = new_name
        if len(self.name.strip()) == 0:
            self._set_text()
        else:
            self.setText(self.name)

    def update_index(self, index: int) -> None:
        self.index = index


class TeamListItem(QListWidgetItem):
    def __init__(self, name: str, index: int) -> None:
        super().__init__()
        self.name: str = name
        self.index: int = index

        self.set_text()

    def set_text(self) -> None:
        self.setText(self.name)

    def update_text(self, new_name: str) -> None:
        self.name = new_name
        self.setText(self.name)


class InputWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self.leagues: list[LeagueListItem] = list()
        self.teams: list[list[TeamListItem]] = list()

        self._is_team_edit: bool = False

        self._set_window_information()
        self._create_initial_ui()
        self._create_initial_league()
        self._set_initial_text()
        self._set_layout()

    def _create_initial_ui(self) -> None:
        self.widget = QWidget()

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
        self._team_name_le.returnPressed.connect(self._add_edit_team_by_enter)
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

    def _create_initial_league(self) -> None:
        league = LeagueListItem(len(self.leagues))
        self._league_list.addItem(league)
        self._league_list.setCurrentItem(league)
        self.leagues.append(league)
        self.teams.append(list())
        self._set_start_btn_bool()

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

        self.widget.setLayout(global_vbox)
        self.set_widget(self.widget)

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
        self._set_start_btn_bool()

    def _set_current_league_second_round(self) -> None:
        league: LeagueListItem = self._league_list.currentItem()
        if self._second_round_cb.isChecked():
            league.second_round = True
            league.setBackground(QColor('white'))
        else:
            league.second_round = False
            league.setBackground(QColor('light grey'))

    def _set_new_current_team_name(self) -> None:
        team: TeamListItem = self._teams_list.currentItem()
        name: str = self._team_name_le.text()
        if name == team.name:
            self.set_status_bar("Keine Änderung des Teamnamen %s." % name)
        team.update_text(name)
        self._team_name_le.clear()
        self._teams_list.setCurrentItem(None)
        self._set_is_team_edit(False)

    def _set_current_league(self) -> None:
        league: LeagueListItem = self._league_list.currentItem()
        self._set_is_team_edit(False)

        self._league_name_le.setText(league.name)
        self._league_name_le.setPlaceholderText("Liga " + str(league.index + 1))

        self._active_cb.setChecked(True if league.active else False)
        self._second_round_cb.setChecked(True if league.second_round else False)

        self._team_name_le.clear()
        self._teams_list.clear()

        self._remove_all_teams_btn.setEnabled(len(self.teams[league.index]) > 0)

        new_teams = list()
        for team in self.teams[league.index]:
            new_team: TeamListItem = TeamListItem(name=team.name, index=team.index)
            self._teams_list.addItem(new_team)
            new_teams.append(new_team)
        self.teams[league.index] = new_teams

    def _set_current_team(self, item: TeamListItem) -> None:
        self._set_is_team_edit(edit=True, team=item)

    def _set_is_team_edit(self, edit: bool, team: TeamListItem = None):
        if edit:
            self._is_team_edit = edit

            self._add_team_btn.setEnabled(False)
            self._remove_team_btn.setEnabled(True)
            self._edit_team_btn.setEnabled(True)

            self._team_name_lb.setText("Teamname bearbeiten:")
            self._team_name_le.setText(team.name)
            self._team_name_le.setPlaceholderText("Altes Team")

        else:
            self._is_team_edit = edit

            self._remove_team_btn.setEnabled(False)
            self._edit_team_btn.setEnabled(False)
            self._teams_list.setCurrentItem(None)

            self._team_name_lb.setText("Teamname:")
            self._team_name_le.setPlaceholderText("Neues Team")

    def _set_start_btn_bool(self) -> None:
        self._start_btn.setEnabled(self._is_valid_output())

    def _add_league(self) -> None:
        league = LeagueListItem(len(self.leagues))
        self._league_list.addItem(league)
        self.leagues.append(league)
        self.teams.append(list())
        self._league_list.setCurrentItem(league)
        self._set_current_league()
        self._set_start_btn_bool()

    def _add_team_to_current_league(self) -> None:
        team_name: str = self._team_name_le.text()
        current_league_index: int = self._league_list.currentItem().index
        if len(team_name.strip()) > 0:
            new_team: TeamListItem = TeamListItem(team_name.strip(), len(self.teams[current_league_index]))
            for team in self.teams[current_league_index]:
                if team.name == new_team.name:
                    self.set_status_bar("Team bereits vorhanden")
                    return
            self._teams_list.addItem(new_team)
            self.teams[current_league_index].append(new_team)
            self._team_name_le.clear()
            self._remove_all_teams_btn.setEnabled(True)
            self._set_start_btn_bool()

        else:
            self.set_status_bar("Kein Teamname vorhanden")

    def _add_edit_team_by_enter(self) -> None:
        team_name: str = self._team_name_le.text()
        if len(team_name.strip()) > 0:
            if self._is_team_edit:
                self._set_new_current_team_name()
                self._set_is_team_edit(False)
            else:
                self._add_team_to_current_league()
        else:
            self.set_status_bar("Kein Teamname vohanden")

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

    def _remove_league(self) -> None:
        if len(self.leagues) > 0:
            item: LeagueListItem = self._league_list.currentItem()
            self._league_list.takeItem(item.index)
            del self.teams[item.index]
            del self.leagues[item.index]
            self._update_league_index()
            if len(self.leagues) > 0:
                self._league_list.setCurrentItem(self.leagues[item.index - 1])
                self._set_current_league()
                for league in self.leagues:
                    league.update_text(league.name)
            else:
                self._create_initial_league()
                self._league_list.setCurrentItem(self.leagues[0])
                self._set_current_league()

            self._set_start_btn_bool()
        else:
            self.set_status_bar("keine Liga vorhanden")

    def _remove_all_leagues(self) -> None:
        if self._get_remove_all_leagues_commit():
            self.leagues.clear()
            self._league_list.clear()
            self.teams.clear()

            self._set_is_team_edit(False)

            self._create_initial_league()
            self._league_list.setCurrentItem(self.leagues[0])
            self._set_current_league()
            self._set_start_btn_bool()

    def _remove_team_from_current_league(self) -> None:
        current_team: TeamListItem = self._teams_list.currentItem()
        current_league_index: int = self._league_list.currentItem().index

        if len(self.teams[current_league_index]) > 0:
            self._teams_list.takeItem(self.teams[current_league_index].index(current_team))
            self.teams[current_league_index].remove(current_team)

            self._team_name_le.clear()

            self._set_is_team_edit(edit=False)
            self._update_team_index(current_league_index)

            if len(self.teams[current_league_index]) == 0:
                self._remove_all_teams_btn.setEnabled(False)

            self._set_start_btn_bool()

        else:
            self.set_status_bar("Keine Teams vorhanden")

    def _remove_all_teams_from_current_league(self) -> None:
        if self._get_remove_all_teams_commit():
            current_league_index: int = self._league_list.currentItem().index

            if len(self.teams[current_league_index]) > 0:
                self._teams_list.clear()
                self._team_name_le.clear()
                self.teams[current_league_index] = list()
                self._set_is_team_edit(edit=False)
                self._remove_all_teams_btn.setEnabled(False)
                self._set_start_btn_bool()

            else:
                self.set_status_bar("Keine Teams vorhanden")

    def _update_league_index(self) -> None:
        for index, league in enumerate(self.leagues):
            league.index = index

    def _update_team_index(self, league_index: int) -> None:
        for index, team in enumerate(self.teams[league_index]):
            team.index = index

    def _get_remove_all_leagues_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)

        msg.setText("Alle Ligen löschen?")
        msg.setInformativeText("Du bist dabei alle Ligen zu löschen. Dadurch gehen alle bisherigen Eingaben verloren!")
        msg.setWindowTitle("Löschen aller Ligen")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Ok

    def _get_remove_all_teams_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)

        msg.setText("Alle Teams dieser Liga löschen?")
        msg.setInformativeText("Du bist dabei alle Teams dieser Liga zu löschen. "
                               "Dadurch gehen alle bisherigen Team-Eingaben dieser Liga verloren!")
        msg.setWindowTitle("Löschen aller Teams der Liga")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Ok

    def _is_valid_output(self, start: StartCheck = StartCheck.CHECK) -> bool:
        # check if league
        if len(self.leagues) == 0:
            if start == StartCheck.START:
                self.set_status_bar("Keine Liga vorhanden")
            return False

        # check if less than two teams per league
        for teams in self.teams:
            if len(teams) < 2:
                if start == StartCheck.START:
                    self.set_status_bar("Liga %s enthält nicht genügend Teams" % self.leagues[
                        self.teams.index(teams)].name)
                return False

        # check if any league is active
        league_active: bool = False
        for league in self.leagues:
            if league.active:
                league_active = True
                break
        if not league_active:
            if start == StartCheck.START:
                self.set_status_bar("keine aktive Liga")
            return False

        # is valid input
        return True

    def _start(self) -> None:
        # ([league_name:str, active:bool, second_round:bool, [teams:list[str]],[next league])
        if self._is_valid_output(start=StartCheck.START):
            output: list[list[str, bool, bool, list[str]]] = list()
            for league in self.leagues:
                team_output: list[str] = list()
                for team in self.teams[league.index]:
                    team_output.append(team.name)
                league_output: list[str, bool, bool, list[str]] = [
                    league.name if len(league.name) > 0 else "liga " + str(league.index + 1),
                    league.active, league.second_round, team_output
                ]
                output.append(league_output)
            self.close()
            main_manager.process_data_from_input_window(initial_input=tuple(output))


window = InputWindow


def create_input_window():
    app = QApplication(sys.argv)
    global window
    window = InputWindow()
    app.exec_()
