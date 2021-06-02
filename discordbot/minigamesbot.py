import asyncio

from discord.ext.commands import Bot
from discord.utils import find

from discordbot.commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand, \
    RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command, QuizCommand, BlackjackCommand, \
    DbCommand, StatsCommand
from discordbot.categories.developer import Developer
from discordbot.categories.minigames import Minigames
from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.user.gamemanager import GameManager
from discordbot.user.minigamesdb import MinigamesDB
from discordbot.utils.private import DISCORD
from generic.scheduler import Scheduler
from minigames.lexicon import Lexicon

# TODO: edit readme to remove scheduler things
# TODO: UPDATE PRIVATE.PY
# TODO: custom prefixes
# TODO: custom send?
# TODO: on_errors
# TODO: minigames: checkers, uno, chess
# TODO: bug reports


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        self.called_on_ready = False
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
        self.db.on_startup(self)
        self.lexicon.on_startup()

        self.scheduler = Scheduler()  # REMOVE THIS LINE
        self.scheduler.add(10, self.routine_updates)  # REMOVE THIS LINE

    async def on_message(self, message):
        context = await self.get_context(message)
        self.ctx = context
        await self.invoke(context)

    async def on_ready(self):
        if not self.called_on_ready:
            self.called_on_ready = False
            channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
            await channel.send("**READY**")

    async def on_guild_remove(self, guild):
        channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send("LEFT GUILD '{0}' ({1}).".format(guild.name, guild.id))

    async def on_guild_join(self, guild):
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}! The command prefix for this bot is "?".\n'
                               'Type ?help for a list of commands.'.format(guild.name))
        channel =  await self.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send("JOINED GUILD '{0}' ({1}).".format(guild.name, guild.id))

    def load_commands(self):
        for command in self.my_commands:
            command.add_command(self)

    async def send(self, msg, channel_id=None):
        if channel_id is not None:
            channel = self.fetch_channel(channel_id)
            await channel.send(msg)
        else:
            await self.ctx.send(msg)

    async def routine_updates(self):
        while True:
            await self.db.update()
            await asyncio.sleep(60*20)
