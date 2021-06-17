from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager


class Connect4Command(Command):
    bot = None
    name = "connect4"
    help = "Play connect4 against another player, check out the rules with the rules command."
    brief = "Play connect4 against another player."
    args = "@player2"
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(args) == 0:
            await context.reply("You need to tag a second player to play with.")
            return

        import re
        try:
            player2 = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))
        except IndexError:
            await context.reply("You need to tag a second player to play with.")
            return

        if player2.bot:
            await context.reply("You can not start connect4 with a bot.")
            return

        message = await context.send("Starting **connect4** minigame")
        await GameManager.create_session(message, "connect4", context.author, player2)
