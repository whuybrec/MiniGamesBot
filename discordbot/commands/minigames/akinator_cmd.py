from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.akinator_dc import AkinatorDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class AkinatorCommand(Command):
    bot = None
    name = "akinator"
    help = "Start the akinator to guess with yes/no questions what character you are thinking of. Character can be fictional or real."
    brief = "Start the akinator to guess with yes/no questions what character you are thinking of."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **akinator** minigame")

        session = SinglePlayerSession(message, "akinator", AkinatorDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
