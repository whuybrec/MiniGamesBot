from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.guess_dc import MastermindDisc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class MastermindCommand(Command):
    bot = None
    name = "mastermind"
    help = "Start a game of mastermind, check out the rules with the rules command."
    brief = "Start a game of mastermind."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting Mastermind minigame")

        session = Session(cls.bot, context, msg, "mastermind", MastermindDisc, [context.author])
        await GameManager.start_session(session)
