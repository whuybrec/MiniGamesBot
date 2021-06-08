from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.flood_dc import FloodDisc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class FloodCommand(Command):
    bot = None
    name = "flood"
    help = "Get the grid to turn into one color by iteratively flooding it, check out the rules with the rules command."
    brief = "Get the grid to turn into one color by iteratively flooding it."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **flood** minigame")

        session = Session(cls.bot, context, msg, "flood", FloodDisc, [context.author])
        await GameManager.start_session(session)
