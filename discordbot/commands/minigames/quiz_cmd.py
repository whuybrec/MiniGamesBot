from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.quiz_dc import QuizDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


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

        session = SinglePlayerSession(message, "quiz", QuizDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
