from discord.ext.commands import Bot

from commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand, \
    RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command, QuizCommand, BlackjackCommand
from discordbot.categories.developer import Developer
from discordbot.categories.minigames import Minigames
from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.user.gamemanager import GameManager
from discordbot.utils.private import DISCORD
from discordbot.user.databasemanager import DataBaseManager
from minigames.lexicon import Lexicon


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        super().__init__(command_prefix=self.prefix)
        self.game_manager = GameManager
        self.database_manager = DataBaseManager
        self.lexicon = Lexicon

        self.categories = [
            Miscellaneous,
            Developer,
            Minigames
        ]
        self.my_commands = [SayCommand, HelpCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand,
                            RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command,
                            QuizCommand, BlackjackCommand]

        self.load_commands()

        GameManager.on_startup(self)
        DataBaseManager.on_startup()
        Lexicon.on_startup()

    async def on_message(self, message):
        context = await self.get_context(message)
        await self.invoke(context)

    def load_commands(self):
        for command in self.my_commands:
            command.add_command(self)


bot = MiniGamesBot("!")
bot.run(DISCORD["TOKEN"])

