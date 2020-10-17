import discord
import discord.client
from discord.ext.commands import Bot
from discord.utils import find

from Commands.developer import delete_command, say_command
from Commands.minigames import blackjack_command, chess_command, connect4_command, quiz_command, hangman_command, \
    scramble_command, uno_command, guessword_command, checkers_command
from Commands.miscellaneous import help_command, set_prefix_command
from Other.private import Private
from Other.variables import on_startup
from Database.database import DataBase

class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        super().__init__(command_prefix=self.prefix)
        self.on_startup()
        self.called = False

        self.my_commands = [help_command.HelpCommand, blackjack_command.BlackjackCommand, chess_command.ChessCommand,
                            connect4_command.Connect4Command, hangman_command.HangmanCommand, quiz_command.QuizCommand,
                            guessword_command.GuesswordCommand, scramble_command.ScrambleCommand, uno_command.UnoCommand,
                            delete_command.DeleteCommand, say_command.SayCommand, set_prefix_command.SetPrefixCommand,
                            checkers_command.CheckersCommand]
        for command in self.my_commands:
            command.add_command(self)

    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return
        if str(message.channel.guild.id) in Private.prefixes.keys():
            if message.content.startswith(Private.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix + message.content[len(Private.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        ctxt = await self.get_context(message)
        await self.invoke(ctxt)

    def on_startup(self):
        print("Loading database...")
        DataBase.initialize(self)
        print("Loading files...")
        on_startup()
        print("Done!")

