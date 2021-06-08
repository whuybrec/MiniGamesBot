from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.variables import *


RULES = {
    "blackjack": BLACKJACK_RULES,
    "chess": CHESS_RULES,
    "hangman": HANGMAN_RULES,
    "quiz": QUIZ_RULES,
    "scramble": SCRAMBLE_RULES,
    "connect4": CONNECT4_RULES,
    "flood": FLOOD_RULES,
    "mastermind": MASTERMIND_RULES,
    "akinator": AKINATOR_RULES
}


class RulesCommand(Command):
    bot = None
    name = "rules"
    help = "Shows the rules for the minigame given as argument to the command."
    brief = "Shows the rules for the given minigame."
    args = "minigame"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(args) == 0:
            await context.reply("Please specify a minigame for which you want to see the rules as argument.")
            return

        minigame = args.split(" ")[0].lower()
        try:
            rules = RULES[minigame]
            await context.reply(rules)
        except KeyError:
            await context.reply("Please specify a correct minigame for which you want to see the rules as argument.")

