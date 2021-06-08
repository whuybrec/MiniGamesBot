from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.connect4_dc import Connect4Disc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class Connect4Command(Command):
    bot = None
    name = "connect4"
    help = "Start a game of connect4, check out the rules with the rules command."
    brief = "Start a game of connect4."
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
            await context.reply("You can not start Connect4 with a bot.")
            return

        msg = await context.send("Starting Connect4 minigame")
        session = Session(cls.bot, context, msg, "connect4", Connect4Disc, [context.author, player2])
        await GameManager.start_session(session)

