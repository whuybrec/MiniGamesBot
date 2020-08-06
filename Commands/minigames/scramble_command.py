from Other.variables import Variables
from Commands.discord_command import DiscordCommand

class ScrambleCommand(DiscordCommand):
    bot = None
    name = "scramble"
    help = Variables.SCRULES
    brief = "Start a game of scramble"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        # CONNECTION CLASS
        await cls.bot.game_manager.add_game(context, "scramble", context.author.id)
