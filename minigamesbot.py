import random
import sys
import time
import traceback

import discord
import discord.client
import asyncio
from discord.ext.commands import Bot, Cog, CommandNotFound
from discord.utils import find

from Commands.developer import delete_command, say_command, temperature_command
from Commands.minigames import blackjack_command, chess_command, connect4_command, quiz_command, hangman_command, \
    scramble_command, uno_command, guessword_command, checkers_command
from Commands.miscellaneous import help_command, info_command, set_prefix_command, bug_command, request_command, \
    stats_command, announcements_command
from Other.private import Private
from Other.variables import on_startup, Variables
from Database.database import DataBase
from Statistics.global_statistics import Statistics

ctx = None
_self = None

class MiniGamesBot(Bot):
    def __init__(self, prefix, testing=False):
        self.prefix = prefix
        self.testing = testing
        super().__init__(command_prefix=self.prefix)
        self.on_startup()
        self.called = False

        self.my_commands = [help_command.HelpCommand, blackjack_command.BlackjackCommand, chess_command.ChessCommand,
                            connect4_command.Connect4Command, hangman_command.HangmanCommand, quiz_command.QuizCommand,
                            guessword_command.GuesswordCommand, scramble_command.ScrambleCommand, uno_command.UnoCommand,
                            delete_command.DeleteCommand, say_command.SayCommand, temperature_command.TemperatureCommand,
                            info_command.InfoCommand, set_prefix_command.SetPrefixCommand,
                            bug_command.BugCommand, request_command.RequestCommand, stats_command.StatsCommand,
                            announcements_command.AnnouncementsCommand, checkers_command.CheckersCommand]
        for command in self.my_commands:
            command.add_command(self)

        self.command(name="exec", brief="<dev> exec belleketrek")(self.execute)
        self.command(name="exit", brief="<dev> Reboots connect4")(self.reboot)

        Variables.scheduler.add(60, self.change_status)

    async def on_message(self, message):
        if message.channel.id == Private.ANNOUNCEMENTS_CHANNELID:
            await self.post_mail(message)
            return
        if isinstance(message.channel, discord.DMChannel):
            return
        if str(message.channel.guild.id) in Private.prefixes.keys():
            if message.content.startswith(Private.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix + message.content[len(Private.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        ctxt = await self.get_context(message)
        await self.invoke(ctxt)

    async def on_guild_remove(self, guild):
        channel = self.get_channel(Private.STACK_CHANNELID)
        await channel.send("LEFT GUILD '{0}' ({1}).".format(guild.name, guild.id))

    async def on_guild_join(self, guild):
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}! The command prefix for this bot is "?".\n'
                               'Type ?help for a list of commands.'.format(guild.name))
        channel = self.get_channel(Private.STACK_CHANNELID)
        await channel.send("JOINED GUILD '{0}' ({1}).".format(guild.name, guild.id))

    def on_startup(self):
        if not self.testing:
            print("Getting statistics...")
            Statistics.initialize(self)
        print("Loading database...")
        DataBase.initialize(self)
        print("Loading files...")
        on_startup()
        print("Done!")

    async def on_ready(self):
        if not self.called:
            self.called = True
            channel = self.get_channel(Private.STACK_CHANNELID)
            await channel.send("READY.")

    async def change_status(self):
        n = random.randint(0, len(Variables.game_names)-1)
        game = discord.Game(Variables.game_names[n])
        await self.change_presence(status=discord.Status.online, activity=game)
        Variables.scheduler.add(60*60, self.change_status)

    async def post_mail(self, message):
        channels = DataBase.run("SELECT channel_id FROM announcement_channels")
        channels = channels[0]
        for cid in channels:
            try:
                c = self.get_channel(cid)
                await c.send(message.content)
            except Exception as e:
                context = await self.get_context(message)
                await self.on_command_error(context, e)

    async def reboot(self, context):
        if context.author.id in Private.DEV_IDS.keys():
            await context.send("Rebooting...")
            print("See you soon...")
            sys.exit()

    async def send(self, c, text):
        MSG_LENTGH = 1800
        l = len(text)
        j = 0
        while MSG_LENTGH < l:
            await c.send("```\n" + text[j*MSG_LENTGH:(j+1)*MSG_LENTGH] + "```\n")
            l -= MSG_LENTGH
            j += 1
        await c.send("```\n" + text[j * MSG_LENTGH:] + "```\n")

    async def on_error(self, event_method, *args, **kwargs):
        e = sys.exc_info()
        if e[0] is discord.Forbidden:
            context = await self.get_context(args[0].message)
            await context.channel.send("I am missing permissions in this server, "
                                       "make sure that I can manage messages (to delete reactions) and can send DMs.")
        text = "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "args: {2}\n\n" \
               "kwargs: {3}\n\n" \
               "e: {4}\n\n"\
            .format(time.strftime("%b %d %Y %H:%M:%S"), event_method, args, kwargs, traceback.format_exc())
        channel = self.get_channel(Private.LOGS_COMMANDS_CHANNELID)
        await self.send(channel, text)

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            return
        if self.extra_events.get('on_command_error', None):
            return
        if hasattr(context.command, 'on_error'):
            return

        cog = context.cog
        if cog:
            if Cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if isinstance(exception, discord.Forbidden):
            await context.channel.send("I am missing permissions in this server, "
                                       "make sure that I can manage messages (to delete reactions) and can send DMs.")

        text = "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "Exception: {2}\n\n" \
            .format(time.strftime("%b %d %Y %H:%M:%S"), context.command, exception)
        channel = self.get_channel(Private.LOGS_COMMANDS_CHANNELID)
        await self.send(channel, text)
        result = traceback.format_exception(type(exception), exception, exception.__traceback__)
        result = "".join(result)
        await self.send(channel, result)

    async def execute(self, context):
        global ctx, _self
        ctx = context
        _self = self
        if context.message.author.id == Private.DEVALPHA_ID:
            lines = context.message.content[len("?exec "):].split("\n")
            func = ["async def get():",
                    "    try:",
                    "        global returnv",
                    "        returnv = None",
                    "        returnv = await func()",
                    "        if returnv is not None:",
                    "            await ctx.send(f'```python\\n{repr(returnv)}\\n```')",
                    "    except Exception as e:",
                    "        await ctx.send(f'```python\\n{e}\\n```')",
                    "asyncio.Task(get())",
                    "async def func():",
                    "    " + "\n    ".join(lines[:-1])]

            keywords = ["return ",
                        "import ",
                        "from ",
                        "for ",
                        "with ",
                        "def ",
                        "else "]

            if lines[-1].startswith(" ") or lines[-1].startswith("\t") or any(
                    lines[-1].startswith(s) for s in keywords):
                func.append("    " + lines[-1])
            else:
                func += ["    try:",
                         "        return " + lines[-1],
                         "    except:",
                         "        " + lines[-1]]

            try:
                exec("\n".join(func), globals())
            except Exception as e:
                await context.send("```python\n" + str(e) + "\n```")
