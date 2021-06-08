from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.chess_dc import ChessDisc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class ChessCommand(Command):
    bot = None
    name = "chess"
    help = "Start a game of chess, check out the rules with the rules command."
    brief = "Start a game of chess."
    args = "@player2"
    category = Minigames

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(args) == 0:
            await context.reply("You need to tag a second player to play with.")
            return

        import re
        try:
            player2 = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))
        except Exception as e:
            print(e)
            await context.reply("You need to tag a second player to play with.")
            return

        if player2.bot:
            await context.reply("You can not start Chess with a bot.")
            return

        msg = await context.channel.send("Starting Chess minigame")
        session = Session(cls.bot, context, msg, "chess", ChessDisc, [context.author, player2], True)
        await GameManager.start_session(session)

