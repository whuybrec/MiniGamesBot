from minigamesbot import MiniGamesBot
from Other.private import Private
from Other.topgg import setup

TESTING = False

if TESTING: # for testing
    bot = MiniGamesBot("!")
    bot.run(Private.TOKENTEST)
else:
    bot = MiniGamesBot("?")
    setup(bot)
    bot.run(Private.TOKEN)
