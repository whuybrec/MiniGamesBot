from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.blackjack_dc import BlackjackDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class BlackjackCommand(Command):
    bot = None
    name = "blackjack"
    help = "Play a game of blackjack against the bot as dealer, check out the rules with the rules command."
    brief = "Play a game of blackjack against the bot as dealer."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **blackjack** minigame")

        session = SinglePlayerSession(message, "blackjack", BlackjackDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
