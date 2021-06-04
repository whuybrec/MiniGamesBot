from discordbot.utils.emojis import SPLIT, STOP, ALPHABET, ARROW_LEFT_2

TIMEOUT = 60*5
WIN = 0
LOSE = 1
DRAW = 2

MINIGAMES = [
    "blackjack",
    "scramble",
    "hangman",
    "quiz",
    "connect4"
]

QUIZ_CATEGORIES = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]

BLACKJACK_RULES = f"**Blackjack**\n" \
                  f"{ALPHABET['h']} to ask for extra card ('hit').\n" \
                  f"{ALPHABET['s']} to signal that you have enough cards ('stand').\n" \
                  f"{SPLIT} to split your hand when both your cards are of the same rank at the start of the game.\n" \
                  f"{STOP} to end the game (automatically results in loss)."

CHESS_RULES = f"**Chess**\n" \
              f"Click letters and numbers to create your move.\n" \
              f"{STOP} to end the game (automatically results in loss for player who pressed it)."

CONNECT4_RULES = f"**Connect4**\n" \
                 f"Click a number to indicate the column for your coin.\n" \
                 f"{STOP} to end the game (automatically results in loss for player who pressed it)."

HANGMAN_RULES = f"**Hangman**\n" \
                f"Click letters to make your guess.\n" \
                f"{STOP} to end the game (automatically results in loss)."

QUIZ_RULES = f"**Quiz**\n" \
             f"There are 4 categories available: General Knowledge, Sports, Films, Music and Video Games.\n" \
             f"First select your category, then select the right answer for your question.\n" \
             f"{STOP} to end the game (automatically results in loss)."

SCRAMBLE_RULES = f"**Scramble**\n" \
                 f"Unscramble the given word by clicking on the letters in the correct order.\n" \
                 f"{ARROW_LEFT_2} to undo your last move.\n" \
                 f"{STOP} to end the game (automatically results in loss)."
