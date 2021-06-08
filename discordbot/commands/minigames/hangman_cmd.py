from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.hangman_dc import HangmanDisc
from discordbot.gamemanager import GameManager
from discordbot.user.session import Session


class HangmanCommand(Command):
    bot = None
    name = "hangman"
    help = "Play hangman against the bot, check out the rules with the rules command."
    brief = "Play hangman against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **hangman** minigame")

        session = Session(cls.bot, context, msg, "hangman", HangmanDisc, [context.author], True)
        await GameManager.start_session(session)
