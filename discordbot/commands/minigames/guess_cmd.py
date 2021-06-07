from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.guess_dc import GuessDisc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class GuessCommand(Command):
    bot = None
    name = "guess"
    help = "Start a game of guess, check out the rules with the rules command."
    brief = "Start a game of guess."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting Guess minigame")

        session = Session(cls.bot, context, msg, "guess", GuessDisc, [context.author])
        await GameManager.start_session(session)
