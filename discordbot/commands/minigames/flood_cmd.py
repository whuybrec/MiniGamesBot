from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.flood_dc import FloodDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class FloodCommand(Command):
    bot = None
    name = "flood"
    help = "Get the grid to turn into one color by iteratively flooding it, check out the rules with the rules command."
    brief = "Get the grid to turn into one color by iteratively flooding it."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **flood** minigame")

        session = SinglePlayerSession(message, "flood", FloodDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
