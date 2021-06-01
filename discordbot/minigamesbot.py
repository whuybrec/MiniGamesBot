from discord.ext.commands import Bot

from discordbot.commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand, \
    RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command, QuizCommand, BlackjackCommand, \
    DbCommand, StatsCommand
from discordbot.categories.developer import Developer
from discordbot.categories.minigames import Minigames
from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.user.gamemanager import GameManager
from discordbot.user.minigamesdb import MinigamesDB
from minigames.lexicon import Lexicon


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        self.ctx = None
        super().__init__(command_prefix=self.prefix)
        self.game_manager = GameManager
        self.db = MinigamesDB
        self.lexicon = Lexicon

        self.categories = [
            Miscellaneous,
            Developer,
            Minigames
        ]
        self.my_commands = [SayCommand, HelpCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand,
                            RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command,
                            QuizCommand, BlackjackCommand, DbCommand, StatsCommand]

        self.load_commands()

        self.game_manager.on_startup(self)
        self.db.on_startup()
        self.lexicon.on_startup()

    async def on_message(self, message):
        context = await self.get_context(message)
        self.ctx = context
        await self.invoke(context)

    def load_commands(self):
        for command in self.my_commands:
            command.add_command(self)

    async def send(self, msg):
        await self.ctx.send(msg)
