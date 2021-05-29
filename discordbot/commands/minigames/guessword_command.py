from discordbot.variables import Variables
from discordbot.commands.command import Command
from games.Minigames.guessword import GuessWord

class GuesswordCommand(Command):
    bot = None
    name = "guessword"
    help = Variables.GWRULES
    brief = "Start a game of guessword"
    args = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of GuessWord...")
        tmp = GuessWord(cls.bot, "guessword", msg, context.author.id)
        await tmp.start_game()
