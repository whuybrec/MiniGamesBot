from Other.variables import Variables
from Commands.discord_command import DiscordCommand

class GuesswordCommand(DiscordCommand):
    bot = None
    name = "guessword"
    help = Variables.GWRULES
    brief = "Start a game of guessword"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        # CONNECTION CLASS
        await cls.bot.game_manager.add_game(context, "guessword", context.author.id)
