from Other.variables import Variables
from Commands.discord_command import DiscordCommand
from discord.member import Member
from Minigames.connect4 import Connect4


class Connect4Command(DiscordCommand):
    bot = None
    name = "connect4"
    help = Variables.C4RULES
    brief = "Start a game of connect4."
    usage = "[@player2]"
    category = "minigame"

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
            msg = await context.channel.send("Starting a game of Connect4...")
            tmp = Connect4(cls.bot, "connect4", msg, players)
            await tmp.start_game()
        else:
            await cls.illegal_command(context)

