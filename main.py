from minigamesbot import MiniGamesBot
from Other.private import Private
from Other.topgg import setup_1

TESTING = False


if TESTING:  # for testing
    bot = MiniGamesBot("!")
    bot.run(Private.TOKENTEST)
else:
    bot = MiniGamesBot("?")
    setup_1(bot)
    bot.run(Private.TOKEN)
