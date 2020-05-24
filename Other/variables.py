from Other import scheduler
import random
import datetime
import time
import json
from Other.private import Private

games_names_short = ["hm", "c4", "sc", "gw", "bj", "qz"]
game_names = ["hangman", "connect4", "scramble", "guessword", "blackjack", "quiz"]
randwords = list()

class Variables:
    EXTRA = ""
    DEADLINE = 600 * 2
    scheduler = scheduler.Scheduler()
    eng_dict = None
    questions_dict = None

    game_names = ["hangman", "connect4", "scramble", "guessword", "blackjack", "quiz"]

    amtPlayedGames = {game_names[i]: 0 for i in range(len(game_names))}
    history = list()

    games_names_short = ["hm", "c4", "sc", "gw", "bj", "qz"]

    quiz_categories = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]


    SPLIT_EMOJI = "↔️"
    INC_EMOJI1 = "⬆️"
    INC_EMOJI2 = "⏫"
    STOP_EMOJI = "❌"
    BACK_EMOJI = "◀"
    NEXT_EMOJI = "➡️"
    DICT_ALFABET = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭',
                          'i': '🇮', 'j': '🇯',
                          'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷',
                          's': '🇸', 't': '🇹',
                          'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}  # letter: emoji
    NUMBERS = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    REACTIONS_CONNECT4 = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

    HANGMAN0 = ""

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
               " |  /|\ \n" \
               " |\n" \
               "_|_ _ _"

    HANGMAN9 = " _____\n" \
               " |/  |\n" \
               " |   o\n" \
               " |  /|\ \n" \
               " |  /\n" \
               "_|_ _ _"

    HANGMAN10 = " _____\n" \
                " |/  |\n" \
                " |   o\n" \
                " |  /|\ \n" \
                " |  / \ \n" \
                "_|_ _ _"

    hangmen = [HANGMAN0, HANGMAN1, HANGMAN2, HANGMAN3, HANGMAN4, HANGMAN5, HANGMAN6, HANGMAN7, HANGMAN8, HANGMAN9, HANGMAN10]

    BJRULES = "Ace is worth either 1 or 11 points.\n" \
              "Jack, Queen and King are worth 10 points.\n" \
              "The other cards are worth their number.\n" \
              "If the first two cards are the same, the player can choose to split their hand.\n" \
              "If the player chooses to split, then he or she can play the rest of the game with 2 hands.\n" \
              "If the player has 21 points from the start, he or she has BlackJack.\n" \
              "The dealer (bot) has one card open untill the player is done playing.\n" \
              "The dealer stops asking for cards as soon as it gets passed 17 points (included).\n" \
              "The player wins the game when he or she has a higher score than the dealer but below 21 (included).\n" \
              "The player draws with the dealer if they both end up with the same number of points.\n" \
              "In all other cases the player loses.\n" \
              "Press the indicated reactions on the message to make your move.\n" \
              "Press " + STOP_EMOJI + " to close the game.\n"
    C4RULES = "Who starts is chosen randomly.\n" \
              "You can only play when it is your turn.\n" \
              "A player wins when there are 4 coins of his or hers color diagonally/horizontally/vertically next to eachother.\n" \
              "Press the indicated reactions on the message to make your move.\n"
    GWRULES = "Guess the word from the given definition.\n" \
              "Press the indicated reactions on the message to make your move.\n" \
              "Press " + STOP_EMOJI + " to close the game.\n"
    HMRULES = "Try to guess the hidden word.\n" \
              "There are only lowercase letters in the word.\n" \
              "Press the indicated reactions on the message to make your move.\n" \
              "Press " + STOP_EMOJI + " to close the game.\n"
    SCRULES = "Try to unscramble the letters that the bot scrambled.\n" \
              "Press the indicated reactions on the message to make your move.\n" \
              "Press " + STOP_EMOJI + " to close the game.\n"
    QZRULES = "Try to give the correct answer to the questions.\n" \
              "Questions are always multiple choice and have 4 possible answers.\n" \
              "Only one answer is the correct one.\n" \
              "There are different categories available.\n" \
              "You can get a new question after answering the previous one with " + NEXT_EMOJI + ".\n" \
              "Press the indicated reactions on the message to make your move.\n" \
              "Press " + STOP_EMOJI + " to close the game.\n"

def on_startup():
    global randwords
    json1_file = open('Data/dictionary.json')
    json1_str = json1_file.read()
    Variables.eng_dict = json.loads(json1_str)
    json1_file.close()

    json1_file = open('Data/questions.json')
    json1_str = json1_file.read()
    Variables.questions_dict = json.loads(json1_str)
    json1_file.close()

    json1_file = open('Data/prefixes.json')
    json1_str = json1_file.read()
    Private.prefixes = json.loads(json1_str)
    json1_file.close()

    with open("Data/10k words.txt") as f:
        randwords = f.readlines()
    f.close()

def getRandomWord():
    global randwords
    return randwords[random.randint(0,5458)].rstrip()

def get_next_midnight_stamp():
    datenow = datetime.date.today() + datetime.timedelta(days=1)
    unix_next = datetime.datetime(datenow.year, datenow.month, datenow.day, 0)
    unixtime = time.mktime(unix_next.timetuple())
    return unixtime

def increment_game(game):
    Variables.amtPlayedGames[game] = int(Variables.amtPlayedGames[game]) + 1