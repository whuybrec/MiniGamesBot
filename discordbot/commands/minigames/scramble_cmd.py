from discordbot.categories.minigames import Minigames
from discordbot.commands.command import Command
from discordbot.discordminigames.singleplayergames.scramble_dc import ScrambleDiscord
from discordbot.user.singleplayersession import SinglePlayerSession


class ScrambleCommand(Command):
    bot = None
    name = "scramble"
    help = "Unscramble the letters of a random word, check out the rules with the rules command."
    brief = "Unscramble the letters of a random word."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **scramble** minigame")

        session = SinglePlayerSession(message, "scramble", ScrambleDiscord, context.author)
        await cls.bot.game_manager.start_session(session)
