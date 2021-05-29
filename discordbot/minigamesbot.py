from discord.ext.commands import Bot

from commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand, \
    RestartCommand, InfoCommand
from private import DISCORD
from categories import *


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        super().__init__(command_prefix=self.prefix)
        self.categories = [
            Miscellaneous,
            Developer,
        ]
        self.my_commands = [SayCommand, HelpCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand,
                            RestartCommand, InfoCommand]

        self.load_commands()

    async def on_message(self, message):
        context = await self.get_context(message)
        await self.invoke(context)

    def load_commands(self):
        for command in self.my_commands:
            command.add_command(self)


bot = MiniGamesBot("!")
bot.run(DISCORD["TOKEN"])

