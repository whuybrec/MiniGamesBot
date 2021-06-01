from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.quiz_dc import QuizDisc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class QuizCommand(Command):
    bot = None
    name = "quiz"
    help = "Start a game of quiz in a category of you choice, check out the different categories with the rules command."
    brief = "Start a quiz."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting Quiz")

        session = Session(cls.bot, context, msg, "quiz", QuizDisc, [context.author])
        await GameManager.start_session(session)
