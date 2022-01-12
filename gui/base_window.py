# Purpur Tentakel
# 09.01.2022
# KickerRechner // Base Window

from PyQt5.QtWidgets import QMainWindow, QWidget


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def set_widget(self, widget):
        self.setCentralWidget(widget)

    def set_status_bar(self, massage: str):
        self.statusBar().showMessage("Info: " + massage, 5000)
