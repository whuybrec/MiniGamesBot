from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.quiz_dc import QuizDisc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class QuizCommand(Command):
    bot = None
    name = "quiz"
    help = "Answer a random question of a category of your choice, check out the different categories with the rules command."
    brief = "Answer a random question of a category of your choice."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **quiz**")

        session = Session(cls.bot, context, msg, "quiz", QuizDisc, [context.author])
        await GameManager.start_session(session)
