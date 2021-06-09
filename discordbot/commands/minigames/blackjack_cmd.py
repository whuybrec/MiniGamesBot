from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager
from discordbot.user.discord_games.blackjack_dc import BlackjackDisc
from discordbot.user.session import Session


class BlackjackCommand(Command):
    bot = None
    name = "blackjack"
    help = "Play a game of blackjack against the bot as dealer, check out the rules with the rules command."
    brief = "Play a game of blackjack against the bot as dealer."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **blackjack** minigame")

        session = Session(cls.bot, context, msg, "blackjack", BlackjackDisc, [context.author])
        await GameManager.start_session(session)
