# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenuBar, QMenu, QFileDialog
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
        self.restart()

    @staticmethod
    def _quit():
        qApp.quit()

    def load(self):
        transition.crate_save_directory()
        file_name, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                       "saves", "KickerRechner(*.json)")
        if check:
            transition.load(filename=file_name)
        else:
            self.set_status_bar("Keine Datei geladen")

    @staticmethod
    def restart():
        print("restart")

    @staticmethod
    def quit():
        qApp.quit()

    def close_(self):
        self.close()
