from discordbot.commands.command import Command
from discordbot.user.variables import Variables
from minigames.Minigames.uno import Uno


class UnoCommand(Command):
    bot = None
    name = "uno"
    help = Variables.UNORULES
    brief = "Start a game of uno"
    args = "[@player2] ... [@player10]"
    category = "minigame"

    @classmethod
    async def handler(cls, context, *args):
        import re
        try:
            player_ids = re.findall(r'\d+', args[0])
            player_ids.append(context.author.id)
            player_ids = set(player_ids)
            players = [context.message.guild.get_member(int(p_id)) for p_id in player_ids]
        except:
            await cls.illegal_command(context)
            return

        if not 1 < len(players) < 11:
            await context.message.channel.send("Invalid command: minimum of 2 and maximum of 10 players allowed.")
            return

        msg = await context.channel.send("Starting a game of Uno...")
        tmp = Uno(cls.bot, "uno", msg, players)
        await tmp.start_game()
