from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager
from discordbot.user.hangman_dc import HangmanDisc
from discordbot.user.session import Session


class HangmanCommand(Command):
    bot = None
    name = "hangman"
    help = "Start a game of hangman, check out the rules with the rules command."
    brief = "Start a game of hangman."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting Hangman minigame")

        session = Session(cls.bot, context, msg, HangmanDisc, [context.author])
        await GameManager.start_session(session)
