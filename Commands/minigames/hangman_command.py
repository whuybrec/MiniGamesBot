from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from Minigames.hangman import HangMan

class HangmanCommand(DiscordCommand):
    bot = None
    name = "hangman"
    help = Variables.BJRULES
    brief = "Start a game of hangman"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of Hangman...")
        tmp = HangMan(cls.bot, "hangman", msg, context.author.id)
        await tmp.start_game()