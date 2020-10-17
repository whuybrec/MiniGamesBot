from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from Minigames.guessword import GuessWord

class GuesswordCommand(DiscordCommand):
    bot = None
    name = "guessword"
    help = Variables.GWRULES
    brief = "Start a game of guessword"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of GuessWord...")
        tmp = GuessWord(cls.bot, "guessword", msg, context.author.id)
        await tmp.start_game()
