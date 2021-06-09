from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager
from discordbot.user.discord_games.scramble_dc import ScrambleDisc
from discordbot.user.session import Session


class ScrambleCommand(Command):
    bot = None
    name = "scramble"
    help = "Unscramble the letters of a random word, check out the rules with the rules command."
    brief = "Unscramble the letters of a random word."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **scramble** minigame")

        session = Session(cls.bot, context, msg, "scramble", ScrambleDisc, [context.author])
        await GameManager.start_session(session)
