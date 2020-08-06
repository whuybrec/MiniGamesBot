from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from discord.member import Member

class ChessCommand(DiscordCommand):
    bot = None
    name = "chess"
    help = Variables.CHESSRULES
    brief = "Start a game of chess."
    usage = "[@player2]"
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args: Member, **kwargs):
        print(args)
        if len(args) > 1:
            await context.message.channel.send("Invalid command to start chess game, try: \"?chess [@player2]\", "
                                               "and player2 being the other person to play with")
        p2 = args[0]
        if context.author.id != p2.id:
            players = [context.author.id, p2.id]
            await cls.bot.game_manager.add_game(context, "chess", players[0], players[1])
        else:
            await context.message.channel.send("Invalid command to start chess game, try: \"?chess [@player2]\", "
                                               "and player2 being the other person to play with")

