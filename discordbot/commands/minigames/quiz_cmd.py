from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class QuizCommand(Command):
    bot = None
    name = "quiz"
    help = "Answer a random question of a category of your choice, check out the different categories with the rules command."
    brief = "Answer a random question of a category of your choice."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **quiz**")

        await GameManager.create_session(message, "quiz", context.author)
