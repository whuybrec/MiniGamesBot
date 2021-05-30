from discord import Member

from discordbot.user.variables import Variables


class ChessManager:
    def __init__(self, bot):
        self.bot = bot

        self.bot.command(name="chess", brief="Start a game of chess", usage="[@player2]",
                         help=Variables.CHESSRULES)(self.chess_game)

    async def chess_game(self, context, p2: Member, *args):
        """Minigame handler to start a chess minigame."""
        if args:
            await context.message.channel.send("Invalid command to start chess game, try: \"?chess [@player2]\", "
                                               "and player2 being the other person to play with")
        elif context.author.id != p2.id:
            players = [context.author.id, p2.id]
            await self.bot.game_manager.add_game(context, "chess", players[0], players[1])
        else:
            await context.message.channel.send("Invalid command to start chess game, try: \"?chess [@player2]\", "
                                               "and player2 being the other person to play with")
