from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class ScrambleCommand(Command):
    bot = None
    name = "scramble"
    help = "Unscramble the letters of a random word, check out the rules with the rules command."
    brief = "Unscramble the letters of a random word."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **scramble** minigame")

        await GameManager.create_session(message, "scramble", context.author)
