import copy
from random import shuffle

from minigames.lexicon import Lexicon
from minigames.minigame import Minigame


class Scramble(Minigame):
    def __init__(self):
        word = list(Lexicon.get_random_word())
        self.word = word
        self.pointer = 0
        self.scrambled_word = copy.deepcopy(self.word)
        self.current_word = ["_" for i in self.word]
        shuffle(self.scrambled_word)

    def guess(self, char):
        if char not in self.scrambled_word:
            return
        self.scrambled_word.remove(char)
        self.current_word[self.pointer] = char
        self.pointer += 1

    def remove_last(self):
        if self.pointer - 1 < 0:
            return "_"

        self.pointer -= 1
        c = self.current_word[self.pointer]
        if c != "_":
            self.scrambled_word.append(self.current_word[self.pointer])
            self.current_word[self.pointer] = "_"
        return c

    def has_won(self):
        print("".join(self.word))
        print("".join(self.current_word))
        return "".join(self.word) == "".join(self.current_word)

    def has_lost(self):
        pass  # no lose condition in scramble

    def has_drawn(self):
        pass  # can't draw in scramble
