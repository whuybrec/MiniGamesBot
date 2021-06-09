from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager
from discordbot.user.discord_games.akinator_dc import AkinatorDisc
from discordbot.user.session import Session


class AkinatorCommand(Command):
    bot = None
    name = "akinator"
    help = "Start the akinator to guess with yes/no questions what character you are thinking of. Character can be fictional or real."
    brief = "Start the akinator to guess with yes/no questions what character you are thinking of."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **akinator** minigame")

        session = Session(cls.bot, context, msg, "akinator", AkinatorDisc, [context.author])
        await GameManager.start_session(session)
