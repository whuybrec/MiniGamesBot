from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.connect4_dc import Connect4Disc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class Connect4Command(Command):
    bot = None
    name = "connect4"
    help = "Start a game of connect4, check out the rules with the rules command."
    brief = "Start a game of connect4."
    args = "*@player2*"
    category = Minigames

    @classmethod
    async def handler(cls, context, *args):
        if not args:
            await context.channel.send("You need to tag a second player to play with.")
            return

        import re
        try:
            player2 = await cls.bot.fetch_user(int(re.findall(r'\d+', args[0])[0]))
        except Exception as e:
            print(e)
            return

        msg = await context.channel.send("Starting Connect4 minigame")
        session = Session(cls.bot, context, msg, Connect4Disc, [context.author, player2])
        await GameManager.start_session(session)

