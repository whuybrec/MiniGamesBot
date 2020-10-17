from Other import scheduler
import random
import json
from Other.private import Private

class Variables:
    game_names = ["hangman", "connect4", "scramble", "guessword", "blackjack", "quiz", "uno", "chess"]
    database_file = "Data/user_statistics.db"

    EXTRA = "New MiniGame: CHESS! If you encounter any bugs/suggestions, " \
            "let me know on my github page or use the bug command!\n"

    TIMEOUT = 360
    scheduler = scheduler.Scheduler()
    eng_dict = None
    questions_dict = None
    randwords = list()

    games_names_short = ["hm", "c4", "sc", "gw", "bj", "qz", "uno", "chess"]

    quiz_categories = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]

    colors_uno = {"Blue": "🟦", "Green": "🟩", "Red": "🟥", "Yellow": "🟨"}
    white = {"White": "⬜"}

    SPLIT_EMOJI = "↔️"
    INC_EMOJI1 = "⬆️"
    INC_EMOJI2 = "⏫"
    STOP_EMOJI = "❌"
    BACK_EMOJI = "◀"
    FORWARD_EMOJI = "▶️"
    REPEAT_EMOJI = "🔁"
    NEXT_EMOJI = "➡️"
    DICT_ALFABET = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭',
                    'i': '🇮', 'j': '🇯',
                    'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷',
                    's': '🇸', 't': '🇹',
                    'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}  # letter: emoji
    NUMBERS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
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

    hangmen = [HANGMAN0, HANGMAN1, HANGMAN2, HANGMAN3, HANGMAN4,
               HANGMAN5, HANGMAN6, HANGMAN7, HANGMAN8, HANGMAN9, HANGMAN10]

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
              "A player wins when there are 4 coins of his or hers color " \
              "diagonally/horizontally/vertically next to eachother.\n" \
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
    UNORULES = "Every message you type in the bot DM will be visible to other players in the \"CHAT\" message.\n" \
               "Only the person who's turn it is can play.\n" \
               "Playable cards are marked with an emoji.\n" \
               "Match cards by color or value.\n" \
               "Wild cards and Wild Draw 4 cards can be played without matching color or value.\n" \
               "Press " + STOP_EMOJI + " to draw a card.\n" \
               "If you need to draw multiple cards, use " + INC_EMOJI2 + " to take cards.\n" \
               "After drawn a card, use " + NEXT_EMOJI + " to end turn.\n" \
               "When you have on card remaining type \"uno\" in chat." \
               "Players can type \"no uno\" in chat to catch someone not saying uno.\n" \
               "The rest of the rules are according to the official Uno rules.\n"
    CHESSRULES = "Start a game of chess with 2 players, one game per channel allowed.\n" \
                 "Making moves is done by typing the coordinates in the chat, for example: A7 to A5.\n" \
                 "Close the game by clicking on the " + STOP_EMOJI + " ."
    CHECKERSRULES = "Start a game of checkers (English draughts) with 2 players, one game per channel allowed.\n" \
                 "Making moves is done by typing the coordinates in the chat, for example: B6 to C5.\n" \
                 "Close the game by clicking on the " + STOP_EMOJI + " ."

def on_startup():
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
        Variables.randwords = f.readlines()
    f.close()

def get_random_word():
    word = Variables.randwords[random.randint(0,1524)].rstrip()
    while len(word) < 5:
        word = Variables.randwords[random.randint(0, 1524)].rstrip()
    return word

def convert(seconds: int):
    try:
        day = str(int(seconds // (24 * 3600)))
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        if hour < 10:
            hour = "0" + str(int(hour))
        else:
            hour = str(int(hour))
        seconds %= 3600
        minutes = seconds // 60
        if minutes < 10:
            minutes = "0" + str(int(minutes))
        else:
            minutes = str(int(minutes))
        seconds %= 60
        if seconds < 10:
            seconds = "0" + str(int(seconds))
        else:
            seconds = str(int(seconds))
        if day == "0":
            return "{0}:{1}:{2}".format(hour, minutes, seconds)
        return "{0} days {1}:{2}:{3}".format(day, hour, minutes, seconds)
    except:
        return "00:00:00"
