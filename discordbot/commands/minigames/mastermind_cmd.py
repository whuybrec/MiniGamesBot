from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class MastermindCommand(Command):
    bot = None
    name = "mastermind"
    help = "Play mastermind against the bot, check out the rules with the rules command."
    brief = "Play mastermind against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **mastermind** minigame")

        await GameManager.create_session(message, "mastermind", context.author)
