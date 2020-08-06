from Other.variables import Variables
from Commands.discord_command import DiscordCommand

class HangmanCommand(DiscordCommand):
    bot = None
    name = "hangman"
    help = Variables.BJRULES
    brief = "Start a game of hangman"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        # CONNECTION CLASS
        await cls.bot.game_manager.add_game(context, "hangman", context.author.id)
