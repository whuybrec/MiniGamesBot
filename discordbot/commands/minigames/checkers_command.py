from discordbot.commands.command import Command
from discordbot.utils.variables import Variables
from minigames.Minigames.checkers.checkers import Checkers


class CheckersCommand(Command):
    bot = None
    name = "checkers"
    help = Variables.CHECKERSRULES
    brief = "Start a game of checkers."
    args = "[@player2]"
    category = "minigame"
    open_games = dict()

    @classmethod
    async def handler(cls, context, *args):
        import re
        try:
            p_id = int(re.findall(r'\d+', args[0])[0])
            player2 = context.message.guild.get_member(p_id)
        except:
            await cls.illegal_command(context)
            return

        if context.author.id != p_id:
            players = [context.author, player2]
            if context.channel.id in cls.open_games.keys():
                if not cls.open_games[context.channel.id].terminated:
                    await context.message.channel.send("There can only be one open checkers game per channel. "
                                           "Finish the previous one before starting a new one or "
                                           "consider going to a different channel.")
                    return
            msg = await context.channel.send("Starting a game of Checkers...")
            cls.open_games[context.channel.id] = Checkers(cls.bot, "checkers", msg, players)
            await cls.open_games[context.channel.id].start_game()
        else:
            await cls.illegal_command(context)




