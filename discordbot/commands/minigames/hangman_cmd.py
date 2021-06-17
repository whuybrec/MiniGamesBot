from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class HangmanCommand(Command):
    bot = None
    name = "hangman"
    help = "Play hangman against the bot, check out the rules with the rules command."
    brief = "Play hangman against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **hangman** minigame")

        await GameManager.create_session(message, "hangman", context.author)
