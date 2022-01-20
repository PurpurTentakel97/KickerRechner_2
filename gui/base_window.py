# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

import webbrowser

import transition

window: QMainWindow | None = None


class BaseWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._set_base_window_information()
        self._set_menu()

    def _set_base_window_information(self) -> None:
        self.setWindowIcon(QIcon("assets/icons/main_icon.png"))

    def _set_menu(self) -> None:
        save_action: QAction = QAction(QIcon("assets/icons/save_icon.png"), '&Speichern', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save)

        load_action: QAction = QAction(QIcon("assets/icons/load_icon.png"), '&Laden', self)
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self._load)

        load_autosave_action: QAction = QAction(QIcon("assets/icons/load_autosave_icon.png"), '&Autosave laden', self)
        load_autosave_action.triggered.connect(self._load_autosave)

        restart_action: QAction = QAction(QIcon("assets/icons/restart_icon.png"), '&Neustart', self)
        restart_action.setShortcut("Ctrl+R")
        restart_action.triggered.connect(self._restart)

        about_action: QAction = QAction(QIcon("assets/icons/info_icon.png"), '&Infos', self)
        about_action.setShortcut("Ctrl+I")
        about_action.triggered.connect(self.about)

        close_action: QAction = QAction(QIcon("assets/icons/quit_icon.png"), '&Schließen', self)
        close_action.triggered.connect(self._quit)

        menu_bar: QMenuBar = self.menuBar()

        file_menu: QMenu = menu_bar.addMenu("&Datei")
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(load_autosave_action)
        file_menu.addSeparator()
        file_menu.addAction(restart_action)
        file_menu.addSeparator()
        file_menu.addAction(about_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)

    def set_widget(self, widget) -> None:
        self.setCentralWidget(widget)

    def set_status_bar(self, massage: str) -> None:
        self.statusBar().showMessage("Info: " + massage, 5000)

    def _save(self) -> None:
        self.set_status_bar("Im Input Window kann nicht gespeichert werden.")

    def _load(self) -> None:
        self.load()

    def _load_autosave(self) -> None:
        if self.get_load_autosave_commit():
            self.load_autosave()

    def _restart(self) -> None:
        if self._get_restart_commit():
            self.restart()

    def _quit(self) -> None:
        if self._get_close_commit():
            qApp.quit()

    def load(self) -> None:
        transition.crate_save_directory()
        file_name, check = QFileDialog.getOpenFileName(None, "Turnier laden",
                                                       "saves", "KickerRechner(*.json)")
        if check:
            transition.load(filename=file_name)
        else:
            self.set_status_bar("Kein Turnier geladen")

    @staticmethod
    def load_autosave() -> None:
        transition.load_autosave()

    @staticmethod
    def restart() -> None:
        transition.restart()

    def about(self) -> None:
        self._display_infos()

    @staticmethod
    def quit() -> None:
        qApp.quit()

    def close_(self) -> None:
        self.close()

    def get_load_autosave_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest den letzten Autosave laden?")
        msg.setInformativeText('Du kannst im InputWindow nicht speichen. '
                               'Starte das Tunier, wenn du vorher Speichern willst. '
                               'Du kannst deine Eingabe nächstes Mal nach dem Laden mit "Neustart" editieren.')
        msg.setWindowTitle("Letzten Autosave laden?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Yes

    def _get_restart_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest das Turnier neu starten?")
        msg.setInformativeText('Du kannst im InputWindow nicht speichen. '
                               'Starte das Tunier, wenn du vorher Speichern willst. '
                               'Du kannst deine Eingabe nächstes Mal nach dem Laden mit "Neustart" editieren.')
        msg.setWindowTitle("Turnier Neustarten?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Yes

    def _get_close_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest du den KickerRechner schlißen?")
        msg.setInformativeText('Du kannst im InputWindow nicht speichen. '
                               'Starte das Tunier, wenn du vorher Speichern willst. '
                               'Du kannst deine Eingabe nächstes Mal nach dem Laden mit "Neustart" editieren.')
        msg.setWindowTitle("KickerRechner Beenden?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Yes

    def _display_infos(self) -> None:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Infos:")
        msg.setInformativeText('PurpurTentakel \n'
                               'Python 3.10.\n'
                               'Der KickerRechner ist dafür gedacht ein Turnier durchzuführen.\n'
                               'Urprünglich entworfen für die zahlreichen KickerTurniere, wie wir veranstalten.\n'
                               'Bei Bugs gerne im Discord melden. THX.')
        msg.setWindowTitle("Infos")
        msg.addButton(QMessageBox.Ok)
        yes_button = msg.addButton('Discord', QMessageBox.YesRole)
        yes_button.clicked.connect(self.open_discord)

        retval = msg.exec_()

    @staticmethod
    def open_discord() -> None:
        webbrowser.open("https://discord.gg/JG5fsFZqEE")
