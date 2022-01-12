# Purpur Tentakel
# 12.01.2022
# KickerRechner // Main Window

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QTableWidget, QTabWidget, \
    QHBoxLayout, QVBoxLayout, QGridLayout

from gui.base_window import BaseWindow


class MainWindow(BaseWindow):
    def __init__(self, initial_input: tuple):
        super().__init__()

        self._create_initial_ui()
        self._create_initial_text()
        self._create_initial_layout()

    def _create_initial_ui(self):
        self.widget = QWidget()

        # Top Left
        self._league_lb = QLabel()
        self._league_list = QListWidget()

        # Top Right games
        self._game_tabs = QTabWidget()
        self._first_day_game_hbox = QHBoxLayout()  # Hinrunde
        self._second_day_game_hbox = QHBoxLayout()  # Rückrunde
        self._add_tabs_to_game_tabs()

        self._first_day_list = QListWidget()
        self._first_game_list = QListWidget()
        self._second_day_list = QListWidget()
        self._second_game_list = QListWidget()

        # Top Right next game
        self._next_game_lb = QLabel()
        self._team_1_lb = QLabel()
        self._team_2_lb = QLabel()
        self._score_1_le = QLineEdit()
        self._score_2_le = QLineEdit()
        self._add_score_btn = QPushButton()

        # Bottom
        self._table_lb = QLabel()
        self._table_tabs = QTabWidget()
        self._first_round_table = QTableWidget()
        self._second_round_table = QTableWidget()
        self._total_table = QTableWidget()
        self._add_tabs_to_table_tabs()

    def _create_initial_text(self):
        # Top Left
        self._league_lb.setText("Ligen:")

        # Top Right games
        # no initial text

        # Top Right next game
        self._next_game_lb.setText("Nächstes Spiel:")
        self._team_1_lb.setText("Anita Becker - Anton Fritzen")
        self._team_2_lb.setText("Maria Müller - Herbert Haberich")
        self._score_1_le.setPlaceholderText("Score Team 1")
        self._score_2_le.setPlaceholderText("Score Team 2")
        self._add_score_btn.setText("Ergebnis hinzufügen")

    def _create_initial_layout(self):
        # Top Left
        league_lb_hbox = QHBoxLayout()
        league_lb_hbox.addWidget(self._league_lb)
        league_lb_hbox.addStretch()

        league_vbox = QVBoxLayout()
        league_vbox.addLayout(league_lb_hbox)
        league_vbox.addWidget(self._league_list)

        # Top Right games
        # game_tabs
        # created in UI
        self._first_day_game_hbox.addWidget(self._first_day_list)
        self._first_day_game_hbox.addWidget(self._first_game_list)

        # created in UI
        self._second_day_game_hbox.addWidget(self._second_day_list)
        self._second_day_game_hbox.addWidget(self._second_game_list)

        # Top Right next game
        next_game_lb_hbox = QHBoxLayout()
        next_game_lb_hbox.addWidget(self._next_game_lb)
        next_game_lb_hbox.addStretch()

        add_game_gl = QGridLayout()
        add_game_gl.addWidget(self._team_1_lb, 0, 0)

        add_game_gl.addWidget(QLabel("gegen"), 1, 0)
        add_game_gl.addWidget(self._team_2_lb, 2, 0)
        add_game_gl.addWidget(self._score_1_le, 0, 1)
        add_game_gl.addWidget(self._score_2_le, 2, 1)
        add_game_gl.addWidget(self._add_score_btn, 2, 2)

        add_game_hbox = QHBoxLayout()
        add_game_hbox.addLayout(add_game_gl)
        add_game_hbox.addStretch()

        top_right_vbox = QVBoxLayout()
        top_right_vbox.addWidget(self._game_tabs)
        top_right_vbox.addLayout(next_game_lb_hbox)
        top_right_vbox.addLayout(add_game_hbox)

        # Top
        top_hbox = QHBoxLayout()
        top_hbox.addLayout(league_vbox)
        top_hbox.addLayout(top_right_vbox)

        # Global
        global_vbox = QVBoxLayout()
        global_vbox.addLayout(top_hbox)
        global_vbox.addWidget(self._table_tabs)

        self.widget.setLayout(global_vbox)
        self.set_widget(widget=self.widget)

        self.show()

    def _add_tabs_to_game_tabs(self):
        first_widget = QWidget()
        first_widget.setLayout(self._first_day_game_hbox)
        self._game_tabs.addTab(first_widget, "Hinrunde")
        second_widget = QWidget()
        second_widget.setLayout(self._second_day_game_hbox)
        self._game_tabs.addTab(second_widget, "Rückrunde")

    def _add_tabs_to_table_tabs(self):
        self._table_tabs.addTab(self._first_round_table, "Hinrunde")
        self._table_tabs.addTab(self._second_round_table, "Rückrunde")
        self._table_tabs.addTab(self._total_table, "Gesamt")


window: MainWindow | None = None


def create_main_window(initial_input: tuple):
    global window
    window = MainWindow(initial_input=initial_input)
