from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.hangman_dc import HangmanDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class HangmanCommand(Command):
    bot = None
    name = "hangman"
    help = "Play hangman against the bot, check out the rules with the rules command."
    brief = "Play hangman against the bot."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **hangman** minigame")

        session = SinglePlayerSession(message, "hangman", HangmanDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
