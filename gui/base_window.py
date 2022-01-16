# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_window_information()

    def set_window_information(self):
        self.setWindowIcon(QIcon("../gui/Icon.png"))

    def set_widget(self, widget):
        self.setCentralWidget(widget)

    def set_status_bar(self, massage: str):
        self.statusBar().showMessage("Info: " + massage, 5000)
