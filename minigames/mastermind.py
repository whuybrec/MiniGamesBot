import random

from minigames.minigame import Minigame

COLORS = ["blue", "red", "purple", "yellow", "green", "orange"]


class Mastermind(Minigame):
    def __init__(self):
        self.history = []
        self.code = list()
        while len(self.code) < 4:
            color = COLORS[random.randint(0, 5)]
            if color not in self.code:
                self.code.append(color)
        self.correct_place = 0
        self.wrong_place = 0
        self.lives = 10

    def guess(self, code):
        self.correct_place = 0
        self.wrong_place = 0
        for i in range(len(code)):
            if code[i] == self.code[i]:
                self.correct_place += 1
            elif code[i] in self.code:
                self.wrong_place += 1

        if not self.has_won():
            self.lives -= 1

        self.history.append([code, self.correct_place, self.wrong_place])

    def has_won(self):
        return self.correct_place == 4

    def has_drawn(self):
        pass

    def has_lost(self):
        return self.lives == 0
