from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.user.discord_games.blackjack_dc import BlackjackDisc
from discordbot.user.gamemanager import GameManager
from discordbot.user.session import Session


class BlackjackCommand(Command):
    bot = None
    name = "blackjack"
    help = "Start a game of blackjack, check out the rules with the rules command."
    brief = "Start a game of blackjack."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context, *args):
        msg = await context.channel.send("Starting blackjack minigame")

        session = Session(cls.bot, context, msg, BlackjackDisc, [context.author])
        await GameManager.start_session(session)
