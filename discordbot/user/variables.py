TIMEOUT = 60*5
WIN = 0
LOSE = 1
DRAW = 2


class Variables:
    # database_file = "bin/user_statistics.db"

    quiz_categories = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]

    SPLIT_EMOJI = "↔️"
    INC_EMOJI1 = "⬆️"
    INC_EMOJI2 = "⏫"
    STOP_EMOJI = "❌"
    BACK_EMOJI = "◀"
    FORWARD_EMOJI = "▶️"
    REPEAT_EMOJI = "🔁"
    NEXT_EMOJI = "➡️"

    NUMBERS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    REACTIONS_CONNECT4 = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

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
    # json1_file = open('bin/prefixes.json')
    # json1_str = json1_file.read()
    # Private.prefixes = json.loads(json1_str)
    # json1_file.close()
    pass
