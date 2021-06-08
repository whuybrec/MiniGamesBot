from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.akinator_dc import AkinatorDisc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class AkinatorCommand(Command):
    bot = None
    name = "akinator"
    help = "Think of character and by asking yes/no questions the Akinator will guess who it is. Character can be fictional or real."
    brief = "Think of character and by asking questions the Akinator will guess who it is."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting Akinator minigame")

        session = Session(cls.bot, context, msg, "akinator", AkinatorDisc, [context.author])
        await GameManager.start_session(session)
