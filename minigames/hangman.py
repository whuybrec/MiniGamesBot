from minigames.lexicon import Lexicon
from minigames.minigame import Minigame


class Hangman(Minigame):
    def __init__(self):
        self.lives = 10
        self.word = list(Lexicon.get_random_word())
        self.current_word = ["_" for i in self.word]
        self.guessed = []

    def guess(self, char):
        if char in self.guessed:
            return

        if char not in self.word:
            self.lives -= 1
            self.guessed.append(char)
            return

        for i in range(len(self.word)):
            if self.word[i] == char:
                self.current_word[i] = char
        self.guessed.append(char)

    def has_won(self):
        return "_" not in self.current_word

    def has_lost(self):
        return self.lives <= 0

    def has_drawn(self):
        pass  # can't draw in hangman


HANGMAN0 = "_______"

HANGMAN1 = "  |\n" \
           "  |\n" \
           "  |\n" \
           "  |\n" \
           " _|_ _ _"

HANGMAN2 = " _____\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN3 = " _____\n" \
           " |/\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN4 = " _____\n" \
           " |/  |\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN5 = " _____\n" \
           " |/  |\n" \
           " |   0\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN6 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |   |\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN7 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\n" \
           " |\n" \
           "_|_ _ _"

HANGMAN8 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\\ \n" \
           " |\n" \
           "_|_ _ _"

HANGMAN9 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\\ \n" \
           " |  /\n" \
           "_|_ _ _"

HANGMAN10 = " _____\n" \
            " |/  |\n" \
            " |   o\n" \
            " |  /|\\ \n" \
            " |  / \\ \n" \
            "_|_ _ _"

HANGMEN = [HANGMAN10, HANGMAN9, HANGMAN8, HANGMAN7, HANGMAN6, HANGMAN5, HANGMAN4, HANGMAN3, HANGMAN2, HANGMAN1,
           HANGMAN0]
