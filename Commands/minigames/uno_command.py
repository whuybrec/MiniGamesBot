from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from discord.member import Member

class UnoCommand(DiscordCommand):
    bot = None
    name = "uno"
    help = Variables.UNORULES
    brief = "Start a game of uno"
    usage = "[@player2] ... [@player10]"
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args: Member, **kwargs):
        players = set()
        for arg in args:
            players.add(arg)
        if len(players) != len(args):
            await context.message.channel.send("Invalid command: tag unique players to start uno game.")
            return
        players.add(cls.bot.get_user(context.author.id))
        if not 1 < len(players) < 11:
            await context.message.channel.send("Invalid command: minimum of 2 and maximum of 10 players allowed.")
            return
        await cls.bot.game_manager.add_game(context, "uno", list(players))
