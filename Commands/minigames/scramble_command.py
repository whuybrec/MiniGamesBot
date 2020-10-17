from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from Minigames.scramble import Scramble

class ScrambleCommand(DiscordCommand):
    bot = None
    name = "scramble"
    help = Variables.SCRULES
    brief = "Start a game of scramble"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of Scramble...")
        tmp = Scramble(cls.bot, "scramble", msg, context.author.id)
        await tmp.start_game()