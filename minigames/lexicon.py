import json
import random


class Lexicon:
    QUESTIONS = dict()
    WORDS = []

    @classmethod
    def on_startup(cls):
        f = open('bin/questions.json')
        cls.QUESTIONS = json.loads(f.read())
        f.close()

        with open("bin/10k words.txt") as f:
            cls.WORDS = f.readlines()
        f.close()

    @classmethod
    def get_random_word(cls):
        word = cls.WORDS[random.randint(0, len(cls.WORDS) - 1)].rstrip()
        while len(word) < 5:
            word = cls.WORDS[random.randint(0, len(cls.WORDS) - 1)].rstrip()
        return word
