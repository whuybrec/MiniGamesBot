from Other.variables import Variables
from Commands.discord_command import DiscordCommand

class BlackjackCommand(DiscordCommand):
    bot = None
    name = "blackjack"
    help = Variables.BJRULES
    brief = "Start a game of blackjack"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        # CONNECTION CLASS
        await cls.bot.game_manager.add_game(context, "blackjack", context.author.id)
