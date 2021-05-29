from discordbot.variables import Variables
from discordbot.commands.command import Command
from games.Minigames.quizmaster import QuizMaster

class QuizCommand(Command):
    bot = None
    name = "quiz"
    help = Variables.BJRULES
    brief = "Start a quiz"
    args = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a Quiz...")
        tmp = QuizMaster(cls.bot, "quiz", msg, context.author.id)
        await tmp.start_game()