from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class BlackjackCommand(Command):
    bot = None
    name = "blackjack"
    help = "Play a game of blackjack against the bot as dealer, check out the rules with the rules command."
    brief = "Play a game of blackjack against the bot as dealer."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **blackjack** minigame")

        await GameManager.create_session(message, "blackjack", context.author)
