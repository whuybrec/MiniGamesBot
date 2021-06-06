import asyncio
import json
import time
import traceback
from zipfile import ZipFile

import discord
from discord.ext.commands import Bot, CommandNotFound, Cog
from discord.utils import find

from discordbot.categories.developer import Developer
from discordbot.categories.minigames import Minigames
from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands import HelpCommand, SayCommand, DeleteCommand, ClearCommand, TemperatureCommand, \
    ExecuteCommand, \
    RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command, QuizCommand, \
    BlackjackCommand, \
    GamesCommand, StatsCommand, SetPrefixCommand, BugCommand, ChessCommand, ServersCommand, FloodCommand
from discordbot.user.databasemanager import DatabaseManager
from discordbot.user.gamemanager import GameManager
from discordbot.utils.private import DISCORD
from discordbot.utils.topgg import TopGG
from generic.scheduler import Scheduler
from minigames.lexicon import Lexicon

PREFIXES_FILE = "bin/server_prefixes.json"


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        self.called_on_ready = False
        self.ctx = None
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=self.prefix, intents=intents)
        self.game_manager = GameManager
        self.db = DatabaseManager
        self.lexicon = Lexicon

        # load commands
        self.categories = [
            Miscellaneous,
            Developer,
            Minigames
        ]
        self.my_commands = [SayCommand, HelpCommand, DeleteCommand, ClearCommand, TemperatureCommand, ExecuteCommand,
                            RestartCommand, InfoCommand, HangmanCommand, RulesCommand, ScrambleCommand, Connect4Command,
                            QuizCommand, BlackjackCommand, GamesCommand, StatsCommand, SetPrefixCommand, BugCommand, ChessCommand,
                            ServersCommand, FloodCommand]
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

        self.scheduler = Scheduler()
        self.scheduler.add(20, self.routine_updates)

        # REMOVE THIS TRY EXCEPT
        try:
            self.add_cog(TopGG(self))
        except Exception as e:
            print(e)

    async def on_message(self, message):
        if str(message.channel.guild.id) in self.prefixes.keys():
            if message.content.startswith(self.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix + message.content[len(self.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        context = await self.get_context(message)
        self.ctx = context
        await self.invoke(context)

    async def on_ready(self):
        if not self.called_on_ready:
            self.called_on_ready = False
            channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
            await channel.send("**READY**")

    async def on_guild_remove(self, guild):
        if guild.name is None:
            return
        self.db.add_to_servers_table(guild.id, "\"LEAVE\"")
        channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send("LEFT GUILD '{0}' ({1}).".format(guild.name, guild.id))

    async def on_guild_join(self, guild):
        self.db.add_to_servers_table(guild.id, "\"JOIN\"")
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {0}! The command prefix for this bot is **?**.\n'
                               'Type **?help** for a list of possible commands.'.format(guild.name))
        channel = await self.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send("JOINED GUILD '{0}' ({1}).".format(guild.name, guild.id))

    def load_commands(self):
        for command in self.my_commands:
            command.add_command(self)

    async def send(self, content, channel_id=None):
        max_length = 1900
        message_length = len(content)
        j = 0
        formatted = False
        if content.startswith("```"):
            content = content[3:-3]
            formatted = True

        if channel_id is not None:
            channel = await self.fetch_channel(channel_id)
        else:
            channel = self.ctx.channel

        while max_length < message_length:
            if formatted:
                await channel.send("```\n" + content[j * max_length:(j + 1) * max_length] + "```\n")
            else:
                await channel.send(content[j * max_length:(j + 1) * max_length])
            message_length -= max_length
            j += 1

        if formatted:
            await channel.send("```\n" + content[j * max_length:] + "```\n")
        else:
            await channel.send(content[j * max_length:])

    async def routine_updates(self):
        while True:
            await self.db.update()
            await self.save_prefixes()
            await asyncio.sleep(60*30)

    async def save_prefixes(self):
        f = open(PREFIXES_FILE, 'w')
        prefixes_json = json.dumps(self.prefixes)
        f.write(prefixes_json)
        f.close()

        with ZipFile("bin/prefixes_backup.zip", "w") as zip_f:
            zip_f.write(PREFIXES_FILE)
        channel = await self.fetch_channel(DISCORD["BACKUP_CHANNEL"])
        await channel.send(file=discord.File("bin/prefixes_backup.zip"))

    async def on_error(self, event_method, *args, **kwargs):
        text = "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "args: {2}\n\n" \
               "kwargs: {3}\n\n" \
               "e: {4}\n\n"\
            .format(time.strftime("%b %d %Y %H:%M:%S"), event_method, args, kwargs, traceback.format_exc())
        channel = self.get_channel(DISCORD["ERROR_CHANNEL"])
        await self.send("```"+text+"```", channel.id)

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            return
        if self.extra_events.get('on_command_error', None):
            return
        if hasattr(context.command, 'on_error'):
            return

        cog = context.cog
        if cog and Cog._get_overridden_method(cog.cog_command_error) is not None:
            return

        text = "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "Exception: {2}\n\n" \
            .format(time.strftime("%b %d %Y %H:%M:%S"), context.command, exception)
        channel = self.get_channel(DISCORD["ERROR_CHANNEL"])
        await self.send("```"+text+"```", channel.id)
        result = traceback.format_exception(type(exception), exception, exception.__traceback__)
        result = "".join(result)
        await self.send("```"+result+"```", channel.id)
