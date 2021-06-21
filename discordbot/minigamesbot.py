import asyncio
import importlib
import inspect
import json
import os
import random
import time
import traceback
from zipfile import ZipFile

import discord
from discord import DMChannel, Permissions
from discord.ext.commands import Bot, CommandNotFound, Cog
from discord.utils import find

from discordbot.categories import *
from discordbot.commands.command import Command
from discordbot.databasemanager import DatabaseManager
from discordbot.gamemanager import GameManager
from discordbot.messagemanager import MessageManager
from discordbot.utils.private import DISCORD
from discordbot.utils.topgg import TopGG
from discordbot.utils.variables import MINIGAMES
from generic.scheduler import Scheduler
from minigames.lexicon import Lexicon

PREFIXES_FILE = "bin/server_prefixes.json"


class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        super().__init__(command_prefix=self.prefix, intents=intents, max_messages=5000)

        self.called_on_ready = False
        self.ctx = None
        self.uptime = time.time()
        self.prefixes = {}
        self.my_commands = []
        self.scheduler = Scheduler()
        self.game_manager = GameManager()

        # load commands
        self.categories = [
            Miscellaneous,
            Developer,
            Minigames
        ]

        self.load_commands()

        # load managers
        self.db = DatabaseManager
        self.lexicon = Lexicon
        self.message_manager = MessageManager
        self.db.on_startup(self)
        self.lexicon.on_startup()
        self.message_manager.on_startup(self)

        # load prefixes
        self.load_prefixes()

        self.scheduler.add(30, self.game_manager.close_inactive_sessions)
        self.scheduler.add(30, self.routine_updates)

        # REMOVE THIS TRY EXCEPT
        try:
            self.add_cog(TopGG(self))
        except Exception as e:
            print(e)

    async def on_message(self, message):
        if message.author.bot or isinstance(message.channel, DMChannel):
            return

        if str(message.channel.guild.id) in self.prefixes.keys():
            if message.content.startswith(self.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix + message.content[len(self.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        context = await self.get_context(message)
        self.ctx = context
        await self.invoke(context)

    async def on_raw_reaction_add(self, payload):
        await MessageManager.on_raw_reaction(payload)

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

    def load_prefixes(self):
        try:
            file = open(PREFIXES_FILE)
            json_strings = file.read()
            self.prefixes = json.loads(json_strings)
        except FileNotFoundError:
            file = open(PREFIXES_FILE, 'w')
            prefixes_json = json.dumps(self.prefixes)
            file.write(prefixes_json)
        file.close()

    def load_commands(self):
        modules = self.get_modules(os.path.join(os.getcwd(), "discordbot", "commands"), "discordbot.commands")
        for module in modules:
            imp = importlib.import_module(module)
            for key, cmd in imp.__dict__.items():
                if inspect.isclass(cmd) and issubclass(cmd, Command) and cmd != Command:
                    self.my_commands.append(cmd)
                    cmd.add_command(self)

    def get_modules(self, path, module):
        modules = []
        for file in os.listdir(path):
            if file == "__pycache__":
                continue
            if os.path.isdir(os.path.join(path, file)):
                for submodule in self.get_modules(os.path.join(path, file), f"{module}.{file}"):
                    modules.append(submodule)
            elif os.path.isfile(os.path.join(path, file)):
                modules.append(f"{module}.{file[:-3]}")
        return modules

    async def send(self, content, channel_id=None):
        if content.startswith("```"):
            await self.send_formatted(content, channel_id)
            return
        max_length = 1900
        message_length = len(content)
        j = 0

        if channel_id is not None:
            channel = await self.fetch_channel(channel_id)
        else:
            channel = self.ctx.channel

        while max_length < message_length:
            await channel.send(content[j * max_length:(j + 1) * max_length])
            message_length -= max_length
            j += 1

        await channel.send(content[j * max_length:])

    async def send_formatted(self, content, channel_id=None):
        max_length = 1900
        message_length = len(content)
        j = 0
        content = content[3:-3]

        if channel_id is not None:
            channel = await self.fetch_channel(channel_id)
        else:
            channel = self.ctx.channel

        while max_length < message_length:
            await channel.send("```\n" + content[j * max_length:(j + 1) * max_length] + "\n```")
            message_length -= max_length
            j += 1

        await channel.send("```\n" + content[j * max_length:] + "\n```")

    async def send_error(self, content):
        channel = self.get_channel(DISCORD["ERROR_CHANNEL"])

        max_length = 1900
        contents = content.split("\n")

        content = ""
        for part in contents:
            temp = content + "\n" + part
            if len(temp) > max_length:
                await channel.send("```\n" + content + "\n```")
                content = part
            else:
                content = temp
        await channel.send("```\n" + content + "\n```")

    async def routine_updates(self):
        while True:
            await self.db.update()
            await self.save_prefixes()
            await self.change_status()
            self.remove_old_binaries()
            await asyncio.sleep(60 * 30)

    async def on_restart(self):
        await self.game_manager.on_restart()
        await self.db.update()
        await self.save_prefixes()

    async def change_status(self):
        n = random.randint(0, len(MINIGAMES) - 1)
        game = discord.Game(MINIGAMES[n])
        await self.change_presence(status=discord.Status.online, activity=game)

    async def save_prefixes(self):
        f = open(PREFIXES_FILE, 'w')
        prefixes_json = json.dumps(self.prefixes)
        f.write(prefixes_json)
        f.close()

        with ZipFile("bin/prefixes_backup.zip", "w") as zip_f:
            zip_f.write(PREFIXES_FILE)
        channel = await self.fetch_channel(DISCORD["BACKUP_CHANNEL"])
        await channel.send(file=discord.File("bin/prefixes_backup.zip"))

    def remove_old_binaries(self):
        direc = os.path.join(os.getcwd(), 'bin')
        now = time.time()
        dt = now - 60 * 60 * 24
        for filename in os.listdir(direc):
            f_path = os.path.join(direc, filename)
            f_created = os.path.getctime(f_path)
            if (filename.endswith(".svg") or filename.endswith(".png")) and f_created < dt:
                os.remove(f_path)

    async def on_error(self, event_method, *args, **kwargs):
        error = "Time: {0}\n\n" \
                "Ignoring exception in command {1}:\n\n" \
                "args: {2}\n\n" \
                "kwargs: {3}\n\n" \
                "e: {4}\n\n" \
            .format(time.strftime("%b %d %Y %H:%M:%S"), event_method, args, kwargs, traceback.format_exc())
        await self.send_error(error)

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

        original_error = getattr(exception, 'original', exception)
        if isinstance(original_error, discord.Forbidden):
            await self.send_missing_permissions(context, self.get_missing_permissions(context))

        error = "Time: {0}\n\n" \
                "Ignoring exception in command {1}:\n\n" \
                "Exception: \n\n{2}" \
            .format(time.strftime("%b %d %Y %H:%M:%S"),
                    context.command,
                    ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

        await self.send_error(error)

    def get_missing_permissions(self, context):
        permissions: Permissions = context.channel.permissions_for(context.channel.guild.me)
        missing_permissions = list()
        if not permissions.manage_messages:
            missing_permissions.append("Manage messages")
        if not permissions.read_message_history:
            missing_permissions.append("Add reactions")
        if not permissions.use_external_emojis:
            missing_permissions.append("Use external emojis")
        if not permissions.attach_files:
            missing_permissions.append("Attach files")
        return missing_permissions

    async def send_missing_permissions(self, context, missing_permissions):
        if len(missing_permissions) == 0:
            return
        content = "I am missing the following permissions in this channel. Please enable these so the bot can work properly:\n"
        for missing_permission in missing_permissions:
            content += f"- {missing_permission}\n"
        await context.send(content)
