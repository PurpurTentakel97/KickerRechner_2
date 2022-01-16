# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenuBar, QMenu
from PyQt5.QtGui import QIcon

import transition


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._set_base_window_information()
        self._set_menu()

    def _set_base_window_information(self):
        self.setWindowIcon(QIcon("gui/Icons/Icon.png"))

    def _set_menu(self):
        save_action: QAction = QAction(QIcon("gui/Icons/Icon.png"), '&Speichern', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save)

        load_action: QAction = QAction(QIcon("gui/Icons/Icon.png"), '&Laden', self)
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self._load)

        restart_action: QAction = QAction(QIcon("gui/Icons/Icon.png"), '&Neustart', self)
        restart_action.setShortcut("Ctrl+R")
        restart_action.triggered.connect(self._restart)

        close_action: QAction = QAction(QIcon("gui/Icons/Icon.png"), '&Schließen', self)
        close_action.setShortcut("Alt+F4")
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
        print("saved")
        transition.save(filename="Neues File")

    def _load(self):
        self._save()
        print("loaded")

    def _restart(self):
        self._save()
        print("restart")

    def _quit(self):
        self._save()
        qApp.quit()
