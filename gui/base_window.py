# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

import transition

window: QMainWindow | None = None


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_base_window_information()
        self._set_menu()

    def _set_base_window_information(self):
        self.setWindowIcon(QIcon("gui/Icons/main_icon.png"))

    def _set_menu(self):
        save_action: QAction = QAction(QIcon("gui/Icons/save_icon.png"), '&Speichern', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save)

        load_action: QAction = QAction(QIcon("gui/Icons/load_icon.png"), '&Laden', self)
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self._load)

        restart_action: QAction = QAction(QIcon("gui/Icons/restart_icon.png"), '&Neustart', self)
        restart_action.setShortcut("Ctrl+R")
        restart_action.triggered.connect(self._restart)

        close_action: QAction = QAction(QIcon("gui/Icons/quit_icon.png"), '&Schließen', self)
        close_action.triggered.connect(self._quit)

        menu_bar: QMenuBar = self.menuBar()

        file_menu: QMenu = menu_bar.addMenu("&Datei")
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(restart_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)

    def set_widget(self, widget):
        self.setCentralWidget(widget)

    def set_status_bar(self, massage: str):
        self.statusBar().showMessage("Info: " + massage, 5000)

    def _save(self):
        self.set_status_bar("Im Input Window kann nicht gespeichert werden.")

    def _load(self):
        self.load()

    def _restart(self):
        if self._get_restart_commit():
            self.restart()

    def _quit(self):
        if self._get_close_commit():
            qApp.quit()

    def load(self):
        transition.crate_save_directory()
        file_name, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                       "saves", "KickerRechner(*.json)")
        if check:
            transition.load(filename=file_name)
        else:
            self.set_status_bar("Kein Turnier geladen")

    @staticmethod
    def restart():
        transition.restart()

    @staticmethod
    def quit():
        qApp.quit()

    def close_(self):
        self.close()

    def _get_close_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest du den KickerRechner schlißen?")
        msg.setInformativeText('Du kannst im InputWindow nicht speichen. '
                               'Starte das Tunier, wenn du vorher Speichern willst. '
                               'Du kannst deine Eingabe nächstes Mal nach dem Laden mit "Neustart" editieren.')
        msg.setWindowTitle("KickerRechner Beenden?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Ok

    def _get_restart_commit(self) -> bool:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setText("Möchtest das Turnier neu starten?")
        msg.setInformativeText('Du kannst im InputWindow nicht speichen. '
                               'Starte das Tunier, wenn du vorher Speichern willst. '
                               'Du kannst deine Eingabe nächstes Mal nach dem Laden mit "Neustart" editieren.')
        msg.setWindowTitle("Turnier Neustarten?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

        return retval == QMessageBox.Ok
