from discordbot.variables import Variables
from discordbot.commands.command import Command
from games.Minigames.scramble import Scramble

class ScrambleCommand(Command):
    bot = None
    name = "scramble"
    help = Variables.SCRULES
    brief = "Start a game of scramble"
    args = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of Scramble...")
        tmp = Scramble(cls.bot, "scramble", msg, context.author.id)
        await tmp.start_game()