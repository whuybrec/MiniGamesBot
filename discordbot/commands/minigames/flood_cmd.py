from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class FloodCommand(Command):
    bot = None
    name = "flood"
    help = "Get the grid to turn into one color by iteratively flooding it, check out the rules with the rules command."
    brief = "Get the grid to turn into one color by iteratively flooding it."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **flood** minigame")

        await GameManager.create_session(message, "flood", context.author)
