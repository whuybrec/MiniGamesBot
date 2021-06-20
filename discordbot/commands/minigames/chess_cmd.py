from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.multiplayergames.chess_dc import ChessDiscord
from discordbot.user.multiplayersession import MultiPlayerSession


class ChessCommand(Command):
    bot = None
    name = "chess"
    help = "Play chess against another player, check out the rules with the rules command."
    brief = "Play chess against another player."
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
            await context.reply("You can not start chess with a bot.")
            return

        message = await context.send("Starting **chess** minigame")
        session = MultiPlayerSession(message, "chess", ChessDiscord, context.author, player2)
        await cls.bot.game_manager.start_session(session)
