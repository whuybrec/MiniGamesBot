from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from Minigames.quizmaster import QuizMaster

class QuizCommand(DiscordCommand):
    bot = None
    name = "quiz"
    help = Variables.BJRULES
    brief = "Start a quiz"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a Quiz...")
        tmp = QuizMaster(cls.bot, "quiz", msg, context.author.id)
        await tmp.start_game()