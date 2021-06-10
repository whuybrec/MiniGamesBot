from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.gamemanager import GameManager
from discordbot.user.discord_games.mastermind_dc import MastermindDisc
from discordbot.user.session import Session


class MastermindCommand(Command):
    bot = None
    name = "mastermind"
    help = "Play mastermind against the bot, check out the rules with the rules command."
    brief = "Play mastermind against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def handler(cls, context):
        msg = await context.channel.send("Starting **mastermind** minigame")

        session = Session(cls.bot, context, msg, "mastermind", MastermindDisc, [context.author])
        await GameManager.start_session(session)
