import asyncio
import json
from zipfile import ZipFile

import discord
from discord.ext.commands import Bot
from discord.utils import find

from discordbot.commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand, \
    RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command, QuizCommand, BlackjackCommand, \
    DbCommand, StatsCommand, SetPrefixCommand
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

PREFIXES_FILE = "bin/server_prefixes.json"


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        self.called_on_ready = False
        self.ctx = None
        super().__init__(command_prefix=self.prefix)
        self.game_manager = GameManager
        self.db = MinigamesDB
        self.lexicon = Lexicon

        # load commands
        self.categories = [
            Miscellaneous,
            Developer,
            Minigames
        ]
        self.my_commands = [SayCommand, HelpCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand,
                            RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command,
                            QuizCommand, BlackjackCommand, DbCommand, StatsCommand, SetPrefixCommand]
        self.load_commands()

        # load managers
        self.game_manager.on_startup(self)
        self.db.on_startup(self)
        self.lexicon.on_startup()

        # load prefixes
        try:
            file = open(PREFIXES_FILE)
            json_strings = file.read()
            self.prefixes = json.loads(json_strings)
            file.close()
        except FileNotFoundError:
            self.prefixes = {}
            f = open(PREFIXES_FILE, 'w')
            prefixes_json = json.dumps(self.prefixes)
            f.write(prefixes_json)
            f.close()

        # Next 2 lines are for showing stats in my own server, ignore this
        self.scheduler = Scheduler()  # REMOVE THIS LINE
        self.scheduler.add(10, self.routine_updates)  # REMOVE THIS LINE

    async def on_message(self, message):
        if str(message.channel.guild.id) in self.prefixes.keys() \
                and message.content.startswith(self.prefixes[str(message.channel.guild.id)]):
            message.content = self.prefix + message.content[len(self.prefixes[str(message.channel.guild.id)]):]

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
        channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
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
            await self.save_prefixes()
            await asyncio.sleep(60*20)

    async def save_prefixes(self):
        f = open(PREFIXES_FILE, 'w')
        prefixes_json = json.dumps(self.prefixes)
        f.write(prefixes_json)
        f.close()

        with ZipFile("bin/prefixes_backup.zip", "w") as zip_f:
            zip_f.write(PREFIXES_FILE)
        channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send(file=discord.File("bin/prefixes_backup.zip"))
