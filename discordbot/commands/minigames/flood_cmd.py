from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.flood_dc import FloodDisc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class FloodCommand(Command):
    bot = None
    name = "flood"
    help = "Start a game of flood, check out the rules with the rules command."
    brief = "Start a game of flood."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting Flood minigame")

        session = Session(cls.bot, context, msg, "flood", FloodDisc, [context.author])
        await GameManager.start_session(session)
