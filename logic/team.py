# Purpur Tentakel
# 09.01.2022
# KickerRechner // Team

class Team:
    def __init__(self, name: str) -> None:
        self.name: str = name

        self.first_round_points: int = 0
        self.second_round_points: int = 0
        self.points: int = int()

        self.first_round_goals: int = 0
        self.second_round_goals: int = 0
        self.goals: int = int()

        self.first_round_counter_goals: int = 0
        self.second_round_counter_goals: int = 0
        self.counter_goals: int = int()

        self.first_round_wins: int = 0
        self.second_round_wins: int = 0
        self.wins: int = int()

        self.first_round_draw: int = 0
        self.second_round_draw: int = 0
        self.draw: int = int()

        self.first_round_loose: int = 0
        self.second_round_loose: int = 0
        self.loose: int = int()

    def set_total_values(self) -> None:
        self.points: int = self.first_round_points + self.second_round_points

        self.goals: int = self.first_round_goals + self.second_round_goals

        self.counter_goals: int = self.first_round_counter_goals + self.second_round_counter_goals

        self.wins: int = self.first_round_wins + self.second_round_wins

        self.draw: int = self.first_round_draw + self.second_round_draw

        self.loose: int = self.first_round_loose + self.second_round_loose
