from Other.variables import Variables
from Commands.discord_command import DiscordCommand

class QuizCommand(DiscordCommand):
    bot = None
    name = "quiz"
    help = Variables.BJRULES
    brief = "Start a game of quiz"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        # CONNECTION CLASS
        await cls.bot.game_manager.add_game(context, "quiz", context.author.id)
