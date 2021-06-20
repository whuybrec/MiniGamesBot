from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.mastermind_dc import MastermindDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class MastermindCommand(Command):
    bot = None
    name = "mastermind"
    help = "Play mastermind against the bot, check out the rules with the rules command."
    brief = "Play mastermind against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **mastermind** minigame")

        session = SinglePlayerSession(message, "mastermind", MastermindDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
