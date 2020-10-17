from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from Minigames.blackjack import BlackJack

class BlackjackCommand(DiscordCommand):
    bot = None
    name = "blackjack"
    help = Variables.BJRULES
    brief = "Start a game of blackjack"
    usage = ""
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting a game of Blackjack...")
        tmp = BlackJack(cls.bot, "blackjack", msg, context.author.id)
        await tmp.start_game()