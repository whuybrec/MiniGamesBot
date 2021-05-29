from discordbot.variables import Variables
from discordbot.commands.command import Command
from games.Minigames.hangman import HangMan

class HangmanCommand(Command):
    bot = None
    name = "hangman"
    help = Variables.BJRULES
    brief = "Start a game of hangman"
    args = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of Hangman...")
        tmp = HangMan(cls.bot, "hangman", msg, context.author.id)
        await tmp.start_game()